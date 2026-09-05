import json
from pathlib import Path

class RAGService:
    def __init__(self, json_file_path: str = "data/culture_knowledge.json"):
        self.file_path = Path(json_file_path)

    def get_state_culture_data(self, state_name: str) -> dict | None:
        """Reads and retrieves cultural facts for a specific state from JSON."""
        if not self.file_path.exists():
            return None

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            for key in data:
                if key.lower() == state_name.lower().strip():
                    return data[key]
        except Exception as e:
            print(f"Error reading JSON knowledge base: {e}")
            return None

        return None