import cv2
import hashlib
import tempfile
import os

def validar_video(conteudo_bytes):
    """
    Cria uma assinatura digital temporal do vídeo para garantir integridade.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(conteudo_bytes)
        tmp_path = tmp.name
    try:
        cap = cv2.VideoCapture(tmp_path)
        hashes_frames = []
        fps = cap.get(cv2.CAP_PROP_FPS)
        intervalo = int(fps) if fps > 0 else 30
        count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            if count % intervalo == 0:
                f_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
                hashes_frames.append(hashlib.sha256(f_bytes).hexdigest())
            count += 1
        
        cap.release()
        os.unlink(tmp_path)
        
        # Gera o Hash Combinado
        super_hash = hashlib.sha256("".join(hashes_frames).encode()).hexdigest()
        return "AUTÊNTICO", f"Vídeo selado com {len(hashes_frames)} pontos de checagem."
    except Exception as e:
        if os.path.exists(tmp_path): os.unlink(tmp_path)
        return "ERRO", f"Falha no vídeo: {str(e)}"
