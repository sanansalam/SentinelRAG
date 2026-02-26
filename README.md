# 🛡️ SentinelRAG: Cybersecurity & Fraud Intelligence

SentinelRAG is an AI-powered assistant designed for banking institutions to bridge the gap between complex regulatory policies (CFPB/FFIEC) and real-world transaction data.

---

## 🚀 Setup Instructions for Windows

### 1. Clone the Repository
Open **PowerShell** or **Command Prompt** and run the following commands to download the project:
```bash
git clone https://github.com/sanansalam/SentinelRAG.git
cd SentinelRAG
```

### 2. Set Up Virtual Environment
Create a dedicated environment to keep the project dependencies organized:
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies
Install all required libraries, including LangChain, Streamlit, and Plotly:
```bash
pip install -r requirements.txt
```

### 4. Download the Dataset
The credit card dataset is too large for GitHub and must be added manually.

Download Link: (https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud).

Action: Download the creditcard.csv file.

Placement: Navigate to your project folder and place the file inside data/raw/.


### 5. Configure Groq API Key
The chatbot uses Groq's Llama-3 models for high-speed inference.

Get Key: Visit the (https://console.groq.com/home) and click "Create API Key".

Action: Create a new file in the root directory named .env.

Content: Paste the following line into that file:

```plaintext
GROQ_API_KEY=your_actual_key_here
```

### 🛠️ Running the Project

#### Step A: Ingest Data
Before starting the app, you must process the PDFs and CSV to build the local search database:
```bash
python src/ingest.py
```

#### Step B: Launch Chatbot
Start the Streamlit interface:
```bash
streamlit run src/app.py
```

### 📊 Presentation Demo Script
The Policy Expert: Ask the bot, "What is the CFPB rule on how fast a bank has to investigate a disputed charge?".

The Technical Audit: Ask, "What does the FFIEC manual say about Identity Proofing for high-risk transactions?".

Visual Analytics: Use the sidebar checkbox "Show Dataset Analytics" to display transaction trends and fraud ratios.

The Killer Feature: Click "🚨 Simulate Fraud Alert" to pull a real fraud sample from the Kaggle data and have the AI explain the risk based on the manuals.











