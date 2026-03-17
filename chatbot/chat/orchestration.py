import json
import logging

from openai import OpenAI, Omit

from chatbot.tools.registry import ToolRegistry

logger = logging.getLogger(__name__)

BASE_PROMPT = """\
You are an expert HR employee with more than 20 years of experience. Your job is to answer every question the company
employee may have.

# What to do
- Use tools where you can.
- If the user's question can be answered from company documents, use the `search_database` tool.
- If the question is about user's or other employee's vacation, use the `get_vacation_days` tool.
- If you don't have enough information from tool results and your own knowledge base, you MUST say so.
- You MUST cite document source files if available in metadata.
- When multiple documents address the same topic, prefer the most recent one based on the effective date or version 
  number found in the document metadata or text. If a document explicitly states it updates or supersedes another,
  follow the newer document.
- After finding policy documents, always perform a second search for any updates, amendments, or changes to that policy
  before giving a final answer.

# What not to do
- You MUST NOT fabricate information.

# Output style
- Speak in complete sentences.
- Use precise terminology.
- Avoid watered down or generic language.
- Use more concise language and avoid fluff.
"""


def run_agent_loop(
    user_input: str,
    tool_registry: ToolRegistry,
    conversation_history: list[dict],
    model: str = "gpt-4o",
    max_iterations: int = 10,
) -> str:
    """
    Execute agent loop:

    :param user_input: The user prompt
    :param tool_registry: Registry of all tools
    :param conversation_history: Full conversation history for complete context
    :param model: Model to use for answering the user prompt
    :param max_iterations: Maximum iterations to prevent infinite tool-call loops
    :return:
    """
    client = OpenAI()

    conversation_history.append({"role": "user", "content": user_input})

    available_tools = tool_registry.get_openai_schemas()

    logger.info(f"Running agent loop with user prompt: {user_input}")

    for i in range(max_iterations):
        logger.info(f"Running loop {i}")
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": BASE_PROMPT}, *conversation_history],
            tools=available_tools if available_tools else Omit(),
        )

        choice = response.choices[0]
        message = choice.message

        logger.debug(f"Model returned message: {message}")

        # The agent finished with the task
        if choice.finish_reason == "stop":
            final_answer = message.content or ""
            conversation_history.append({"role": "assistant", "content": final_answer})

            logger.info(f"Returning answer: {final_answer}")
            return final_answer

        # The agent needs to call tools
        if choice.finish_reason == "tool_calls":
            conversation_history.append(message.model_dump())

            for tool_call in message.tool_calls:
                tool_name: str = tool_call.function.name
                tool_arguments: dict = json.loads(tool_call.function.arguments)

                logger.debug(f"Calling tool '{tool_name}' with arguments: {tool_arguments}")
                result = tool_registry.execute(tool_name, tool_arguments)

                conversation_history.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    }
                )

            # Loop continues with new info from tools
            continue

        # Something unexpected happened.
        logger.warning(f"An unexpected finish_reason: '{choice.finish_reason}'")
        break

    return "I was unable to complete your request. Please try again."
