# Set up a logger
from src.logger_config.logger_config import setup_logger
import logging
setup_logger()
logger=logging.getLogger(__name__)

# Load settings from environmental variables
from src.rag_doc_ingestion.config.rag_doc_ingestion_settings import RAG_DocIngestionSettings
settings         = RAG_DocIngestionSettings()
docs_dir_path    = settings.DOCUMENTS_DIR
vector_store_dir = settings.VECTOR_STORE_DIR
collection_name  = settings.COLLECTION_NAME

# Download and load embedding model
logger.info("Loading HuggingFaceEmbedding model...")
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
embed_model      = HuggingFaceEmbedding()
logger.info("Embedding model loaded successfully")
#------------------vectorization---------------#
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SimpleNodeParser
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex

#---------------main function --------------------#
def build_vector_from_docs():
    logger.info("Starting Vector Store ingestion process.")
    try:
        logger.debug(f"Loading docs from dir:{docs_dir_path}.")
        loader            = SimpleDirectoryReader(input_dir=docs_dir_path)
        documents         = loader.load_data()
        logger.info(f"Loaded {len(documents)} documents")
        if not documents:
            logger.warning("No documents found in input directory")
            return 1

        logger.info("Parsing documents as Nodes (chunks).")
        parser            = SimpleNodeParser.from_defaults(chunk_size=1024, chunk_overlap=50)
        nodes             = parser.get_nodes_from_documents(documents)
        logger.info(f"Generated {len(nodes)} nodes.")

        logger.info(f"Initializing ChromaDB persistent client")
        logger.debug(f" Vector Store Path : {vector_store_dir}.")
        db                = chromadb.PersistentClient(path=vector_store_dir)
        chroma_collection = db.get_or_create_collection(name=collection_name)

        logger.info(f"Creating Chroma Vector Store")
        logger.debug(f"Collection name: {collection_name}")
        vector_store      = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context   = StorageContext.from_defaults(vector_store=vector_store)

        logger.info(f"Building Vector Store Index")
        index             = VectorStoreIndex(
            nodes           = nodes,
            storage_context = storage_context,
            vector_store    = vector_store,
            embed_model     = embed_model
        )

        logger.info("Vector Store Built Successfully")
        return 0
    except Exception as e:
        logger.error(f"Error during Vector Store build :\n{e}")
        return 1


if __name__=="__main__":
    build_vector_from_docs()