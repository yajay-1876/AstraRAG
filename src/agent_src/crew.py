from crewai import Crew

from src.agent_src.tasks.question_answer_task import qa_task
from src.agent_src.agents.question_answer_agent import qa_agent

qa_crew= Crew(
    tasks=[qa_task],
    agents=[qa_agent],
    verbose=True
)