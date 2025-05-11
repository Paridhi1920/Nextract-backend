from flask import Flask, jsonify, request
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

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


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

        if file.filename.endswith(".pdf"):
            extracted_text = extract_text_from_pdf(file_path)
        elif file.filename.endswith(".docx"):
            extracted_text = extract_text_from_docx(file_path)
        elif file.filename.endswith(".pptx"):
            extracted_text = extract_text_from_pptx(file_path)
        else:
            return jsonify({"error": "Unsupported file format"}), 400

        if not extracted_text.strip():
            return jsonify({"error": "No text extracted from file"}), 400

        try:
            print("Extracted Text: ", extracted_text[:300])
            print("Summary Length: ", length)
            summary = abstractive_summary(extracted_text, length=length)
            print("Summary: ", summary[:300])
            return jsonify({"summary": summary})
        except Exception as e:
            import traceback
            traceback.print_exc()  # Add this line to log full error
            return jsonify({"error": f"Summary generation failed: {str(e)}"}), 500

    return jsonify({"error": "Invalid file format"}), 400  


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)