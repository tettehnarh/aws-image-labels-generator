from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import uuid
import io
import csv
from dataclasses import asdict, is_dataclass

from config import Config
from services.image_processor import ImageProcessor
from services.aws_authenticator import AWSAuthenticator
from services.s3_manager import S3Manager
from services.rekognition_manager import RekognitionManager
from services.results_manager import ResultsManager

app = Flask(__name__)
app.config.from_object(Config)

# In-memory stores for demo/dev
UPLOADS: dict[str, dict] = {}
RESULTS: dict[str, dict] = {}


def _to_dict(obj):
    if is_dataclass(obj):
        return asdict(obj)
    if isinstance(obj, list):
        return [ _to_dict(x) for x in obj ]
    if isinstance(obj, dict):
        return {k: _to_dict(v) for k, v in obj.items()}
    return obj


@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/upload", methods=["POST"])
def upload():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    if not ImageProcessor.allowed_file(filename, app.config['ALLOWED_EXTENSIONS']):
        return jsonify({"error": "Unsupported file extension"}), 400

    file_bytes = file.read()
    ok, err = ImageProcessor.validate_image(file_bytes, app.config['MAX_CONTENT_LENGTH'])
    if not ok:
        return jsonify({"error": err}), 400

    if not app.config['S3_BUCKET']:
        return jsonify({"error": "S3_BUCKET not configured"}), 500

    session_id = uuid.uuid4().hex

    try:
        authenticator = AWSAuthenticator(region_name=app.config['AWS_REGION'])
        aws_sess = authenticator.create_session()
        s3m = S3Manager(aws_sess, app.config['S3_BUCKET'])
        key = s3m.generate_key(filename, session_id)
        s3m.upload_bytes(file_bytes, key, file.mimetype or 'application/octet-stream')
        url = s3m.presigned_url(key)
    except Exception as e:
        return jsonify({"error": f"Upload failed: {e}"}), 502

    UPLOADS[session_id] = {"key": key, "image_url": url, "filename": filename}
    return jsonify({"session_id": session_id, "image_url": url})


@app.route("/analyze", methods=["POST"])
def analyze():
    payload = request.get_json(silent=True) or request.form
    session_id = payload.get('session_id') if payload else None
    if not session_id or session_id not in UPLOADS:
        return jsonify({"error": "Invalid or missing session_id"}), 400

    max_labels = int(payload.get('max_labels') or app.config['DEFAULT_MAX_LABELS'])
    min_conf = float(payload.get('confidence_threshold') or app.config['DEFAULT_CONFIDENCE_THRESHOLD'])

    try:
        authenticator = AWSAuthenticator(region_name=app.config['AWS_REGION'])
        aws_sess = authenticator.create_session()
        rek = RekognitionManager(aws_sess)
        key = UPLOADS[session_id]['key']
        resp = rek.detect_labels(app.config['S3_BUCKET'], key, max_labels=max_labels, min_confidence=min_conf)
        result = ResultsManager.parse_rekognition_response(resp)
        result.s3_key = key
        result.image_url = UPLOADS[session_id]['image_url']
        result_dict = _to_dict(result)
        RESULTS[session_id] = result_dict
        return jsonify({"session_id": session_id, "results": result_dict})
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {e}"}), 502


@app.route("/results/<session_id>")
def results(session_id):
    res = RESULTS.get(session_id)
    return render_template("results.html", session_id=session_id, results=res)


@app.route('/export/<fmt>/<session_id>')
def export(fmt, session_id):
    res = RESULTS.get(session_id)
    if not res:
        return jsonify({"error": "No results for session"}), 404
    if fmt == 'json':
        from flask import Response
        import json
        return Response(json.dumps(res, indent=2), mimetype='application/json', headers={'Content-Disposition': f'attachment; filename=labels-{session_id}.json'})
    elif fmt == 'csv':
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['filename', 'label', 'confidence'])
        filename = UPLOADS.get(session_id, {}).get('filename', '')
        for label in res.get('labels', []):
            writer.writerow([filename, label.get('name', ''), label.get('confidence', 0)])
        mem = io.BytesIO(output.getvalue().encode('utf-8'))
        return send_file(mem, mimetype='text/csv', as_attachment=True, download_name=f'labels-{session_id}.csv')
    else:
        return jsonify({"error": "Unsupported export format"}), 400


if __name__ == "__main__":
    app.run(debug=True)

