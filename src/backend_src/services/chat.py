#-------------setup logger-----------------------#
from src.logger_config.logger_config import setup_logger
import logging
setup_logger()
logger=logging.getLogger(__name__)
#------------------------------------------------#

from src.agent_src.crew import qa_crew

def get_answer(chat_history: list)-> dict:
    logger.info("Received chat_history.")
    last_user_message= chat_history[-1]
    user_query=last_user_message["content"]
    logger.info(f"Extracted User query : {user_query}")
    history_without_last = chat_history[:-1]

    input_data={
        "user_query":user_query,
        "chat_history":history_without_last
    }
    logger.debug(f"Input for qa_crew : \n{input_data}")
    result=qa_crew.kickoff(input_data)
    result_dict=result.to_dict()
    logger.info(f"Result from crew:{result_dict}")
    return result_dict

