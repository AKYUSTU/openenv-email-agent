import os
import json
from openai import OpenAI
from env.environment import EmailEnv

# ✅ MUST use these
client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
)

def get_llm_action(obs):
    prompt = f"""
    Classify this email and respond in JSON.

    Subject: {obs['subject']}
    Body: {obs['body']}

    Return JSON:
    {{
        "action_type": "...",
        "category": "...",
        "priority": "...",
        "response": "..."
    }}
    """

    # 🔥 FORCE API CALL
    response = client.chat.completions.create(
        model=os.environ["MODEL_NAME"],
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.choices[0].message.content

    try:
        action = json.loads(text)
    except:
        action = {}

    return {
        "action_type": action.get("action_type", "reply"),
        "category": action.get("category", "support"),
        "priority": action.get("priority", "medium"),
        "response": action.get("response", text[:100])
    }

def run():
    print("[START]")

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

    print("[END]")

if __name__ == "__main__":
    run()
