import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from docuai.models import FileMetadata

class DocuAIAgent:
    def __init__(self):
        # Check for OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OpenAI API key not found. Please set it using one of these methods:\n"
                "1. Environment variable: export OPENAI_API_KEY='your-key-here'\n"
                "2. Create a .env file in your current directory with: OPENAI_API_KEY=your-key-here\n"
                "3. Set it in your shell profile (~/.bashrc, ~/.zshrc, etc.)"
            )
        
        self.llm = ChatOpenAI(model="gpt-5", temperature=0)
        
        self.doc_prompt = ChatPromptTemplate.from_template(
            """
            You are an expert software engineer. Generate comprehensive documentation for the following code.
            
            File: {file_path}
            
            Code Structure:
            {structure}
            
            Source Code:
            {code}
            
            Please provide:
            1. A high-level summary of what this file does.
            2. Detailed documentation for each class and function.
            3. Usage examples if applicable.
            
            Output in Markdown format.
            """
        )
        
        self.smell_prompt = ChatPromptTemplate.from_template(
            """
            You are an expert code reviewer. Analyze the following code for code smells, anti-patterns, and potential bugs.
            
            File: {file_path}
            
            Source Code:
            {code}
            
            Identify:
            1. Code Smells (e.g., long functions, duplicated code, tight coupling).
            2. Security Vulnerabilities.
            3. Performance Issues.
            4. Suggestions for improvement.
            
            Output in Markdown format.
            """
        )

    def generate_docs(self, metadata: FileMetadata) -> str:
        # Reconstruct code or read it again? 
        # We have code snippets in metadata, but full context is better.
        # For now, let's assume we pass the full file content or reconstruct it.
        # Actually, let's read the file again here for simplicity or pass it in.
        
        with open(metadata.file_path, "r") as f:
            full_code = f.read()
            
        structure_summary = f"Classes: {[c.name for c in metadata.classes]}, Functions: {[f.name for f in metadata.functions]}"
        
        chain = self.doc_prompt | self.llm | StrOutputParser()
        return chain.invoke({
            "file_path": metadata.file_path,
            "structure": structure_summary,
            "code": full_code
        })

    def analyze_code(self, file_path: str) -> str:
        with open(file_path, "r") as f:
            full_code = f.read()
            
        chain = self.smell_prompt | self.llm | StrOutputParser()
        return chain.invoke({
            "file_path": file_path,
            "code": full_code
        })

    def generate_repo_docs(self, metadata_list: list[FileMetadata]) -> str:
        repo_content = ""
        for meta in metadata_list:
            try:
                with open(meta.file_path, "r") as f:
                    code = f.read()
                repo_content += f"\n\n--- File: {meta.file_path} ---\n{code}"
            except Exception as e:
                repo_content += f"\n\n--- File: {meta.file_path} ---\n(Error reading file: {e})"

        prompt = ChatPromptTemplate.from_template(
            """
            You are an expert software engineer. Generate comprehensive documentation for the following repository.
            
            Repository Content:
            {repo_content}
            
            Please provide:
            1. A high-level overview of the project.
            2. Architecture and design patterns used.
            3. Detailed documentation for key modules and files.
            4. Usage examples and workflows.
            
            Output in Markdown format.
            """
        )
        
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"repo_content": repo_content})

    def analyze_repo(self, file_paths: list[str]) -> str:
        repo_content = ""
        for path in file_paths:
            try:
                with open(path, "r") as f:
                    code = f.read()
                repo_content += f"\n\n--- File: {path} ---\n{code}"
            except Exception as e:
                repo_content += f"\n\n--- File: {path} ---\n(Error reading file: {e})"

        prompt = ChatPromptTemplate.from_template(
            """
            You are an expert code reviewer. Analyze the following repository for code smells, anti-patterns, and potential bugs.
            
            Repository Content:
            {repo_content}
            
            Identify:
            1. Global Code Smells and Architectural Issues.
            2. Security Vulnerabilities across the project.
            3. Performance Issues.
            4. Suggestions for improvement and refactoring.
            
            Output in Markdown format.
            """
        )
        
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"repo_content": repo_content})
