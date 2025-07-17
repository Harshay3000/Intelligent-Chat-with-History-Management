# Intelligent-Chat-with-History-Management
This project is a conversational chatbot powered by Large Language Models (LLMs) served through the **Groq API**, with persistent memory using a JSON file. The chatbot can remember past interactions and respond accordingly. The interface is built with **Streamlit**, making it simple to deploy as a web app.

---

## 🚀 Features

- ✅ Uses **Groq API** for LLM responses (supports LLaMA-3 and other models)
- 🧠 Implements **persistent memory** using a JSON file to remember previous interactions
- 💾 Memory can be exported and reused later
- ✂️ Long LLM responses are **automatically summarized** to reduce file size
- 🌐 User-friendly chat interface using **Streamlit**
- 📁 Automatically saves each conversation to `memory.json`

---

## 🛠️ Technologies Used

- [Python 3.10+](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [Groq API](https://console.groq.com/)
- JSON for memory persistence

---

## 📂 File Structure
.
├── app.py # Main Streamlit application
├── memory.json # Persistent memory storage
├── summarizer.py # Summarization function for long LLM replies
├── utils.py # Helper utilities (loading/saving memory, etc.)
├── requirements.txt # Required Python packages
└── README.md # Project documentation

## 🧠 How Memory Works

- Every user message and bot reply is stored in a JSON file (`memory.json`)
- Before sending a new message to the LLM, the last **N interactions** (configurable) are loaded as context
- This allows the bot to **remember names**, preferences, and topics from earlier in the conversation
- Long AI responses are automatically summarized before being saved to memory, helping to keep the context concise and manage token limits for the LLM.

---

## 📝 Example Use Cases
- A chatbot that remembers your name and past questions
- Long-term support assistant with historical context
- Personalized study assistant or tutor
- Conversational journaling app

---

## 📦 Exporting Memory
- You can export the current conversation memory anytime by accessing or downloading the memory.json file. This allows you to reuse or analyze conversations later.

---

## ▶️ How to Run the App
1. **Clone the repository**

   - git clone https://github.com/your-username/llm-chatbot-groq.git
   - cd llm-chatbot-groq

2. **Create virtual environment (optional but recommended)**
   - python -m venv venv
   - source venv/bin/activate        # macOS/Linux
   - venv\Scripts\activate           # Windows

3. **Install dependencies**
    - pip install -r requirements.txt
   
4. **Add your Groq API key**
    - export GROQ_API_KEY=your_groq_api_key   # Linux/macOS
    - set GROQ_API_KEY=your_groq_api_key      # Windows

---

## 🧑‍💻 Author
- Harshay Chouhan
- Data Science enthusiast | AI Developer






