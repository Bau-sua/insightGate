from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool
from insightgape.tools import AlphaVantageTool


@CrewBase
class InsightGapeCrew:
    """InsightGape Black Box Auditor Crew."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def financial_data_scraper(self) -> Agent:
        return Agent(
            config=self.agents_config["financial_data_scraper"],  # type: ignore[index]
            tools=[AlphaVantageTool()],
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def market_sentiment_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["market_sentiment_analyst"],  # type: ignore[index]
            tools=[SerperDevTool()],
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def dissonance_auditor(self) -> Agent:
        return Agent(
            config=self.agents_config["dissonance_auditor"],  # type: ignore[index]
            verbose=True,
            llm="openai/gpt-4o",
            reasoning=True,
        )

    @agent
    def reporting_officer(self) -> Agent:
        return Agent(
            config=self.agents_config["reporting_officer"],  # type: ignore[index]
            verbose=True,
        )

    @task
    def financial_scrape_task(self) -> Task:
        return Task(
            config=self.tasks_config["financial_scrape_task"],  # type: ignore[index]
        )

    @task
    def sentiment_gather_task(self) -> Task:
        return Task(
            config=self.tasks_config["sentiment_gather_task"],  # type: ignore[index]
            context=[self.financial_scrape_task()],
        )

    @task
    def audit_task(self) -> Task:
        return Task(
            config=self.tasks_config["audit_task"],  # type: ignore[index]
            context=[self.financial_scrape_task(), self.sentiment_gather_task()],
        )

    @task
    def report_task(self) -> Task:
        return Task(
            config=self.tasks_config["report_task"],  # type: ignore[index]
            context=[
                self.financial_scrape_task(),
                self.sentiment_gather_task(),
                self.audit_task(),
            ],
            markdown=True,
        )

    @crew
    def audit_crew(self) -> Crew:
        """Creates the InsightGape Audit Crew."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            memory=False,  # Disable OpenAI 403 embeddings\n            cache=True,
            tracing=True,
        )
