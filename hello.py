import os
import io
from flask import Flask, request, render_template, redirect, url_for, Response
from werkzeug.utils import secure_filename
from PIL import Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
import numpy as np
import pandas


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/Users/shashi/flask/data/'
app.config['MAX_CONTENT_PATH'] = 16*1024*1024


@app.route('/')
def hello_world():
    return 'Hello world new'


@app.route('/show_image')
def show_data():
    img = "/static/brainy_quotes.png"
    content = {
        'a': '2',
        'x': ' I dont know'
    }

    print(img)
    return render_template('disp_data.html', data=content)


@app.route('/loaddata_values')
def loadtxt_data():
    f = np.loadtxt(
        '/Users/shashikantkunwar/flask_project/flask/data/config_L32_Temp3.600000_J21.000000.dat')
    dim_1 = np.shape(f)[0]
    dim_2 = np.shape(f)[1]
    dim_L = int(np.sqrt(dim_2))
    print(np.shape(f))
    fig = Figure()
    axis = fig.add_subplot(1, 3, 1)
    axis.imshow(np.reshape(f[1000], (dim_L, dim_L)),
                origin='lower')
    axis1 = fig.add_subplot(1, 3, 2)
    axis1.imshow(np.reshape(f[2000], (dim_L, dim_L)),
                 origin='lower')
    axis2 = fig.add_subplot(1, 3, 3)
    axis2.imshow(np.reshape(f[5000], (dim_L, dim_L)),
                 origin='lower')
    axis.set_xticks([])
    axis1.set_xticks([])
    axis2.set_xticks([])
    axis.set_yticks([])
    axis1.set_yticks([])
    axis2.set_yticks([])
    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")


@app.route('/upload_data')
def upload_file():
    return render_template('form_data.html')


@app.route('/save_data', methods=['GET', 'POST', ])
def save_file():
    if request.method == 'POST':
        f = request.files['file']
        # f.save(os.path.join('app.config['UPLOAD_FOLDER']',secure_filename(f.filename)))
        f.save(os.path.join('/Users/shashikantkunwar/flask_project/flask/data/',
               secure_filename(f.filename)))
        return redirect(url_for('upload_model'))


@app.route('/upload_model')
def upload_model():
    return render_template('form_model.html')


@app.route('/save_model', methods=['GET', 'POST', ])
def save_model():
    if request.method == 'POST':
        f = request.files['file']
        # f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
        f.save(os.path.join('/Users/shashikantkunwar/flask_project/flask/model/',
               secure_filename(f.filename)))

    return 'Well done'


if __name__ == "__main__":
    app.run()
