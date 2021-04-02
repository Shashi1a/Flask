import os
import io
import random
import collections
from flask import Flask, request, render_template, redirect, url_for, Response
from werkzeug.utils import secure_filename
from PIL import Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
import pandas
from tensorflow import keras


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/Users/shashi/flask/data/'
app.config['MAX_CONTENT_PATH'] = 16*1024*1024


@app.route('/loaddata_values')
def loadtxt_data():
    f = np.loadtxt(
        '/Users/shashikantkunwar/flask_project/flask/data/config_L32_Temp3.600000_J21.000000.dat')
    dim_1 = np.shape(f)[0]
    dim_2 = np.shape(f)[1]
    dim_L = int(np.sqrt(dim_2))
    img_id = []
    for i in range(5):
        img_id.append(random.randint(0, dim_1))

    print(img_id)
    fig = Figure(figsize=(12, 4))
    for j in range(1, 6, 1):
        axis = fig.add_subplot(1, 5, j)
        axis.imshow(np.reshape(f[img_id[j-1]], (dim_L, dim_L)),
                    origin='lower')
        axis.set_xticks([])
        axis.set_yticks([])

    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")


@app.route('/')
def upload_file():
    return render_template('form_data.html')


@app.route('/save_data', methods=['GET', 'POST', ])
def save_file():
    if request.method == 'POST':
        data_f = request.files['data']
        model_f = request.files['model']

        data_fname = os.path.join('/Users/shashikantkunwar/flask_project/flask/data/',
                                  secure_filename(data_f.filename))
        data_f.save(os.path.join('/Users/shashikantkunwar/flask_project/flask/data/',
                                 secure_filename(data_f.filename)))

        model_fname = os.path.join('/Users/shashikantkunwar/flask_project/flask/model/',
                                   secure_filename(model_f.filename))
        model_f.save(os.path.join('/Users/shashikantkunwar/flask_project/flask/model/',
                                  secure_filename(model_f.filename)))

        results = data_predict(data_fname, model_fname)
        print(results)
     
        # return redirect('/first', data_fname, model_fname)
        return "success"


@app.route('/predict')
def data_predict(inp1, inp2):
    data_f = inp1
    model_f = inp2
    print(model_f)
    print(data_f)

    data = np.loadtxt(data_f)
    dim_1 = np.shape(data)[0]
    dim_2 = np.shape(data)[1]
    dim_L = int(np.sqrt(dim_2))
    print(dim_1, dim_2, dim_L)
    data = np.reshape(data, (dim_1, dim_L, dim_L))
    print(np.shape(data))
    data = np.expand_dims(data, axis=3)
    print(np.shape(data))

    ml_model = keras.models.load_model(model_f)
    result = ml_model.predict(data)
    print(result)
    phase_i = []
    for j in range(np.shape(result)[0]):
        phase_i.append(np.argmax(result[j]))
    res_count = collections.Counter(np.array(phase_i))
    print(res_count)
    max_key = max(res_count, key=res_count.get)
    print(max_key)
    pred = {
        0: 'Ferromagnet',
        1: 'Antiferromagnet',
        2: 'Stripe',
        3: 'Paramagnet'
    }
    print(pred[max_key])

    results = {
        "fullstat": res_count,
        "pred": pred,
        "result": pred[max_key]
    }
   # print(results)

    return results


if __name__ == "__main__":
    app.run()
