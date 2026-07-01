# RAG Compliance Chatbot

A Retrieval-Augmented Generation (RAG) chatbot designed to answer compliance-related queries by retrieving relevant information from enterprise documents and generating accurate responses using Large Language Models.

The project consists of:

- **Backend:** Flask + LangChain + ChromaDB
- **Frontend:** React
- **Embedding Model:** Sentence Transformers
- **LLM:** Groq (Llama 3.1 8B Instant)
- **Vector Database:** ChromaDB

---

# Project Structure

```text
RAG-compliance-chatbot/
│
├── backend/
│   ├── api.py
│   ├── config.py
│   ├── requirements.txt
│   ├── src/
│   │   ├── data/
│   │   ├── ingest.py
│   │   └── ...
│   ├── chroma_db/
│   └── ...
│
├── frontend/
│
├── start-backend.bat
├── start-frontend.bat
│
└── README.md
```

---

# Prerequisites

Install the following before running the project:

- Python 3.11 or later
- Node.js (v18 or later)
- npm
- Git

---

# 1. Clone the Repository

```bash
git clone <repository-url>
cd RAG-compliance-chatbot
```

---

# 2. Configure the Backend

Navigate to the backend folder.

```bash
cd backend
```

Create a file named

```text
config.py
```

and add the following:

```python
GEMINI_API_KEY = "AQ.**"
GEMINI_MODEL = "gemini-2.5-flash"

GROQ_API_KEY = "**"
GROQ_MODEL = "llama-3.1-8b-instant"
```

Replace the API keys with your own credentials.

> **Note:** The application currently uses **Groq (Llama 3.1 8B Instant)** for inference. The Gemini configuration is retained for future use.

---

# 3. Add Your Documents

Place all PDF documents that should be indexed inside:

```text
backend/src/data/
```

These documents will be converted into embeddings and stored in ChromaDB.

---

# 4. Generate the Vector Database

Before starting the backend, generate the embeddings.

Navigate to the source folder.

```bash
cd src
```

Run

```bash
python ingest.py
```

This script will:

- Read every PDF from `backend/src/data/`
- Split documents into chunks
- Generate embeddings
- Store the embeddings inside ChromaDB

> **Important:** This step must be performed before starting the backend and may take upto 1hr in some cases to get ingested.

Whenever documents are added, removed, or modified, run `ingest.py` again to rebuild the vector database.

---

# 5. Start the Backend

### Option 1 (Recommended)

From the project root, simply run:

```bash
start-backend.bat
```

The script automatically:

- Creates a Python virtual environment (first run only)
- Installs all backend dependencies from `requirements.txt` (first run only)
- Starts the Flask API server

The backend will be available at:

```
http://localhost:8000
```

---

### Option 2 (Manual Setup)

If you prefer to start the backend manually:

Navigate to the backend directory.

```bash
cd backend
```

Create a virtual environment:

**Windows**

```bash
python -m venv .venv
```

Activate the virtual environment:

```bash
.venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```


Finally, start the backend API:

```bash
python api.py
```

The backend will now be running at:

```
http://localhost:8000
```


## 5.1 Running the Chatbot in a Python IDE

If you want to interact with the chatbot directly from a Python IDE (such as VS Code, PyCharm, or IDLE) without starting the Flask API or frontend, you can run the pipeline script.

Navigate to the backend directory:

```bash
cd backend
```

Activate the virtual environment if it has already been created.

**Windows**

```bash
.venv\Scripts\activate
```

Run either of the following scripts:

```bash
python pipeline.py
```

or

```bash
python pipeline1.py
```

The script will start an interactive chatbot session in the terminal, allowing you to enter queries and receive responses directly without using the web interface.

---

# 6. Start the Frontend

Open **another terminal** and run:

```bash
start-frontend.bat
```

The script automatically:

- Installs frontend dependencies (first run only)
- Starts the React development server

Once started, open the URL displayed in the terminal (typically):

```
http://localhost:5173
```

---

# Running the Application

After the initial setup, running the project requires only two commands.

### Terminal 1

```bash
start-backend.bat
```

### Terminal 2

```bash
start-frontend.bat
```

Open the frontend URL in your browser to begin using the chatbot.

---

# Updating the Knowledge Base

Whenever the document collection changes:

1. Add or remove PDFs inside

```text
backend/src/data/
```

2. Rebuild the embeddings

```bash
cd backend/src
python ingest.py
```

3. Restart the backend

```bash
start-backend.bat
```

The chatbot will now use the updated knowledge base.

---

# Technologies Used

### Backend

- Flask
- LangChain
- ChromaDB
- Sentence Transformers
- Groq API
- Google Gemini API (optional)

### Frontend

- React
- JavaScript
- Vite

---

# Troubleshooting

## Backend fails to start

Ensure:

- Python is installed
- `config.py` exists
- API keys are valid
- Embeddings have been generated using `ingest.py`

---

## No answers are retrieved

Make sure:

- PDFs are placed inside

```text
backend/src/data/
```

- `python ingest.py` has been executed successfully.

---

## Frontend fails to start

Run:

```bash
start-frontend.bat
```

If it is the first run, dependency installation may take a few minutes.

---

## Invalid API Key

Verify the values in:

```text
backend/config.py
```

---

## Documents are not reflected in responses

After modifying the documents:

1. Run

```bash
python backend/src/ingest.py
```

2. Restart the backend.

---

# License

This project is intended for educational and research purposes.

---

