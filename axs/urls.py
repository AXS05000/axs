from django.urls import path
from .views import convert_word_to_pdf, upload_docx

urlpatterns = [
    path("convert-word-to-pdf/", convert_word_to_pdf, name="convert_word_to_pdf"),
     path("upload/", upload_docx, name="upload_docx"),
]
