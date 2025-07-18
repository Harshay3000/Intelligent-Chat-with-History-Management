import json
import os
from typing import List, Dict, Any, Optional
from langchain_core.memory import BaseMemory
from langchain_core.messages import BaseMessage
from langchain_core.messages import HumanMessage, AIMessage
from pydantic import Field
from langchain_core.language_models import BaseLLM # Import BaseLLM for type hinting

MAX_HISTORY =   20

class JSONMemory(BaseMemory):
    memory_file: str = Field(default="memory.json", description="Path to the memory JSON file.")
    chat_memory: List[Any] = Field(default_factory=list)
    llm: BaseLLM # Add an LLM instance for summarization
    summarize_threshold: int = Field(default=500, description="Character length threshold for summarization.")

    def __init__(self, memory_file: Optional[str] = "memory.json",llm: BaseLLM = None, summarize_threshold: int = 500, **kwargs):
        if llm is None:
            raise ValueError("An LLM instance must be provided for summarization.")
        super().__init__(memory_file=memory_file,llm=llm, summarize_threshold=summarize_threshold, **kwargs)
        self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as f:
                try:
                    data = json.load(f)
                    self.chat_memory = []
                    for item in data:
                        if "human" in item:
                            self.chat_memory.append(HumanMessage(content=item["human"]))
                        elif "ai" in item:
                            self.chat_memory.append(AIMessage(content=item["ai"]))
                    self.chat_memory = self.chat_memory[-MAX_HISTORY:]
                except json.JSONDecodeError:
                    self.chat_memory = []
                except Exception as e:
                    print(f"Error loading memory file {self.memory_file}: {e}")
                    self.chat_memory = []
        else:
            self.chat_memory = []

    def _save_memory(self):
        serializable_memory = []
        for m in self.chat_memory:
            if isinstance(m, HumanMessage):
                serializable_memory.append({"human": m.content})
            elif isinstance(m, AIMessage):
                serializable_memory.append({"ai": m.content})
        with open(self.memory_file, "w") as f:
            json.dump(serializable_memory, f, indent=4)

        
    @property
    def memory_variables(self) -> List[str]:
        return ["history"]

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        return {"history": self.chat_memory}

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, Any]) -> None:
        user_message = inputs.get("input")
        ai_response = outputs.get("response") 
        if user_message:
            self.chat_memory.append(HumanMessage(content=user_message))
        
        if ai_response:
            processed_ai_response = ai_response
            # Check summarization 
            if len(ai_response) > self.summarize_threshold:
                print(f"AI response length ({len(ai_response)}) exceeds summarization threshold ({self.summarize_threshold}). Summarizing...")
                summarize_prompt = f"Please summarize the following text concisely:\n\n{ai_response}"
                try:
                   
                    summary_message = self.llm.invoke([HumanMessage(content=summarize_prompt)])
                    processed_ai_response = summary_message.content
                    print("Summary generated successfully.")
                except Exception as e:
                    print(f"Error during summarization: {e}. Saving original response.")
                    # response if summarization fails
                    processed_ai_response = ai_response
            
            self.chat_memory.append(AIMessage(content=processed_ai_response))
        
        self.chat_memory = self.chat_memory[-MAX_HISTORY:]
        self._save_memory()

    def clear(self) -> None:
        self.chat_memory = []
        self._save_memory()
    
    @property
    def messages(self) -> List[BaseMessage]:
        return self.chat_memory
    

    def add_messages(self, messages: List[BaseMessage]) -> None:
            self.chat_memory.extend(messages)
            self.chat_memory = self.chat_memory[-MAX_HISTORY:]  # Keep last N messages
            self._save_memory()
