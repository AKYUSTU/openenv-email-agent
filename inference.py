import os
import json
import threading
from fastapi import FastAPI
from openai import OpenAI
from env.environment import EmailEnv

# ✅ SAFE ENV VARIABLES (prevents crash)
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
API_KEY = os.environ.get("API_KEY", "dummy")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o-mini")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

app = FastAPI()

# 🔥 SAFE LLM FUNCTION (NO CRASH + API CALL ALWAYS ATTEMPTED)
def get_llm_action(obs):
    history_text = "\n".join(obs.get("history", []))

    prompt = f"""
    Classify this email and respond in JSON.

    Subject: {obs.get('subject', '')}
    Body: {obs.get('body', '')}

    Return JSON:
    {{
        "action_type": "...",
        "category": "...",
        "priority": "...",
        "response": "..."
    }}
    """

    action = {}

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.choices[0].message.content

        try:
            action = json.loads(text)
        except:
            action = {}

    except Exception as e:
        print("[STEP] API ERROR:", str(e))

    return {
        "action_type": action.get("action_type", "reply"),
        "category": action.get("category", "support"),
        "priority": action.get("priority", "medium"),
        "response": action.get("response", "Processing your request.")
    }

# 🚀 MAIN ENV EXECUTION
def run_env():
    print("[START]")

    try:
        for task in ["easy", "medium", "hard"]:
            print(f"[STEP] Running {task}")

            env = EmailEnv(task)
            obs = env.reset()

            total_reward = 0
            done = False

            while not done:
                action = get_llm_action(obs)
                obs, reward, done, _ = env.step(action)
                total_reward += reward

            print(f"[STEP] Score: {total_reward}")

    except Exception as e:
        print("[STEP] Runtime Error:", str(e))

    print("[END]")

# 🔥 RUN IN BACKGROUND (keeps logs + execution)
threading.Thread(target=run_env).start()

# ✅ OPENENV REQUIRED ENDPOINTS
env_instance = EmailEnv("easy")

@app.post("/reset")
def reset():
    try:
        obs = env_instance.reset()
        return obs
    except Exception as e:
        return {"error": str(e)}

@app.post("/step")
def step(action: dict):
    try:
        obs, reward, done, info = env_instance.step(action)
        return {
            "observation": obs,
            "reward": reward,
            "done": done,
            "info": info
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def root():
    return {"status": "running"}
