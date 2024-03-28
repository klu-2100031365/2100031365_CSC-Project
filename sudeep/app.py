import os
from flask import Flask, render_template, request, send_file
import boto3

app = Flask(__name__)

# Initialize AWS Polly client
polly_client = boto3.client('polly', region_name='us-east-1')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert_text_to_speech():
    text = request.form['text']
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    # Save the audio file locally
    file_path = 'output.mp3'
    with open(file_path, 'wb') as f:
        f.write(response['AudioStream'].read())

    # Send the audio file back to the client
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
