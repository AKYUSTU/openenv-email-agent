def compute_reward(email, action):
    reward = 0.0

    # ✅ category correctness
    if action.get("category") == email.get("true_category"):
        reward += 0.2
    else:
        reward -= 0.1

    # ✅ priority correctness
    if action.get("priority") == email.get("true_priority"):
        reward += 0.2
    else:
        reward -= 0.1

    # ✅ action correctness
    if action.get("action_type") == email.get("expected_action"):
        reward += 0.3
    else:
        reward -= 0.2

    # ✅ response quality
    if action.get("response"):
        if len(action["response"]) > 20:
            reward += 0.2
        else:
            reward -= 0.1

    # ❌ critical mistake penalty
    if email.get("true_priority") == "high" and action.get("action_type") == "ignore":
        reward -= 0.5

    # 🔥 cost awareness (real-world feature)
    if action.get("response") and len(action["response"]) > 150:
        reward -= 0.1

    # ✅ small positive bias to avoid 0
    reward += 0.05

    # 🔥 STRICT RANGE FIX (MANDATORY)
    return max(0.01, min(reward, 0.99))
