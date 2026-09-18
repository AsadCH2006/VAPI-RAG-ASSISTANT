# Real-Time RAG Voice Assistant 🎙️⚡

An ultra-low latency, real-time conversational voice assistant equipped with Retrieval-Augmented Generation (RAG). Built to deliver human-like, speech-to-speech interactions while fetching precise context from custom document knowledge bases.

---

## ✨ Features

- **⚡ Real-Time Voice Pipeline:** Ultra-fast voice input and output streaming powered by WebSockets.
- **📚 Knowledge Base Grounding (RAG):** Upload and index custom documents (PDFs, TXT, Markdown) to deliver context-aware, grounded responses.
- **🔊 Natural Speech Synthesis:** Dynamic, human-like voice synthesis with conversational fluidity.
- **🎨 Modern Interactive UI:** Clean, responsive, and minimalist web interface for managing active calls, microphone feeds, and document contexts.
- **🛠️ Extensible Architecture:** Modular architecture supporting flexible integration of custom LLMs, vector indices, and STT/TTS models.

---

## 🛠️ Architecture Overview

1. **Client / Web UI:** Capture audio stream from user microphone and render live state visualizer.
2. **Real-Time Gateway (LiveKit):** Manages bi-directional audio transport with minimal latency.
3. **Voice Agent Engine:** Performs realtime Speech-to-Text (STT), queries vector stores for context (RAG), feeds context to an LLM, and streams generated text to Text-to-Speech (TTS).

---

## 🚀 Getting Started

Follow these instructions to set up and run the application on your local machine.

### Prerequisites

Ensure you have the following installed on your system:
- [Python 3.10+](https://www.python.org/)
- [Node.js 18+](https://nodejs.org/)
- `pip` and `npm` package managers

---

### 1. Installation

Clone this repository or extract the project source files locally:

```bash
cd real-time-rag-voice-assistant
```

#### Backend Setup (Python)
Create and activate a virtual environment, then install required Python packages:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Frontend Setup (Node.js)
Install frontend dependencies:

```bash
npm install
```

---

### 2. Environment Configuration

Create a `.env` file in the root folder of the project based on `.env.example`:

```bash
cp .env.example .env
```

Open the `.env` file and fill in your credential values:

```env
# LiveKit Credentials
LIVEKIT_URL=wss://your-livekit-project.livekit.cloud
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret

# AI Models & Services
OPENAI_API_KEY=your_openai_api_key
# Optional: ELEVENLABS_API_KEY / GROQ_API_KEY if configured in backend
```

---

### 3. Running Locally

To run the application, you need to execute both the agent backend and the web frontend simultaneously.

#### Terminal 1: Backend Voice Agent
```bash
# Ensure virtual environment is activated
source venv/bin/activate # or venv\Scripts\activate on Windows

# Start agent in development mode
python agent.py dev
```

#### Terminal 2: Frontend Web UI
```bash
npm run dev
```

Once both processes are running, open your browser and navigate to:
```
http://localhost:3000
```

---

## 🎥 Demo & Usage

1. Grant microphone permissions in your browser.
2. Upload a text or PDF document to populate the local RAG knowledge base.
3. Click **Connect / Start Session** and speak naturally into your microphone.
4. The assistant will transcribe your query, retrieve relevant facts from your document, and respond in real-time.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).