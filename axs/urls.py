from django.urls import path
from .views import convert_word_to_pdf

urlpatterns = [
    path("convert-word-to-pdf/", convert_word_to_pdf, name="convert_word_to_pdf"),
]
