def compute_reward(email, action):
    reward = 0.0

    # category correctness
    if action.get("category") == email["true_category"]:
        reward += 0.25

    # priority correctness
    if action.get("priority") == email["true_priority"]:
        reward += 0.25

    # correct decision (reply / escalate / ignore)
    if action.get("action_type") == email["expected_action"]:
        reward += 0.3

    # response quality
    if action.get("response"):
        if len(action["response"]) > 20:
            reward += 0.2
        else:
            reward -= 0.1

    # penalty for wrong critical action
    if email["true_priority"] == "high" and action.get("action_type") == "ignore":
        reward -= 0.5

    return max(0.0, min(reward, 1.0))