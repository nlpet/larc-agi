import openai
import os
from typing import Optional


class OpenAIModel:
    def solve_dummy(self, prompt: str):
        return "The correct answer is [C]"

    def solve(
        self, prompt: str, model: str = "gpt-3.5", max_tokens: int = 32
    ) -> Optional[str]:
        """
        Send a prompt to the specified OpenAI model and return the response.

        Args:
        prompt (str): The input prompt to send to the model.
        model (str): The model to use. Defaults to "gpt-4".
        max_tokens (int): The maximum number of tokens in the response. Defaults to 150.

        Returns:
        Optional[str]: The model's response, or None if an error occurred.
        """
        # Ensure the API key is set
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
            )

        openai.api_key = api_key

        try:
            response = openai.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                n=1,
                stop=None,
                temperature=0,
            )

            # Extract the response text
            response_text = response.choices[0].message["content"].strip()
            return response_text

        except openai.error.OpenAIError as e:
            print(f"An error occurred while querying the OpenAI API: {str(e)}")
            return None
