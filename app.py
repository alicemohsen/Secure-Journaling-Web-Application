from flask import Flask, render_template, request, Response
from gcm import encrypt_journal


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


@app.route('/export', methods=['POST'])
def export_page():
    try:
        # get the plaintext from the input
        plaintext = request.json['plaintext'].strip()
        password = request.json['password'].strip()
        if not plaintext:
            return {"error": "Journal must not be empty"}, 400
        print(f'Plaintext: "{plaintext}"')
        if not password:
            return {"error": "Password is required"}, 400
        # encrypt the plaintext
        encrypted_data = encrypt_journal(password, plaintext)
        # download the file
        return Response(
            encrypted_data,
            mimetype='application/octet-stream',
            headers={
                'Content-Disposition': 'attachment; filename="journal.enc"'
            }
        )
    except Exception as e:
        return {"error": f"Unfortunately an error occurred. Please try again.\nError: {e}"}, 500


if __name__ == '__main__':
    app.run(debug=True)
