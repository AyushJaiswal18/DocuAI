# DocuAI

<div align="center">

**AI-Powered Code Documentation & Analysis**

[![PyPI version](https://badge.fury.io/py/docuai.svg)](https://pypi.org/project/docuai/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Generate comprehensive documentation and analyze code quality for Python, JavaScript, TypeScript, and React projects using GPT-5.

[Installation](#installation) • [Quick Start](#quick-start) • [Features](#features) • [Documentation](#documentation)

</div>

---

## 🚀 Features

- **🤖 AI-Powered** - Uses OpenAI's GPT-5 for intelligent documentation generation
- **⚡ Multi-Language** - Supports Python, JavaScript, TypeScript, JSX, and TSX
- **📝 Auto-Save** - All reports automatically saved to `.md` files
- **🔍 Code Analysis** - Identifies code smells, security issues, and architectural problems
- **🌐 GitHub Integration** - Analyze repositories directly from URLs
- **📂 Recursive Traversal** - Processes entire projects including subdirectories
- **🎯 Repo-Level Insights** - Generates comprehensive project-wide documentation

## 📦 Installation

```bash
pip install docuai
```

### Requirements
- Python 3.9 or higher
- OpenAI API key

## ⚙️ Configuration

DocuAI requires an OpenAI API key. Set it using one of these methods:

### Option 1: Environment Variable (Recommended)
```bash
export OPENAI_API_KEY='your-api-key-here'
```

Add to your shell profile for persistence:
```bash
echo "export OPENAI_API_KEY='your-key'" >> ~/.bashrc  # or ~/.zshrc
```

### Option 2: .env File
Create a `.env` file in your project directory:
```env
OPENAI_API_KEY=your-api-key-here
```

### Option 3: Per-Command
```bash
OPENAI_API_KEY='your-key' docuai generate script.py
```

## 🎯 Quick Start

### Generate Documentation

```bash
# Single file (saves to filename_docs.md)
docuai generate app.py

# Entire project (saves to dirname_documentation.md)
docuai generate .

# GitHub repository
docuai generate https://github.com/username/repo --output docs.md
```

### Analyze Code Quality

```bash
# Single file (saves to filename_analysis.md)
docuai analyze app.py

# Entire project (saves to dirname_analysis.md)
docuai analyze .

# Custom output
docuai analyze . --output analysis.md
```

## 📚 Usage Examples

### Python Project
```bash
docuai generate my_project/
```
**Output:** Comprehensive documentation including:
- Project overview and architecture
- Class and function documentation
- Usage examples
- Best practices

### React/TypeScript Application
```bash
docuai analyze src/
```
**Output:** Code quality report with:
- Code smells and anti-patterns
- Security vulnerabilities
- Performance issues
- Refactoring suggestions

### Full-Stack Project Analysis
```bash
# Analyze entire codebase
docuai generate . --output PROJECT_DOCS.md
```

## 🛠️ Commands

### `generate`
Generate comprehensive documentation for code files, directories, or repositories.

**Syntax:**
```bash
docuai generate <input_path> [--output OUTPUT]
```

**Arguments:**
- `input_path` - File path, directory path, or GitHub URL
- `--output` - Optional custom output filename

**Examples:**
```bash
docuai generate app.py                    # Single file
docuai generate .                         # Current directory
docuai generate /path/to/project          # Specific directory
docuai generate https://github.com/user/repo  # GitHub repo
```

### `analyze`
Analyze code for quality issues, smells, and improvements.

**Syntax:**
```bash
docuai analyze <input_path> [--output OUTPUT]
```

**Examples:**
```bash
docuai analyze app.py                     # Single file
docuai analyze .                          # Current directory
docuai analyze https://github.com/user/repo --output report.md
```

## 🌍 Supported Languages

| Language   | File Extensions | Parser |
|------------|----------------|--------|
| Python     | `.py`          | AST    |
| JavaScript | `.js`, `.jsx`  | Esprima |
| TypeScript | `.ts`, `.tsx`  | Esprima |

## 📖 Documentation

### Directory Traversal

DocuAI recursively processes all supported files in directories and subdirectories.

**Automatically Ignored:**
- `.git`, `.venv`, `venv`
- `node_modules`
- `__pycache__`, `dist`, `build`
- `.idea`, `.vscode`

### GitHub Integration

Analyze any public GitHub repository:

```bash
docuai generate https://github.com/username/repo
```

**How it works:**
1. Clones repository to temporary directory
2. Processes all supported files
3. Generates documentation
4. Cleans up temporary files

**For private repositories:**
```bash
git clone https://github.com/username/private-repo
cd private-repo
docuai generate .
```

### Output Files

All commands automatically save results to `.md` files:

| Command | Default Output |
|---------|---------------|
| `docuai generate file.py` | `file_docs.md` |
| `docuai analyze file.py` | `file_analysis.md` |
| `docuai generate .` | `dirname_documentation.md` |
| `docuai analyze .` | `dirname_analysis.md` |

Use `--output` to specify custom filenames.

## 🔧 Troubleshooting

### API Key Not Found
```
ValueError: OpenAI API key not found
```
**Solution:** Set your API key using one of the methods in [Configuration](#configuration)

### Unsupported File Type
```
ValueError: Unsupported file type
```
**Solution:** DocuAI only supports `.py`, `.js`, `.jsx`, `.ts`, `.tsx` files

### No Files Found
```
No supported files found
```
**Solution:** Ensure your directory contains supported file types and isn't in the ignore list

## 💡 Tips

- **Large Projects:** Use `--output` to save results to a specific file
- **API Costs:** DocuAI uses GPT-5, which costs ~$0.01 per file analyzed
- **Best Results:** Ensure your code has clear function/class names and comments
- **Performance:** Processing large repositories may take a few minutes

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **PyPI:** https://pypi.org/project/docuai/
- **GitHub:** https://github.com/AyushJaiswal18/DocuAI
- **Issues:** https://github.com/AyushJaiswal18/DocuAI/issues

## 🙏 Acknowledgments

- Built with [LangChain](https://github.com/langchain-ai/langchain)
- Powered by [OpenAI GPT-5](https://openai.com/)
- CLI built with [Typer](https://typer.tiangolo.com/)

---

<div align="center">

**Made with ❤️ by [Ayush Jaiswal](https://github.com/AyushJaiswal18)**

If you find DocuAI useful, please consider giving it a ⭐ on GitHub!

</div>
