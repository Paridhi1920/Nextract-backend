from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from summarizer import abstractive_summary
from file_handler import extract_text_from_docx, extract_text_from_pdf, extract_text_from_pptx
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": [
    "http://localhost:5173",
    "https://nextract-frontend.vercel.app",
    "https://nextract-frontend-963h.vercel.app"
]}}, supports_credentials=True)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "pptx", "docx"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if not exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ======= ROUTE TO UPLOAD FILE AND RETURN SUMMARY ========
@app.route("/uploads", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if file and allowed_file(file.filename):
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        length = request.form.get("length", "medium")

        # Extract text from file
        try:
            if file.filename.endswith(".pdf"):
                extracted_text = extract_text_from_pdf(file_path)
            elif file.filename.endswith(".docx"):
                extracted_text = extract_text_from_docx(file_path)
            elif file.filename.endswith(".pptx"):
                extracted_text = extract_text_from_pptx(file_path)
            else:
                return jsonify({"error": "Unsupported file format"}), 400
        except Exception as e:
            return jsonify({"error": f"Text extraction failed: {str(e)}"}), 500

        if not extracted_text.strip():
            return jsonify({"error": "No text extracted from file"}), 400

        # Summarize
        try:
            print("Extracted Text:", extracted_text[:300])
            summary = abstractive_summary(extracted_text, length=length)
            print("Summary:", summary[:300])
            return jsonify({"summary": summary})
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({"error": f"Summary generation failed: {str(e)}"}), 500

    return jsonify({"error": "Invalid file format"}), 400

# ======= OPTIONAL ROUTE TO SERVE FILES IF NEEDED ========
@app.route('/uploads/<filename>', methods=["GET"])
def serve_uploaded_file(filename):
    try:
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
    except Exception as e:
        return jsonify({"error": f"File not found: {str(e)}"}), 404

# ======= MAIN ========
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
