# from storages.backends.azure_storage import AzureStorage
# from .models import AzureStorageConfig

# def get_azure_config():
#     """
#     Retorna as credenciais do Azure armazenadas no banco de dados.
#     Se não houver nenhuma configuração, levanta um erro.
#     """
#     config = AzureStorageConfig.objects.first()
#     if not config:
#         raise Exception("Nenhuma configuração do Azure Storage encontrada no banco de dados.")
#     return config

# class AzureMediaStorage(AzureStorage):
#     config = get_azure_config()
#     account_name = config.account_name
#     account_key = config.account_key
#     azure_container = config.azure_container
#     expiration_secs = None  # Links permanentes
