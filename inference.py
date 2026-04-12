import os
import json
import threading
from fastapi import FastAPI
from openai import OpenAI
from env.environment import EmailEnv

# ✅ Initialize client using PROVIDED ENV VARIABLES (MANDATORY)
client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
)

app = FastAPI()

# 🔥 LLM ACTION FUNCTION (MANDATORY FOR VALIDATION)
def get_llm_action(obs):
    prompt = f"""
    You are an AI email assistant.

    Email:
    Subject: {obs['subject']}
    Body: {obs['body']}

    Decide:
    - category
    - priority
    - action_type (reply, escalate, ignore)
    - response

    Return ONLY valid JSON in this format:
    {{
        "action_type": "...",
        "category": "...",
        "priority": "...",
        "response": "..."
    }}
    """

    try:
        response = client.chat.completions.create(
            model=os.environ["MODEL_NAME"],
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.choices[0].message.content

        # Try parsing JSON
        action = json.loads(text)

        return action

    except Exception:
        # Fallback (IMPORTANT to avoid crashes)
        return {
            "action_type": "reply",
            "category": "support",
            "priority": "medium",
            "response": "We are reviewing your request."
        }

# 🚀 MAIN ENV RUNNER
def run_env():
    print("[START]")

    for task in ["easy", "medium", "hard"]:
        print(f"[STEP] Running {task}")

        env = EmailEnv(task)
        obs = env.reset()

        total_reward = 0
        done = False

        while not done:
            action = get_llm_action(obs)

            obs, reward, done, info = env.step(action)
            total_reward += reward

        print(f"[STEP] Score: {total_reward}")

    print("[END]")

# 🔥 RUN IN BACKGROUND (so server stays alive)
threading.Thread(target=run_env).start()

# ✅ REQUIRED FOR HUGGING FACE HEALTH CHECK
@app.get("/")
def root():
    return {"status": "running"}
