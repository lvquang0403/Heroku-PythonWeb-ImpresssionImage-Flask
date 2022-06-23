import os
import sys
from huffman import *
from LZW import *
from PIL import  Image
import numpy as np
import cv2
from flask import Flask, request, jsonify, render_template, send_from_directory,url_for
UPLOAD_FOLDER = './upload'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/favicon.png')


@app.route('/')
@app.route('/home')
def get_home():
    return render_template("index")

@app.route("/test", methods=['POST','GET'])
def huffman1():
  if request.method == "POST":
    if 'img' not in request.files:
        return "these is no file"
    image = request.files['img']
    path = app.config['UPLOAD_FOLDER'] + "/" + image.filename
    if not os.path.isdir(app.config['UPLOAD_FOLDER']):
        os.mkdir(app.config['UPLOAD_FOLDER'])
    print(path)
    print("img ",image)
    image.save(path)
    # image = request.form["img"]
    string,filename=huffman(path)
    url = url_for('downloadfile', filename=filename)
    return "<div><a href="+url+">Download</a></td></div><br>"+"<div>"+string+"</div>"
    # print("img ",image)

@app.route("/LZW", methods=['POST','GET'])
def LZW():
  if request.method == "POST":
    if 'img' not in request.files:
        return "these is no file"
    image = request.files['img']
    path = app.config['UPLOAD_FOLDER'] + "/" + image.filename
    if not os.path.isdir(app.config['UPLOAD_FOLDER']):
        os.mkdir(app.config['UPLOAD_FOLDER'])
    print(path)
    print("img ",image)
    image.save(path)
    # image = request.form["img"]
    string,filename=compress(path)
    url = url_for('downloadfile', filename=filename)
    return "<div><a href="+url+">Download</a></td></div><br>"+"<div>"+string+"</div>"
    # print("img ",image)
@app.route('/downloadfile/<filename>',methods=['GET', 'POST'])
def downloadfile(filename):
    return send_from_directory('./compressed',filename, as_attachment=True)

if __name__ == "__main__":
    app.run()
