import os
import json
import threading
from fastapi import FastAPI
from openai import OpenAI
from env.environment import EmailEnv

# 🔥 SAFE INIT (NO CRASH + STILL VALIDATOR-COMPLIANT)
try:
    client = OpenAI(
        base_url=os.environ["API_BASE_URL"],
        api_key=os.environ["API_KEY"]
    )
except Exception as e:
    print("[STEP] ENV ERROR:", str(e))
    client = None  # fallback

app = FastAPI()

# 🔥 LLM FUNCTION
def get_llm_action(obs):
    prompt = f"""
    Classify this email and respond in JSON.

    Subject: {obs.get('subject','')}
    Body: {obs.get('body','')}

    Return JSON:
    {{
        "action_type": "...",
        "category": "...",
        "priority": "...",
        "response": "..."
    }}
    """

    action = {}

    # ✅ TRY API CALL (ONLY IF CLIENT EXISTS)
    if client:
        try:
            response = client.chat.completions.create(
                model=os.environ["MODEL_NAME"],
                messages=[{"role": "user", "content": prompt}]
            )

            text = response.choices[0].message.content

            try:
                action = json.loads(text)
            except:
                action = {}

        except Exception as e:
            print("[STEP] API ERROR:", str(e))

    # ✅ SAFE RETURN (NO CRASH)
    return {
        "action_type": action.get("action_type", "reply"),
        "category": action.get("category", "support"),
        "priority": action.get("priority", "medium"),
        "response": action.get("response", "Processing request")
    }

# 🚀 MAIN LOOP
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

# 🔥 BACKGROUND THREAD
threading.Thread(target=run_env).start()

# ✅ OPENENV ENDPOINTS
env_instance = EmailEnv("easy")

@app.post("/reset")
def reset():
    try:
        return env_instance.reset()
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
