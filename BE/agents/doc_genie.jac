import from utils.diagram_gen { generate_mermaid_diagram };
import os;


walker DocGenieWalker {
can generate_documentation with Repository entry {
repo = here;


std.out("DocGenie: creating documentation parts...");


parts = [];


parts.push(self.create_overview(repo.readme_summary));
parts.push(self.create_file_structure(repo.file_tree));
parts.push(self.create_api_reference(repo.ccg));


diagram = generate_mermaid_diagram(repo.ccg);
parts.push("## Architecture\n\n```mermaid\n" + diagram + "\n```\n");


parts.push(self.create_usage_examples(repo.ccg));


repo.documentation = std.join(parts, "\n\n");


# save to outputs
name = repo.local_path.split("/")[std.len(repo.local_path.split("/")) - 1];
output_dir = "outputs/" + name;
with try {
os.makedirs(output_dir, exist_ok=True);
with open(output_dir + "/docs.md", "w") as f {
f.write(repo.documentation);
}
repo.status = "completed";
report {"message": "docs_generated", "output_path": output_dir + "/docs.md"};
} with except {
repo.status = "error";
report {"error": "failed to write docs"};
}
can create_overview(summary: str) ->