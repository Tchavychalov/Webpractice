from .services import FileService, NNService

file_service = FileService()
nn_service = NNService()

def get_fileservice():
    return file_service

def get_nnservice():
    return nn_service