from env.environment import EmailEnv

def run_task(task):
    env = EmailEnv(task)
    obs = env.reset()

    total_reward = 0
    done = False

    while not done:
        action = {
            "action_type": "reply",
            "category": "support",
            "priority": "high",
            "response": "We are looking into your issue and will resolve it soon."
        }

        obs, reward, done, info = env.step(action)
        total_reward += reward

    return total_reward

def main():
    print("[START]")

    for task in ["easy", "medium", "hard"]:
        print(f"[STEP] Running {task}")

        score = run_task(task)

        print(f"[STEP] Score: {score}")

    print("[END]")

if __name__ == "__main__":
    main()