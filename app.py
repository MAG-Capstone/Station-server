from flask import Flask, send_file, request, jsonify
import hashlib
import qrcode
import time
import io

app = Flask(__name__)

SECRET_KEY = 12345


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>" # Get current timestamp (for example, in seconds)


@app.route("/qr_generator/<station_id>")
def qr_generator(station_id):
    return generate_qr_code(station_id,SECRET_KEY)

def generate_qr_code(station_id, secret_key):
    timestamp = int(time.time())
    
    hash_input = f"{station_id}:{timestamp}:{secret_key}"
    
    hash_object = hashlib.sha256(hash_input.encode())
    hash_hex = hash_object.hexdigest()
    
    # Embed the timestamp with the hash to help validate expiration later
    qr_data = f"{hash_hex}:{timestamp}"
    
    qr = qrcode.QRCode(box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    # Send the image as a response with the correct MIME type
    return send_file(img_io, mimetype='image/png')
    #return jsonify({"qr_data:"qr_data})

def send_qr_to_main(data):
    #TODO: Connect to main server
