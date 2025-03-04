import os
import openai
from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__)

# Set OpenAI API Key
openai.api_key = "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"

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route("/transform", methods=['GET', 'POST'])
def transform_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    # Save uploaded image
    image_file = request.files["image"]
    file_path = os.path.join(UPLOAD_FOLDER,"image_file.jpg")
    image_file.save(file_path)

    # Open image and convert to Base64 for OpenAI
    with open(file_path, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode("utf-8")

    # Send image to OpenAI for transformation
    response = openai.Image.create_edit(
        model="dall-e-2",
        image=base64_image,
        prompt="A futuristic robot dog with metallic features based on the uploaded image.",
        n=1,
        size="1024x1024"
    )

    # Get transformed image URL
    transformed_image_url = response["data"][0]["url"]

    return jsonify({"transformedImageUrl": transformed_image_url}), 200

if __name__== "_main_":
    app.run(debug=True,port=5000)
