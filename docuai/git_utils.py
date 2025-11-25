import os
import shutil
import tempfile
import subprocess
from typing import Generator

def clone_repo(repo_url: str) -> str:
    """
    Clones a git repository to a temporary directory.
    Returns the path to the temporary directory.
    """
    temp_dir = tempfile.mkdtemp()
    try:
        subprocess.check_call(["git", "clone", repo_url, temp_dir])
        return temp_dir
    except subprocess.CalledProcessError as e:
        shutil.rmtree(temp_dir)
        raise RuntimeError(f"Failed to clone repository: {e}")

def cleanup_repo(path: str):
    """
    Removes the temporary directory.
    """
    shutil.rmtree(path)

def get_repo_files(path: str) -> Generator[str, None, None]:
    """
    Yields all supported file paths in the repository.
    Recursively traverses all subdirectories.
    """
    ignore_dirs = {".git", ".venv", "venv", "node_modules", "__pycache__", "dist", "build", ".idea", ".vscode"}
    
    for root, dirs, files in os.walk(path):
        # Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        for file in files:
            if file.endswith((".py", ".js", ".ts", ".tsx", ".jsx")):
                yield os.path.join(root, file)
