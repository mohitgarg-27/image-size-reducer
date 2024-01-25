from flask import Flask, render_template, request
from PIL import Image
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resize', methods=['POST'])
def resize_image():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    scale_percent = int(request.form['scale_percent'])

    original_path = 'uploads/original.jpg'
    resized_path = 'static/resized.jpg'

    file.save(original_path)

    original_image = Image.open(original_path)
    original_width, original_height = original_image.size
    original_dimensions = f"{original_width} x {original_height}"

    if original_image.mode == 'RGBA':
        original_image = original_image.convert('RGB')

    original_file_size = os.path.getsize(original_path)  # Get original file size

    new_width = int(original_width * scale_percent / 100)
    new_height = int(original_height * scale_percent / 100)

    resized_image = original_image.resize((new_width, new_height))
    resized_image.save(resized_path)

    resized_width, resized_height = resized_image.size
    resized_dimensions = f"{resized_width} x {resized_height}"

    uploaded_image = '/uploads/original.jpg'
    resized_image = '/static/resized.jpg'

    os.remove(original_path)

    return render_template('index.html', uploaded_image=uploaded_image, resized_image=resized_image, original_width=original_width, original_height=original_height, original_dimensions=original_dimensions, resized_width=resized_width, resized_height=resized_height, resized_dimensions=resized_dimensions, original_file_size=original_file_size)

if __name__ == '__main__':
    app.run(debug=True)
