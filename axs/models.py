from django.db import models

class AzureStorageConfig(models.Model):
    account_name = models.CharField(max_length=255, verbose_name="Nome da Conta")
    account_key = models.CharField(max_length=255, verbose_name="Chave de Acesso")
    azure_container = models.CharField(max_length=100, verbose_name="Container", default="media2")

    def __str__(self):
        return f"Azure Storage - {self.account_name}"
