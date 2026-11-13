"""
IBM watsonx.ai (Granite) client wrapper.
Handles authentication and text generation using IBM Granite models.
"""
import os
from dotenv import load_dotenv
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

load_dotenv()

_client: ModelInference | None = None


def _get_client() -> ModelInference:
    global _client
    if _client is not None:
        return _client

    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

    if not api_key or not project_id:
        raise EnvironmentError(
            "Missing WATSONX_API_KEY or WATSONX_PROJECT_ID in environment. "
            "Copy .env.example to .env and fill in your IBM Cloud credentials."
        )

    credentials = Credentials(url=url, api_key=api_key)
    _client = ModelInference(
        model_id="ibm/granite-4-h-small",
        credentials=credentials,
        project_id=project_id,
        params={
            GenParams.MAX_NEW_TOKENS: 1024,
            GenParams.TEMPERATURE: 0.7,
            GenParams.TOP_P: 0.9,
            GenParams.REPETITION_PENALTY: 1.1,
        },
    )
    return _client


def generate_text(prompt: str, max_tokens: int = 1024) -> str:
    """Generate text using IBM Granite via watsonx.ai."""
    client = _get_client()
    response = client.generate_text(
        prompt=prompt,
        params={GenParams.MAX_NEW_TOKENS: max_tokens},
    )
    return response.strip()
