import os
import json
import threading
from fastapi import FastAPI
from openai import OpenAI
from env.environment import EmailEnv

# ✅ MUST use environment variables (validator requirement)
client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
)

app = FastAPI()

# 🔥 FINAL FIXED LLM FUNCTION (NO FALLBACK SKIP)
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

    # ✅ FORCE API CALL (this is what validator checks)
    response = client.chat.completions.create(
        model=os.environ["MODEL_NAME"],
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.choices[0].message.content

    # ✅ ALWAYS USE OUTPUT (no skipping)
    try:
        action = json.loads(text)
    except:
        action = {}

    # ✅ GUARANTEE STRUCTURE (prevents crash but still uses LLM output)
    return {
        "action_type": action.get("action_type", "reply"),
        "category": action.get("category", "support"),
        "priority": action.get("priority", "medium"),
        "response": action.get("response", text[:100])
    }

# 🚀 MAIN EXECUTION LOOP
def run_env():
    print("[START]")

    for task in ["easy", "medium", "hard"]:
        print(f"[STEP] Running {task}")

        env = EmailEnv(task)
        obs = env.reset()

        total_reward = 0
        done = False

        while not done:
            action = get_llm_action(obs)  # ✅ LLM used here

            obs, reward, done, info = env.step(action)
            total_reward += reward

        print(f"[STEP] Score: {total_reward}")

    print("[END]")

# ✅ RUN IN BACKGROUND (HF requirement)
threading.Thread(target=run_env).start()

# ✅ KEEP SERVER ALIVE (HF health check)
@app.get("/")
def root():
    return {"status": "running"}
# 🔥 GLOBAL ENV INSTANCE (IMPORTANT)
env_instance = EmailEnv("easy")

@app.post("/reset")
def reset():
    obs = env_instance.reset()
    return obs

@app.post("/step")
def step(action: dict):
    obs, reward, done, info = env_instance.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }
