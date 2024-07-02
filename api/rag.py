from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_openai import ChatOpenAI
from operator import itemgetter


from dotenv import load_dotenv
import os 

from db.qdrant import vector_store

load_dotenv()

model = ChatOpenAI(
    model="gpt-4-turbo-preview",
    api_key=os.getenv('OPENAI_API_KEY'),
    temperature=0,
)

prompt_template = """
Anwser the question based on the context, in a concise manner and using bullet points where applicable.

Context: {context}
Question: {question}
Answer:
"""

prompt = ChatPromptTemplate.from_template(prompt_template)

retriever = vector_store.as_retriever()

def create_chain():
    chain = (
        {
            "context":retriever.with_config(top_k=4),
            "question": RunnablePassthrough(),
        }
        | RunnableParallel({
            "response": prompt | model,
            "context": itemgetter("context"),
        })
    )
    return chain

def get_answer_and_docs(question: str):
    chain = create_chain()
    response = chain.invoke(question)
    answer = response["response"].content
    context = response["context"]
    print("CONTEXT: ", context)
    return {
        "answer": answer,
        "context": context
    }

response = get_answer_and_docs("How does one address relay setting application issues?")


print(response)

