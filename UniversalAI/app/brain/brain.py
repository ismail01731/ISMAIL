from app.llm.provider_factory import get_provider
from app.memory.memory import save_user, save_assistant, get_history
from app.context.context_manager import ContextManager
from app.agents.controller import AgentController
from app.agents.multi_agent import MultiAgent


llm = get_provider()
context = ContextManager()
agent = AgentController()
multi_agent = MultiAgent()

async def process_message(message: str):

    agent_summary = await multi_agent.execute(message)

    print(agent_summary)

    from app.memory.memory import (
        save_user,
        save_assistant,
        get_history
    )

    # User message save
    save_user(message)

    # Agent Execute
    print("STEP 1")
    agent_result = await agent.execute(message)
    print("STEP 2")
    history = get_history()
    print("STEP 3")
    prompt = context.build(
        message,
        history,
        results
    )
    print("STEP 4")
    answer = await llm.generate(prompt)
    print("STEP 5")
    
    prompt = context.build(...)
    

    intent = agent_result["intent"]

    results = agent_result["results"]

    plan = agent_result["plan"]

    # Load conversation history
   

    # Build Prompt
    

    print("========== PROMPT ==========")
    print(prompt)
    print("============================")

    # Generate Answer
    answer = await llm.generate(prompt)


    print("TYPE:", type(answer))
    print("REPR:", repr(answer))
    print("ANSWER:", answer)

    print("========== ANSWER ==========")
    print(answer)
    print("============================")

    # Save Assistant Message
    save_assistant(answer)

    return {
        "success": True,
        "intent": intent,
        "plan": plan,
        "history": history,
        "answer": answer
    }