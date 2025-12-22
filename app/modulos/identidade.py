import face_recognition
import numpy as np
import io

def validar_rosto(foto_usuario_bytes, foto_documento_bytes):
    try:
        rosto_atual = face_recognition.load_image_file(io.BytesIO(foto_usuario_bytes))
        rosto_doc = face_recognition.load_image_file(io.BytesIO(foto_documento_bytes))

        enc_atual = face_recognition.face_encodings(rosto_atual)[0]
        enc_doc = face_recognition.face_encodings(rosto_doc)[0]

        resultado = face_recognition.compare_faces([enc_doc], enc_atual)
        
        if resultado[0]:
            return "IDENTIFICADO", "Firma reconhecida via biometria facial."
        return "SUSPEITO", "Rosto não confere com o documento registrado."
    except Exception:
        return "ERRO", "Falha na análise biométrica."
