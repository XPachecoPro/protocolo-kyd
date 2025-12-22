import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def salvar_registro(dados_certificado):
    try:
        data = {
            "registro_id": dados_certificado["registro_id"],
            "proprietario": dados_certificado["proprietario"],
            "hash_digital": dados_certificado["hash_digital"],
            "tipo_arquivo": dados_certificado["metadados"]["tipo"],
            "veredito_ia": dados_certificado["analise_ia"]["veredito"],
            "json_completo": dados_certificado
        }
        response = supabase.table("registros").insert(data).execute()
        return response
    except Exception as e:
        print(f"Erro ao salvar no banco: {e}")
        return None
