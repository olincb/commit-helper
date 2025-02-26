__all__ = ["co_mit"]
import llama_index.core.workflow

# `pip install llama-index-llms-openai` if you don't already have it
from llama_index.llms.openai import OpenAI


class CommitEvent(llama_index.core.workflow.Event):
    msg: str


class HaikuEvent(llama_index.core.workflow.Event):
    msg: str


class CommitFlow(llama_index.core.workflow.Workflow):
    llm = OpenAI(model="o1-mini")

    @llama_index.core.workflow.step
    async def generate_commit(
        self,
        ctx: llama_index.core.workflow.Context,
        ev: llama_index.core.workflow.StartEvent,
    ) -> CommitEvent:
        topic = ev.topic
        print(f"Generating commit message for {topic}...")

        prompt = f"Write a haiku about {topic}."
        print(self.llm.model)
        response = await self.llm.acomplete(prompt)
        ctx.write_event_to_stream(HaikuEvent(msg=str(response)))
        return CommitEvent(msg=str(response))

    @llama_index.core.workflow.step
    async def critique_haiku(
        self, ev: CommitEvent
    ) -> llama_index.core.workflow.StopEvent:
        msg = ev.msg
        print(f"Critiquing haiku: {msg}")

        prompt = f"Briefly critique the following haiku, remembering that haikus must have 5 syllables in the first line, 7 in the second, and 5 in the third:\n{msg}"
        response = await self.llm.acomplete(prompt)
        return llama_index.core.workflow.StopEvent(result=str(response))


async def co_mit() -> None:
    print("Starting commit flow...")
    commit_flow = CommitFlow(timeout=60, verbose=False)
    print("Running commit flow...")
    handler = commit_flow.run(topic="a sloth in a cucumber canoe")
    print("Streaming events...")
    async for event in handler.stream_events():
        if isinstance(event, HaikuEvent):
            print(event.msg)
    result = await handler
    print(str(result))
