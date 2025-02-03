from flask import Flask, render_template, request, Response, jsonify
from gcm import encrypt_journal, decrypt_journal


# create the flask app
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


@app.route('/import', methods=['GET', 'POST'])
def import_page():
    # display import form page
    if request.method == 'GET':
        return render_template('import.html')
    # decrypt the given file with the given password
    elif request.method == 'POST':
        # get the file and password from the request body
        uploaded_file: str = request.json['file']
        password = request.json['password'].strip()

        # handle empty cases
        if not uploaded_file:
            return jsonify({"error": "No file uploaded"})
        if not password:
            return jsonify({"error": "Password is required"})

        # read encrypted file data
        encrypted_data = uploaded_file
        # decrypt using gcm
        decrypted_content = decrypt_journal(password, encrypted_data)
        # return decrypted content as a response
        return jsonify({"decrypted_content": decrypted_content})


# route to encrypt given journal
@app.route('/export', methods=['POST'])
def export_page():
    try:
        # get the plaintext from the request body
        plaintext = request.json['plaintext'].strip()
        password = request.json['password'].strip()
        if not plaintext:
            return {"error": "Journal must not be empty"}, 400
        if not password:
            return {"error": "Password is required"}, 400
        # encrypt the plaintext using gcm
        encrypted_data = encrypt_journal(password, plaintext)
        # send the file as a response
        return Response(
            encrypted_data,
            mimetype='application/octet-stream',
            headers={
                'Content-Disposition': 'attachment; filename="journal.enc"'
            }
        )
    except Exception as e:
        return {"error": f"Unfortunately an error occurred. Please try again.\nError: {e}"}, 500


# run the app
if __name__ == '__main__':
    app.run(debug=True)
