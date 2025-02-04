from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage
#from langchain_core import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from config import Config


# openai_llm = ChatOpenAI(api_key = Config.OPEN_API_KEY, model="gpt-4o-mini")
# groq_llm = ChatGroq(groq_api_key=Config.GROQ_API_KEY, model="llama-3.3-70b-versatile")

#search_tool = TavilySearchResults(api_key=Config.TAVIILY_API_KEY,max_results=2)
system_prompt = "Act as an AI chatbot who is smart and frindly"

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    if provider == 'Groq':
        llm = ChatGroq(groq_api_key=Config.GROQ_API_KEY, model=llm_id)
    elif (provider == "OpenAI"):
        llm = ChatOpenAI(api_key = Config.OPEN_API_KEY, model=llm_id)

    tools = [TavilySearchResults(api_key=Config.TAVIILY_API_KEY,max_results=2)] if allow_search else []

    agent = create_react_agent(
        model = llm,
        tools=tools,
        state_modifier = system_prompt
    )

    #query = "tell me about the trends in crypto market"

    state={"messages": query}
    response = agent.invoke(state)
    messages = response.get("messages")
    ai_message = [message.content for message in messages if isinstance(message, AIMessage)]
    #print(ai_message[-1])
    return ai_message[-1]