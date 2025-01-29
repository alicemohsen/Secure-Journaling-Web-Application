from flask import Flask, render_template, request, Response, jsonify
from gcm import encrypt_journal, decrypt_journal


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
    if request.method == 'GET':
        return render_template('import.html')
    elif request.method == 'POST':
        # Access the uploaded file and password
        uploaded_file: str = request.json['file']
        password = request.json['password'].strip()

        if not uploaded_file:
            return jsonify({"error": "No file uploaded"}), 400
        if not password:
            return jsonify({"error": "Password is required"}), 400

        # Read the encrypted file data
        encrypted_data = uploaded_file
        # Decrypt the file using the provided password
        decrypted_content = decrypt_journal(password, encrypted_data)
        # Return the decrypted content as a response
        return jsonify({"decrypted_content": decrypted_content})


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
