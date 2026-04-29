"""
Travel Agent — LangChain agent with Amadeus tool integrations.
"""


class TravelAgent:
    """Main travel planning agent."""

    def __init__(self):
        # TODO: init LangChain graph, tools, LLM
        pass

    async def process_message(self, message: str, conversation_id: int) -> dict:
        # TODO: route to appropriate tool, return response
        return {"role": "agent", "content": "Not implemented yet."}
