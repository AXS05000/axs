import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings
from .utils import convert_docx_to_pdf

@csrf_exempt
def convert_word_to_pdf(request):
    if request.method == "POST" and request.FILES.get("file"):
        word_file = request.FILES["file"]

        # Criar caminhos para armazenar o arquivo temporariamente
        word_path = os.path.join(settings.MEDIA_ROOT, word_file.name)
        pdf_path = word_path.replace(".docx", ".pdf")

        # Salvar o arquivo temporariamente
        with default_storage.open(word_path, 'wb+') as destination:
            for chunk in word_file.chunks():
                destination.write(chunk)

        try:
            # Converter para PDF
            convert_docx_to_pdf(word_path, pdf_path)

            # Remover o arquivo Word original
            os.remove(word_path)

            # Retornar a URL do PDF gerado
            pdf_url = request.build_absolute_uri(settings.MEDIA_URL + os.path.basename(pdf_path))
            return JsonResponse({"pdf_url": pdf_url}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Arquivo não enviado"}, status=400)
