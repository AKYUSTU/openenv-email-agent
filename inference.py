from fastapi import FastAPI
from pydantic import BaseModel
from env.environment import EmailEnv

app = FastAPI()

env = EmailEnv("easy")  # default

# ------------------ MODELS ------------------

class ActionModel(BaseModel):
    action_type: str
    category: str = None
    priority: str = None
    response: str = None

# ------------------ OPENENV ENDPOINTS ------------------

@app.post("/reset")
def reset():
    obs = env.reset()
    return {
        "observation": obs,
        "reward": 0.0,
        "done": False,
        "info": {}
    }

@app.post("/step")
def step(action: ActionModel):
    obs, reward, done, info = env.step(action.dict())
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    return env.state()

# ------------------ HEALTH CHECK ------------------

@app.get("/")
def root():
    return {"status": "running"}
