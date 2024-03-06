import json

from autogenstudio import AgentWorkFlowConfig, AutoGenWorkFlowManager

# load an agent specification in JSON
agent_spec = json.load(open("Python Workflow.json"))
# Create an AutoGen Workflow Configuration from the agent specification
agent_work_flow_config = AgentWorkFlowConfig(**agent_spec)

# Create a Workflow from the configuration
agent_work_flow = AutoGenWorkFlowManager(agent_work_flow_config)

# Run the workflow on a task
task_query = "Create a function that takes in a file, and then counts how many characters it has."
agent_work_flow.run(message=task_query)