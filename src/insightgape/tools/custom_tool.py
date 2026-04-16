from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


from .alpha_vantage_tool import AlphaVantageTool
# SerperDevTool from crewai_tools.SerperDevTool() in agent instantiation
# Custom tools ready for financial_scrape_task
