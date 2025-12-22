from web3 import Web3
import hashlib

def registrar_selagem_blockchain(registro_id, hash_arquivo, proprietario):
    """
    Simula o registro do DNA do documento na rede Polygon.
    """
    try:
        # Geramos um hash único que representa a 'assinatura' na blockchain
        dados_vivos = f"{registro_id}{hash_arquivo}{proprietario}"
        tx_hash = "0x" + hashlib.sha256(dados_vivos.encode()).hexdigest()
        return tx_hash
    except Exception as e:
        print(f"Erro na Blockchain: {e}")
        return "Erro de Rede - Gravado Localmente"
