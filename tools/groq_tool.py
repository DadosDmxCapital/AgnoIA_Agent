"""
Groq integration tool for the Agno AI agent.
This module provides a tool for interacting with Groq's LLM API.
"""

from typing import Dict, Any, Optional, List
import requests
import json

import config

# Check if groq is available
try:
    import groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    print("Warning: groq library not available. Using fallback HTTP requests.")

class GroqTool:
    """Tool for interacting with Groq's LLM API."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the Groq tool.

        Args:
            api_key: Groq API key. If not provided, will use the one from config.
            model: Groq model to use. If not provided, will use the default from config.
        """
        self.api_key = api_key or config.GROQ_API_KEY
        self.model = model or config.DEFAULT_GROQ_MODEL

        # Always use the fallback method for better compatibility
        self.client = None

    def generate_text(self,
                     prompt: str,
                     max_tokens: int = 1000,
                     temperature: float = 0.7,
                     system_prompt: Optional[str] = None) -> str:
        """
        Generate text using Groq's LLM API.

        Args:
            prompt: The user prompt to send to the model
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for text generation (0.0 to 1.0)
            system_prompt: Optional system prompt to set context

        Returns:
            Generated text as a string
        """
        messages = []

        # Add system prompt if provided
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        # Add user prompt
        messages.append({"role": "user", "content": prompt})

        try:
            if GROQ_AVAILABLE and self.client:
                # Use the groq library if available
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )

                return response.choices[0].message.content
            else:
                # Fallback to direct API calls
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }

                payload = {
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature
                }

                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json=payload
                )

                if response.status_code == 200:
                    return response.json()["choices"][0]["message"]["content"]
                else:
                    return f"Error: API returned status code {response.status_code}: {response.text}"

        except Exception as e:
            return f"Error generating text with Groq: {str(e)}"

    def get_available_models(self) -> List[str]:
        """
        Get a list of available models from Groq.

        Returns:
            List of model names
        """
        try:
            if GROQ_AVAILABLE and self.client:
                # Use the groq library if available
                models = self.client.models.list()
                return [model.id for model in models.data]
            else:
                # Fallback to direct API calls
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }

                response = requests.get(
                    "https://api.groq.com/openai/v1/models",
                    headers=headers
                )

                if response.status_code == 200:
                    return [model["id"] for model in response.json()["data"]]
                else:
                    print(f"Error: API returned status code {response.status_code}: {response.text}")
                    return ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"]
        except Exception as e:
            print(f"Error fetching models from Groq: {str(e)}")
            # Return some default models
            return ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"]
