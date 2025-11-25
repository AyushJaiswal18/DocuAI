from abc import ABC, abstractmethod
from docuai.models import FileMetadata

class BaseParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> FileMetadata:
        pass
