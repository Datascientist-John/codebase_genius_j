import from utils.github_cloner { GitHubCloner }
import from utils.tree_parser { TreeParser }
import json;

# Node to store repository information
node RepoNode {
    has url: str;
    has local_path: str;
    has repo_name: str;
    has status: str = "pending";
    has file_tree: dict = {};
    has readme_summary: str = "";
    has documentation: str = "";
}

# Supervisor walker - orchestrates the entire workflow
walker CodeGenius {
    has github_url: str;
    has result: dict = {
        "status": "pending",
        "message": "",
        "documentation": ""
    };
    
    can start with `root entry {
        print("Starting Code Genius...");
        
        # Step 1: Validate and clone repository
        cloner = GitHubCloner();
        
        try {
            (is_valid, msg) = cloner.validate_url(self.github_url);
            
            if not is_valid {
                self.result["status"] = "error";
                self.result["message"] = msg;
                return;
            }
            
            # Clone repository
            (local_path, repo_name) = cloner.clone_repo(self.github_url);
            print(f"Repository cloned to: {local_path}");
            
            # Create repo node
            repo_node = RepoNode(
                url=self.github_url,
                local_path=local_path,
                repo_name=repo_name,
                status="cloned"
            );
            
            root ++> repo_node;
            
            # Step 2: Map repository
            repo_node spawn RepoMapper(repo_node=repo_node);
            
            self.result["status"] = "success";
            self.result["repo_name"] = repo_name;
            
        } except Exception as e {
            self.result["status"] = "error";
            self.result["message"] = str(e);
        }
    }
}

# Walker to handle repository mapping
walker RepoMapper {
    has repo_node: RepoNode;
    
    can map_repository with RepoNode entry {
        print(f"Mapping repository: {here.repo_name}");
        
        # Generate file tree
        parser = TreeParser(here.local_path);
        file_tree = parser.generate_tree();
        here.file_tree = file_tree;
        
        # Find and summarize README
        readme_path = parser.find_readme();
        if readme_path {
            with open(readme_path, 'r') as f {
                readme_content = f.read();
            }
            here.readme_summary = readme_content;
        }
        
        # Find entry points
        entry_points = parser.find_entry_points();
        
        print(f"Found {len(entry_points)} entry points");
        here.status = "mapped";
        
        # Spawn code analyzer
        
        spawn CodeAnalyzer(repo_node=here, entry_points=entry_points);
    }
}
        