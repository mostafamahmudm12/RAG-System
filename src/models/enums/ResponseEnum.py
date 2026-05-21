from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATION_SUCCESS = "File validation Success"
    FILE_TYPE_NOT_SUPPORTED = "File type not supported"
    FILE_SIZE_EXCEEDED = "File size exceeds the maximum allowed size"
    FILE_UPLOAD_SUCCESS = "File uploaded successfully"
    FILE_UPLOAD_FAILED = "File upload failed"
    PROCCESSING_FAILED = "File processing failed"
    PROCCESSING_SUCCESS = "File processed successfully"
    NO_FILES_TO_PROCESS = "No files to process"
    FILE_NOT_FOUND = "File not found with the provided file_id"
    PROJECT_NOT_FOUND = "Project not found with the provided project_id"
    INDEXING_FAILED = "Failed to index chunks into vector database"
    INDEXING_SUCCESS = "Chunks indexed into vector database successfully"
    INDEX_INFO_RETRIEVED = "Index information retrieved successfully"