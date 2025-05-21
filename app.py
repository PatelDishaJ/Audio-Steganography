from flask import Flask, render_template, request, redirect, url_for, send_file, flash#pip install flask
import os
from algorithms.encode import encode
from algorithms.decode import decode

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'static/uploads/'
RESULT_FOLDER = 'static/results/'
EXTRACTED_FOLDER = 'static/extracted/'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)
os.makedirs(EXTRACTED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encode', methods=['GET', 'POST'])
def encode_audio():
    if request.method == 'POST':
        audio_file = request.files['audio_file']
        secret_message = request.form.get('secret_message', '')  # May be empty
        image_file = request.files.get('image_file')  # Optional

        if not audio_file or (not secret_message and not image_file):
            flash('Please upload an audio file and either enter a message or upload an image.')
            return redirect(url_for('encode_audio'))

        audio_path = os.path.join(UPLOAD_FOLDER, audio_file.filename)
        output_filename = f"encoded_{audio_file.filename}"
        output_path = os.path.join(RESULT_FOLDER, output_filename)

        audio_file.save(audio_path)

        try:
            if image_file:
                image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
                image_file.save(image_path)
                encode(audio_path, output_path, secret_message=None, image_path=image_path)
            else:
                encode(audio_path, output_path, secret_message, image_path=None)

            flash('Encoding successful! Download the encoded audio below.')
            return render_template('encode.html', download_url=url_for('download_file', filename=output_filename))
        except Exception as e:
            flash(f'Error: {e}')
            return redirect(url_for('encode_audio'))

    return render_template('encode.html')

@app.route('/decode', methods=['GET', 'POST'])
def decode_audio():
    if request.method == 'POST':
        audio_file = request.files['audio_file']

        if not audio_file:
            flash('Please upload an audio file.')
            return redirect(url_for('decode_audio'))

        audio_path = os.path.join(UPLOAD_FOLDER, audio_file.filename)
        audio_file.save(audio_path)

        try:
            decoded_message, extracted_image = decode(audio_path)

            if extracted_image:
                extracted_filename = os.path.basename(extracted_image)
                return render_template('decode.html', message=None, image_url=url_for('download_image', filename=extracted_filename))
            else:
                return render_template('decode.html', message=decoded_message, image_url=None)

        except Exception as e:
            flash(f'Error: {e}')
            return redirect(url_for('decode_audio'))

    return render_template('decode.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(RESULT_FOLDER, filename), as_attachment=True, download_name=filename)

@app.route('/download_image/<filename>')
def download_image(filename):
    return send_file(os.path.join(EXTRACTED_FOLDER, filename), as_attachment=True, download_name=filename)

if __name__ == '__main__':
    app.run(debug=True)

