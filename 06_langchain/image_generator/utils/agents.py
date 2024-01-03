from utils.custom_tools import ImageGeneratorTool
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI


def image_generator_agent():
    tools=[ImageGeneratorTool()]

    return initialize_agent(agent=AgentType.OPENAI_FUNCTIONS,
                            tools=tools,
                            llm=ChatOpenAI(temperature=0, model='gpt-3.5-turbo', request_timeout=120),
                            max_iterations=1,
                            verbose=True,
                            )


