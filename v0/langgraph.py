import importlib
from typing import Any, Dict

class AIClientSDK:
    def __init__(self):
        """Initialize the SDK with dynamic client handling."""
        self.clients = {}

    def register_client(self, name: str, module_name: str, class_name: str, init_args: Dict[str, Any] = {}):
        """Dynamically register a client and store its instance."""
        try:
            module = importlib.import_module(module_name)
            client_class = getattr(module, class_name)
            self.clients[name] = client_class(**init_args)
        except (ImportError, AttributeError) as e:
            raise RuntimeError(f"Error loading {class_name} from {module_name}: {e}")

    def get_client(self, name: str) -> Any:
        """Retrieve a registered client instance by name."""
        if name not in self.clients:
            raise ValueError(f"Client '{name}' is not registered.")
        return self.clients[name]


# Example Usage
if __name__ == "__main__":
    sdk = AIClientSDK()

    # Register LangGraph Client
    sdk.register_client("langgraph", "langgraph.graph", "StateGraph")

    # Register LangChain OpenAI Client
    sdk.register_client("langchain_openai", "langchain.llms", "OpenAI", init_args={"model_name": "gpt-3.5-turbo"})

    # Get LangGraph Client
    langgraph_client = sdk.get_client("langgraph")
    print(langgraph_client)  # Returns the LangGraph client instance

    # Get LangChain OpenAI Client
    langchain_client = sdk.get_client("langchain_openai")
    print(langchain_client)  # Returns the OpenAI client instance