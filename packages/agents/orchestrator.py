from typing import Annotated, Any, Dict, List, Sequence, TypedDict, Union
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from packages.agents.llm_agents import ProductManager, TechLead, CodingAgent, DebuggingAgent, Task, ProjectSpecs

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], "The messages in the conversation"]
    next_agent: str
    project_specs: ProjectSpecs
    architecture: Dict[str, Any]
    tasks: List[Task]
    current_task_id: str
    repository_path: str
    logs: List[str]

# Initialize Agents
pm = ProductManager()
tl = TechLead()
coder = CodingAgent()
debugger = DebuggingAgent()

def product_manager_node(state: AgentState):
    print("--- PM NODE ---")
    requirements = state["messages"][-1].content
    specs = pm.analyze_requirements(requirements)
    return {
        "project_specs": specs,
        "tasks": specs.tasks,
        "messages": [HumanMessage(content=f"PM analyzed requirements and created {len(specs.tasks)} tasks.")],
        "next_agent": "tech_lead"
    }

def tech_lead_node(state: AgentState):
    print("--- TL NODE ---")
    specs = state["project_specs"]
    architecture = tl.plan_architecture(specs)
    return {
        "architecture": architecture,
        "messages": [HumanMessage(content="TL designed the system architecture.")],
        "next_agent": "coding"
    }

def coding_node(state: AgentState):
    print("--- CODING NODE ---")
    tasks = [t for t in state["tasks"] if t.id not in [msg.additional_kwargs.get("completed_task_id") for msg in state["messages"]]]
    if not tasks:
        return {"next_agent": END}
    
    task = tasks[0]
    code = coder.generate_code(task, str(state["architecture"]))
    
    # In a real system, we'd write to disk here
    msg = HumanMessage(content=f"Coder implemented task: {task.title}")
    msg.additional_kwargs["completed_task_id"] = task.id
    
    return {
        "messages": [msg],
        "next_agent": "coding" if len(tasks) > 1 else "end"
    }

# Build Graph
workflow = StateGraph(AgentState)
workflow.add_node("pm", product_manager_node)
workflow.add_node("tl", tech_lead_node)
workflow.add_node("coding", coding_node)

workflow.set_entry_point("pm")
workflow.add_edge("pm", "tl")
workflow.add_edge("tl", "coding")
workflow.add_conditional_edges(
    "coding",
    lambda x: x["next_agent"],
    {
        "coding": "coding",
        "end": END
    }
)

graph = workflow.compile()
