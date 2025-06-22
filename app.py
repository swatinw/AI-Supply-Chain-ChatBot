import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAI

# Page setup
st.set_page_config(page_title="📦 AI Supply Chain ChatBot", layout="wide")

# Sidebar: choose sample or upload
st.sidebar.title("🗂️ Sample Data or Upload Your Own")
sample_files = {
    "Sample Sales Data": "sample_data/train_0irEZ2H.csv",
    "Sample Submission Format": "sample_data/sample_submission_pzljTaX.csv",
    "Sample Test Data": "sample_data/test_nfaJ3J5.csv"
}
selected_sample = st.sidebar.selectbox("Choose sample CSV or upload below", list(sample_files.keys()))
use_sample = st.sidebar.checkbox("Use selected sample file")
uploaded_file = None if use_sample else st.file_uploader("Upload your own CSV", type=["csv"])

# API key from env
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("❌ OPENAI_API_KEY not found. Set it as an environment variable.")
    st.stop()

# Main title
st.markdown("<h1 style='text-align: center;'>📦 AI Supply Chain ChatBot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey;'>Upload a CSV or use a sample. Ask supply chain questions. Get charts & insights instantly.</p>", unsafe_allow_html=True)

# Load Data
df = None
try:
    if use_sample:
        df = pd.read_csv(sample_files[selected_sample], on_bad_lines='warn')
    elif uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, encoding='utf-8', on_bad_lines='warn')
        except UnicodeDecodeError:
            df = pd.read_csv(uploaded_file, encoding='ISO-8859-1', on_bad_lines='warn')
except Exception as e:
    st.error(f"⚠️ Failed to load file: {e}")
    st.stop()

# Show Data + Handle Queries
if df is not None:
    st.subheader("📊 Data Preview")
    st.dataframe(df.head(), use_container_width=True)

    llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)
    agent = create_pandas_dataframe_agent(llm=llm, df=df, verbose=False, allow_dangerous_code=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    query = st.text_input("💬 Ask a question like 'Top 5 SKUs by units sold' or 'Price trend over time'")

    if query:
        with st.spinner("🧠 Thinking..."):
            try:
                if "top" in query.lower() and "sku" in query.lower():
                    top_skus = df.groupby("sku_id")["units_sold"].sum().sort_values(ascending=False).head(5).reset_index()
                    st.success("✅ Top 5 SKUs by Units Sold")
                    st.dataframe(top_skus)
                    st.bar_chart(top_skus.set_index("sku_id"))
                    st.session_state.chat_history.append((query, top_skus.to_markdown(index=False)))
                else:
                    response = agent.run(query)
                    st.success("✅ Answer:")
                    st.markdown(f"<div style='background-color:#F0F2F6;padding:1rem;border-radius:0.5rem;'>{response}</div>", unsafe_allow_html=True)
                    st.session_state.chat_history.append((query, response))
            except Exception as e:
                st.error(f"⚠️ Error: {e}")

    # Show chat history
    if st.session_state.chat_history:
        st.markdown("### 🕒 Chat History")
        for q, a in st.session_state.chat_history[::-1]:
            st.markdown(f"**You:** {q}")
            st.markdown(f"<div style='background-color:#f9f9f9;padding:0.75rem;border-left:4px solid #3f51b5;border-radius:0.5rem'>{a}</div>", unsafe_allow_html=True)
