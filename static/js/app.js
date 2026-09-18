const API_BASE = "/api/documents";

const uploadForm = document.getElementById("uploadForm");
const fileInput = document.getElementById("fileInput");
const uploadBtn = document.getElementById("uploadBtn");
const uploadBtnText = document.getElementById("uploadBtnText");
const uploadStatus = document.getElementById("uploadStatus");
const documentsList = document.getElementById("documentsList");
const statDocs = document.getElementById("statDocs");
const statChunks = document.getElementById("statChunks");
const sidebar = document.getElementById("sidebar");
const sidebarToggle = document.getElementById("sidebarToggle");
const mobileMenuBtn = document.getElementById("mobileMenuBtn");

// ===================== Sidebar Toggle (Mobile) =====================
mobileMenuBtn?.addEventListener("click", () => sidebar.classList.add("open"));
sidebarToggle?.addEventListener("click", () => sidebar.classList.remove("open"));

// ===================== Upload =====================
uploadForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const file = fileInput.files[0];
    if (!file) return;

    uploadBtn.disabled = true;
    uploadBtnText.textContent = "Indexing...";
    uploadStatus.textContent = "";
    uploadStatus.className = "status-message";

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch(`${API_BASE}/upload`, {
            method: "POST",
            body: formData,
        });

        const data = await response.json();

        if (response.ok) {
            uploadStatus.textContent = `${data.filename} indexed (${data.chunks} chunks)`;
            uploadStatus.classList.add("success");
            fileInput.value = "";
            loadDocuments();
            loadStats();
        } else {
            throw new Error(data.error || "Upload failed");
        }
    } catch (err) {
        uploadStatus.textContent = err.message;
        uploadStatus.classList.add("error");
    } finally {
        uploadBtn.disabled = false;
        uploadBtnText.textContent = "Upload & Index";
    }
});

// ===================== Load Documents =====================
async function loadDocuments() {
    try {
        const response = await fetch(`${API_BASE}/list`);
        const data = await response.json();
        const documents = data.documents || [];

        if (documents.length === 0) {
            documentsList.innerHTML = `<p class="empty-state">No documents yet</p>`;
            return;
        }

        documentsList.innerHTML = documents
            .map(
                (doc) => `
                <div class="document-item" data-filename="${escapeHtml(doc.filename)}">
                    <div class="document-info">
                        <span class="document-name" title="${escapeHtml(doc.filename)}">${escapeHtml(doc.filename)}</span>
                        <span class="document-chunks">${doc.chunks} chunks</span>
                    </div>
                    <button class="delete-btn" data-filename="${escapeHtml(doc.filename)}">✕</button>
                </div>
            `
            )
            .join("");
    } catch (err) {
        documentsList.innerHTML = `<p class="empty-state">Failed to load documents</p>`;
    }
}

// Event delegation instead of inline onclick="" (safe for filenames with quotes/special chars)
documentsList.addEventListener("click", (e) => {
    const btn = e.target.closest(".delete-btn");
    if (!btn) return;
    deleteDocument(btn.dataset.filename);
});

// ===================== Delete Document =====================
async function deleteDocument(filename) {
    if (!confirm(`Delete "${filename}" from knowledge base?`)) return;

    try {
        const response = await fetch(`${API_BASE}/${encodeURIComponent(filename)}`, {
            method: "DELETE",
        });

        if (!response.ok) throw new Error("Delete failed");

        loadDocuments();
        loadStats();
    } catch (err) {
        alert("Failed to delete document: " + err.message);
    }
}

// ===================== Load Stats =====================
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const data = await response.json();

        statDocs.textContent = data.total_documents ?? 0;
        statChunks.textContent = data.total_chunks ?? 0;
    } catch (err) {
        statDocs.textContent = "-";
        statChunks.textContent = "-";
    }
}

function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
}

// ===================== Vapi Voice Assistant =====================
let vapi = null;
let callStartTime = null;
let timerInterval = null;

const micBtn = document.getElementById("micBtn");
const voiceVisual = document.getElementById("voiceVisual");
const pulseRing = document.getElementById("pulseRing");
const voiceStatus = document.getElementById("voiceStatus");
const callTimer = document.getElementById("callTimer");
const transcriptLog = document.getElementById("transcriptLog");
const infoStatus = document.getElementById("infoStatus");
const clearBtn = document.getElementById("clearBtn");

async function initVapi() {
    if (!window.VAPI_PUBLIC_KEY || !window.VAPI_ASSISTANT_ID) {
        voiceStatus.textContent = "Voice assistant is not configured (missing API key or assistant ID).";
        console.error("VAPI_PUBLIC_KEY or VAPI_ASSISTANT_ID is missing/empty.");
        return;
    }

    try {
        // @vapi-ai/web ships as a CJS bundle, so loading it with a plain
        // <script src="...unpkg.../vapi.js"> tag throws "exports is not
        // defined" and window.Vapi never gets defined. esm.sh re-wraps
        // the package as a real browser ES module instead.
        const { default: Vapi } = await import("https://esm.sh/@vapi-ai/web@latest");
        vapi = new Vapi(window.VAPI_PUBLIC_KEY);
        attachVapiEvents();
    } catch (err) {
        console.error("Failed to load Vapi SDK:", err);
        voiceStatus.textContent = "Failed to load voice assistant SDK.";
    }
}

function attachVapiEvents() {
    vapi.on("call-start", () => {
        micBtn.classList.add("active");
        pulseRing.classList.add("active");
        document.getElementById("micIcon").textContent = "⏹️";
        voiceStatus.textContent = "Listening...";
        infoStatus.textContent = "Connected";
        clearTranscriptPlaceholder();
        startTimer();
    });

    vapi.on("call-end", () => {
        micBtn.classList.remove("active");
        pulseRing.classList.remove("active");
        document.getElementById("micIcon").textContent = "🎤";
        voiceStatus.textContent = "Tap the mic to start talking";
        infoStatus.textContent = "Idle";
        stopTimer();
    });

    vapi.on("speech-start", () => {
        voiceStatus.textContent = "Assistant is speaking...";
    });

    vapi.on("speech-end", () => {
        voiceStatus.textContent = "Listening...";
    });

    vapi.on("message", (message) => {
        if (message.type === "transcript" && message.transcriptType === "final") {
            addTranscriptBubble(message.role, message.transcript);
        }
    });

    vapi.on("error", (err) => {
        voiceStatus.textContent = "Something went wrong. Try again.";
        micBtn.classList.remove("active");
        pulseRing.classList.remove("active");
        stopTimer();
        console.error("Vapi error:", err);
    });
}

function clearTranscriptPlaceholder() {
    const placeholder = transcriptLog.querySelector(".empty-state");
    if (placeholder) placeholder.remove();
}

function addTranscriptBubble(role, text) {
    const bubble = document.createElement("div");
    bubble.className = `transcript-bubble ${role === "user" ? "user" : "assistant"}`;
    bubble.textContent = text;
    transcriptLog.appendChild(bubble);
    transcriptLog.scrollTop = transcriptLog.scrollHeight;
}

function startTimer() {
    callStartTime = Date.now();
    timerInterval = setInterval(() => {
        const seconds = Math.floor((Date.now() - callStartTime) / 1000);
        const mins = String(Math.floor(seconds / 60)).padStart(2, "0");
        const secs = String(seconds % 60).padStart(2, "0");
        callTimer.textContent = `${mins}:${secs}`;
    }, 1000);
}

function stopTimer() {
    clearInterval(timerInterval);
    callTimer.textContent = "";
}

micBtn.addEventListener("click", () => {
    if (!vapi) return;

    if (micBtn.classList.contains("active")) {
        vapi.stop();
    } else {
        vapi.start(window.VAPI_ASSISTANT_ID);
    }
});

async function loadAssistantInfo() {
    try {
        const response = await fetch("/api/vapi/assistant-info");
        const data = await response.json();

        document.getElementById("infoModel").textContent = `${data.model_provider} / ${data.model_name}`;
        document.getElementById("infoVoice").textContent = data.voice_provider;
        document.getElementById("infoTranscriber").textContent = data.transcriber_provider;
    } catch (err) {
        console.error("Failed to load assistant info", err);
    }
}

clearBtn?.addEventListener("click", () => {
    // Agar call chal rahi hai to pehle end karo
    if (vapi && micBtn.classList.contains("active")) {
        vapi.stop();
    }

    // Transcript clear karke placeholder wapas dikhao
    transcriptLog.innerHTML = `<p class="empty-state">Your conversation will appear here</p>`;

    // Timer aur status reset
    stopTimer();
    voiceStatus.textContent = "Tap the mic to start talking";
    infoStatus.textContent = "Idle";
});

// ===================== Init =====================
document.addEventListener("DOMContentLoaded", () => {
    loadDocuments();
    loadStats();
    initVapi();
    loadAssistantInfo();
});