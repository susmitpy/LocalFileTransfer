from flask import Flask, request, redirect, url_for, send_from_directory, make_response
import os
import socket
import qrcode

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
DOWNLOAD_FOLDER = './downloads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Handle file uploads
        files = request.files.getlist('file')
        saved_files = []
        for file in files:
            if file.filename:
                filename = file.filename
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                saved_files.append(filename)

        # Handle text input
        text_content = request.form.get('text_content')
        if text_content:
            text_filename = 'input_text.txt'
            text_path = os.path.join(UPLOAD_FOLDER, text_filename)
            with open(text_path, 'w') as f:
                f.write(text_content)
            saved_files.append(text_filename)

        return redirect(url_for('upload_file'))

    # List files in the download directory
    files = os.listdir(DOWNLOAD_FOLDER)
    files_list = '<ol>' + ''.join([f'<li><a href="{url_for("download_file", filename=file)}" download="{file}">{file}</a></li>' for file in files]) + '</ol>'
    return '''
    <!doctype html>
    <title>Upload and Download Files</title>
    <h1>Upload New Files</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file multiple>
      <input type=text name=text_content placeholder="Enter text here">
      <input type=submit value=Upload onclick="this.disabled=true;this.value='Uploading…';this.form.submit();">
    </form>
    <h2>Download Files</h2>
    ''' + files_list

@app.route('/downloads/<filename>')
def download_file(filename):
    response = make_response(send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True))
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response

def get_ip():
    return socket.gethostbyname(socket.gethostname())

def generate_qr_code(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.show()

if __name__ == "__main__":
    ip = get_ip()
    port = 5000
    url = f"http://{ip}:{port}"
    generate_qr_code(url)
    print(f"Server running on {url}")
    app.run(host='0.0.0.0', port=port)  # This will make the server accessible on your network
