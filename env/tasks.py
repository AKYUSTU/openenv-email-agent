def load_task(task_name):
    if task_name == "easy":
        return {
            "emails": [
                {
                    "id": 1,
                    "subject": "Refund request",
                    "body": "I want refund for my order",
                    "true_category": "support",
                    "true_priority": "high",
                    "expected_action": "reply"
                }
            ]
        }

    elif task_name == "medium":
        return {
            "emails": [
                {
                    "id": 1,
                    "subject": "Delay in delivery",
                    "body": "My package is late",
                    "true_category": "support",
                    "true_priority": "medium",
                    "expected_action": "reply"
                }
            ]
        }

    elif task_name == "hard":
        return {
            "emails": [
                {
                    "id": 1,
                    "subject": "Legal complaint",
                    "body": "I will take legal action",
                    "true_category": "legal",
                    "true_priority": "high",
                    "expected_action": "escalate"
                }
            ]
        }