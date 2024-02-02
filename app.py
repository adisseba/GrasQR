from flask import Flask, request, render_template, send_file
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # HTML formulář pro zadávání dat

@app.route('/generate', methods=['POST'])
def generate_qr():
    # Získání dat z formuláře
    data = request.form.to_dict()
    
    # Převod dat na vCard formát
    vcard = f"""
BEGIN:VCARD
VERSION:3.0
FN:{data.get('jmeno')} {data.get('prijmeni')}
N:{data.get('prijmeni')};{data.get('jmeno')};;;
TEL;TYPE=HOME,VOICE:{data.get('telefon')}
EMAIL;TYPE=PREF,INTERNET:{data.get('email')}
ADR;TYPE=WORK,PREF:;;{data.get('adresa')};;;;;
NOTE:{data.get('poznamka')}
END:VCARD
    """.strip()  # .strip() odstraní počáteční a koncové bílé znaky

    # Generování QR kódu
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(vcard)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Příprava QR kódu pro odeslání
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
