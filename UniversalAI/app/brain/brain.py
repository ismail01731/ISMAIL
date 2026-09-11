from app.llm.provider_factory import get_provider
from app.memory.memory import save_user, save_assistant, get_history
from app.context.context_manager import ContextManager
from app.agents.controller import AgentController
from app.agents.modules.medical_safety import MedicalSafety

llm = get_provider()
context = ContextManager()
agent = AgentController()
medical_safety = MedicalSafety()


async def process_message(message: str):
    # Save user message
    save_user(message)

    # Agent + Planner + Plugins
    agent_result = await agent.execute(message)

    intent = agent_result["intent"]
    plan = agent_result["plan"]
    results = agent_result["results"]

    # Conversation history
    history = get_history()

    # Build LLM prompt
    prompt = context.build(
        message,
        history,
        results
    )

    # Generate answer ONCE
    answer = await llm.generate(prompt)

    # -------------------------------------------------
    # MEDICAL SAFETY LAYER
    # -------------------------------------------------
    if "medical" in intent:
        try:
            # Apply deterministic medical safety filtering
            answer = medical_safety.quality_filter(
                message,
                answer
            )

            # Validate final response
            if not medical_safety.validate_response(answer):
                answer = (
                    "এই প্রশ্নের জন্য নিরাপদ ও নির্ভরযোগ্য তথ্য দিতে "
                    "চিকিৎসকের পরামর্শ নেওয়া সবচেয়ে ভালো। "
                    "যদি গুরুতর উপসর্গ থাকে, দ্রুত চিকিৎসা সহায়তা নিন।"
                )

        except Exception as e:
            print("Medical Safety Error:", e)

            # Fail-safe response
            answer = (
                "স্বাস্থ্যসংক্রান্ত এই বিষয়ে নিশ্চিতভাবে "
                "পরামর্শ দেওয়ার জন্য চিকিৎসকের সঙ্গে কথা বলা "
                "সবচেয়ে নিরাপদ। গুরুতর উপসর্গ থাকলে দ্রুত "
                "চিকিৎসা সহায়তা নিন।"
            )

    # Save final safe answer
    save_assistant(answer)

    return {
        "success": True,
        "intent": intent,
        "plan": plan,
        "history": history,
        "answer": answer
    }