import os;


walker DocGenie {
    has repo_node: RepoNode;
    has ccg: CodeContextGraph;
   
    can generate_documentation with RepoNode entry {
        print("Generating documentation...");
       
        # Build markdown document
        doc = self.build_markdown(here);
       
        # Save to file
        output_dir = f"outputs/{here.repo_name}";
        os.makedirs(output_dir, exist_ok=True);
       
        output_path = f"{output_dir}/DOCUMENTATION.md";
        with open(output_path, 'w') as f {
            f.write(doc);
        }
       
        here.documentation = doc;
        here.status = "documented";
       
        print(f"Documentation saved to: {output_path}");
    }
   
    can build_markdown(repo_node: RepoNode) -> str {
        doc = f"# {repo_node.repo_name}\n\n";
       
        # Project Overview
        doc += "## Project Overview\n\n";
        doc += f"{repo_node.readme_summary}\n\n";
       
        # File Structure
        doc += "## File Structure\n\n";
        doc += self.format_tree(repo_node.file_tree, 0);
        doc += "\n\n";
       
        # API Reference
        doc += "## API Reference\n\n";
       
        ccg_data = self.ccg.to_dict();
       
        # Functions
        if ccg_data['functions'] {
            doc += "### Functions\n\n";
            for func_name, func_info in ccg_data['functions'].items() {
                doc += f"#### `{func_name}()`\n\n";
                if func_info.get('docstring') {
                    doc += f"{func_info['docstring']}\n\n";
                }
                doc += f"**Location:** `{func_info['file']}`:{func_info['lineno']}\n\n";
               
                if func_info['args'] {
                    doc += f"**Arguments:** `{', '.join(func_info['args'])}`\n\n";
                }
            }
        }
       
        # Classes
        if ccg_data['classes'] {
            doc += "### Classes\n\n";
            for class_name, class_info in ccg_data['classes'].items() {
                doc += f"#### `{class_name}`\n\n";
                if class_info.get('docstring') {
                    doc += f"{class_info['docstring']}\n\n";
                }
                doc += f"**Location:** `{class_info['file']}`:{class_info['lineno']}\n\n";
               
                if class_info['bases'] {
                    doc += f"**Inherits from:** {', '.join(class_info['bases'])}\n\n";
                }
               
                if class_info['methods'] {
                    doc += f"**Methods:** {', '.join(class_info['methods'])}\n\n";
                }
            }
        }
       
        return doc;
    }
   
    can format_tree(tree: dict, level: int) -> str {
    indent = "  " * level;
    
    # Fix the ternary operator
    if tree['type'] == 'directory' {
        result = f"{indent}- {tree['name']}/\n";
    } else {
        result = f"{indent}- {tree['name']}\n";
    }
    
    # Check for children
    if tree.get('children') {
        for child in tree['children'] {
            result += self.format_tree(child, level + 1);
        }
    }
    
    return result;
}
    
    
