import esprima
from docuai.parsers.base import BaseParser
from docuai.models import FileMetadata, ClassMetadata, FunctionMetadata

class JSParser(BaseParser):
    def parse(self, file_path: str) -> FileMetadata:
        with open(file_path, "r") as f:
            source = f.read()
        
        tree = esprima.parseScript(source, {"loc": True, "comment": True})
        lines = source.splitlines()
        
        classes = []
        functions = []
        imports = [] # Esprima script parsing might not catch modules easily without parseModule, but let's try.
        
        # Simple traversal
        for node in tree.body:
            if node.type == 'FunctionDeclaration':
                functions.append(self._parse_function(node, lines))
            elif node.type == 'ClassDeclaration':
                classes.append(self._parse_class(node, lines))
            # Add more node types as needed (e.g., VariableDeclaration for arrow functions)

        return FileMetadata(
            file_path=file_path,
            classes=classes,
            functions=functions,
            imports=imports
        )

    def _parse_function(self, node, lines: list[str]) -> FunctionMetadata:
        start_line = node.loc.start.line
        end_line = node.loc.end.line
        
        code = "\n".join(lines[start_line-1:end_line])
        
        args = [param.name for param in node.params]
        
        return FunctionMetadata(
            name=node.id.name if node.id else "anonymous",
            args=args,
            returns=None, # JS doesn't have explicit return types in standard syntax usually
            docstring=None, # Need to parse comments separately or attach them
            code=code,
            start_line=start_line,
            end_line=end_line
        )

    def _parse_class(self, node, lines: list[str]) -> ClassMetadata:
        start_line = node.loc.start.line
        end_line = node.loc.end.line
        
        methods = []
        for item in node.body.body:
            if item.type == 'MethodDefinition':
                methods.append(self._parse_function(item.value, lines))
                # Fix name for methods
                methods[-1].name = item.key.name

        return ClassMetadata(
            name=node.id.name,
            docstring=None,
            methods=methods,
            start_line=start_line,
            end_line=end_line
        )
