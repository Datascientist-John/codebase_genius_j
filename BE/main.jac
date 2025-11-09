import from byllm.llm { Model }
import from dotenv { load_dotenv }
import from agents.supervisor { CodeGenius, RepoNode, RepoMapper }
import json;


# Root node for the application
node root {}



glob llm = Model(model_name="gemini/gemini-2.0-flash", verbose=False);

# API walker to handle requests
walker generate_docs {
    has github_url: str;
    has response: dict = {};
    
    can execute with `root entry {
        print(f"Received request for: {self.github_url}");
        
        # Spawn supervisor
        supervisor = root spawn CodeGenius(github_url=self.github_url);
        
        # Get result
        self.response = supervisor.result;

        #Print result so streamlit can capture
        print(json.dumps(self.response));
    }
}

# Walker to check status
walker health_check {
    has status: str = "healthy";
    has response: dict = {};
    
    can check with `root entry {
        ts = str(datetime.datetime.now());
        self.response = {
            "status": self.status,
            "model": "gemini/gemini-2.0-flash",
            
        };
        print(json.dumps(self.response));
    }
}

with entry {
    load_dotenv();
}
