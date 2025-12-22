import cv2
import numpy as np

def validar_foto(conteudo_bytes):
    try:
        nparr = np.frombuffer(conteudo_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        
        # Analisa frequências para detectar padrões de grade (Moiré)
        f = np.fft.fft2(img)
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)
        
        desvio = np.std(magnitude_spectrum)
        if desvio > 35:
            return "SUSPEITO", "Padrão de captura de tela detectado."
        return "AUTÊNTICO", "Imagem capturada em ambiente físico."
    except Exception as e:
        return "ERRO", str(e)
