from pydantic import BaseModel
from typing import List, Optional

class FunctionMetadata(BaseModel):
    name: str
    args: List[str]
    returns: Optional[str]
    docstring: Optional[str]
    code: str
    start_line: int
    end_line: int

class ClassMetadata(BaseModel):
    name: str
    docstring: Optional[str]
    methods: List[FunctionMetadata]
    start_line: int
    end_line: int

class FileMetadata(BaseModel):
    file_path: str
    classes: List[ClassMetadata]
    functions: List[FunctionMetadata]
    imports: List[str]
