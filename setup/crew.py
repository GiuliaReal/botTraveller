from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai_tools import SerperDevTool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class BotTourCrew():

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def pesquisador_destinos(self) -> Agent:
        return Agent(
            config=self.agents_config['pesquisador_destinos'], 
            verbose=True,
            tools=[SerperDevTool()]
        )
    
    @agent
    def consultor_turismo(self) -> Agent:
        return Agent(
            config=self.agents_config['consultor_turismo'],
            verbose=True
        )

    @task
    def pesquisar_task(self) -> Task:
        return Task(
            config=self.tasks_config['pesquisar_task'],
        )

    @task
    def roteirizar_task(self) -> Task:
        return Task(
            config=self.tasks_config['roteirizar_task'], 
        )

    @before_kickoff
    def before_kickoff_function(self, inputs):
        print('A BotTour vai criar o melhor roteiro de viagens da sua vida...')
        return inputs

    @after_kickoff
    def after_kickoff_function(self, result):
        print('Se prepare para boas experiências no seu destino...')
        return result

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents, 
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )