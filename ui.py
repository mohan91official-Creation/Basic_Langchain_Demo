import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(
    page_title="AI Brainstorming Studio",
    page_icon="🧠",
    layout="centered"
)

# 2. Load environment variables (LangSmith is still tracking!)
load_dotenv()

# 3. Build the UI Header
st.title("🧠 AI Brainstorming Studio")
st.caption("Powered by LangChain, OpenAI, and Streamlit")
st.divider()

# 4. Initialize LangChain Components
# We initialize the LLM and Prompt just like before
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are an expert YouTube strategist. Keep your answers concise, engaging, and conversational."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])

chain = prompt_template | llm | StrOutputParser()

# 5. Handle Memory via Streamlit Session State
# Streamlit reruns on every interaction, so we must store the memory database in session_state
if "store" not in st.session_state:
    st.session_state.store = {}

def get_session_history(session_id: str):
    if session_id not in st.session_state.store:
        st.session_state.store[session_id] = InMemoryChatMessageHistory()
    return st.session_state.store[session_id]

conversational_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)

# 6. Initialize UI Chat History
# This keeps the text visible on the screen after a rerun
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all previous messages in the UI
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 7. The Chat Input and Streaming Logic
if user_input := st.chat_input("What should we brainstorm today?"):

    # Immediately show the user's message in the UI
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate and stream the AI's response
    with st.chat_message("assistant"):
        # We pass the LangChain stream directly to Streamlit's write_stream feature!
        stream_generator = conversational_chain.stream(
            {"question": user_input},
            config={"configurable": {"session_id": "alpha_ui_session"}}
        )
        # st.write_stream creates the typewriter effect and returns the full final string
        full_response = st.write_stream(stream_generator)

    # Save the full AI response to the UI memory
    st.session_state.messages.append({"role": "assistant", "content": full_response})
