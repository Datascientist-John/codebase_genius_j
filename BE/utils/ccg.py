import ast
import os
from collections import defaultdict

class CodeContextGraph:
    def __init__(self):
        self.functions = {}  # function_name -> metadata
        self.classes = {}    # class_name -> metadata
        self.calls = defaultdict(list)  # caller -> [callees]
        self.imports = defaultdict(list)  # file -> [imports]
    
    def analyze_file(self, file_path):
        """Analyze a single Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read(), filename=file_path)
            
            self._extract_info(tree, file_path)
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
    
    def _extract_info(self, tree, file_path):
        """Extract functions, classes, and calls"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    'name': node.name,
                    'file': file_path,
                    'lineno': node.lineno,
                    'args': [arg.arg for arg in node.args.args],
                    'docstring': ast.get_docstring(node)
                }
                self.functions[node.name] = func_info
                
                # Extract function calls
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        if isinstance(child.func, ast.Name):
                            self.calls[node.name].append(child.func.id)
            
            elif isinstance(node, ast.ClassDef):
                class_info = {
                    'name': node.name,
                    'file': file_path,
                    'lineno': node.lineno,
                    'bases': [self._get_name(base) for base in node.bases],
                    'methods': [],
                    'docstring': ast.get_docstring(node)
                }
                
                # Extract methods
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        class_info['methods'].append(item.name)
                
                self.classes[node.name] = class_info
            
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    self.imports[file_path].append(alias.name)
            
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    self.imports[file_path].append(node.module)
    
    def _get_name(self, node):
        """Get name from AST node"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return str(node)
    
    def get_function_callers(self, func_name):
        """Find which functions call this function"""
        callers = []
        for caller, callees in self.calls.items():
            if func_name in callees:
                callers.append(caller)
        return callers
    
    def get_class_hierarchy(self, class_name):
        """Get inheritance hierarchy"""
        if class_name not in self.classes:
            return None
        
        info = self.classes[class_name]
        return {
            'class': class_name,
            'bases': info['bases'],
            'methods': info['methods']
        }
    
    def to_dict(self):
        """Export as dictionary"""
        return {
            'functions': self.functions,
            'classes': self.classes,
            'calls': dict(self.calls),
            'imports': dict(self.imports)
        }