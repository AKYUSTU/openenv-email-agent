def compute_reward(email, action):
    reward = 0.0

    # category
    if action.get("category") == email.get("true_category"):
        reward += 0.2
    else:
        reward -= 0.1

    # priority
    if action.get("priority") == email.get("true_priority"):
        reward += 0.2
    else:
        reward -= 0.1

    # action correctness
    if action.get("action_type") == email.get("expected_action"):
        reward += 0.3
    else:
        reward -= 0.2

    # response quality
    if action.get("response"):
        if len(action["response"]) > 20:
            reward += 0.2
        else:
            reward -= 0.1

    # critical penalty
    if email.get("true_priority") == "high" and action.get("action_type") == "ignore":
        reward -= 0.5

    # small reward for completion
    reward += 0.05

    return max(0.0, min(reward, 1.0))
