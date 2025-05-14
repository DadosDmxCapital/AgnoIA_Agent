"""
Gemini Tool for the Agno AI agent.
This tool provides access to Google's Gemini API for text generation.
"""

import os
import json
import requests
from typing import Optional, Dict, Any, List

import config

class GeminiTool:
    """
    Tool for interacting with Google's Gemini API.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the Gemini tool.

        Args:
            api_key: Gemini API key. If not provided, will use the one from config.
            model: Gemini model to use. If not provided, will use the default from config.
        """
        self.api_key = api_key or config.GEMINI_API_KEY
        self.model = model or config.DEFAULT_GEMINI_MODEL
        self.base_url = f"https://generativelanguage.googleapis.com/v1/models/{self.model}"
    
    def generate_text(self, prompt: str, system_prompt: Optional[str] = None, 
                     max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """
        Generate text using the Gemini API.

        Args:
            prompt: The prompt to generate text from
            system_prompt: Optional system prompt to provide context
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for text generation (0.0 to 1.0)

        Returns:
            Generated text
        """
        try:
            # Construct the API endpoint URL with the API key
            endpoint = f"{self.base_url}:generateContent?key={self.api_key}"
            
            # Prepare the request payload
            payload = {
                "contents": []
            }
            
            # Add system prompt if provided
            if system_prompt:
                payload["contents"].append({
                    "role": "system",
                    "parts": [{"text": system_prompt}]
                })
            
            # Add user prompt
            payload["contents"].append({
                "role": "user",
                "parts": [{"text": prompt}]
            })
            
            # Add generation parameters
            payload["generationConfig"] = {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
                "topP": 0.95,
                "topK": 40
            }
            
            # Make the API request
            response = requests.post(
                endpoint,
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload)
            )
            
            # Check if the request was successful
            if response.status_code == 200:
                response_data = response.json()
                
                # Extract the generated text from the response
                if "candidates" in response_data and len(response_data["candidates"]) > 0:
                    candidate = response_data["candidates"][0]
                    if "content" in candidate and "parts" in candidate["content"]:
                        parts = candidate["content"]["parts"]
                        if len(parts) > 0 and "text" in parts[0]:
                            return parts[0]["text"]
                
                # If we couldn't extract the text in the expected format
                return f"Error: Unexpected response format: {response_data}"
            else:
                # Handle API errors
                error_message = f"API Error ({response.status_code}): {response.text}"
                print(error_message)
                return f"Error: Failed to generate text. {error_message}"
                
        except Exception as e:
            # Handle any exceptions
            error_message = f"Exception: {str(e)}"
            print(error_message)
            return f"Error: {error_message}"
    
    def list_models(self) -> List[Dict[str, Any]]:
        """
        List available Gemini models.

        Returns:
            List of available models
        """
        try:
            # Construct the API endpoint URL with the API key
            endpoint = f"https://generativelanguage.googleapis.com/v1/models?key={self.api_key}"
            
            # Make the API request
            response = requests.get(endpoint)
            
            # Check if the request was successful
            if response.status_code == 200:
                response_data = response.json()
                
                # Extract the models from the response
                if "models" in response_data:
                    return response_data["models"]
                
                # If we couldn't extract the models in the expected format
                return []
            else:
                # Handle API errors
                error_message = f"API Error ({response.status_code}): {response.text}"
                print(error_message)
                return []
                
        except Exception as e:
            # Handle any exceptions
            error_message = f"Exception: {str(e)}"
            print(error_message)
            return []
