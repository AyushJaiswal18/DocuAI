import ast
from docuai.parsers.base import BaseParser
from docuai.models import FileMetadata, ClassMetadata, FunctionMetadata

class PythonParser(BaseParser):
    def parse(self, file_path: str) -> FileMetadata:
        with open(file_path, "r") as f:
            source = f.read()
        
        tree = ast.parse(source)
        lines = source.splitlines()
        
        classes = []
        functions = []
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                # Simplified import extraction
                imports.append(ast.unparse(node))
            
            elif isinstance(node, ast.FunctionDef):
                # Only top-level functions (not methods inside classes, handled separately)
                # But ast.walk visits everything. We need to check parent or traversal order.
                # Easier to iterate top-level nodes for structure.
                pass

        # Better approach: Iterate top-level nodes
        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                imports.append(ast.unparse(node))
            elif isinstance(node, ast.ClassDef):
                classes.append(self._parse_class(node, lines))
            elif isinstance(node, ast.FunctionDef):
                functions.append(self._parse_function(node, lines))
                
        return FileMetadata(
            file_path=file_path,
            classes=classes,
            functions=functions,
            imports=imports
        )

    def _parse_function(self, node: ast.FunctionDef, lines: list[str]) -> FunctionMetadata:
        start_line = node.lineno
        end_line = node.end_lineno if hasattr(node, "end_lineno") else start_line # Python 3.8+
        
        # Extract source code for the function
        code = "\n".join(lines[start_line-1:end_line])
        
        args = [arg.arg for arg in node.args.args]
        returns = ast.unparse(node.returns) if node.returns else None
        docstring = ast.get_docstring(node)
        
        return FunctionMetadata(
            name=node.name,
            args=args,
            returns=returns,
            docstring=docstring,
            code=code,
            start_line=start_line,
            end_line=end_line
        )

    def _parse_class(self, node: ast.ClassDef, lines: list[str]) -> ClassMetadata:
        start_line = node.lineno
        end_line = node.end_lineno if hasattr(node, "end_lineno") else start_line
        
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(self._parse_function(item, lines))
                
        docstring = ast.get_docstring(node)
        
        return ClassMetadata(
            name=node.name,
            docstring=docstring,
            methods=methods,
            start_line=start_line,
            end_line=end_line
        )
