import os
from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv
from google.adk.agents import LlmAgent,SequentialAgent
from google.adk.tools import google_search
from vertexai import agent_engines
import vertexai
from vertexai.preview import reasoning_engines
from Weather_agent.instructions import (
    WEATHER_DETAILS_INSTRUCTION,
    FARMING_REASEACH_INSTRUCTION,
    WEATHER_ORCHESTRATOR_INSTRUCTION
)
load_dotenv()
MODEL_NAME = os.environ.get("GOOGLE_GENAI_MODEL", "gemini-2.0-flash")

Weather_details_Agent = LlmAgent(
    name="Weather_Details_instructions",
    model=MODEL_NAME,
    instruction=WEATHER_DETAILS_INSTRUCTION,
    tools=[google_search],
    output_key="weather_details_summary"
)

Farming_Reasearch_Agent = LlmAgent(
    name="Farming_Details_Reasearch",
    model=MODEL_NAME,
    instruction=FARMING_REASEACH_INSTRUCTION,
    output_key="Farming_Reasearch"
)


Weather_orchestrator= SequentialAgent(
    name="Weather_Based_Farming",
    description=WEATHER_ORCHESTRATOR_INSTRUCTION,
    sub_agents=[
        Weather_details_Agent,
        Farming_Reasearch_Agent
    ]
)

root_agent = Weather_orchestrator