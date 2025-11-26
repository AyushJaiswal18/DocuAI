import esprima
from docuai.parsers.base import BaseParser
from docuai.models import FileMetadata, FunctionMetadata, ClassMetadata

class JSParser(BaseParser):
    def parse(self, file_path: str) -> FileMetadata:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Try parsing with different options for better TypeScript/JSX support
        try:
            # Try parseModule first (for ES6 modules)
            tree = esprima.parseModule(source, {'jsx': True, 'tolerant': True, 'range': True})
        except Exception:
            try:
                # Fallback to parseScript (for regular scripts)
                tree = esprima.parseScript(source, {'jsx': True, 'tolerant': True, 'range': True})
            except Exception as e:
                # If parsing fails completely, return empty metadata
                # This allows the AI to still analyze the raw code
                return FileMetadata(
                    file_path=file_path,
                    language="javascript",
                    classes=[],
                    functions=[]
                )
        
        functions = []
        classes = []
        
        def extract_params(params):
            """Extract parameter names from function parameters."""
            param_names = []
            for param in params:
                if param.type == 'Identifier':
                    param_names.append(param.name)
                elif param.type == 'AssignmentPattern':
                    # Default parameters
                    if param.left.type == 'Identifier':
                        param_names.append(param.left.name)
                elif param.type == 'RestElement':
                    # Rest parameters
                    if param.argument.type == 'Identifier':
                        param_names.append(f"...{param.argument.name}")
            return param_names
        
        def traverse(node):
            if node.type == 'FunctionDeclaration':
                functions.append(FunctionMetadata(
                    name=node.id.name if node.id else '<anonymous>',
                    args=extract_params(node.params),
                    return_type=None,
                    docstring=None,
                    code_snippet=source[node.range[0]:node.range[1]] if hasattr(node, 'range') else ""
                ))
            elif node.type == 'ClassDeclaration':
                class_name = node.id.name if node.id else '<anonymous>'
                class_methods = []
                for item in node.body.body:
                    if item.type == 'MethodDefinition':
                        class_methods.append(FunctionMetadata(
                            name=item.key.name if hasattr(item.key, 'name') else str(item.key.value),
                            args=extract_params(item.value.params),
                            return_type=None,
                            docstring=None,
                            code_snippet=""
                        ))
                classes.append(ClassMetadata(
                    name=class_name,
                    methods=class_methods,
                    docstring=None,
                    code_snippet=source[node.range[0]:node.range[1]] if hasattr(node, 'range') else ""
                ))
            
            # Traverse child nodes
            for key, value in node.__dict__.items():
                if isinstance(value, list):
                    for item in value:
                        if hasattr(item, 'type'):
                            traverse(item)
                elif hasattr(value, 'type'):
                    traverse(value)
        
        traverse(tree)
        
        return FileMetadata(
            file_path=file_path,
            language="javascript",
            classes=classes,
            functions=functions
        )
