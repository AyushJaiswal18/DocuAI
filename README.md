# DocuAI

**DocuAI** is an autonomous AI agent and CLI tool that analyzes codebases and generates comprehensive documentation automatically. It supports Python and JavaScript/TypeScript projects.

## Features

-   **Multi-Language Support**: Parses Python (using `ast`) and JavaScript (using `esprima`).
-   **AI-Powered Documentation**: Uses OpenAI's GPT models to generate detailed documentation for classes, functions, and modules.
-   **Code Analysis**: Identifies code smells, security vulnerabilities, and architectural issues.
-   **GitHub Support**: Clone and analyze entire repositories directly from a URL.
-   **Directory Support**: Analyze local projects with smart file traversal (ignores `.venv`, `node_modules`, etc.).
-   **Repo-level Insights**: Generates a single comprehensive report for the entire project.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/docuai.git
    cd docuai
    ```

2.  Install dependencies:
    ```bash
    pip install -e .
    ```

## Configuration

**DocuAI** requires an OpenAI API key to function. You can set it in multiple ways:

### Option 1: Environment Variable (Recommended for global install)
```bash
export OPENAI_API_KEY='your-api-key-here'
```

Add this to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.) to make it permanent.

### Option 2: .env File (For development)
Create a `.env` file in your project directory:
```env
OPENAI_API_KEY=your-api-key-here
LANGCHAIN_TRACING_V2=true  # Optional: for LangSmith tracing
LANGCHAIN_API_KEY=your-langchain-api-key  # Optional
```

### Option 3: Per-command
```bash
OPENAI_API_KEY='your-key' docuai generate script.py
```

## Global Installation

To install **DocuAI** globally on your system so you can use it from any directory:

### Option 1: Using pipx (Recommended)
`pipx` installs the tool in an isolated environment but makes the command available globally.
```bash
pipx install .
```

### Option 2: Using pip
```bash
pip install .
```

### Publishing to PyPI
To share this tool with the world, you can publish it to PyPI:

1.  **Build the package**:
    ```bash
    python -m build
    ```
    This creates `dist/docuai-0.1.0.tar.gz` and `dist/docuai-0.1.0-py3-none-any.whl`

2.  **Test locally** (optional but recommended):
    ```bash
    pip install dist/docuai-0.1.0-py3-none-any.whl
    ```

3.  **Upload to PyPI**:
    ```bash
    twine upload dist/*
    ```
    
4.  **Users can then install via**:
    ```bash
    pip install docuai
    ```

## Usage

### Generate Documentation

**Single File:**
```bash
docuai generate ./path/to/file.py
```

**Local Directory (Project-level):**
```bash
docuai generate . --output project_docs.md
```

**GitHub Repository:**
```bash
docuai generate https://github.com/username/repo --output repo_docs.md
```

### Analyze Code

**Single File:**
```bash
docuai analyze ./path/to/file.py
```

**Local Directory (Project-level):**
```bash
docuai analyze .
```

**GitHub Repository:**
```bash
docuai analyze https://github.com/username/repo
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

[MIT License](LICENSE)
