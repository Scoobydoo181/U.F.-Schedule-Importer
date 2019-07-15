from flask import Flask, render_template, request
from Static.Python.google_calendar import upload_gcal

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/how-it-works/')
def how_it_works():
    return render_template('how_it_works.html')

@app.route('/import/')
def import_():
    return render_template('import.html')

@app.route('/calendar_import', methods=['POST'])
def calendar_import():
    upload_gcal(request.files['file'])
    return render_template('success.html')


if __name__ == '__main__':    
    app.run()