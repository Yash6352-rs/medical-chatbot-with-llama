import os
from flask import Flask, render_template, request
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Pinecone as LangchainPinecone
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import CTransformers
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
INDEX_NAME = "medical-chatbot"

# Flask App
app = Flask(__name__)
qa = None

def setup_pipeline():
    global qa

    pc = Pinecone(api_key=PINECONE_API_KEY)

    if INDEX_NAME not in pc.list_indexes().names():
        pc.create_index(
            name=INDEX_NAME,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region=PINECONE_ENVIRONMENT)
        )
    else:
        print("Pinecone index already exists.")

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    index = pc.Index(INDEX_NAME)
    stats = index.describe_index_stats()
    vector_count = stats.get("total_vector_count", 0)

    if vector_count == 0:
        loader = DirectoryLoader("data/", glob="*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
        chunks = splitter.split_documents(documents)
        print(f"Split into {len(chunks)} chunks.")

        LangchainPinecone.from_texts(
            [t.page_content for t in chunks],
            embedding=embeddings,
            index_name=INDEX_NAME
        )
        print("Upload complete.")
    else:
        print(f"Pinecone has {vector_count} vectors. Skipping upload.")

    docsearch = LangchainPinecone.from_existing_index(INDEX_NAME, embeddings)

    # Load LLM 
    llm = CTransformers(
        model="model/llama-2-7b-chat.ggmlv3.q4_0.bin",
        model_type="llama",
        config={"max_new_tokens": 512, "temperature": 0.7}
    )
    print("LLM loaded.")

    prompt_template = """
    Use the following pieces of information to answer the user's question.
    If you don't know the answer, just say that you don't know — don't make it up.

    Context: {context}
    Question: {question}

    Only return the helpful answer below and nothing else.
    Helpful answer:
    """
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=docsearch.as_retriever(search_kwargs={"k": 2}),
        return_source_documents=False,
        chain_type_kwargs={"prompt": PROMPT}
    )
    print("RetrievalQA chain ready.")


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html") 

@app.route("/get", methods=["POST"])
def get_response():
    user_msg = request.form.get("msg")
    if not user_msg:
        return "No message received."

    try:
        result = qa({"query": user_msg})
        answer = result["result"]
        return answer
    except Exception as e:
        print(f"Error during QA: {e}")
        return "Sorry, something went wrong while processing your request."

if __name__ == "__main__":
    # Avoid reinitialization on debug reload
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or os.environ.get("FLASK_ENV") != "development":
        setup_pipeline()
        print("🚀 Ready for requests.")

    app.run(debug=True)
