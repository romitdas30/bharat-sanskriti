from pydantic import BaseModel, Field

class CultureRequest(BaseModel):
    state_name: str = Field(..., example="Rajasthan", description="Name of the Indian State")
    user_query: str = Field(..., example="What challenges are local puppeteers facing?", description="User research question")

class CultureResponse(BaseModel):
    state_name: str
    user_query: str
    found_in_json: bool
    ai_response: str
    status: str = "success"