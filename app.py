import os

from flask import Flask, render_template, request, redirect

from inference import get_prediction
from commons import format_class_name
import PIL
from PIL import Image
import base64
import os
import io

if not os.path.exists('./static/tmp/'):
    os.makedirs('./static/tmp/')

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files.get('file')
        if not file:
            return
        img_bytes = file.read()
        input_image = Image.open(io.BytesIO(img_bytes))
        input_image.save('./static/tmp/in.jpg')
        class_id, class_name = get_prediction(image_bytes=img_bytes)
        class_name = format_class_name(class_name)
        return render_template('result.html', class_id=class_id,
                               class_name=class_name)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
