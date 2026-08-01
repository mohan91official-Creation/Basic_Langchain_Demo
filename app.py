from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

# 1. Load environment variables (LangSmith is still tracking everything in the background!)
load_dotenv()

# 2. Initialize the LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# 3. Create a Chat Prompt Template
# We use MessagesPlaceholder to tell LangChain exactly where to insert the memory
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are an expert YouTube strategist. Keep your answers concise, engaging, and conversational."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])

# 4. Create the base chain
chain = prompt_template | llm | StrOutputParser()

# 5. Set up Memory Storage
# This dictionary acts as our temporary database for chat sessions
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# 6. Wrap the chain with Memory
conversational_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)

# 7. The Interactive Chat Loop
print("🚀 Welcome to the AI Brainstorming Studio! (Type 'quit' to exit)")
print("-" * 55)

# We define a session ID so the AI knows which memory bank to pull from
session_id = "alpha_workspace_1"

while True:
    user_input = input("\nYou: ")

    if user_input.lower() == 'quit':
        print("Exiting application. Catch you later!")
        break

    print("\nAI: ", end="", flush=True)

    # STREAMING: We use .stream() instead of .invoke()
    # It yields chunks of text in real-time
    for chunk in conversational_chain.stream(
        {"question": user_input},
        config={"configurable": {"session_id": session_id}}
    ):
        # Print each chunk as it arrives, without adding a new line
        print(chunk, end="", flush=True)

    print("\n" + "-" * 55)
