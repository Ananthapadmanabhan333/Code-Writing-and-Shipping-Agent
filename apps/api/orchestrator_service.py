import os
import asyncio
from typing import Dict, Any, List
from packages.agents.llm_agents import ProductManager, TechLead, CodingAgent, DebuggingAgent
from packages.sandbox.executor import SandboxExecutor

class AutonomousEngine:
    def __init__(self):
        self.pm = ProductManager()
        self.tl = TechLead()
        self.coder = CodingAgent()
        self.debugger = DebuggingAgent()
        self.sandbox = SandboxExecutor()

    async def run_project(self, requirements: str, project_id: str):
        # 1. Analyze Requirements
        print(f"[{project_id}] PM: Analyzing requirements...")
        specs = self.pm.analyze_requirements(requirements)
        
        # 2. Plan Architecture
        print(f"[{project_id}] TL: Planning architecture...")
        architecture = self.tl.plan_architecture(specs)
        
        # 3. Task Execution Loop
        for task in specs.tasks:
            print(f"[{project_id}] Coder: Working on task {task.title}...")
            code = self.coder.generate_code(task, str(architecture))
            
            # Save code to temporary directory
            workdir = f"./temp/{project_id}/{task.id}"
            os.makedirs(workdir, exist_ok=True)
            with open(f"{workdir}/main.py", "w") as f:
                f.write(code)
            
            # 4. Run & Debug Loop
            success = False
            retries = 0
            while not success and retries < 3:
                print(f"[{project_id}] Sandbox: Running task {task.title} (Attempt {retries + 1})...")
                result = self.sandbox.run_command("python main.py", workdir)
                
                if result["status"] == "success":
                    print(f"[{project_id}] Task {task.title} PASSED.")
                    success = True
                else:
                    print(f"[{project_id}] Task {task.title} FAILED. Debugging...")
                    logs = result.get("logs", "")
                    fixed_code = self.debugger.debug_failure(task, logs, code)
                    with open(f"{workdir}/main.py", "w") as f:
                        f.write(fixed_code)
                    code = fixed_code
                    retries += 1
            
            if not success:
                print(f"[{project_id}] Task {task.title} failed after {retries} retries.")

        print(f"[{project_id}] Project Execution Complete.")
