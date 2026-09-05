import os
from groq import Groq

class GroqService:
    def __init__(self, model_name: str = "openai/gpt-oss-120b"):
    # def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set.")
        self.client = Groq(api_key=api_key)
        self.model_name = model_name

    def generate_cultural_response(self, state_name: str, user_query: str, context_data: dict | None) -> str:
        """Constructs prompt with grounded context and queries the Groq API."""
        if context_data:
            context_str = f"""
            State: {state_name}
            Famous Culture: {context_data.get('famous_culture')}
            Threats Facing: {context_data.get('threats_facing')}
            Preservation Strategies: {context_data.get('preservation_strategies')}
            """
            system_prompt = f"""
            You are an expert Indian Cultural Preservation Researcher.
            Answer the user query using the GROUND TRUTH facts provided below:

            === LOCAL KNOWLEDGE BASE ===
            {context_str}
            ============================

            Provide a clear, structured, and helpful response highlighting issues and solutions.
            """
        else:
            system_prompt = f"""
            You are an expert Indian Cultural Preservation Researcher. 
            Answer using general knowledge for the state of {state_name}.
            """

        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            temperature=0.2,
            max_tokens=600
        )

        return completion.choices[0].message.content