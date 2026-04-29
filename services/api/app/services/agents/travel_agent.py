"""
Travel Agent — LangChain agent with travel search tool integrations.

Uses LangGraph for multi-step reasoning:
1. Parse user intent
2. Determine which tools to call
3. Format results as rich cards for the UI
"""

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from app.config import settings
from app.services.agents.tools import get_travel_tools


class TravelAgent:
    """Main travel planning agent."""

    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.llm_model,
            api_key=settings.openai_api_key,
            temperature=0.3,
        )
        self.tools = get_travel_tools()
        self.graph = create_react_agent(self.llm, self.tools)

    async def process_message(self, message: str, conversation_id: int) -> dict:
        """
        Process a user message through the agent.

        Returns:
            dict with role, content, and optional metadata for rich cards
        """
        try:
            response = await self.graph.ainvoke({
                "messages": [("user", message)]
            })

            # Extract the agent's final response
            ai_message = response["messages"][-1]
            content = ai_message.content

            # Detect if response contains search results for rich cards
            metadata = self._extract_card_metadata(content)

            return {
                "role": "agent",
                "content": content,
                "metadata": metadata,
            }
        except Exception as e:
            return {
                "role": "agent",
                "content": f"I'm having trouble connecting right now. Please try again in a moment. ({str(e)})",
                "metadata": None,
            }

    def _extract_card_metadata(self, content: str) -> dict | None:
        """Parse agent response to detect structured data for rich cards."""
        # TODO: Use structured output parsing to extract flight/hotel cards
        # For now, return None (plain text response)
        return None
