
from langchain_core.language_models import BaseLLM
from langchain_core.outputs import LLMResult
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from typing import List, Optional
import requests
from config import GROQ_API_KEY, GROQ_ENDPOINT


class GrokLLM(BaseLLM):
    model: str = "llama-3.3-70b-versatile"
    temperature: float = 0.7
    grok_api_key: str = GROQ_API_KEY
    grok_endpoint: str = GROQ_ENDPOINT
    
    def _generate(       
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs
    ) -> LLMResult:
        completions = []

        for prompt in prompts:
            headers = {
                "Authorization": f"Bearer {self.grok_api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": self.model,
                "temperature": self.temperature,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }

            response = requests.post(self.grok_endpoint, headers=headers, json=data)

            try:
        
                res_json = response.json()
                print("Grok raw response:", res_json)  
                if "response" in res_json:
                    result = res_json["response"]
                elif "choices" in res_json:
                    result = res_json["choices"][0]["message"]["content"]
                else:
                    result = "[ERROR] Unexpected response format"
                #result = result.strip().split("\n\n")[0]
     
            except Exception as e:
                 result = f"[ERROR parsing JSON]: {str(e)}"
            completions.append(result)

        return LLMResult(generations=[[{"text": c}] for c in completions])

    @property
    def _llm_type(self) -> str:
        return "grok"

