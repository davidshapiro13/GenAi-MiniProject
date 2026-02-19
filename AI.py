from llmproxy import LLMProxy
import random

class AI():

    def __init__(self, model_name='4o-mini', query_num=5):
        self.client = LLMProxy()
        self.model_name = model_name
        self.temperature = 0.0
        self.last_queries = query_num
        self.rag_enabled = False
        self.session_id_value = 'conversation-' + str(random.random())

    def run(self, system_prompt, query_prompt):
        output = self.client.generate(
            model = self.model_name,
            system = system_prompt,
            query = query_prompt,
            temperature = self.temperature,
            lastk = self.last_queries,
            session_id = self.session_id_value,
            rag_usage = self.rag_enabled,
        )['result']
        return output