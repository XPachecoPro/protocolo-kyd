from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
import io

def gerar_pdf_certificado(dados):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    largura, altura = A4

    # Design do Certificado
    c.setStrokeColor(colors.black)
    c.rect(1*cm, 1*cm, largura-2*cm, altura-2*cm)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(largura/2, altura - 3*cm, "PROTOCOLO KYD - CERTIFICADO")
    
    # Informações Técnicas
    c.setFont("Helvetica", 10)
    y = altura - 5*cm
    c.drawString(2*cm, y, f"ID Registro: {dados['registro_id']}")
    c.drawString(2*cm, y-0.6*cm, f"Proprietário: {dados['proprietario']}")
    c.drawString(2*cm, y-1.2*cm, f"Hash Digital: {dados['hash_digital']}")
    c.drawString(2*cm, y-1.8*cm, f"Transação Blockchain: {dados['blockchain_tx']}")
    
    # Veredito da IA
    y -= 3*cm
    c.setFont("Helvetica-Bold", 12)
    status = dados['analise_ia']['veredito']
    c.setFillColor(colors.darkgreen if status == "AUTÊNTICO" else colors.red)
    c.drawString(2*cm, y, f"VEREDITO IA: {status}")
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(2*cm, y-0.6*cm, f"Detalhes: {dados['analise_ia']['detalhes']}")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()
