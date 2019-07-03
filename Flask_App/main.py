from flask import Flask, render_template, request

app = Flask(__name__)
    

@app.route('/calendar_import')
def calendar_import():
    pass

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/how-it-works/')
def how_it_works():
    return render_template('how_it_works.html')

@app.route('/import/')
def import_():
    return render_template('import.html')


if __name__ == '__main__':    
    app.run(debug=True)