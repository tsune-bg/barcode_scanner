import os
import logging
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import barcode_scanner
import product_database

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key_for_development")

# Configure upload settings
UPLOAD_FOLDER = "/tmp/barcode_uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max upload


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan_barcode():
    # Check if image file was uploaded
    if "image" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["image"]

    # Check if user submitted an empty form
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Check if file is allowed
    if not allowed_file(file.filename):
        return (
            jsonify(
                {
                    "error": "File type not allowed. Please upload an image (PNG, JPG, JPEG, GIF)"
                }
            ),
            400,
        )

    try:
        # Save the file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Scan the barcode
        logger.debug(f"Scanning barcode from image: {filepath}")
        barcode_data = barcode_scanner.scan_barcode(filepath)

        # If no barcode found
        if not barcode_data:
            return (
                jsonify(
                    {
                        "error": "No barcode detected in the image. Please try another image with a clearer barcode."
                    }
                ),
                400,
            )

        # Look up product information
        barcode_number = barcode_data.get("data")
        barcode_type = barcode_data.get("type")

        logger.debug(f"Barcode detected: {barcode_number} (Type: {barcode_type})")

        product_info = product_database.get_product_by_barcode(barcode_number)

        # Clean up the uploaded file
        os.remove(filepath)

        # Always return barcode info, with or without product info
        # Change status code to 200 even if product not found
        return (
            jsonify(
                {
                    "barcode": barcode_number,
                    "type": barcode_type,
                    "product": product_info,  # This will be None if product not found
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"Error processing barcode: {str(e)}")
        return jsonify({"error": f"Error processing the image: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
