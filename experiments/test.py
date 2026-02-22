from llmproxy import LLMProxy
import time

client = LLMProxy()
model_name = '4o-mini'
last_queries = 8
rag_enabled = True
session_id_value = 'testFILffffffffE'
output = client.upload_file(file_path="syllabus.pdf", session_id=session_id_value, strategy="smart")
time.sleep(10)
output = client.generate(
        model = '4o-mini',
        system = 'You are a professor.',
        lastk=10,
        query = "What's the name of the class?",
        session_id = session_id_value,
        rag_usage = True,
        rag_k=5,
        rag_threshold=0.3
    )

print(output)
