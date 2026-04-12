def compute_reward(email, action):
    reward = 0.0

    if action.get("category") == email.get("true_category"):
        reward += 0.2
    else:
        reward -= 0.1

    if action.get("priority") == email.get("true_priority"):
        reward += 0.2
    else:
        reward -= 0.1

    if action.get("action_type") == email.get("expected_action"):
        reward += 0.3
    else:
        reward -= 0.2

    if action.get("response"):
        if len(action["response"]) > 20:
            reward += 0.2
        else:
            reward -= 0.1

    if email.get("true_priority") == "high" and action.get("action_type") == "ignore":
        reward -= 0.5

    # 🔥 cost penalty
    if action.get("response") and len(action["response"]) > 150:
        reward -= 0.1

    reward += 0.05

    return max(0.01, min(reward, 0.99))
