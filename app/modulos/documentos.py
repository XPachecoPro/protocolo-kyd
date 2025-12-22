import io
from PyPDF2 import PdfReader
from datetime import datetime

def validar_pdf(conteudo_bytes):
    """
    Analisa a 'saúde' estrutural e a veracidade de um PDF.
    """
    try:
        leitor = PdfReader(io.BytesIO(conteudo_bytes))
        info = leitor.metadata
        
        if not info:
            return "ALERTA", "Documento sem metadados. Origem não rastreável."

        # Checagem de Edição (Criação vs Modificação)
        data_criacao = info.get('/CreationDate', '')[2:10]
        data_mod = info.get('/ModDate', '')[2:10]
        ferramenta = info.get('/Producer', 'Desconhecido')

        if data_criacao and data_mod and data_criacao != data_mod:
            veredito = "SUSPEITO"
            detalhes = f"Editado após criação. Gerado por: {ferramenta}"
        else:
            veredito = "AUTÊNTICO"
            detalhes = f"Estrutura íntegra. Gerado por: {ferramenta}"

        # Checagem de Camada de Texto
        texto = leitor.pages[0].extract_text()
        if len(texto.strip()) < 5:
            detalhes += " | Nota: PDF é uma imagem escaneada."

        return veredito, detalhes
    except Exception as e:
        return "ERRO", f"Falha estrutural: {str(e)}"
