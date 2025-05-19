#  Nextract - AI Summarizer API (Backend)

This is the Flask-based backend for **Nextract**, an AI-powered summarization app that processes uploaded files and returns abstractive summaries using NLP.

## 🌐 Deployed URL

Backend: [https://nextract-backend.onrender.com](https://nextract-backend.onrender.com)

## 📦 Features

- 🧠 Abstractive Summarization using HuggingFace Transformers (BART/T5)
- 🔍 Extractive Summarization using TextRank
- 📂 File Uploads (.pdf, .docx, .pptx)
- 📥 Returns summaries in JSON format
- 🖇️ CORS enabled for frontend integration

## ⚙️ Tech Stack

- **Backend:** Python, Flask
- **Libraries:** pdfPlumber, python-docx, python-pptx, transformers, flask-cors

## 📦 Setup Instructions

```bash
git clone https://github.com/yourusername/nextract-backend.git
cd nextract-backend
pip install -r requirements.txt
python app.py
