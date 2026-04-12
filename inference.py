import os
import json
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from env.environment import EmailEnv

app = FastAPI()

# ─────────────────────────────────────────────
# LLM helper – always uses injected env vars
# ─────────────────────────────────────────────
def get_llm_action(obs: dict) -> dict:
    """Call the LiteLLM proxy and return a structured action dict."""

    api_base = os.environ.get("API_BASE_URL")
    api_key  = os.environ.get("API_KEY")
    model    = os.environ.get("MODEL_NAME", "gpt-4o-mini")

    if not api_base or not api_key:
        print("[ERROR] API_BASE_URL or API_KEY env vars not set")
        return {
            "action_type": "reply",
            "category": "support",
            "priority": "medium",
            "response": "API not configured"
        }

    client = OpenAI(base_url=api_base, api_key=api_key)

    prompt = f"""You are an email triage assistant. Classify the email below and decide what action to take.

Subject: {obs.get('subject', '')}
Body: {obs.get('body', '')}

Reply with a JSON object (no markdown, no extra text) with exactly these keys:
{{
  "action_type": "<reply|ignore|escalate>",
  "category": "<support|spam|business|legal|security>",
  "priority": "<low|medium|high>",
  "response": "<short reply message if action_type is reply, else empty string>"
}}"""

    try:
        print(f"[LLM] Calling proxy: model={model}, base_url={api_base}")
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )
        text = completion.choices[0].message.content.strip()
        print(f"[LLM] Response: {text}")

        # Strip markdown code fences if present
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()

        action = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON parse failed: {e} | raw text: {text}")
        action = {}
    except Exception as e:
        print(f"[ERROR] LLM call failed: {e}")
        action = {}

    return {
        "action_type": action.get("action_type", "reply"),
        "category":    action.get("category",    "support"),
        "priority":    action.get("priority",     "medium"),
        "response":    action.get("response",     "Thank you for reaching out."),
    }


# ─────────────────────────────────────────────
# Shared environment instances (one per task)
# ─────────────────────────────────────────────
envs: dict[str, EmailEnv] = {
    "easy":   EmailEnv("easy"),
    "medium": EmailEnv("medium"),
    "hard":   EmailEnv("hard"),
}


# ─────────────────────────────────────────────
# Request / response models
# ─────────────────────────────────────────────
class ObservationRequest(BaseModel):
    subject: str = ""
    body:    str = ""
    history: list = []


class StepRequest(BaseModel):
    action: dict


# ─────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "running", "agent": "openenv-email-agent"}


# ── /act  (PRIMARY endpoint the validator uses) ──────────────────────────────
# The validator sends an observation and expects the agent to return an action
# generated via the LLM proxy.
@app.post("/act")
def act(obs: ObservationRequest):
    """Receive an observation, call the LLM proxy, return an action."""
    observation = obs.dict()
    action = get_llm_action(observation)
    print(f"[ACT] obs={observation} -> action={action}")
    return action


# ── /reset & /step  (environment management endpoints) ───────────────────────
@app.post("/reset")
def reset(task: str = "easy"):
    task = task if task in envs else "easy"
    obs = envs[task].reset()
    print(f"[RESET] task={task} -> obs={obs}")
    return obs


@app.post("/step")
def step(body: StepRequest, task: str = "easy"):
    """
    Advance the environment with the given action.
    The action MUST have been produced by calling /act first.
    """
    task = task if task in envs else "easy"
    obs, reward, done, info = envs[task].step(body.action)
    result = {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info,
    }
    print(f"[STEP] task={task} reward={reward} done={done}")
    return result


# ── /run  (convenience: runs a full episode and uses the LLM for every step) ─
@app.post("/run")
def run_episode(task: str = "easy"):
    """Run a complete episode end-to-end, calling the LLM proxy at every step."""
    task = task if task in envs else "easy"
    env = envs[task]
    obs = env.reset()

    total_reward = 0.0
    steps = 0

    while True:
        action = get_llm_action(obs)
        obs, reward, done, _ = env.step(action)
        total_reward += reward
        steps += 1
        if done:
            break

    return {"task": task, "total_reward": total_reward, "steps": steps}
