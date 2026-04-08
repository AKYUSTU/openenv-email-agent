from fastapi import FastAPI
from pydantic import BaseModel
from env.environment import EmailEnv

app = FastAPI()

env = EmailEnv("easy")

# ------------------ MODELS ------------------

class ActionModel(BaseModel):
    action_type: str
    category: str = None
    priority: str = None
    response: str = None

# ------------------ OPENENV API ------------------

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

@app.get("/")
def root():
    return {"status": "running"}

# ------------------ BASELINE SCRIPT ------------------

def run_baseline():
    print("[START]")

    for task in ["easy", "medium", "hard"]:
        print(f"[STEP] Running {task}")

        env = EmailEnv(task)
        obs = env.reset()

        total_reward = 0
        done = False

        while not done:
            action = {
                "action_type": "reply",
                "category": "support",
                "priority": "high",
                "response": "We are looking into your issue."
            }

            obs, reward, done, info = env.step(action)
            total_reward += reward

        print(f"[STEP] Score: {total_reward}")

    print("[END]")

# IMPORTANT: only runs locally, not in HF server
if __name__ == "__main__":
    run_baseline()
