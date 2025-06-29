from flask import Flask, render_template, request, redirect
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
import io
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/historia_clinica', methods=['POST'])
def historia_clinica():
    paciente = request.form['paciente']
    diagnostico = request.form['diagnostico']
    tratamiento = request.form['tratamiento']
    fecha = request.form['fecha']

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    fondo = ImageReader('static/fondo.png')
    c.drawImage(fondo, 0, 0, width=612, height=792)

    color_azul = HexColor("#001f4d")
    c.setFillColor(color_azul)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(200, 750, "Historia Clínica")

    c.setFont("Helvetica", 14)
    c.drawString(50, 700, f"Paciente: {paciente}")
    c.drawString(50, 670, f"Diagnóstico: {diagnostico}")
    c.drawString(50, 640, f"Tratamiento: {tratamiento}")
    c.drawString(50, 610, f"Fecha: {fecha}")

    c.setFont("Helvetica-Oblique", 12)
    c.drawString(50, 100, "Firma del Médico: ___________________________")

    c.showPage()
    c.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='historia_clinica.pdf', mimetype='application/pdf')

@app.route('/logout')
def logout():
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
