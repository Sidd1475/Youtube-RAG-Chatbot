# Youtube RAG Chatbot

A Retrieval-Augmented Generation (RAG) based chatbot that allows users to ask questions directly from YouTube videos using transcript retrieval, semantic search, FAISS vector database, and Gemini LLM.

The project was built completely from scratch to understand the complete lifecycle of a modern RAG pipeline — from transcript ingestion to frontend deployment.

---

# 🚀 Features

* 🎥 Ask questions directly from YouTube videos
* 🧠 RAG pipeline built from scratch (without LangChain chains)
* 🔎 Semantic retrieval using FAISS
* 🤖 Gemini-powered answer generation
* 🌐 Multi-language subtitle support
* 💬 Chat-style conversational UI
* 📚 Source citation with timestamps
* ⚡ Duplicate chunk removal
* 🧾 Conversation memory support
* ☁️ Streamlit cloud deployment
* 🛡️ Graceful handling for blocked transcripts & API failures

---

# 🏗️ Project Architecture

```text
YouTube Video
      ↓
Transcript Extraction
      ↓
Preprocessing
      ↓
Chunking
      ↓
Embeddings
      ↓
FAISS Vector Store
      ↓
Semantic Retrieval
      ↓
Prompt Building
      ↓
Gemini LLM
      ↓
Final Answer + Sources
```

---

# 📂 Project Structure

```text
Youtube-RAG-Chatbot/
│
├── app.py                     # Streamlit frontend
├── main.py                    # CLI-based execution
├── requirements.txt
│
├── src/
│   ├── ingestion/
│   │   ├── youtube_loader.py
│   │   └── preprocess.py
│   │
│   ├── indexing/
│   │   ├── chunker.py
│   │   ├── embedder.py
│   │   └── vector_store.py
│   │
│   ├── generation/
│   │   ├── llm.py
│   │   └── prompt_builder.py
│   │
│   ├── pipeline/
│   │   └── rag_pipeline.py
│   │
│   └── utils/
│
└── data/
```

---

# ⚙️ How the Pipeline Was Built

## 1. Transcript Ingestion

`youtube_loader.py`

* Fetches subtitles using `youtube-transcript-api`
* Supports multiple subtitle languages
* Includes fallback language handling

---

## 2. Preprocessing

`preprocess.py`

* Cleans transcript text
* Removes noise & extra spaces
* Structures transcript data

---

## 3. Chunking

`chunker.py`

* Splits transcript into semantic chunks
* Preserves timestamps
* Improves retrieval quality

---

## 4. Embedding Generation

`embedder.py`

* Converts chunks into vector embeddings
* Uses Sentence Transformers
* Embeddings power semantic retrieval

---

## 5. Vector Database

`vector_store.py`

* FAISS-based vector storage
* Stores chunk embeddings
* Handles similarity search
* Supports save/load indexing

---

## 6. Retrieval

Inside `rag_pipeline.py`

* Converts user query → embedding
* Searches FAISS index
* Retrieves top relevant chunks
* Removes duplicate chunks

---

## 7. Prompt Engineering

`prompt_builder.py`

* Builds structured RAG prompt
* Injects:

  * retrieved context
  * timestamps
  * source references
  * conversation history

---

## 8. LLM Generation

`llm.py`

* Gemini API integration
* Generates grounded responses
* Handles model busy/server errors

---

# 💻 Running the Project

## Clone Repository

```bash
git clone <your-repo-url>
cd Youtube-RAG-Chatbot
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Add Gemini API Key

Create `.env`

```env
GEMINI_API_KEY=your_api_key
```

---

# ▶️ Run CLI Version

`main.py` provides a terminal-based RAG chatbot.

```bash
python main.py
```

Flow:

```text
Enter Video ID
→ Process Transcript
→ Create Embeddings
→ Retrieve Relevant Chunks
→ Generate Answer
```

---

# 🌐 Run Streamlit Frontend

`app.py` provides a chat-style frontend.

```bash
streamlit run app.py
```

Features:

* Chat interface
* Multi-language support
* Source timestamps
* Session-based memory
* Error handling
* Real-time processing feedback

---

# 🧠 Conversation Memory

The chatbot supports conversational follow-up questions.

Example:

```text
Q1: Who was Ram?
Q2: Why did he leave Ayodhya?
```

The system rewrites short follow-up questions using previous conversation context.

---

# 📚 Source Citation

Every response includes:

* relevant transcript chunks
* timestamps
* retrieved source context

Example:

```text
⏱ 12:30 - 13:05
```

---

# 🌐 Multi-language Support

Supports:

* English subtitles
* Hindi subtitles
* Translation fallback using `deep-translator`

---

# ☁️ Deployment

The project was deployed on Streamlit Cloud.

Deployment setup included:

* Streamlit secrets management
* Gemini API configuration
* dependency optimization
* cloud-compatible FAISS handling

---
# UI Images - Streamlit
<img width="1600" height="868" alt="b2f10527-6952-474d-b758-876474a37093" src="https://github.com/user-attachments/assets/446ea80e-b10b-47fe-a66a-74c7f28197f1" />
<img width="1546" height="892" alt="1d12f343-6e9e-457b-8255-bd0b0aadbfc3" src="https://github.com/user-attachments/assets/423b89c8-0d41-420d-86de-70f9b763e975" />



# ⚠️ Challenges Faced During Development

## 1. FAISS Index Handling

Initially retrieval failed because:

* embeddings were not being persisted correctly
* vector store state mismatched UI state

Solution:

* implemented save/load logic
* added vector store validation

---

## 2. Query Retrieval Bugs

Issues:

* duplicate chunks
* incorrect similarity indexing
* retrieval inconsistencies

Solution:

* deduplication logic
* chunk trimming
* retrieval filtering

---

## 3. Streamlit Session State

Managing:

* chat history
* current processed video
* persistent UI state

was one of the major frontend challenges.

---

## 4. Gemini API Failures

Handled:

* model busy errors
* server overload
* API configuration issues

using graceful error handling.

---

## 5. YouTube Transcript Blocking

One major challenge was:

* transcript requests being blocked on cloud deployment

Solution:

* fallback transcript handling
* retry strategy
* multi-language fallback
* graceful UI errors

---

# ✨ What Makes This Project Unique

Unlike many wrapper-based RAG apps, this project:

* builds the RAG pipeline manually
* implements custom retrieval logic
* manages FAISS directly
* handles retrieval optimization
* supports conversational memory
* includes cloud deployment handling

The focus of this project was not only building a chatbot, but understanding how real-world RAG systems are engineered end-to-end.

---

# 🔮 Future Improvements

* Separate vector DB per video
* Hybrid search (semantic + keyword)
* Streaming responses
* Better transcript reliability
* Caching embeddings
* Advanced reranking
* Video summarization mode

---

# 🛠️ Tech Stack

* Python
* Streamlit
* FAISS
* Sentence Transformers
* Gemini API
* YouTube Transcript API

---

# 📌 Learning Outcomes

This project helped in understanding:

* complete RAG architecture
* semantic search systems
* vector databases
* embedding pipelines
* prompt engineering
* frontend/backend integration
* deployment challenges in GenAI systems

---

# 🙌 Final Note

This project was built as a hands-on exploration of how modern AI retrieval systems work internally — beyond just using frameworks.

The goal was to deeply understand:

* indexing
* retrieval
* vector search
* grounding
* conversational memory
* deployment realities

while building a fully functional AI application end-to-end.
