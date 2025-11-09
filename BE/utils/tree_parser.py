import os
import json

class TreeParser:
    # Directories to ignore
    IGNORE_DIRS = {
        '.git', 'node_modules', '__pycache__', 'venv', 'env',
        '.venv', 'dist', 'build', '.idea', '.vscode', 'target'
    }
    
    # Files to ignore
    IGNORE_FILES = {
        '.DS_Store', 'Thumbs.db', '.gitignore'
    }
    
    def __init__(self, root_path):
        self.root_path = root_path
    
    def generate_tree(self):
        """Generate file tree structure"""
        tree = {
            'name': os.path.basename(self.root_path),
            'type': 'directory',
            'path': self.root_path,
            'children': []
        }
        
        self._build_tree(self.root_path, tree)
        return tree
    
    def _build_tree(self, path, node):
        """Recursively build tree"""
        try:
            items = sorted(os.listdir(path))
        except PermissionError:
            return
        
        for item in items:
            if item in self.IGNORE_DIRS or item in self.IGNORE_FILES:
                continue
            
            item_path = os.path.join(path, item)
            
            if os.path.isdir(item_path):
                child = {
                    'name': item,
                    'type': 'directory',
                    'path': item_path,
                    'children': []
                }
                self._build_tree(item_path, child)
                node['children'].append(child)
            else:
                child = {
                    'name': item,
                    'type': 'file',
                    'path': item_path,
                    'extension': os.path.splitext(item)[1]
                }
                node['children'].append(child)
    
    def find_readme(self):
        """Find README file"""
        readme_names = ['README.md', 'readme.md', 'README', 'README.txt']
        for name in readme_names:
            path = os.path.join(self.root_path, name)
            if os.path.exists(path):
                return path
        return None
    
    def find_entry_points(self):
        """Find likely entry point files"""
        entry_names = ['main.py', 'app.py', '__main__.py', 'index.py', 
                       'main.jac', 'app.jac', 'cli.py']
        entry_points = []
        
        for root, dirs, files in os.walk(self.root_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in self.IGNORE_DIRS]
            
            for file in files:
                if file in entry_names:
                    entry_points.append(os.path.join(root, file))
        
        return entry_points
    
    def get_python_files(self):
        """Get all Python files"""
        python_files = []
        
        for root, dirs, files in os.walk(self.root_path):
            dirs[:] = [d for d in dirs if d not in self.IGNORE_DIRS]
            
            for file in files:
                if file.endswith(('.py', '.jac')):
                    python_files.append(os.path.join(root, file))
        
        return python_files