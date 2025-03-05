from flask import Flask
import logging
from reportExtractor import report_extractor_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

app = Flask(__name__)
app.register_blueprint(report_extractor_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port= 8000, debug=True)
