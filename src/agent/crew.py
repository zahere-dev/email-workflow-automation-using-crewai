from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.asana_tool import AsanaTool
from tools.db_ops_tool import db_ops_tool
from openai import OpenAI
import os

# Uncomment the following line to use an example of a custom tool
# from agent.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool



@CrewBase
class AgentCrew:
    """Agent crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def email_parser_triage_agent(self) -> Agent:
        print(self.agents_config)
        return Agent(
            config=self.agents_config["email_parser_triage_agent"],
            verbose=True,
            allow_delegation=False
        )

    @agent
    def asana_ops_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['asana_ops_agent'],
            tools=[AsanaTool],
            verbose=True
        )

    @agent
    def database_ops_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['database_ops_agent'],
            tools=[db_ops_tool],
            verbose=True
        )

    @task
    def parse_and_triage_task(self) -> Task:
        return Task(
            config=self.tasks_config["parse_and_triage_task"],
        )


    @task
    def asana_task_creation(self) -> Task:
        return Task(
            config=self.tasks_config['asana_task_creation'],
        )

    @task
    def db_storage_task(self) -> Task:
        return Task(
            config=self.tasks_config['db_storage_task']
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Agent crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True
        )
