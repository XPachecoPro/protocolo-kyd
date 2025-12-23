import requests

# Endereço oficial do seu cartório no Railway
URL_API = "https://kydprotocolo.up.railway.app/selar_firma"

# Certifique-se de ter dois arquivos de imagem na mesma pasta para o teste
files = {
    "selfie": ("selfie.jpg", open("sua_selfie.jpg", "rb"), "image/jpeg"),
    "documento": ("documento.jpg", open("seu_documento.jpg", "rb"), "image/jpeg")
}

data = {"usuario_id": "Vinicius_Engenheiro"}

print("🚀 Iniciando validação biométrica no Protocolo KYD...")

try:
    response = requests.post(URL_API, data=data, files=files)
    if response.status_code == 200:
        print("✅ Resposta do Servidor:", response.json())
    else:
        print(f"❌ Erro na API (Status {response.status_code}):", response.text)
except Exception as e:
    print(f"⚠️ Falha na conexão: {e}")
