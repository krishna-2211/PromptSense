# 🧠 PromptSense

PromptSense is a **context-aware LLM instruction optimizer** that transforms vague user intent into structured, high-quality prompts for better LLM outputs.

It acts as an **intelligence layer between users and LLMs**, improving prompt quality using:

* rule-based reasoning
* LLM refinement (Ollama)
* external context via MCP (files + web)

---

# 🚀 Features

* 🔍 Prompt type classification (learning, resume, analysis, etc.)
* 🧠 Missing context detection
* ✨ Intelligent prompt optimization (hybrid: rules + LLM)
* 📊 Confidence scoring
* 👀 Expected output preview
* 🔀 Prompt variants (concise, detailed, professional)
* 📁 File-based context (Filesystem MCP)
* 🌐 Web-based context (Playwright MCP)

---

# 🏗️ Tech Stack

### Frontend

* React + Vite
* Tailwind CSS

### Backend

* Python + FastAPI
* Pydantic

### AI Layer

* Ollama (local LLMs like LLaMA3 / Mistral)

### Context Layer (MCP)

* Filesystem MCP
* Playwright MCP

---

# ⚙️ Prerequisites

Before running locally, make sure you have:

### ✅ Required

* Python 3.10+
* Node.js (v18+)
* Git

### ✅ Optional but Recommended

* Ollama (for hybrid intelligence)

Install Ollama:
👉 [https://ollama.com](https://ollama.com)

Then pull a model:

```bash
ollama pull llama3
```

---

# 🛠️ Run Locally

## 1️⃣ Clone Repo

```bash
git clone https://github.com/krishna-2211/PromptSense.git
cd PromptSense
```

---

## 2️⃣ Start Backend

```bash
cd backend

python -m venv venv
venv\Scripts\activate   # Mac/Linux: source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

👉 Runs on:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 3️⃣ Start Frontend

```bash
cd frontend

npm install
npm run dev
```

👉 Runs on:
[http://localhost:5173](http://localhost:5173)

---

## 4️⃣ Start MCP Server

```bash
cd mcp_server

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python server.py
```

👉 MCP server handles:

* file reading
* web scraping via Playwright

---

## 5️⃣ Start Ollama (if using hybrid mode)

```bash
ollama serve
```

If already running, you’ll see:

> address already in use → that’s fine

---

# 🧪 Example

### Input

```
explain data science
```

### Output

```
Explain data science in a structured, beginner-friendly way. Cover its core concepts, applications, and practical examples...
```

---

# ⚠️ Troubleshooting

### ❌ Error to start the mcp server

```
Received exception from stream: 1 validation error for JSONRPCMessage
```

✅ Solution: .\venv\Scripts\Activate.ps1 use this to activate the virtual environment for MCP instead of venv\Scripts\activate

---


### ❌ Port already in use (Ollama)

```
Error: listen tcp 127.0.0.1:11434
```

✅ Solution: Ollama is already running → no action needed

---

### ❌ MCP not working

* Ensure `mcp_server` is running
* Check backend logs

---

### ❌ File upload not working

* Ensure `/uploads` folder exists (backend)
* Check file_id returned

---

### ❌ LLM returning weird outputs

* Happens with local models
* fallback system will handle it
