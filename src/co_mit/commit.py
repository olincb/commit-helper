__all__ = ["co_mit"]
import llama_index.core.agent.workflow as llama_agent_workflow
import llama_index.llms.openai
import rich

from . import config, tools


SYSTEM_PROMPT = """
## Background
- You are an experienced software developer working on a project.
- You have made some changes to the codebase and you need to write a commit message to describe the changes you have made.

## Goal
- The most important thing to understand is the changes you have made and why you have made them.
- You must stage the files that you want to commit.
- You must perform the commit.

## Considerations
- If the user indicates they'd like to quit (e.g. by typing 'cancel' or 'quit'), end the conversation with a curt message noting that the commit has been cancelled (do not tell user they can ask for more help).
- If you need to determine how long this commit took to develop, you must check the commit history and the last modified times of the files in the directory.
- If the user provides feedback, make any necessary changes and try again.
- When done, simply say "Done." to end the conversation.
"""


def create_user_msg() -> str:
    if not config.Config.example:
        msg = "Commit this code using conventional commit format for the message."
    else:
        msg = f"Commit this code using this format for the message:\n'''{config.Config.example}\n'''"
    msg += "\nYou should return only the commit message, without additional information, backticks, quotes, or any other formatting."
    return msg


async def co_mit() -> None:
    commit_agent = llama_agent_workflow.AgentWorkflow.from_tools_or_functions(
        [
            tools.git.add,
            tools.git.commit,
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
    rich.print("[bold green]" + str(result) + "[/]")
