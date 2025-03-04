__all__ = ["co_mit"]
import llama_index.core.agent.workflow as llama_agent_workflow
import llama_index.llms.openai
import rich

from . import config, tools


SYSTEM_PROMPT = """
You are an experienced software developer working on a project.
You have made some changes to the codebase and you need to write a commit message to describe the changes you have made.
"""


def create_user_msg(example: str | None = None) -> str:
    if not example:
        msg = "Create a commit message using conventional commit format."
    else:
        msg = f"Create a commit message using this format:\n'''{example}\n'''"
    msg += "\nYou should return only the commit message, without additional information, backticks, quotes, or any other formatting."
    return msg


async def co_mit(example: str | None = None) -> None:
    commit_agent = llama_agent_workflow.AgentWorkflow.from_tools_or_functions(
        [
            tools.git.diff,
            tools.git.diff_cached,
            tools.git.status,
            tools.os.read_file,
        ],
        llm=llama_index.llms.openai.OpenAI(
            model="gpt-4o", api_key=config.Config.openai_api_key
        ),
        system_prompt=SYSTEM_PROMPT,
    )
    msg = create_user_msg(example)
    result = await commit_agent.run(user_msg=msg)
    if not config.Config.quiet:
        rich.print("[bold green]Done.[/]")
    rich.print(str(result))
