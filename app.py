from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)


UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
FONT_PATH = "fonts/DejaVuSans.ttf"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


pdfmetrics.registerFont(TTFont("TurkceFont", FONT_PATH))

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        ad = request.form.get("ad")
        eposta = request.form.get("eposta")
        tel = request.form.get("telefon")
        diller = request.form.get("diller")
        tecrubeler = request.form.get("tecrubeler")
        araclar = request.form.get("araclar")

        # Fotoğrafı kaydet
        foto = request.files["foto"]
        foto_ad = secure_filename(foto.filename)
        foto_yolu = os.path.join(app.config["UPLOAD_FOLDER"], foto_ad)
        foto.save(foto_yolu)

        # PDF oluştur
        dosya_adi = f"{OUTPUT_FOLDER}/{ad.replace(' ', '_')}_cv.pdf"
        c = canvas.Canvas(dosya_adi, pagesize=A4)
        width, height = A4

        c.setFont("TurkceFont", 22)
        c.drawCentredString(width / 2, height - 2*cm, "Ozgecmis ")

        c.setFont("TurkceFont", 12)
        c.drawString(2*cm, height - 4*cm, f"Ad Soyad : {ad}")
        c.drawString(2*cm, height - 5*cm, f"E-posta  : {eposta}")
        c.drawString(2*cm, height - 6*cm, f"Telefon  : {tel}")
        c.drawString(2*cm, height - 7*cm, f"Tarih    : {datetime.now().strftime('%d.%m.%Y')}")

        c.setFont("TurkceFont", 14)
        c.drawString(2*cm, height - 9*cm, " Bildiğiniz Diller:")
        c.setFont("TurkceFont", 12)
        for i, dil in enumerate(diller.split(",")):
            c.drawString(3*cm, height - (10+i)*cm, f"- {dil.strip()}")

        offset = 10 + len(diller.split(","))
        c.setFont("TurkceFont", 14)
        c.drawString(2*cm, height - (offset+1)*cm, " Tecrübeler:")
        c.setFont("TurkceFont", 12)
        for i, t in enumerate(tecrubeler.split(",")):
            c.drawString(3*cm, height - (offset+2+i)*cm, f"- {t.strip()}")

        offset2 = offset + 2 + len(tecrubeler.split(","))
        c.setFont("TurkceFont", 14)
        c.drawString(2*cm, height - (offset2)*cm, " Araçlar:")
        c.setFont("TurkceFont", 12)
        for i, a in enumerate(araclar.split(",")):
            c.drawString(3*cm, height - (offset2+1+i)*cm, f"- {a.strip()}")

        
        try:
            c.drawImage(foto_yolu, width - 7*cm, height - 8*cm, width=5*cm, height=5*cm, mask='auto')
        except:
            pass

        c.setFont("TurkceFont", 10)
        c.drawString(2*cm, 2*cm, "İmza: Coder @ilahici_tg")
        c.save()

        return send_file(dosya_adi, as_attachment=True)

    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)
