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
            system_prompt = f"""You are an expert Indian Cultural Preservation Researcher.

                            === LOCAL KNOWLEDGE BASE ===
                            {context_str}
                            ============================

                            STRICT RESPONSE RULES:
                            1. GREETINGS: If the user query is a simple greeting or pleasantry (e.g., "hello", "hi", "hey", "namaste"), respond with a brief, friendly 1-sentence greeting asking how you can help them explore the culture of {state_name}. Do NOT output background knowledge or detailed information for simple greetings.
                            2. OUT OF SCOPE: If the question is completely UNRELATED to Culture, Tradition, Local Food, or History, politely decline in 1 short sentence.
                            3. GROUND TRUTH & FALLBACK: 
                            - For specific cultural queries, first use the facts from the LOCAL KNOWLEDGE BASE above.
                            - If the answer is not present in the base but is related to Culture, Tradition, Food, or History, give a concise response based on general knowledge.
                            4. BREVITY: Keep all answers directly to the point. Avoid fluff or unnecessary preamble. Highlight key facts, issues, or solutions clearly.
                            5. NO TABLES OR MARKDOWN HEADERS: Do NOT use markdown tables (|), horizontal rules (---), or headings (##) and (**). Use simple bullet points (*) and bold text for clarity."""
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