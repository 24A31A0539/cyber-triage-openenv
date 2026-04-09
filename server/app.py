
from fastapi import FastAPI, Depends, Request
from env import Environment
from models import Action, Observation
import json

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Cyber Sec OpenEnv")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In a multi-user environment, we would use sessions.
# For this script we will use a global singleton for simplicity.
global_env = Environment()

@app.get("/")
def read_root():
    return {"message": "OpenEnv Cybersecurity Triage running"}

@app.post("/reset")
async def reset_env(request: Request):
    # To parse task from kwargs if passed
    try:
        data = await request.json()
        task = data.get("task", "easy")
    except:
        task = "easy"
        
    obs = global_env.reset(task)
    return {"observation": obs.model_dump(), "info": {}}

@app.post("/step")
def step_env(action: Action):
    result = global_env.step(action)
    return result

@app.get("/state")
def get_state():
    return global_env.state()

def main():
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
