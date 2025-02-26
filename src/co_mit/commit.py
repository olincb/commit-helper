__all__ = ["co_mit"]
import llama_index.core.workflow
import llama_index.llms.openai
import rich

from . import git


COMMIT_PROMPT = """
Write a commit message for the following changes.

The git diff:
```diff
{diff}
```

The git status:
```console
{status}
```

"""


class CommitEvent(llama_index.core.workflow.Event):
    msg: str


class HaikuEvent(llama_index.core.workflow.Event):
    msg: str


class CommitFlow(llama_index.core.workflow.Workflow):
    llm = llama_index.llms.openai.OpenAI(model="o1-mini")

    @llama_index.core.workflow.step
    async def generate_commit(
        self,
        ctx: llama_index.core.workflow.Context,
        ev: llama_index.core.workflow.StartEvent,
    ) -> CommitEvent:
        prompt = COMMIT_PROMPT.format(diff=git.diff(), status=git.status())
        response = await self.llm.acomplete(prompt)
        return CommitEvent(msg=str(response))

    @llama_index.core.workflow.step
    async def critique_haiku(
        self, ev: CommitEvent
    ) -> llama_index.core.workflow.StopEvent:
        # msg = ev.msg
        # print(f"Critiquing haiku: {msg}")
        #
        # prompt = f"Briefly critique the following haiku, remembering that haikus must have 5 syllables in the first line, 7 in the second, and 5 in the third:\n{msg}"
        # response = await self.llm.acomplete(prompt)
        return llama_index.core.workflow.StopEvent(result=ev.msg)


async def co_mit() -> None:
    # rich.print(git.diff())
    # print()
    # rich.print(git.status())

    commit_flow = CommitFlow(timeout=60, verbose=False)
    handler = commit_flow.run()
    async for event in handler.stream_events():
        if isinstance(event, HaikuEvent):
            print(event.msg)
    result = await handler
    print(str(result))
