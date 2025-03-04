__all__ = ["co_mit"]
import llama_index.core.agent.workflow as llama_agent_workflow
import llama_index.llms.openai
import rich

from . import config, tools


SYSTEM_PROMPT = """
You are an experienced software developer working on a project.
You have made some changes to the codebase and you need to write a commit message to describe the changes you have made.
The most important thing to understand is the changes you have made and why you have made them.
If you need to determine how long this commit took to develop, you must check the commit history and the last modified times of the files in the directory.
"""


def create_user_msg() -> str:
    if not config.Config.example:
        msg = "Create a commit message using conventional commit format."
    else:
        msg = f"Create a commit message using this format:\n'''{config.Config.example}\n'''"
    msg += "\nYou should return only the commit message, without additional information, backticks, quotes, or any other formatting."
    return msg


async def co_mit() -> None:
    commit_agent = llama_agent_workflow.AgentWorkflow.from_tools_or_functions(
        [
            tools.git.diff,
            tools.git.diff_cached,
            tools.git.log,
            tools.git.status,
            tools.os.ls,
            tools.os.read_file,
        ],
        llm=llama_index.llms.openai.OpenAI(
            model="gpt-4o", api_key=config.Config.openai_api_key
        ),
        system_prompt=SYSTEM_PROMPT,
    )

    msg = create_user_msg()
    result = await commit_agent.run(user_msg=msg)
    if not config.Config.quiet:
        rich.print("[bold green]Done.[/]")
    rich.print(str(result))
