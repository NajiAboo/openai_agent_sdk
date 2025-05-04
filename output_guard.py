from pydantic import BaseModel
from agents import(
    Agent, 
    GuardrailFunctionOutput, 
    OutputGuardrailTripwireTriggered, 
    RunContextWrapper, 
    Runner, 
    output_guardrail
)

from dotenv import load_dotenv
load_dotenv()

import asyncio

class MessageOutput(BaseModel):
    response: str


class MathOutput(BaseModel):
    is_math: bool
    reasoning: str

guardrain_agent = Agent(
    name="Guardrail agent",
    instructions="Check output include any math",
    output_type=MathOutput
)

@output_guardrail
async def math_guardrail(
    ctx: RunContextWrapper, agent: Agent, outuput: MessageOutput
) -> GuardrailFunctionOutput:
    
    result = await Runner.run(guardrain_agent, outuput.response, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output, 
        tripwire_triggered=result.final_output.is_math
    )


agent = Agent(
    name="Customer support agent",
    instructions="You are a customer support agent",
    output_type=MessageOutput, 
    output_guardrails=[math_guardrail]
)





async def main():
    try:

        result = await Runner.run(agent, "How to become a AI architect")
        print(result.final_output)
    except OutputGuardrailTripwireTriggered:
        print("Math problem is asked")


if __name__ == "__main__":
    asyncio.run(main())