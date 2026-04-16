from crewai.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData
import os
from dotenv import load_dotenv

load_dotenv()


class AlphaVantageInput(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol e.g. TSLA")
    function: str = Field(
        default="INCOME_STATEMENT",
        description="Function: INCOME_STATEMENT, BALANCE_SHEET, CASH_FLOW, OVERVIEW",
    )


class AlphaVantageTool(BaseTool):
    name: str = "AlphaVantage Financial Data"
    description: str = "Fetches financial statements (income, balance, cash flow) and overview for a ticker from Alpha Vantage API. Last 4 quarters."
    args_schema: Type[BaseModel] = AlphaVantageInput

    def _run(self, ticker: str, function: str = "INCOME_STATEMENT") -> str:
        api_key = os.getenv("ALPHA_VANTAGE_KEY")
        if not api_key:
            return "ERROR: ALPHA_VANTAGE_KEY missing in .env"

        fd = FundamentalData(key=api_key, output_format="pandas")
        data, meta = (
            fd.get_income_statement(quarterly=True)
            if function == "INCOME_STATEMENT"
            else fd.get_balance_sheet(quarterly=True)
            if function == "BALANCE_SHEET"
            else fd.get_cash_flow(quarterly=True)
            if function == "CASH_FLOW"
            else fd.get_company_overview()
        )

        if function != "OVERVIEW":
            # Last 4 quarters
            recent = data.head(4).to_dict()
            return str({ticker: recent})
        return str(data.iloc[0].to_dict())


class SerperSearchInput(BaseModel):
    query: str = Field(
        ..., description="Search query e.g. 'TSLA CEO earnings call transcript 2026'"
    )
    num_results: int = Field(default=10, ge=1, le=20)


# SerperDevTool already in crewai_tools, but custom wrapper if needed
# For now, document use SerperDevTool directly in agents/tasks
