from flask import Flask, request
import requests
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    address = request.form.get('address')
    id_file = request.files['id_file']

    message = f"""
🏠 <b>New Tenancy Application</b>
👤 Name: {name}
📧 Email: {email}
📞 Phone: {phone}
🏡 Address: {address}
"""

    send_text_message(message)

    if id_file:
        filename = secure_filename(id_file.filename)
        files = {'document': (filename, id_file.stream, id_file.mimetype)}
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument",
            data={'chat_id': TELEGRAM_CHAT_ID, 'caption': f"📎 ID for {name}"},
            files=files
        )

    return {'status': 'ok'}, 200

def send_text_message(text):
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={'chat_id': TELEGRAM_CHAT_ID, 'text': text, 'parse_mode': 'HTML'}
    )

if __name__ == '__main__':
    app.run(debug=True)
