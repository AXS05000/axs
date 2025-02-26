import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from .utils import convert_docx_to_pdf
from .azure_storage import AzureMediaStorage
from .models import AzureStorageConfig

@csrf_exempt
def convert_word_to_pdf(request):
    if request.method == "POST" and request.FILES.get("file"):
        word_file = request.FILES["file"]

        # Criar nomes para os arquivos
        word_name = word_file.name
        pdf_name = word_name.replace(".docx", ".pdf")

        # Pegar as credenciais do banco de dados
        try:
            azure_config = AzureStorageConfig.objects.first()
            if not azure_config:
                return JsonResponse({"error": "Configuração do Azure não encontrada"}, status=500)
        except Exception as e:
            return JsonResponse({"error": f"Erro ao buscar credenciais: {str(e)}"}, status=500)

        # Criar instância do Azure Storage
        azure_storage = AzureMediaStorage()

        # Salvar o arquivo DOCX temporariamente no Azure
        with default_storage.open(word_name, 'wb+') as destination:
            for chunk in word_file.chunks():
                destination.write(chunk)

        try:
            # Caminho temporário para conversão
            word_path = os.path.join("/tmp", word_name)
            pdf_path = os.path.join("/tmp", pdf_name)

            # Baixar do Azure para a máquina para conversão
            with default_storage.open(word_name, "rb") as docx_file:
                with open(word_path, "wb") as temp_word:
                    temp_word.write(docx_file.read())

            # Converter para PDF
            convert_docx_to_pdf(word_path, pdf_path)

            # Apagar o arquivo Word do Azure após conversão
            default_storage.delete(word_name)

            # Enviar o PDF convertido para o Azure Storage
            with open(pdf_path, "rb") as pdf_file:
                azure_storage.save(pdf_name, pdf_file)

            # Apagar arquivos locais temporários
            os.remove(word_path)
            os.remove(pdf_path)

            # Gerar URL do PDF no Azure Storage
            pdf_url = f"https://{azure_config.account_name}.blob.core.windows.net/{azure_config.azure_container}/{pdf_name}"

            return JsonResponse({"pdf_url": pdf_url}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Arquivo não enviado"}, status=400)




import requests
from django.shortcuts import render
from django.http import JsonResponse

def upload_docx(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        url_api = "https://axsconsultoria.com/convert-word-to-pdf/"

        # Enviar o arquivo para a API online
        response = requests.post(url_api, files={"file": file})

        if response.status_code == 200:
            pdf_url = response.json().get("pdf_url")
            return render(request, "upload.html", {"pdf_url": pdf_url})
        else:
            return render(request, "upload.html", {"error": "Erro ao converter. Verifique a API."})

    return render(request, "upload.html")
