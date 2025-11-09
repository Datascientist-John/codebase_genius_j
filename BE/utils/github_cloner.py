import os
import shutil
from git import Repo
from urllib.parse import urlparse

class GitHubCloner:
    def __init__(self, base_dir="temp_repos"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)
    
    def validate_url(self, url):
        """Validate GitHub URL"""
        try:
            parsed = urlparse(url)
            if 'github.com' not in parsed.netloc:
                return False, "Not a GitHub URL"
            return True, "Valid"
        except:
            return False, "Invalid URL format"
    
    def clone_repo(self, url):
        """Clone repository and return local path"""
        is_valid, msg = self.validate_url(url)
        if not is_valid:
            raise ValueError(msg)
        
        # Extract repo name
        repo_name = url.rstrip('/').split('/')[-1].replace('.git', '')
        local_path = os.path.join(self.base_dir, repo_name)
        
        # Remove if exists
        if os.path.exists(local_path):
            shutil.rmtree(local_path)
        
        # Clone
        try:
            Repo.clone_from(url, local_path)
            return local_path, repo_name
        except Exception as e:
            raise Exception(f"Failed to clone: {str(e)}")
    
    def cleanup(self, repo_name):
        """Remove cloned repository"""
        path = os.path.join(self.base_dir, repo_name)
        if os.path.exists(path):
            shutil.rmtree(path)