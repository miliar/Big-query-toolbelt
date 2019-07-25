from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/copy", methods=['POST', 'GET'])
def copy():
    if request.method == 'POST':
        flash(request.form)
    return render_template('copy.html')


@app.route("/delete", methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        flash(request.form)
    return render_template('delete.html')


@app.route("/write", methods=['POST', 'GET'])
def write():
    if request.method == 'POST':
        flash((request.form, request.files))
    return render_template('write.html')


if __name__ == '__main__':
    app.run(debug=True)
