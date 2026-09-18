import requests as http_requests
from flask import Blueprint, jsonify, request

from services.rag import RAGService
from config.settings import VAPI_PRIVATE_KEY, VAPI_ASSISTANT_ID, VAPI_API_BASE_URL

vapi_bp = Blueprint("vapi", __name__)

rag = RAGService()


@vapi_bp.get("/health")
def health():
    return jsonify({"status": "running"})


@vapi_bp.get("/assistant-info")
def assistant_info():
    try:
        response = http_requests.get(
            f"{VAPI_API_BASE_URL}/assistant/{VAPI_ASSISTANT_ID}",
            headers={"Authorization": f"Bearer {VAPI_PRIVATE_KEY}"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        model = data.get("model", {})
        voice = data.get("voice", {})
        transcriber = data.get("transcriber", {})

        return jsonify(
            {
                "model_provider": model.get("provider", "N/A"),
                "model_name": model.get("model", "N/A"),
                "voice_provider": voice.get("provider", "N/A"),
                "transcriber_provider": transcriber.get("provider", "N/A"),
            }
        )
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@vapi_bp.post("/webhook")
def webhook():
    payload = request.get_json(silent=True) or {}
    message = payload.get("message", {})

    if message.get("type") != "tool-calls":
        return jsonify({"received": True})

    results = []
    for tool_call in message.get("toolCalls", []):
        if tool_call.get("function", {}).get("name") != "query_knowledge_base":
            continue

        arguments = tool_call.get("function", {}).get("arguments", {})
        query = arguments.get("query", "").strip()

        if not query:
            answer = "Please provide a question."
        else:
            try:
                answer = rag.ask(query)
            except Exception:
                answer = "Sorry, I couldn't retrieve an answer from the knowledge base."

        results.append({"toolCallId": tool_call.get("id"), "result": answer})

    return jsonify({"results": results})
