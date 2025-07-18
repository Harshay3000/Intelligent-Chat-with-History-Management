from json_memory import JSONMemory
from grok_llm import GrokLLM  
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import AIMessage, HumanMessage
import os 

# LLM Setup
llm = GrokLLM()

# Memory Setup
memory = JSONMemory(memory_file="memory.json",llm=llm, summarize_threshold=500)

# Define the prompt (must match memory keys!)
prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = (
    prompt
    | llm
    | RunnableLambda(lambda text: AIMessage(content=text)) # Convert string output to AIMessage
)

# Wrap chain with memory system
conversation = RunnableWithMessageHistory(
    chain,
    lambda session_id: memory,  
    input_messages_key="input",
    history_messages_key="history"
)

# Streamlit App
st.set_page_config(page_title="🧠 ConversAI", layout="centered")
st.title("🧠 ConversAI")

# Chat input
if "session_id" not in st.session_state:
    st.session_state["session_id"] = "default-user"  # could be random or per-user later
if "input_text_content" not in st.session_state:
    st.session_state["input_text_content"] = ""

def send_message():
    user_input = st.session_state.user_input_widget
    if user_input:
        # Process user input and get respons
        response_obj = conversation.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": st.session_state["session_id"]}}
        )

        # Clear the input box by updating its session state value
        st.session_state.input_text_content = ""
        #st.rerun()

# Display the entire chat history from memory
for message in memory.messages: # memory.messages accesses the chat_memory list
    if isinstance(message, HumanMessage):
        st.markdown(f"**You:** {message.content}")
    elif isinstance(message, AIMessage):
        st.markdown(f"**Grok:** {message.content}")

# User input text box
st.text_input(
    "You:",
    placeholder="Say something...",
    key="user_input_widget",
    on_change=send_message,
    value=st.session_state.input_text_content
)

# Show memory on side panel
with st.sidebar:
    st.title("ConversAI")
    st.header("🗂️ Memory Log")
    if os.path.exists(memory.memory_file):

        try:
            with open("memory.json", "r") as f:
              chat_log = f.read()
              st.code(chat_log, language="json")
            
            st.download_button(
                label="⬇️ Download Memory", 
                data=chat_log, 
                file_name="memory.json", 
                mime="application/json", # MIME type for JSON files
                help="Download the current chat memory as a JSON file."
            )
        except FileNotFoundError:
             st.warning("No memory found yet.")
    else:
        st.warning("No memory found yet.")

    # Optional: Reset memory button
    if st.button("🧹 Clear Memory"):
        memory.clear()
        st.session_state.input_text_content = "" 
        st.success("Memory cleared.")
        st.rerun()

prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}")
])
