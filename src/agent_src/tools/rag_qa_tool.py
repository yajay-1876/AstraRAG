#-------------setup logger-----------------------#
from src.logger_config.logger_config import setup_logger
import logging
setup_logger()
logger=logging.getLogger(__name__)
#--------------------------------------------------#
from crewai.tools import tool
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from llama_index.core import Settings
import chromadb

from src.agent_src.config.agent_settings import AgentSettings

logger.info("Loading Embedding Model...")
embed_model=HuggingFaceEmbedding()
logger.info("Embedding Model loaded successfully")


@tool
def rag_query_tool(query: str) -> dict :
    """
    Answers a query by retrieving relevant documents and generating a response.
    Returns both generated answer and source file names from which the information was retrieved.

    :arguments:
        query (str) : The input query string to be processed.
    :returns:
        dict: A dictionary with thw following keys:
            -'answer': The generated answer string.
            -'source_files':List of source file names used for retrieval.
    """
    logger.info(f"Using embedding model id: {id(embed_model)}")
    settings=AgentSettings()
    vector_store_path=settings.VECTOR_STORE_DIR
    collection_name=settings.COLLECTION_NAME
    # configure llm in llama_index.core.Settings
    Settings.llm=Groq(
        model=settings.MODEL_NAME,
        temperature=settings.MODEL_TEMPERATURE,
        api_key=settings.GROQ_API_KEY
    )
    # Load Chroma collection
    db=chromadb.PersistentClient(path=vector_store_path)
    chroma_collection=db.get_or_create_collection(collection_name)
    # Connect to vector store
    vector_store=ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context=StorageContext.from_defaults(vector_store=vector_store)
    # Load Index from chroma
    index=VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        storage_context=storage_context,
        embed_model=embed_model
    )
    # create query engine
    query_engine=index.as_query_engine(similarity_top_k=3)
    # pass the query to query engine
    response=query_engine.query(query)
    source_file_names={  m.get('file_name') for m in getattr(response, 'metadata', {}).values()  }

    return {
        "answer": response.response,
        "source_files": list(source_file_names)
    }


# For direct testing, uncomment the code below and comment out @tool.
# When using CrewAI, uncomment @tool and comment out the test code.

# output = rag_query_tool(query="Explain transformer in electric")
# print(output)
# print(output["answer"])
# print(output["source_files"])