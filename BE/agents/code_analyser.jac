import from utils.ccg_builder { CodeContextGraph }
import from utils.tree_parser { TreeParser }

walker CodeAnalyzer {
    has repo_node: RepoNode;
    has entry_points: list;
    has ccg: CodeContextGraph;
    
    can analyze_code with RepoNode entry {
        print("Analyzing code structure...");
        
        self.ccg = CodeContextGraph();
        
        # Get all Python/Jac files
        parser = TreeParser(here.local_path);
        python_files = parser.get_python_files();
        
        print(f"Analyzing {len(python_files)} files");
        
        # Analyze each file
        for file_path in python_files {
            try {
                self.ccg.analyze_file(file_path);
            } except Exception as e {
                print(f"Error analyzing {file_path}: {e}");
            }
        }
        
        # Store CCG in node
        here.status = "analyzed";
        
        # Generate documentation
        spawn DocGenie(repo_node=here, ccg=self.ccg);
    }
}