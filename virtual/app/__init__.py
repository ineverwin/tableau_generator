from flask import Flask, request, redirect, render_template, url_for, jsonify, make_response, send_from_directory, abort, session

app = Flask(__name__)

from app import views

app.config['FILES'] = "E:\\Dropbox\\Projects and Freelance\\Bain\\AAGProducts\\python\\my_flask\\virtual\\app\\static\\upload"
app.config["ALLOWED_EXTENSIONS"] = ["XLS", "XLSX"]
app.config["SECRET_KEY"] = "12345"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/uploads/<filename>')
def uploadFile (filename):
    return send_from_directory(app.config['FILES'], filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)