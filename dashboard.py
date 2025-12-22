import streamlit as st
import requests
import json
import time

# Configurações da Página
st.set_page_config(page_title="Cartório Digital KYD", layout="wide", page_icon="🏛️")

st.title("🏛️ Protocolo KYD: Cartório Independente Digital")
st.markdown("---")

# Link do servidor oficial no Railway
API_URL = "https://kydprotocolo.up.railway.app"

# Barra Lateral para Navegação
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1041/1041916.png", width=100)
menu = st.sidebar.selectbox("Menu Principal", ["Selo de Autenticidade", "Reconhecimento de Firma", "Consultar Registro"])

if menu == "Selo de Autenticidade":
    st.header("🛡️ Selar e Autenticar Documento")
    
    col1, col2 = st.columns(2)
    with col1:
        usuario = st.text_input("ID do Proprietário (Ex: Nome ou Empresa)")
        arquivo = st.file_uploader("Carregar Ficheiro (PDF, Imagem ou Vídeo)", type=['png', 'jpg', 'jpeg', 'pdf', 'mp4'])
    
    if st.button("🚀 Gerar Selo Imutável"):
        if arquivo and usuario:
            with st.spinner("A processar IA e a registar na Blockchain..."):
                files = {"arquivo": (arquivo.name, arquivo.getvalue(), arquivo.type)}
                data = {"usuario_id": usuario}
                
                try:
                    response = requests.post(f"{API_URL}/selar", data=data, files=files)
                    if response.status_code == 200:
                        res = response.json()["certificado"]
                        st.success("✅ Documento Selado com Sucesso!")
                        
                        st.metric("ID do Registro", res["registro_id"])
                        st.code(f"HASH DIGITAL: {res['hash_digital']}", language="text")
                        
                        # Botão de Download do Certificado PDF
                        st.markdown(f"### [📥 Baixar Certificado Oficial PDF]({API_URL}/gerar_certificado/{res['registro_id']})")
                    else:
                        st.error("Erro no processamento da API.")
                except Exception as e:
                    st.error(f"Erro de conexão: {e}")

elif menu == "Reconhecimento de Firma":
    st.header("👤 Reconhecimento de Firma via Biometria")
    
    col1, col2 = st.columns(2)
    with col1:
        selfie = st.camera_input("Tirar Selfie")
        doc_foto = st.file_uploader("Carregar foto do Documento", type=['jpg', 'jpeg', 'png'])
        usuario_firma = st.text_input("Nome Completo")

    if st.button("⚖️ Validar Identidade"):
        if selfie and doc_foto and usuario_firma:
            with st.spinner("Análise Biométrica..."):
                files = {
                    "selfie": ("selfie.
