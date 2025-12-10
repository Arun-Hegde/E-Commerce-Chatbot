import streamlit as st
from pathlib import Path
from router import router
from faq import ingest_faq_data, faq_chain
from sql import sql_chain
from smalltalk import talk_chain

st.set_page_config(
    page_title="E-Commerce Chatbot",
    page_icon="🛒",
    layout="centered",
)

st.markdown(
    """
    <style>
    /* Full-page solid background */
    html, body, .stApp {
        height: 100%;
        background: #0f172a !important;  /* dark navy */
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Remove extra vertical space at top */
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 1.5rem !important;
        max-width: 900px;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: #0b1120 !important;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    /* Title + subtitle */
    .app-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 700;
        margin-top: 0.8rem;
        margin-bottom: 0.15rem;
        background: linear-gradient(90deg, #38bdf8, #a855f7, #f97316);
        -webkit-background-clip: text;
        color: transparent;
    }

    .app-subtitle {
        text-align: center;
        font-size: 1rem;
        color: #cbd5e1;
        margin-bottom: 1rem;
    }

    /* Make BOTH user & assistant bubbles the same style */
    .stChatMessage {
        background: rgba(15,23,42,0.9) !important;
        border-radius: 14px !important;
        padding: 10px 14px !important;
        margin-bottom: 8px !important;
    }

    /* Remove inner background so we only see our custom bubble */
    .stChatMessage > div {
        background: transparent !important;
    }

    /* Chat input styling */
    div[data-baseweb="textarea"] textarea {
        border-radius: 999px !important;
        background: rgba(15,23,42,0.95) !important;
        color: #e5e7eb !important;
        border: 1px solid rgba(148,163,184,0.45) !important;
        padding: 10px 18px !important;
    }

    div[data-baseweb="textarea"] textarea::placeholder {
        color: #64748b !important;
    }

    .stChatInputContainer {
        margin-top: 0.5rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="app-title">E-Commerce Chatbot 🛒</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">Ask FAQ or product-based questions about our store.</div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### ❓ FAQ Examples")
    st.markdown(
        """
- What is the return policy of the products?
- Do I get discount with the HDFC credit card?
- How can I track my order?
- What payment methods are accepted?
- How long does it take to process a refund?
        """
    )

    st.markdown("---")
    st.markdown("### 👟 Product Examples")
    st.markdown(
        """
- I want to buy nike shoes that have 50% discount.
- Are there any shoes under Rs. 3000?
- Do you have formal shoes in size 9?
- Are there any Puma shoes on sale?
- What is the price of puma running shoes?
        """
    )

faqs_path = Path(__file__).parent / "resources/faq_data.csv"
if "faq_ingested" not in st.session_state:
    ingest_faq_data(faqs_path)
    st.session_state["faq_ingested"] = True

def ask(query: str):
    route = router(query).name
    if route == "faq":
        return faq_chain(query)
    elif route == "sql":
        return sql_chain(query)
    elif route == 'small_talk':
        return talk_chain(query)
    else:
        return f"Route {route} not implemented Yet"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

MAX_MESSAGES = 10

for message in st.session_state["messages"]:
    avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

query = st.chat_input("Ask a FAQ / product-based question...")

if query:
    st.session_state["messages"].append({"role": "user", "content": query})
    if len(st.session_state["messages"]) > MAX_MESSAGES:
        st.session_state["messages"] = st.session_state["messages"][-MAX_MESSAGES:]

    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(query)

    response = ask(query)

    st.session_state["messages"].append({"role": "assistant", "content": response})
    if len(st.session_state["messages"]) > MAX_MESSAGES:
        st.session_state["messages"] = st.session_state["messages"][-MAX_MESSAGES:]

    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(response)
