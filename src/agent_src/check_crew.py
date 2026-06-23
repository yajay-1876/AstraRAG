from src.agent_src.crew import qa_crew

input_data={
    "user_query":"what is ecosystem",
    "chat_history":{}
}

result= qa_crew.kickoff(input_data)
result_dict=result.to_dict()
print(result_dict)