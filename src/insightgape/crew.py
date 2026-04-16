from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class InsightGapeCrew:
    """InsightGape Black Box Auditor Crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
@agent
    def financial_data_scraper(self) -> Agent:
        from insightgape.tools import AlphaVantageTool
        from crewai_tools import SerperDevTool
        return Agent(
            config=self.agents_config['financial_data_scraper'],  # type: ignore[index]
            tools=[AlphaVantageTool()],
            verbose=True,
            allow_delegation=False
        )

    @agent
    def market_sentiment_analyst(self) -> Agent:
        from crewai_tools import SerperDevTool
        return Agent(
            config=self.agents_config['market_sentiment_analyst'],  # type: ignore[index]
            tools=[SerperDevTool()],
            verbose=True,
            allow_delegation=False
        )

    @agent
    def dissonance_auditor(self) -> Agent:
        return Agent(
            config=self.agents_config['dissonance_auditor'],  # type: ignore[index]
            verbose=True,
            llm="openai/gpt-4o",
            reasoning=True
        )

    @agent
    def reporting_officer(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_officer'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["reporting_analyst"],  # type: ignore[index]
            verbose=True,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
@task
    def financial_scrape_task(self) -> Task:
        return Task(
            config=self.tasks_config['financial_scrape_task'],  # type: ignore[index]
        )

    @task
    def sentiment_gather_task(self) -> Task:
        return Task(
            config=self.tasks_config['sentiment_gather_task'],  # type: ignore[index]
            context=[self.financial_scrape_task()]
        )

    @task
    def audit_task(self) -> Task:
        return Task(
            config=self.tasks_config['audit_task'],  # type: ignore[index]
            context=[self.financial_scrape_task(), self.sentiment_gather_task()]
        )

    @task
    def report_task(self) -> Task:
        return Task(
            config=self.tasks_config['report_task'],  # type: ignore[index]
            context=[self.financial_scrape_task(), self.sentiment_gather_task(), self.audit_task()],
            output_file="outputs/{{ticker}}_audit.md"
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config["reporting_task"],  # type: ignore[index]
            output_file="report.md",
        )

@crew
    def audit_crew(self) -> Crew:
        """Creates the InsightGape Audit Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=2,  # Detailed live logs
            memory=True,
            cache=True,
            output_log_file=True
        )
