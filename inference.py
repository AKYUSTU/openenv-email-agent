import os
import json
import threading
from fastapi import FastAPI
from openai import OpenAI
from env.environment import EmailEnv

client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
)

app = FastAPI()

def get_llm_action(obs):
    history_text = "\n".join(obs["history"])

    prompt = f"""
    You are a professional enterprise email assistant.

    Past actions:
    {history_text}

    Analyze this email:
    Subject: {obs['subject']}
    Body: {obs['body']}

    Decide:
    - category (support, spam, business, legal, security)
    - priority (low, medium, high)
    - action_type (reply, escalate, ignore)
    - response

    Return ONLY JSON:
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
        return json.loads(text)

    except Exception:
        return {
            "action_type": "reply",
            "category": "support",
            "priority": "medium",
            "response": "We are reviewing your request."
        }

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

threading.Thread(target=run_env).start()

@app.get("/")
def root():
    return {"status": "running"}
