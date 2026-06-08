# 🔬 AI_Research_Paper_Assistant and Summarization

Powered by **Groq (Free)** + **Llama 3.1** + **Streamlit**

---

## ✨ Features

* 📄 Upload and analyze research paper PDFs
* 🧠 AI-powered research paper summarization
* 📑 Section-wise paper analysis
* ❓ Ask questions about the uploaded paper
* 🔍 Automatic text chunking for large documents
* ⚡ Fast inference using Groq LLM
* 🎨 Modern and responsive Streamlit UI

---

## 🛠️ Tech Stack

* Python
* Streamlit
* Groq API
* Llama 3.1
* PyPDF
* NLP (Natural Language Processing)
* Prompt Engineering

---

## 🚀 Local Setup

### Step 1 — Install

```bash
pip install -r requirements.txt
```

### Step 2 — Add API Key

Open `.env` and paste your Groq key:

```env
GROQ_API_KEY=gsk_your_key_here
```

### Step 3 — Run

```bash
streamlit run app.py
```

---

## ☁️ Deploy to Streamlit Cloud (Share a Link)

### Step 1 — Push to GitHub

1. Create a new repository on GitHub
2. Upload all project files (except `.env` and `.streamlit/secrets.toml`)

### Step 2 — Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click **New App**
3. Connect your GitHub repository
4. Set **Main file path** to `app.py`
5. Open **Advanced Settings → Secrets**
6. Add:

```toml
GROQ_API_KEY = "gsk_your_actual_key_here"
```

7. Click **Deploy**

### Step 3 — Share the Link 🎉

Streamlit provides a public URL such as:

```text
https://your-app-name.streamlit.app
```

Share the link with users or your company.

---

## 📁 Project Structure

```text
ai_research_groq/
├── app.py
├── requirements.txt
├── .env
├── .gitignore
├── .streamlit/
│   └── secrets.toml
└── utils/
    ├── __init__.py
    ├── pdf_reader.py
    ├── text_splitter.py
    └── groq_api.py
```

---

## 💻 System Requirements

| Resource | Required     |
| -------- | ------------ |
| RAM      | ~150 MB      |
| GPU      | Not Required |
| Internet | Required     |
| Cost     | 100% Free    |

---

## 📌 Future Enhancements

* PDF Summary Export
* FAISS Vector Search
* Citation Support
* Multi-PDF Comparison
* Chat History
* Advanced Semantic Search

