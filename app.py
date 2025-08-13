from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Lazy import services to avoid circulars during early scaffolding
try:
    from services.image_processor import ImageProcessor
except Exception:
    ImageProcessor = None  # Will be implemented


@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/health")
def health():
    return {"status": "ok"}


# Placeholder routes to align with specs; will be implemented fully later
@app.route("/upload", methods=["POST"]) 
def upload():
    return jsonify({"message": "Upload endpoint not yet implemented"}), 501


@app.route("/analyze", methods=["POST"]) 
def analyze():
    return jsonify({"message": "Analyze endpoint not yet implemented"}), 501


@app.route("/results/<session_id>") 
def results(session_id):
    return render_template("results.html", session_id=session_id, results=None)


if __name__ == "__main__":
    app.run(debug=True)

