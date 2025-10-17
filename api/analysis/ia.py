import json

import httpx

from core.env import env_config

from ..models import HttpAgentAIDecision, HttpAgentRequestContext


def ia(context: HttpAgentRequestContext) -> HttpAgentAIDecision | None:
    if not env_config.openrouter_api_key:
        return

    system_prompt = f"""
        You are a cybersecurity analyst.
        Always respond ONLY with a valid JSON object that strictly follows this schema:
        {HttpAgentAIDecision.model_json_schema()}
        Do not add any explanations, comments, or code blocks. Only return the JSON object.
        """

    user_prompt = f"""
        Analyze the following HTTP request context and provide your response in the specified JSON format:
        context: {context.model_dump()}
        """

    with httpx.Client(timeout=60) as client:
        response = client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {env_config.openrouter_api_key}",
                "Content-Type": "application/json",
            },
            json=dict(
                model="openai/gpt-4o-mini",
                messages=[
                    dict(role="system", content=system_prompt),
                    dict(role="user", content=user_prompt),
                ],
            ),
        )

        if not response.status_code == 200:
            return

        data = response.json()
        analysis_text = data["choices"][0]["message"]["content"]

        return HttpAgentAIDecision(**json.loads(analysis_text))


if __name__ == "__main__":
    pass
