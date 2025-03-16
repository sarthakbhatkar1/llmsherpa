import importlib
import yaml
from typing import Any, Dict, Optional

class DynamicAISDK:
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize SDK with configuration-based dynamic library loading."""
        self.config = self.load_config(config_path)
        self.module_cache = {}
        self.active_library = self.config.get("default_library", "langchain")

    def load_config(self, path: str) -> Dict[str, Any]:
        """Load the YAML configuration file."""
        with open(path, "r") as file:
            return yaml.safe_load(file)

    def load_library(self, library_name: str):
        """Dynamically import a library based on config."""
        library_info = self.config["libraries"].get(library_name)
        if not library_info:
            raise ValueError(f"Library '{library_name}' is not configured. Add it to config.yaml.")

        module_name = library_info["module"]
        if module_name in self.module_cache:
            return self.module_cache[module_name]

        try:
            module = importlib.import_module(module_name)
            self.module_cache[module_name] = module
            return module
        except ImportError:
            raise ImportError(f"Library '{module_name}' is not installed. Install it using 'pip install {module_name}'.")

    def invoke(self, query: str, library: Optional[str] = None) -> Any:
        """Dynamically invoke the function of the selected library."""
        library = library or self.active_library
        library_info = self.config["libraries"].get(library)
        
        if not library_info:
            raise ValueError(f"Library '{library}' is not supported. Add it in config.yaml.")

        # Dynamically call the correct function
        invoke_function_name = library_info["invoke_function"]
        if hasattr(self, invoke_function_name):
            return getattr(self, invoke_function_name)(query)
        else:
            raise ValueError(f"Function '{invoke_function_name}' not found in SDK.")

    # Dynamically defined methods for each library
    def invoke_langchain(self, query: str):
        """Invoke LangChain dynamically."""
        from langchain.llms import OpenAI
        llm = OpenAI(model_name="gpt-3.5-turbo")
        return llm.predict(query)

    def invoke_langgraph(self, query: str):
        """Invoke LangGraph dynamically."""
        return f"LangGraph executed query: {query}"

    def invoke_langsmith(self, query: str):
        """Invoke LangSmith dynamically."""
        from langsmith.client import LangSmith
        client = LangSmith()
        return client.log({"query": query})

    def invoke_llamaindex(self, query: str):
        """Invoke LlamaIndex dynamically."""
        from llama_index.llms import OpenAI
        llm = OpenAI(model="gpt-4")
        return llm.complete(query)

    def invoke_haystack(self, query: str):
        """Invoke Haystack dynamically."""
        return f"Haystack executed query: {query}"

# Example Usage
if __name__ == "__main__":
    sdk = DynamicAISDK()
    response = sdk.invoke("What is Generative AI?", library="langchain")
    print(response)