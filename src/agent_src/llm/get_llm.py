from crewai import LLM
from dotenv import load_dotenv
load_dotenv()
from src.agent_src.config.agent_settings import AgentSettings

settings=AgentSettings()
model_name=settings.MODEL_NAME
model=f"groq/{model_name}"
def get_llm_for_agent(agent_name):
    return LLM(
        model=model,
        temperature=settings.MODEL_TEMPERATURE
    )