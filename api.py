from fastapi import FastAPI
from Weather_agent.agent import root_agent  
from pydantic import BaseModel
from google.adk.agents.run_config import RunConfig
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai.types import Content, Part

APP_NAME = "Weather_agent"
session_service = InMemorySessionService()

app = FastAPI()

class QueryInput(BaseModel):
    city:str
    session_id:str
    user_id:str

@app.post("/weather-farming")
async def weather_farming(query: QueryInput):
    
    city =  query.city
    session_id = query.session_id
    user_id =  query.user_id
    
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )
    runner = Runner(
        app_name=APP_NAME,
        agent=root_agent,
        session_service=session_service,
    )

    user_message = Content(role="user", parts=[Part.from_text(text=city)])
    run_config = RunConfig(response_modalities=["TEXT"])
    events = runner.run(
        user_id=session.user_id,
        session_id=session.id,
        new_message=user_message,
        run_config=run_config,
    )

    response_text = ""
    for event in events:
        if event.content and event.content.parts:
            response_text += "".join([
                part.text or ""
                for part in event.content.parts
            ])
    with open("Response.txt","w") as f:
        f.write(response_text.strip())
    return {"response": response_text.strip()}
