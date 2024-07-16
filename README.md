# News Crew

Welcome to the Buzz Weekly Crew project, powered by [crewAI](https://crewai.com).

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [Poetry](https://python-poetry.org/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install Poetry:

```bash
pip install poetry
```

Next, navigate to your project directory and install the dependencies:

1. First lock the dependencies and then install them:
```bash
poetry lock
```
```bash
poetry install
```
### Customizing

** Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/buzz_weekly_crew/config/agents.yaml` to define your agents
- Modify `src/buzz_weekly_crew/config/tasks.yaml` to define your tasks
- Modify `src/buzz_weekly_crew/crew.py` to add your own logic, tools and specific args
- Modify `src/buzz_weekly_crew/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
poetry run buzz_weekly_crew
```

This command initializes the crew, assembling the agents and assigning them tasks as defined in your configuration.

## Understanding Your Crew

The crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding CrewAI.
- Visit the [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join the Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with the CrewAI docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
