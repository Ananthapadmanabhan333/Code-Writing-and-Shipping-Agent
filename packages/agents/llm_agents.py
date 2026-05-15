import os
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

class Task(BaseModel):
    id: str = Field(description="Unique ID for the task")
    title: str = Field(description="Title of the task")
    description: str = Field(description="Detailed description of what needs to be done")
    assigned_to: str = Field(description="Agent type to assign the task to (frontend, backend, devops)")
    dependencies: List[str] = Field(default_factory=list, description="IDs of tasks this task depends on")

class ProjectSpecs(BaseModel):
    name: str
    architecture: str
    tech_stack: List[str]
    tasks: List[Task]

class LLMAgent:
    def __init__(self, model_name: str = "gpt-4-turbo-preview"):
        self.llm = ChatOpenAI(model=model_name, temperature=0)

class ProductManager(LLMAgent):
    def analyze_requirements(self, requirements: str) -> ProjectSpecs:
        prompt = ChatPromptTemplate.from_template(
            "You are a world-class Product Manager. Analyze the following product requirements "
            "and create a detailed technical specification and a list of decomposed tasks.\n\n"
            "Requirements: {requirements}\n\n"
            "Output the result in JSON format matching the schema."
        )
        parser = JsonOutputParser(pydantic_object=ProjectSpecs)
        chain = prompt | self.llm | parser
        return chain.invoke({"requirements": requirements})

class TechLead(LLMAgent):
    def plan_architecture(self, specs: ProjectSpecs) -> Dict[str, Any]:
        prompt = ChatPromptTemplate.from_template(
            "You are an Elite Software Architect. Review the following project specifications "
            "and design a robust system architecture.\n\n"
            "Specifications: {specs}\n\n"
            "Provide detailed architecture components, data flow, and infrastructure requirements."
        )
        chain = prompt | self.llm
        return chain.invoke({"specs": specs.json()})

class CodingAgent(LLMAgent):
    def __init__(self, model_name: str = "gpt-4-turbo-preview", tools=None):
        super().__init__(model_name)
        self.tools = tools
        if tools:
            self.llm = self.llm.bind_tools(tools)

    def generate_code(self, task: Task, context: str) -> str:
        prompt = ChatPromptTemplate.from_template(
            "You are a Senior Software Engineer. Implement the following task.\n\n"
            "Task: {task_title}\n"
            "Description: {task_desc}\n"
            "Context: {context}\n\n"
            "Generate the full source code for this task. Include necessary imports and comments."
        )
        chain = prompt | self.llm
        # For simplicity, we still return the content, but it could call tools if bound
        response = chain.invoke({
            "task_title": task.title,
            "task_desc": task.description,
            "context": context
        })
        return response.content if hasattr(response, 'content') else str(response)

class DebuggingAgent(LLMAgent):
    def debug_failure(self, task: Task, logs: str, code: str) -> str:
        prompt = ChatPromptTemplate.from_template(
            "You are an Expert Debugging Agent. A task failed during execution.\n\n"
            "Task: {task_title}\n"
            "Logs: {logs}\n"
            "Code: {code}\n\n"
            "Identify the root cause and provide a corrected version of the code."
        )
        chain = prompt | self.llm
        return chain.invoke({
            "task_title": task.title,
            "logs": logs,
            "code": code
        }).content
