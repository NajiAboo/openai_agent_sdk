from agents import Agent, Runner
import asyncio

spanish_agent = Agent(
    name="Spanish Agent",
    instructions="You only speak spanish"
)

english_agent = Agent(
    name="English Agent",
    instructions="You can only speak English"
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="Handoff to the appropriate agent based on the language of the request",
    handoffs=[spanish_agent, english_agent]
)


async def main():
    result = await Runner.run(triage_agent, input="Hola, ¿cómo estás?")
    print(result.final_output)


if __name__=="__main__":
    asyncio.run(main())