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
        
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.3)
        
        self.doc_prompt = ChatPromptTemplate.from_template(
            """
            You are an expert software engineer and technical writer. Generate comprehensive, professional documentation for the following code.
            
            File: {file_path}
            
            Code Structure:
            {structure}
            
            Source Code:
            ```
            {code}
            ```
            
            Generate documentation following this structure:
            
            # {file_path}
            
            ## Overview
            Provide a clear, concise summary of what this file does and its purpose in the project.
            
            ## Components
            
            For each class and function:
            - **Name and Signature**: Include full signature with types
            - **Purpose**: What it does in 1-2 sentences
            - **Parameters**: Describe each parameter with type and purpose
            - **Returns**: What it returns and when
            - **Example Usage**: Provide realistic code examples
            - **Notes**: Any important details, edge cases, or gotchas
            
            ## Usage Examples
            
            Provide 2-3 realistic examples showing:
            1. Basic usage
            2. Common use case
            3. Advanced usage (if applicable)
            
            Use proper code formatting with language-specific syntax highlighting.
            Be specific, accurate, and helpful. Avoid generic statements.
            """
        )
        
        self.smell_prompt = ChatPromptTemplate.from_template(
            """
            You are a senior code reviewer and software architect. Perform a thorough code quality analysis.
            
            File: {file_path}
            
            Source Code:
            ```
            {code}
            ```
            
            Analyze the code and provide a structured report:
            
            # Code Quality Analysis: {file_path}
            
            ## Summary
            Brief overview of overall code quality (1-2 sentences).
            
            ## Issues Found
            
            ### 🔴 Critical Issues
            List any critical problems (security vulnerabilities, major bugs, data loss risks):
            - **Issue**: Description
            - **Impact**: What could go wrong
            - **Fix**: Specific solution
            
            ### 🟡 Code Smells
            Identify anti-patterns and design issues:
            - **Smell**: Name and description
            - **Location**: Where in the code
            - **Refactoring**: How to improve
            
            ### 🟢 Performance Concerns
            Note any performance issues:
            - **Issue**: Description
            - **Impact**: Performance impact
            - **Optimization**: Suggested improvement
            
            ## Best Practices Violations
            List any violations of language-specific best practices.
            
            ## Recommendations
            
            Prioritized list of improvements:
            1. **High Priority**: Critical fixes
            2. **Medium Priority**: Important improvements
            3. **Low Priority**: Nice-to-have enhancements
            
            ## Positive Aspects
            Highlight what's done well (good patterns, clean code, etc.).
            
            Be specific with line numbers or code snippets when possible.
            Provide actionable, concrete suggestions.
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
            You are a senior software architect and technical writer. Generate comprehensive project documentation.
            
            Repository Content:
            {repo_content}
            
            Create a professional project documentation following this structure:
            
            # Project Documentation
            
            ## Executive Summary
            - **Purpose**: What problem does this project solve?
            - **Key Features**: Top 3-5 features
            - **Tech Stack**: Main technologies used
            
            ## Architecture Overview
            
            ### System Design
            Describe the overall architecture (e.g., MVC, microservices, layered architecture).
            
            ### Key Components
            List and describe major modules/packages:
            - **Component Name**: Purpose and responsibilities
            - **Dependencies**: What it depends on
            - **Interactions**: How it communicates with other components
            
            ### Data Flow
            Explain how data moves through the system.
            
            ## Module Documentation
            
            For each significant file/module:
            ### [Module Name]
            - **Purpose**: What it does
            - **Key Classes/Functions**: Main functionality
            - **Usage**: How to use it
            
            ## Getting Started
            
            ### Prerequisites
            List required dependencies and setup.
            
            ### Quick Start
            Provide step-by-step usage examples.
            
            ## API Reference (if applicable)
            Document public APIs, endpoints, or interfaces.
            
            ## Design Patterns
            Identify and explain design patterns used.
            
            ## Best Practices
            Highlight good practices implemented in the codebase.
            
            Be thorough but concise. Focus on what developers need to know.
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
            You are a senior software architect and security expert. Perform a comprehensive project-wide code review.
            
            Repository Content:
            {repo_content}
            
            Generate a detailed analysis report:
            
            # Project Code Quality Report
            
            ## Executive Summary
            - **Overall Quality Score**: Rate 1-10 with justification
            - **Critical Issues**: Count of critical problems
            - **Main Concerns**: Top 3 areas needing attention
            
            ## Architectural Analysis
            
            ### Design Quality
            - **Strengths**: What's well-designed
            - **Weaknesses**: Architectural problems
            - **Suggestions**: How to improve structure
            
            ### Code Organization
            - **Modularity**: How well code is organized
            - **Coupling**: Dependencies between modules
            - **Cohesion**: How focused each module is
            
            ## Security Analysis
            
            ### 🔴 Critical Security Issues
            List vulnerabilities that need immediate attention:
            - **Vulnerability**: Type and description
            - **Location**: Which files/modules
            - **Risk**: Potential impact
            - **Fix**: Remediation steps
            
            ### Security Best Practices
            Evaluate adherence to security standards.
            
            ## Code Quality Issues
            
            ### Patterns and Anti-Patterns
            - **Good Patterns**: Design patterns used well
            - **Anti-Patterns**: Problematic patterns found
            
            ### Code Smells by Category
            - **Duplication**: Repeated code
            - **Complexity**: Overly complex functions/classes
            - **Naming**: Unclear or inconsistent names
            - **Error Handling**: Missing or poor error handling
            
            ## Performance Analysis
            - **Bottlenecks**: Potential performance issues
            - **Optimizations**: Suggested improvements
            - **Scalability**: How well it will scale
            
            ## Testing and Quality Assurance
            - **Test Coverage**: Assess testing (if tests exist)
            - **Missing Tests**: Critical areas lacking tests
            - **Test Quality**: Quality of existing tests
            
            ## Maintainability
            - **Documentation**: Code comments and docs
            - **Readability**: How easy to understand
            - **Extensibility**: How easy to extend
            
            ## Recommendations
            
            ### Immediate Actions (High Priority)
            1. Critical fixes needed now
            
            ### Short-term Improvements (Medium Priority)
            2. Important refactoring and improvements
            
            ### Long-term Enhancements (Low Priority)
            3. Nice-to-have improvements
            
            ## Positive Highlights
            Recognize what's done exceptionally well.
            
            Be specific, actionable, and constructive. Provide code examples where helpful.
            """
        )
        
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"repo_content": repo_content})
