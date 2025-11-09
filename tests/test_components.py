import sys
sys.path.append('BE')

from utils.github_cloner import GitHubCloner
from utils.tree_parser import TreeParser
from utils.ccg_builder import CodeContextGraph

def test_cloner():
    print("Testing GitHub Cloner...")
    cloner = GitHubCloner()
    
    # Test with a small public repo
    url = "https://github.com/octocat/Hello-World"
    path, name = cloner.clone_repo(url)
    print(f"✓ Cloned to: {path}")
    
    return path, name

def test_tree_parser(repo_path):
    print("\nTesting Tree Parser...")
    parser = TreeParser(repo_path)
    tree = parser.generate_tree()
    print(f"✓ Generated tree with {len(tree.get('children', []))} items")
    
    readme = parser.find_readme()
    print(f"✓ Found README: {readme}")
    
    return tree

def test_ccg(repo_path):
    print("\nTesting CCG Builder...")
    ccg = CodeContextGraph()
    
    parser = TreeParser(repo_path)
    files = parser.get_python_files()
    
    for file in files[:5]:  # Test first 5 files
        ccg.analyze_file(file)
    
    data = ccg.to_dict()
    print(f"✓ Found {len(data['functions'])} functions")
    print(f"✓ Found {len(data['classes'])} classes")
    
    return ccg

if __name__ == "__main__":
    path, name = test_cloner()
    tree = test_tree_parser(path)
    ccg = test_ccg(path)
    print("\n✅ All tests passed!")