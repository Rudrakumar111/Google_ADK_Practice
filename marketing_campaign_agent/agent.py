import os
try:
    from dotenv import load_dotenv
    load_dotenv()

    MODEL_NAME = os.environ.get("GOOGLE_GENAI_MODEL", "gemini-2.0-flash")
except ImportError:
    print("Warning: dotenv not installed. Ensure API key is set.")

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import google_search
from marketing_campaign_agent.instructions import (
    MARKET_REASEACH_INSTRUCTION,
    MESSAGING_STRATEGIST_INSTRUCTION,
    VISUAL_SUGGESTER_INSTRUCTION,
    FORMATTER_INSTRUCTION,
    CAMPAIGN_ORCHESTRATOR_INSTRUCTION
)

market_research_agent = LlmAgent(
    name="MarketResearcher",
    model=MODEL_NAME,
    instruction=MARKET_REASEACH_INSTRUCTION,
    tools=[google_search],
    output_key="market_research_summary"
)

messaging_strategist_agent = LlmAgent(
    name="MessagingStrategist",
    model=MODEL_NAME,
    instruction=MESSAGING_STRATEGIST_INSTRUCTION,
    output_key="key_messaging"
)

visual_suggester_agent=LlmAgent(
    name="VisualSuggester",
    model=MODEL_NAME,
    instruction=VISUAL_SUGGESTER_INSTRUCTION,
    output_key="visual_concepts"
)

formatter_agent = LlmAgent(
    name="CampaignBriefFormatter",
    model=MODEL_NAME,
    instruction=FORMATTER_INSTRUCTION,
    output_key="final_campaign_brief"
)

campaign_orchestrator = SequentialAgent(
    name="MarketingCampaignAssistant",
    description=CAMPAIGN_ORCHESTRATOR_INSTRUCTION,
    sub_agents=[
        market_research_agent,
        messaging_strategist_agent,
        visual_suggester_agent,
        formatter_agent
    ]
)

root_agent = campaign_orchestrator  
