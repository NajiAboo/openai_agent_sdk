import asyncio
from agents import Agent, Runner, function_tool
from dotenv import load_dotenv

load_dotenv()

@function_tool
def get_weather(city: str) -> str:
    return f"The weather in the {city} is sunny"


aget = Agent(
    name="FunctionTool Agent",
    instructions="You are a helpful agent",
    tools=[get_weather]
)

async def main():
    result = await Runner.run(aget, input="What is the weather in Newyork")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())