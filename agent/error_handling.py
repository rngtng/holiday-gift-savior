"""Error handling utilities for graceful degradation when models are overloaded."""

import logging
from typing import AsyncGenerator, Any
from google.adk.agents import LlmAgent
from google.genai.errors import ServerError

logger = logging.getLogger(__name__)


class GracefulErrorAgent(LlmAgent):
    """
    Wrapper around LlmAgent that catches model overload errors and returns user-friendly messages.

    This agent catches 503 UNAVAILABLE errors from the Gemini API and converts them
    into graceful user-facing messages instead of showing stack traces.
    """

    async def run_async(self, *args, **kwargs) -> AsyncGenerator[Any, None]:
        """
        Override run_async to catch and handle ServerError exceptions gracefully.

        Yields:
            Events from the underlying agent, or an error message event if the model is overloaded
        """
        try:
            async for event in super().run_async(*args, **kwargs):
                yield event
        except ServerError as e:
            # Check if this is a model overload error (503)
            if e.status_code == 503:
                logger.warning(f"Model overloaded (503): {e}")
                # Create a user-friendly error message event
                error_message = (
                    "🎁 I'm sorry, but I'm experiencing high demand right now and can't process your request. "
                    "The Holiday Gift Savior is very popular today! ✨\n\n"
                    "Please try again in a few moments. Your gift recommendations will be worth the wait! 🎄"
                )

                # Yield a text event similar to what the agent would normally produce
                from google.genai.types import Part, Content
                from google.adk.events import Event

                yield Event(
                    content=Content(
                        parts=[Part(text=error_message)],
                        role="model"
                    ),
                    author="agent"
                )
            else:
                # Re-raise other ServerError types
                logger.error(f"ServerError (non-503): {e}", exc_info=True)
                raise
        except Exception as e:
            # Log unexpected errors but still try to provide a graceful message
            logger.error(f"Unexpected error in agent: {type(e).__name__}: {e}", exc_info=True)

            # Provide a generic error message
            error_message = (
                "🎁 I apologize, but I encountered an unexpected issue while processing your request. "
                "Please try again or contact support if the problem persists."
            )

            from google.genai.types import Part, Content
            from google.adk.events import Event

            yield Event(
                content=Content(
                    parts=[Part(text=error_message)],
                    role="model"
                ),
                author="agent"
            )


def create_graceful_agent(agent_class=LlmAgent, **kwargs) -> GracefulErrorAgent:
    """
    Factory function to create an agent with graceful error handling.

    Args:
        agent_class: The base agent class to wrap (default: LlmAgent)
        **kwargs: Arguments to pass to the agent constructor

    Returns:
        A GracefulErrorAgent instance with the specified configuration
    """
    # Create the agent using GracefulErrorAgent which inherits from LlmAgent
    return GracefulErrorAgent(**kwargs)
