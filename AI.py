#AI LLM Access point 

from llmproxy import LLMProxy
import random
from ingest import upload_pdf_to_course
from memory import extract_and_store_memory

class AI():

    #Initializes the AI agent
    def __init__(self, memory_session, chat_session, model_name='4o-mini', query_num=10):
        self.client = LLMProxy()
        self.model_name = model_name
        self.last_queries = query_num
        self.memory_session = memory_session
        self.chat_session = chat_session
        self.rag_enabled = True

    # Run a LLM prompt
    def run(self, system_prompt, query_prompt, session):
        output = self.client.generate(
            model = self.model_name,
            system = system_prompt,
            query = query_prompt,
            lastk = self.last_queries,
            temperature=0.0,
            session_id = session,
            rag_usage = self.rag_enabled,
            rag_threshold = 0.5
        )['result']
        extract_and_store_memory(self.client, query_prompt, output, self.memory_session, self.chat_session)
        return output
    
    #Upload the rag
    def upload_rag(self, path):
        upload_pdf_to_course(self.client, path, self.memory_session)