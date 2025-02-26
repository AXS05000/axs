import os
import platform
import subprocess
from django.core.files.storage import default_storage

# Detecta o sistema operacional
IS_WINDOWS = platform.system() == "Windows"

if IS_WINDOWS:
    import comtypes.client
    import pythoncom

def convert_docx_to_pdf(input_path, output_path):
    """
    Converte um arquivo DOCX para PDF e salva no Azure Storage (media2).
    """
    try:
        if IS_WINDOWS:
            # Conversão no Windows usando Microsoft Word
            pythoncom.CoInitialize()
            word = comtypes.client.CreateObject("Word.Application")
            word.Visible = False
            doc = word.Documents.Open(input_path)
            doc.SaveAs(output_path, FileFormat=17)  # 17 = PDF
            doc.Close()
            word.Quit()
            pythoncom.CoUninitialize()
        
        else:
            # Conversão no Linux usando LibreOffice
            command = [
                "libreoffice", "--headless",
                "--convert-to", "pdf", "--outdir",
                os.path.dirname(output_path), input_path
            ]
            subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Verifica se o arquivo PDF foi gerado
        if not os.path.exists(output_path):
            raise Exception("Erro: o arquivo PDF não foi criado.")

    except Exception as e:
        raise Exception(f"Erro ao converter documento: {str(e)}")
