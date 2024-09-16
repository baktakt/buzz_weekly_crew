import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_groq import ChatGroq
from buzz_weekly_crew.tools.social_tools import SocialTools
from buzz_weekly_crew.tools.browser_tools import BrowserTools
from crewai_tools import DallETool

# Use a constant for the LLM configuration
LLM = ChatGroq(
    temperature=1.5, 
    groq_api_key=os.getenv('GROQ_API_KEY'), 
    model_name=os.getenv('GROQ_MODEL_NAME')
)

# Use a constant for the DALL-E tool configuration
DALLE_TOOL = DallETool(model="dall-e-3", size="1792x1024", quality="hd", n=1)

@CrewBase
class BuzzWeeklyCrew():
	"""LlmCrew crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	def _create_agent(self, config_key, tools=None):
		"""Helper method to create agents with common configuration"""
		return Agent(
			config=self.agents_config[config_key],
			tools=tools,
			allow_delegation=False,
			verbose=True,
			llm=LLM,
		)

	def _create_task(self, config_key, agent, output_file):
		"""Helper method to create tasks with common configuration"""
		return Task(
			config=self.tasks_config[config_key],
			agent=agent,
			output_file=output_file
		)

	@agent
	def news_researcher(self) -> Agent:
		return self._create_agent('news_researcher', [BrowserTools.get_articles_from_feeds])
	
	@agent
	def editor(self) -> Agent:
		return self._create_agent('editor')
	
	@agent
	def formatter(self) -> Agent:
		return self._create_agent('formatter')
	
	@agent
	def publisher(self) -> Agent:
		return self._create_agent('publisher', [SocialTools.create_medium_draft_post])
	
	@agent
	def image_creator(self) -> Agent:
		return self._create_agent('image_creator', [DALLE_TOOL])

	@task
	def extract_articles_task(self) -> Task:
		return self._create_task('extract_articles_task', self.news_researcher(), 'generated/extracted_articles.json')
	
	@task
	def select_articles_task(self) -> Task:
		return self._create_task('select_articles_task', self.editor(), 'generated/selected_articles.json')
	
	@task
	def create_image_task(self) -> Task:
		return self._create_task('create_image_task', self.image_creator(), 'generated/image-url.txt')
	
	@task
	def format_task(self) -> Task:
		return self._create_task('format_task', self.formatter(), 'generated/final_result.md')
	
	@task
	def create_medium_draft_task(self) -> Task:
		return self._create_task('create_medium_draft_task', self.publisher(), 'generated/result_from_medium_create_post.txt')

	@crew
	def crew(self) -> Crew:
		"""Creates the LlmCrew crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			output_log_file="generated/log.txt",
			planning=True
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
