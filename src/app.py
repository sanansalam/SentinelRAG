import os
import streamlit as st
import pandas as pd
import plotly.express as px  # This handles the charts
import random
from dotenv import load_dotenv

# 1. Core Models & Embeddings
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

# 2. Modern Vector Store
from langchain_chroma import Chroma

# 3. Core Prompts
from langchain_core.prompts import ChatPromptTemplate

# 4. Replacement Chain Imports (using the compatibility package)
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

# --- UI Setup ---
load_dotenv()
st.set_page_config(page_title="SentinelRAG", page_icon="🛡️")

st.title("🛡️ SentinelRAG")
st.markdown("### Cybersecurity & Fraud Intelligence")

@st.cache_resource
def load_rag_system():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = Chroma(persist_directory="data/vector_store/", embedding_function=embeddings)
    
    # Use the updated model name here too!
    llm = ChatGroq(
        temperature=0.1, 
        model_name="llama-3.3-70b-versatile", 
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    system_prompt = (
        "You are a highly skilled Banking Fraud & Compliance Analyst. "
        "Use the provided pieces of retrieved context to answer the user's question accurately. "
        "If the answer is not in the context, say that you don't know, but try to summarize what is available. "
        "\n\nContext: {context}"
    )
    prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{input}")])

    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    
    # INCREASE SEARCH DEPTH TO k=5
    return create_retrieval_chain(
        vector_db.as_retriever(search_kwargs={"k": 5}), 
        combine_docs_chain
    )

# Initialize System
try:
    qa_bot = load_rag_system()
except Exception as e:
    st.error(f"❌ System Error: {e}")
    st.stop()

with st.sidebar:
    st.divider()
    st.header("📊 Fraud Data Pulse")
    
    if st.checkbox("Show Dataset Analytics"):
        try:
            # Load a sample to keep it fast
            df_sample = pd.read_csv("data/raw/creditcard.csv", nrows=5000)
            
            # 1. Fraud Distribution Pie Chart
            fraud_counts = df_sample['Class'].value_counts()
            import plotly.express as px
            fig_pie = px.pie(
                values=fraud_counts.values, 
                names=['Legit', 'Fraud'],
                title="Transaction Distribution",
                color_discrete_sequence=['#2ecc71', '#e74c3c']
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # 2. Amount Distribution
            fig_hist = px.histogram(
                df_sample, x="Amount", 
                title="Transaction Volumes",
                nbins=30
            )
            st.plotly_chart(fig_hist, use_container_width=True)
            
        except Exception as e:
            st.error(f"Could not load dashboard: {e}")

# --- PROACTIVE ALERT BUTTON ---
if st.sidebar.button("🚨 Simulate Fraud Alert"):
    try:
        df_full = pd.read_csv("data/raw/creditcard.csv")
        # Filter for fraud rows (Class 1) and pick a random one
        fraud_sample = df_full[df_full['Class'] == 1].sample(1).iloc[0]
        
        # Format a professional inquiry for the bot
        alert_inquiry = (
            f"ALERT: Transaction for ${fraud_sample['Amount']} flagged. "
            f"Feature V17 is {fraud_sample['V17']:.2f}. "
            f"Based on our manuals, is this transaction typical of account takeover fraud?"
        )
        
        st.session_state.messages.append({"role": "user", "content": alert_inquiry})
        st.rerun() # Refresh to show the message in the chat
    except Exception as e:
        st.sidebar.error(f"Error loading CSV: {e}")

# --- Chat Interface ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_query := st.chat_input("Ask about bank fraud policies..."):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing manuals..."):
            response = qa_bot.invoke({"input": user_query})
            answer = response["answer"]
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})