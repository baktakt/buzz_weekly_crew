import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_community.llms import Ollama
from langchain_groq import ChatGroq
from buzz_weekly_crew.tools.social_tools import SocialTools
from buzz_weekly_crew.tools.browser_tools import BrowserTools
from crewai_tools import DallETool


'''
llm = Ollama(
    model = os.getenv('OPENAI_MODEL_NAME'),
    base_url = os.getenv('OPENAI_API_BASE'), temperature=0.2)

'''
llm = ChatGroq(
		temperature=1.5, 
		groq_api_key = os.getenv('GROQ_API_KEY'), 
		model_name=os.getenv('GROQ_MODEL_NAME')
	)

dalle_tool = DallETool(model="dall-e-3",
                       size="1792x1024",
                       quality="hd",
                       n=1)
    
# Uncomment the following line to use an example of a custom tool
# from buzz_weekly.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class BuzzWeeklyCrew():
	"""LlmCrew crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def news_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['news_researcher'],
			tools=[BrowserTools.get_articles_from_feeds],
			allow_delegation=False,
			verbose=True,
#			llm=llm,
		)
	
	@agent
	def editor(self) -> Agent:
		return Agent(
			config=self.agents_config['editor'],
			allow_delegation=False,
			verbose=True,
#			llm=llm,
		)
	
	@agent
	def formatter(self) -> Agent:
		return Agent(
			config=self.agents_config['formatter'],
			allow_delegation=False,
			verbose=True,
#			llm=llm,
		)
	
	@agent
	def publisher(self) -> Agent:
		return Agent(
			config=self.agents_config['publisher'],
			tools=[SocialTools.create_medium_draft_post],
			allow_delegation=False,
			verbose=True,
#			llm=llm,
		)
	
	@agent
	def image_creator(self) -> Agent:
		return Agent(
			config=self.agents_config['image_creator'],
			tools=[dalle_tool],
			allow_delegation=False,
			verbose=True,
#			llm=llm,
		)

	@task
	def extract_articles_task(self) -> Task:
		return Task(
			config=self.tasks_config['extract_articles_task'],
			agent=self.news_researcher(),
			output_file='generated/extracted_articles.json'
		)
	
	@task
	def select_articles_task(self) -> Task:
		return Task(
			config=self.tasks_config['select_articles_task'],
			agent=self.editor(),
			output_file='generated/selected_articles.json'
		)
	
	@task
	def create_image_task(self) -> Task:
		return Task(
			config=self.tasks_config['create_image_task'],
			agent=self.image_creator(),
			output_file='generated/image-url.txt'
		)
	
	@task
	def format_task(self) -> Task:
		return Task(
			config=self.tasks_config['format_task'],
			agent=self.formatter(),
			output_file='generated/final_result.md'
		)
	
	@task
	def create_medium_draft_task(self) -> Task:
		return Task(
			config=self.tasks_config['create_medium_draft_task'],
			agent=self.publisher(),
			output_file='generated/result_from_medium_create_post.txt'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the LlmCrew crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
