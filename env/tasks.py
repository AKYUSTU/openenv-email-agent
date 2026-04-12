def load_task(task_name):
    if task_name == "easy":
        return {
            "emails": [
                {
                    "id": 1,
                    "subject": "Refund request",
                    "body": "I want refund for damaged product",
                    "true_category": "support",
                    "true_priority": "high",
                    "expected_action": "reply"
                },
                {
                    "id": 2,
                    "subject": "Spam offer",
                    "body": "Win iPhone now!!!",
                    "true_category": "spam",
                    "true_priority": "low",
                    "expected_action": "ignore"
                },
                {
                    "id": 3,
                    "subject": "Wrong item delivered",
                    "body": "I received wrong product",
                    "true_category": "support",
                    "true_priority": "medium",
                    "expected_action": "reply"
                },
                {
                    "id": 4,
                    "subject": "Discount inquiry",
                    "body": "Any offers available?",
                    "true_category": "business",
                    "true_priority": "low",
                    "expected_action": "reply"
                },
                {
                    "id": 5,
                    "subject": "Newsletter subscription",
                    "body": "Subscribe me to updates",
                    "true_category": "business",
                    "true_priority": "low",
                    "expected_action": "reply"
                }
            ]
        }

    elif task_name == "medium":
        return {
            "emails": [
                {
                    "id": 1,
                    "subject": "Late delivery complaint",
                    "body": "My order is delayed by 5 days",
                    "true_category": "support",
                    "true_priority": "medium",
                    "expected_action": "reply"
                },
                {
                    "id": 2,
                    "subject": "Partnership proposal",
                    "body": "We want to collaborate",
                    "true_category": "business",
                    "true_priority": "medium",
                    "expected_action": "escalate"
                },
                {
                    "id": 3,
                    "subject": "Account login issue",
                    "body": "Unable to login",
                    "true_category": "support",
                    "true_priority": "high",
                    "expected_action": "reply"
                },
                {
                    "id": 4,
                    "subject": "Fake lottery",
                    "body": "You won $1 million",
                    "true_category": "spam",
                    "true_priority": "low",
                    "expected_action": "ignore"
                },
                {
                    "id": 5,
                    "subject": "Bulk order inquiry",
                    "body": "We need 500 units",
                    "true_category": "business",
                    "true_priority": "high",
                    "expected_action": "escalate"
                }
            ]
        }

    elif task_name == "hard":
        return {
            "emails": [
                {
                    "id": 1,
                    "subject": "Legal notice",
                    "body": "We will take legal action",
                    "true_category": "legal",
                    "true_priority": "high",
                    "expected_action": "escalate"
                },
                {
                    "id": 2,
                    "subject": "Data breach alert",
                    "body": "Customer data leaked",
                    "true_category": "security",
                    "true_priority": "high",
                    "expected_action": "escalate"
                },
                {
                    "id": 3,
                    "subject": "VIP complaint",
                    "body": "I am a premium customer unhappy",
                    "true_category": "support",
                    "true_priority": "high",
                    "expected_action": "escalate"
                },
                {
                    "id": 4,
                    "subject": "Phishing attempt",
                    "body": "Click this link to verify account",
                    "true_category": "spam",
                    "true_priority": "high",
                    "expected_action": "ignore"
                },
                {
                    "id": 5,
                    "subject": "Security vulnerability report",
                    "body": "Your system has a bug",
                    "true_category": "security",
                    "true_priority": "high",
                    "expected_action": "escalate"
                }
            ]
        }
