import os
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain.chains import RetrievalQA
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env file if present

# Set Gemini API key
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

def get_predictor(faiss_folder="../data/faiss_index"):

    """
    Returns a function predict(inputs: dict) -> dict with key "output".
    This function is suitable as the 'target' in langsmith.evaluate(...).
    """
    # load embeddings & vector db (must match what you used to create the db)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = FAISS.load_local(faiss_folder, embeddings, allow_dangerous_deserialization=True)

    retriever = vectordb.as_retriever()

    # Gemini LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",  # Free Gemini model
        temperature=0
    )

    # RAG chain
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")

    def predict(inputs: dict) -> dict:
        q = inputs.get("input") or inputs.get("question")
        if not q:
            return {"output": ""}
        ans = qa.run(q)  # returns string
        return {"output": ans}

    return predict
