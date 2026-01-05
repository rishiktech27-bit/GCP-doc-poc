from fastapi import FastAPI
from adk.evaluation import EvalTask
from agents.root_agent import claim_xpert_root # Import your actual agent object

app = FastAPI()

@app.get("/run-evals")
async def get_evaluation_results():
    # 1. Initialize the EvalTask
    # Ensure the paths point to your actual local files
    task = EvalTask(
        agent=claim_xpert_root, 
        eval_set_path="evals/evalset.json",
        config_path="evals/test_config.json"
    )

    # 2. Run the evaluation
    # Note: Depending on your ADK version, you might use run() or evaluate()
    results = task.run() 

    # 3. Return the JSON to your frontend
    # .to_json() usually returns a string; FastAPI needs a dict to auto-convert to JSON
    import json
    return json.loads(results.to_json())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)