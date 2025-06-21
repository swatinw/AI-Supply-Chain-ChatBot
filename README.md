# 📦 AI Supply Chain ChatBot

**An AI-powered chatbot that analyzes supply chain CSV data using natural language queries — with instant insights, charts, and smart summaries.**

![banner](https://img.shields.io/badge/Streamlit-App-green)  
![Python](https://img.shields.io/badge/Python-3.10+-blue) ![LangChain](https://img.shields.io/badge/LangChain-LLM%20powered-lightgrey)

---

## 🚀 Demo

👉 **Live App**: [https://supply-chain-chatbot.streamlit.app](#) *(Update after deploy)*  
👉 **Try It With Sample Files** or upload your own CSV!

---

## 🧠 What It Does

✅ Upload a CSV file  
✅ Ask questions like:
- “What are the top 5 SKUs by units sold?”
- “Show me a trend of demand over time”
- “Which store had the highest price variance?”

✅ Get:
- 📊 Tabular insights
- 📈 Auto-generated bar/line plots
- 💬 Chat history of your analysis

---

## 🛠 Built With

- **🧠 OpenAI GPT-4** (via LangChain)
- **📊 pandas** (for data analysis)
- **📈 matplotlib** (for visual plots)
- **⚙️ LangChain** (to create the CSV Agent)
- **💻 Streamlit** (for UI & deployment)

---

## 📁 Folder Structure

```
supply_chain_chatbot/
├── app.py                      # Main Streamlit app
├── requirements.txt            # Python dependencies
├── sample_data/                # Sample CSV files for testing
│   ├── train_0irEZ2H.csv
│   ├── sample_submission_pzljTaX.csv
│   └── test_nfaJ3J5.csv
```

---

## ⚙️ Getting Started Locally

```bash
git clone https://github.com/your-username/supply-chain-chatbot.git
cd supply-chain-chatbot
pip install -r requirements.txt

export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxx"  # set your key
streamlit run app.py
```

---

## 🛡️ Security

This app uses `allow_dangerous_code=True` for the agent to run pandas logic. Do **NOT** deploy publicly with unrestricted access unless you sandbox the runtime.

---

## 📬 Connect With Me

Built with ❤️ by [Swati sharma]  
🔗 [LinkedIn](https://www.linkedin.com/in/your-name) | 🌐 [Portfolio](https://yourportfolio.com)
