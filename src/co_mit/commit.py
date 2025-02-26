__all__ = ["co_mit"]
import llama_index.core.workflow
import llama_index.llms.openai
import rich

from . import git


COMMIT_PROMPT = """
Write a commit message for the following changes.
{format_instructions}

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


class CommitFlow(llama_index.core.workflow.Workflow):
    llm = llama_index.llms.openai.OpenAI(model="o1-mini")

    @llama_index.core.workflow.step
    async def generate_commit(
        self,
        ctx: llama_index.core.workflow.Context,
        ev: llama_index.core.workflow.StartEvent,
    ) -> CommitEvent:
        if ev.example:
            format_instructions = f"\nExample commit message:\n```\n{ev.example}\n```"
        else:
            format_instructions = "Follow the conventional commit message format."

        prompt = COMMIT_PROMPT.format(
            diff=git.diff(),
            status=git.status(),
            format_instructions=format_instructions,
        )
        response = await self.llm.acomplete(prompt)
        return CommitEvent(msg=str(response))

    @llama_index.core.workflow.step
    async def second_step(self, ev: CommitEvent) -> llama_index.core.workflow.StopEvent:
        # TODO: further refinement
        return llama_index.core.workflow.StopEvent(result=ev.msg)


async def co_mit(example: str | None = None) -> None:
    commit_flow = CommitFlow(timeout=60, verbose=False)
    handler = commit_flow.run(example=example)
    async for event in handler.stream_events():
        if isinstance(event, CommitEvent):
            rich.print(event.msg)
    result = await handler
    rich.print(str(result))
