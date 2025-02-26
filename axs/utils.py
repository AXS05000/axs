import os
import comtypes.client
import pythoncom  # Importação necessária para inicializar COM no Windows

def convert_docx_to_pdf(input_path, output_path):
    try:
        pythoncom.CoInitialize()  # 🔥 Solução para erro CoInitialize

        word = comtypes.client.CreateObject("Word.Application")
        word.Visible = False

        doc = word.Documents.Open(input_path)
        doc.SaveAs(output_path, FileFormat=17)  # 17 = PDF
        doc.Close()
        word.Quit()

    except Exception as e:
        raise Exception(f"Erro ao converter no Windows: {str(e)}")
    finally:
        pythoncom.CoUninitialize()  # 🔥 Fecha corretamente a inicialização COM
