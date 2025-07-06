🩺 Medical Chatbot Using Llama 2 + LangChain + Pinecone
A locally running medical chatbot that uses Meta’s Llama 2 model to answer health-related questions. Built with Flask, LangChain, and Pinecone for vector search.

<!-- Replace with your image or remove -->

🔍 Features
📚 Understands medical queries and responds intelligently

🧠 Powered by locally hosted Llama 2 model

📁 Retrieves answers from PDFs using LangChain

🌲 Uses Pinecone for vector similarity search

💬 Custom frontend UI (no WhatsApp clone)

🛠️ Tech Stack
Python 3.8

Flask

LangChain

Llama 2 7B Chat (GGML) via ctransformers

Pinecone

HTML + CSS (Custom UI)

🚀 Setup Instructions
1️⃣ Clone the Repository
bash
Copy
Edit
git clone https://github.com/your-username/medical-chatbot
cd medical-chatbot
2️⃣ Create and Activate Environment
bash
Copy
Edit
conda create -n mchatbot python=3.8 -y
conda activate mchatbot
3️⃣ Install Requirements
bash
Copy
Edit
pip install -r requirements.txt
4️⃣ Add Pinecone Credentials
Create a .env file:

ini
Copy
Edit
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_API_ENV=your_pinecone_region
5️⃣ Add Llama 2 Model
Download: llama-2-7b-chat.ggmlv3.q4_0.bin

Place it inside the model/ directory.

6️⃣ Index PDFs
bash
Copy
Edit
python store_index.py
7️⃣ Run the App
bash
Copy
Edit
python app.py
Visit: http://127.0.0.1:5000/

📸 UI Preview
<!-- Optional screenshot of your chatbot -->

🤖 Example Questions You Can Ask
What are the symptoms of diabetes?

How do I take paracetamol?

What is the dosage for vitamin D supplements?

📁 Project Structure
arduino
Copy
Edit
├── app.py
├── store_index.py
├── model/
│   └── llama-2-7b-chat.ggmlv3.q4_0.bin
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── data/
│   └── your-medical-documents.pdf
├── requirements.txt
└── .env
📝 Notes
Model runs locally, no OpenAI or cloud LLMs used.

Works best with domain-specific medical PDFs.

For learning/demo purposes only — not for real clinical use.

💡 Future Improvements
Add user authentication

Integrate speech-to-text

Deploy via RunPod or Hugging Face Spaces

📢 License & Credits
Llama 2 from Meta (via TheBloke's GGML models)

Built with LangChain & Pinecone