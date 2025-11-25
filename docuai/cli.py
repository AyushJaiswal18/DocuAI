import typer
import os
from dotenv import load_dotenv
from rich.console import Console
from docuai.parsers.python_parser import PythonParser
from docuai.parsers.js_parser import JSParser
from docuai.agent import DocuAIAgent
from docuai.git_utils import clone_repo, cleanup_repo, get_repo_files

load_dotenv()

app = typer.Typer()
console = Console()

def get_parser(file_path: str):
    if file_path.endswith(".py"):
        return PythonParser()
    elif file_path.endswith((".js", ".jsx", ".ts", ".tsx")):
        return JSParser()
    else:
        raise ValueError(f"Unsupported file type: {file_path}")

def process_file_generate(file_path: str, output: str = None, agent: DocuAIAgent = None):
    try:
        parser = get_parser(file_path)
        console.print(f"[bold green]Parsing {file_path}...[/bold green]")
        metadata = parser.parse(file_path)
        
        console.print(f"[bold green]Generating documentation for {os.path.basename(file_path)}...[/bold green]")
        docs = agent.generate_docs(metadata)
        
        # Auto-save to .md file
        if output:
            # If output is a directory, save file there
            if os.path.isdir(output):
                out_path = os.path.join(output, os.path.basename(file_path) + ".md")
            else:
                out_path = output
        else:
            # Auto-generate filename
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            out_path = f"{base_name}_docs.md"
            
        with open(out_path, "w") as f:
            f.write(docs)
        console.print(f"[bold blue]✓ Documentation saved to {out_path}[/bold blue]")
            
    except Exception as e:
        console.print(f"[bold red]Error processing {file_path}: {e}[/bold red]")

def process_file_analyze(file_path: str, output: str = None, agent: DocuAIAgent = None):
    try:
        console.print(f"[bold green]Analyzing {file_path}...[/bold green]")
        analysis = agent.analyze_code(file_path)
        
        # Auto-save to .md file
        if output:
            out_path = output
        else:
            # Auto-generate filename
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            out_path = f"{base_name}_analysis.md"
            
        with open(out_path, "w") as f:
            f.write(f"# Code Analysis: {os.path.basename(file_path)}\n\n")
            f.write(analysis)
        console.print(f"[bold blue]✓ Analysis saved to {out_path}[/bold blue]")
            
    except Exception as e:
        console.print(f"[bold red]Error analyzing {file_path}: {e}[/bold red]")

@app.command()
def generate(input_path: str, output: str = None):
    """
    Generate documentation for a code file, a GitHub repository, or a local directory.
    """
    agent = DocuAIAgent()
    
    files = []
    temp_dir = None
    
    try:
        if input_path.startswith("http://") or input_path.startswith("https://"):
            console.print(f"[bold yellow]Cloning repository from {input_path}...[/bold yellow]")
            temp_dir = clone_repo(input_path)
            console.print(f"[bold green]Repository cloned to {temp_dir}[/bold green]")
            files = list(get_repo_files(temp_dir))
        elif os.path.isdir(input_path):
            console.print(f"[bold yellow]Processing directory {input_path}...[/bold yellow]")
            files = list(get_repo_files(input_path))
        else:
            # Single file processing
            process_file_generate(input_path, output, agent)
            return

        # Repo/Dir processing
        if not files:
            console.print("[bold red]No supported files found.[/bold red]")
            return

        console.print(f"[bold green]Parsing {len(files)} files...[/bold green]")
        metadata_list = []
        for f in files:
            try:
                parser = get_parser(f)
                metadata_list.append(parser.parse(f))
            except Exception as e:
                console.print(f"[red]Skipping {f}: {e}[/red]")
        
        console.print("[bold green]Generating repository documentation...[/bold green]")
        docs = agent.generate_repo_docs(metadata_list)
        
        # Auto-save repo docs
        if output:
            out_path = output
        else:
            # Auto-generate filename based on directory name
            dir_name = os.path.basename(os.path.abspath(input_path if not temp_dir else temp_dir))
            out_path = f"{dir_name}_documentation.md"
            
        with open(out_path, "w") as f:
            f.write(docs)
        console.print(f"[bold blue]✓ Documentation saved to {out_path}[/bold blue]")
            
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
    finally:
        if temp_dir:
            cleanup_repo(temp_dir)
            console.print("[bold yellow]Repository cleaned up.[/bold yellow]")

@app.command()
def analyze(input_path: str, output: str = None):
    """
    Analyze code for smells and improvements.
    """
    agent = DocuAIAgent()
    
    files = []
    temp_dir = None
    
    try:
        if input_path.startswith("http://") or input_path.startswith("https://"):
            console.print(f"[bold yellow]Cloning repository from {input_path}...[/bold yellow]")
            temp_dir = clone_repo(input_path)
            console.print(f"[bold green]Repository cloned to {temp_dir}[/bold green]")
            files = list(get_repo_files(temp_dir))
        elif os.path.isdir(input_path):
            console.print(f"[bold yellow]Processing directory {input_path}...[/bold yellow]")
            files = list(get_repo_files(input_path))
        else:
            # Single file processing
            process_file_analyze(input_path, output, agent)
            return

        # Repo/Dir processing
        if not files:
            console.print("[bold red]No supported files found.[/bold red]")
            return

        console.print(f"[bold green]Analyzing {len(files)} files...[/bold green]")
        analysis = agent.analyze_repo(files)
        
        # Auto-save repo analysis
        if output:
            out_path = output
        else:
            # Auto-generate filename based on directory name
            dir_name = os.path.basename(os.path.abspath(input_path if not temp_dir else temp_dir))
            out_path = f"{dir_name}_analysis.md"
            
        with open(out_path, "w") as f:
            f.write(f"# Code Analysis Report\n\n")
            f.write(analysis)
        console.print(f"[bold blue]✓ Analysis saved to {out_path}[/bold blue]")
            
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
    finally:
        if temp_dir:
            cleanup_repo(temp_dir)
            console.print("[bold yellow]Repository cleaned up.[/bold yellow]")

if __name__ == "__main__":
    app()
