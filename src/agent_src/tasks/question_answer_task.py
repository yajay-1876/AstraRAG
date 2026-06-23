from crewai import Task
from pydantic import BaseModel

from src.agent_src.agents.question_answer_agent import qa_agent

class AnswerStructure(BaseModel):
    answer:str
    sources:list[str]
    tool_used:str
    rationale:str

qa_task= Task(
    agent=qa_agent,
    name="Question Answering Task",
    description="""
    Answer thw user query "{user_query}" using Retrieval Augmented Generation (RAG) pipeline.
    chat history : "{chat_history}"
    
    Instructions:
    -Retrieve relevant context from document store.
    -Prioritize evidence that directly addresses the query.
    -Synthesize a clear , accurate answer grounded in retrieved sources or chat history.
    -If query cannot be answered from knowledge source or chat history , do not generate your own response.
     instead , statr clearly that knowledge does not contain the required  information.
     -Provide tanspiracy by including references , tool usage and reasoning steps. 
    """,
    expected_output="""
    A structured JSON object with the following fields.
    {
        "answer":"Direct response to the query (1-3 paragraphs, clear and accurate).
                    if no answer found , return :'The knowledge does not contain the required information.'",
        "sources":["List of document titles, sections, or citations used. (note : return empty list if None)"],
        "tool_used":"Name of the Retrieval analysis tool invoked (Eg.:RagRetriever, VectorDB, Chat History etc.)",
        "rationale":"Brief explanation of why this answer was chosen , or why no relevant information was found"      
     }
    """,
    output_pydantic=AnswerStructure
)