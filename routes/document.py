from flask import Blueprint, jsonify, request

from services.ingestion import DocumentIngestion
from services.qdrant import QdrantService

document_bp = Blueprint("document", __name__)

ingestion = DocumentIngestion()
qdrant = QdrantService()


@document_bp.post("/upload")
def upload_document():
    uploaded_file = request.files.get("file")

    if uploaded_file is None:
        return jsonify({"error": "No file uploaded."}), 400

    try:
        result = ingestion.process(uploaded_file)
        qdrant.add_documents(result["chunks"])

        return jsonify(
            {
                "message": "Document indexed successfully.",
                "filename": result["filename"],
                "chunks": result["total_chunks"],
            }
        )

    except Exception as error:
        return jsonify({"error": str(error)}), 500


@document_bp.get("/list")
def list_documents():
    try:
        documents = qdrant.list_documents()
        return jsonify({"documents": documents})

    except Exception as error:
        return jsonify({"error": str(error)}), 500


@document_bp.get("/stats")
def get_stats():
    try:
        stats = qdrant.get_stats()
        return jsonify(stats)

    except Exception as error:
        return jsonify({"error": str(error)}), 500


@document_bp.delete("/<path:filename>")
def delete_document(filename):
    try:
        qdrant.delete_document(filename)
        return jsonify({"message": f"{filename} deleted successfully."})

    except Exception as error:
        return jsonify({"error": str(error)}), 500
