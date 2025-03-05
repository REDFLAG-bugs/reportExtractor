from flask import Blueprint, request, jsonify
import base64
import io
import fitz 
import logging


report_extractor_bp = Blueprint('reportExtractor', __name__)

@report_extractor_bp.route("/reportExtractor", methods=["POST"])
def report_extractor():
    try:
        data = request.get_json()
        if not data or "base64_str" not in data:
            raise ValueError("Missing 'base64_str' parameter in JSON payload.")
        
        base64_str = data["base64_str"]
        try:
            pdf_bytes = base64.b64decode(base64_str)
        except Exception as decode_error:
            logging.exception("Failed to decode base64 string")
            raise ValueError("Invalid base64 string.") from decode_error
        pdf_stream = io.BytesIO(pdf_bytes)
        try:
            doc = fitz.open(stream=pdf_stream, filetype="pdf")
        except Exception as open_error:
            logging.exception("Failed to open PDF document")
            raise ValueError("Could not open PDF document.") from open_error
        extracted_text = []
        for page in doc:
            extracted_text.append(page.get_text("text"))
        result_text = "\n".join(extracted_text)
        return jsonify({"extracted_text": result_text})

    except Exception as err:
        logging.exception("Error processing /reportExtractor request")
        return jsonify({"error": str(err)}), 400
