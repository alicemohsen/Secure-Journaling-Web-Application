from flask import Flask, render_template


app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates'
)

@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/create')
def create_page():
    return render_template('create.html')


@app.route('/import')
def import_page():
    return render_template('import.html')


if __name__ == '__main__':
    app.run(debug=True)
