from dotenv import load_dotenv
load_dotenv()

from pydantic import BaseModel
from agents import (
    Agent, 
    Runner,
    GuardrailFunctionOutput, 
    InputGuardrailTripwireTriggered, 
    RunContextWrapper, 
    TResponseInputItem, 
    input_guardrail
)

import asyncio

class HomeWorkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str


guardrain_agent = Agent(
    name="Guardrail_Check",
    instructions="Check if the user is  asking to do their math homework",
    output_type=HomeWorkOutput
)


@input_guardrail
async def math_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list | TResponseInputItem
) -> GuardrailFunctionOutput:
    
    result = await Runner.run(guardrain_agent, input=input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output, 
        tripwire_triggered=result.final_output.is_math_homework
    )


agent = Agent(
    name="Customer support agent",
    instructions="You are a customer agent, You help cusotmers",
    input_guardrails=[math_guardrail]
)


async def main():
    try:

        result = await Runner.run(agent, "can you solve (1+3) * 4")
        print(result.final_output)
    except InputGuardrailTripwireTriggered:
        print("Math problem is asked")


if __name__ == "__main__":
    asyncio.run(main())