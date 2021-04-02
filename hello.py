import os
from flask import  Flask,request,render_template,redirect,url_for
from werkzeug.utils import  secure_filename
from PIL import Image


app=Flask(__name__)
app.config['UPLOAD_FOLDER']='/Users/shashi/flask/data/'
app.config['MAX_CONTENT_PATH']=16*1024*1024


@app.route('/')
def hello_world():
	return 'Hello world new'

@app.route('/show_image')
def show_data():
	img="/Users/shashi/flask/data/brainy_quotes.png"
	print(img)
	return render_template('disp_data.html',data=img)


@app.route('/upload_data')
def upload_file():
	return render_template('form_data.html')

@app.route('/save_data',methods=['GET', 'POST',])
def save_file():
	if request.method=='POST':
		f=request.files['file']
		#f.save(os.path.join('app.config['UPLOAD_FOLDER']',secure_filename(f.filename)))
		f.save(os.path.join('/Users/shashi/flask/data/',secure_filename(f.filename)))
		return redirect(url_for('upload_model'))


@app.route('/upload_model')
def upload_model():
	return render_template('form_model.html')

@app.route('/save_model',methods=['GET', 'POST',])
def save_model():
	if request.method=='POST':
		f=request.files['file']
		#f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
		f.save(os.path.join('/Users/shashi/flask/model/',secure_filename(f.filename)))

		return 'Well done'
