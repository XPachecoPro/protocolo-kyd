from app.modulos.blockchain import registrar_selagem_blockchain
from app.modulos.certificador import gerar_pdf_certificado
from app.modulos.video import validar_video
from app.modulos.banco import supabase, salvar_registro
from app.modulos.documentos import validar_pdf
from app.modulos.imagens import validar_foto
from app.modulos.identidade import validar_rosto
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import Response
import hashlib
import time
import os

app = FastAPI(title="Protocolo KYD - Infraestrutura de Verdade Digital")

@app.get("/")
async def root():
    return {"status": "Online", "sistema": "Protocolo KYD", "versao": "1.0.0"}

@app.post("/selar")
async def selar_arquivo(usuario_id: str = Form(...), arquivo: UploadFile = File(...)):
    conteudo = await arquivo.read()
    hash_digital = hashlib.sha256(conteudo).hexdigest()

    # Identifica o tipo de arquivo para aplicar a IA correta
    if arquivo.content_type == "application/pdf":
        veredito, detalhes = validar_pdf(conteudo)
    elif "image" in arquivo.content_type:
        veredito, detalhes = validar_foto(conteudo)
    elif "video" in arquivo.content_type:
        veredito, detalhes = validar_video(conteudo)
    else:
        veredito, detalhes = "AUTÊNTICO", "Arquivo selado sem análise específica."

    tx_id = registrar_selagem_blockchain(f"KYD-{int(time.time())}", hash_digital, usuario_id)

    id_registro = f"KYD-{int(time.time())}"
    certificado = {
        "registro_id": id_registro,
        "proprietario": usuario_id,
        "hash_digital": hash_digital,
        "blockchain_tx": tx_id,
        "analise_ia": {"veredito": veredito, "detalhes": detalhes},
        "metadados": {
            "arquivo_nome": arquivo.filename, 
            "tipo": arquivo.content_type,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
        }
    }
    
    salvar_registro(certificado)
    return {"status": "DADO IMUTÁVEL", "certificado": certificado}

@app.get("/consultar/{registro_id}")
async def consultar_registro(registro_id: str):
    response = supabase.table("registros").select("*").eq("registro_id", registro_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Registro não encontrado.")
    return {"mensagem": "DADO AUTÊNTICO", "dados_originais": response.data[0]['json_completo']}

@app.get("/gerar_certificado/{registro_id}")
async def baixar_certificado(registro_id: str):
    response = supabase.table("registros").select("json_completo").eq("registro_id", registro_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Não encontrado.")
    pdf_bytes = gerar_pdf_certificado(response.data[0]['json_completo'])
    return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=Certificado_{registro_id}.pdf"})
