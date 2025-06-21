import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAI

# --- Page Config ---
st.set_page_config(page_title="📦 AI Supply Chain ChatBot", layout="wide")

# --- Sidebar with Sample Data ---
st.sidebar.title("🗂️ Sample Data or Upload Your Own")
sample_files = {
    "Sample Sales Data": "sample_data/train_0irEZ2H.csv",
    "Sample Submission Format": "sample_data/sample_submission_pzljTaX.csv",
    "Sample Test Data": "sample_data/test_nfaJ3J5.csv"
}
selected_sample = st.sidebar.selectbox("Choose sample CSV or upload below", list(sample_files.keys()))
use_sample = st.sidebar.checkbox("Use selected sample file")

uploaded_file = None if use_sample else st.file_uploader("Upload your own CSV", type=["csv"])

# --- Load API Key ---
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("❌ OPENAI_API_KEY not found. Set it using `export OPENAI_API_KEY=your-key`")
    st.stop()

# --- Header ---
st.markdown("<h1 style='text-align: center;'>📦 AI Supply Chain ChatBot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey;'>Upload your CSV or choose a sample. Ask smart questions. Get charts + insights.</p>", unsafe_allow_html=True)

# --- Load Data ---
if use_sample:
    df = pd.read_csv(sample_files[selected_sample])
elif uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = None

if df is not None:
    st.subheader("📊 Preview of Uploaded Data")
    st.dataframe(df.head(), use_container_width=True)

    # Initialize LLM + Agent
    llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)
    agent = create_pandas_dataframe_agent(llm=llm, df=df, verbose=False, allow_dangerous_code=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.markdown("### 💬 Ask a Question")
    query = st.text_input("e.g. What are the top 5 SKUs by units sold?")

    if query:
        with st.spinner("🧠 Thinking..."):
            try:
                response = agent.run(query)
                st.success("✅ Answer:")
                st.markdown(f"<div style='background-color:#F0F2F6;padding:1rem;border-radius:0.5rem;font-size:16px'>{response}</div>", unsafe_allow_html=True)
                st.session_state.chat_history.append((query, response))

                # Auto-generate plot if query sounds like trend
                if any(kw in query.lower() for kw in ["trend", "top", "chart", "plot", "over time"]):
                    try:
                        fig, ax = plt.subplots()
                        df.plot(ax=ax)
                        st.pyplot(fig)
                    except Exception as chart_error:
                        st.warning(f"📉 Chart error: {chart_error}")

            except Exception as e:
                st.error(f"⚠️ Error: {e}")

    # Chat history
    if st.session_state.chat_history:
        st.markdown("### 🕒 Chat History")
        for q, a in st.session_state.chat_history[::-1]:
            st.markdown(f"**You:** {q}")
            st.markdown(f"<div style='background-color:#f9f9f9;padding:0.75rem;border-left:4px solid #3f51b5;border-radius:0.5rem'>{a}</div>", unsafe_allow_html=True)
