import os

from flask import Flask, render_template, request, redirect

from inference import get_prediction
from commons import format_class_name
import PIL
from PIL import Image
import base64
import os
import io
import numpy as np
import nibabel as nib
from nibabel import FileHolder, Nifti1Image
from gzip import GzipFile
import matplotlib.pyplot as plt
if not os.path.exists('./static/tmp/'):
    os.makedirs('./static/tmp/')

app = Flask(__name__)
def image_normalize(img):
    img = (img - np.min(img))/(np.max(img) - np.min(img))
    img = np.uint8(img*255)
    return img

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files.get('file')
        print('file',file.filename)
        fname = file.filename
        rr = file.read()
        bb = io.BytesIO(rr)
        fh = FileHolder(fileobj=GzipFile(fileobj=bb))
        img = Nifti1Image.from_file_map({'header': fh, 'image': fh})
        print('img',img)
        img_data = image_normalize(img.get_data())
        print('img_data',img_data.shape)
        print('img_data',img_data)
        idx = 100
        #plt.imshow(img_data[:,idx,:])
        #plt.show()
        input_image_1 = Image.fromarray(img_data[:,idx,:])
        input_image_1.save('./static/tmp/in.png')
        class_id, class_name = get_prediction(image_bytes=rr)
        class_name = format_class_name(class_name)
        return render_template('result.html', class_id=class_id,
                               class_name=class_name)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
