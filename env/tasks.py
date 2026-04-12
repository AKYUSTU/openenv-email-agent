def load_task(task_name):
    if task_name == "easy":
        return {
            "emails": [
                {"id": 1, "subject": "Refund request", "body": "I want refund for damaged product",
                 "true_category": "support", "true_priority": "high", "expected_action": "reply"},

                {"id": 2, "subject": "Spam offer", "body": "Win iPhone now!!!",
                 "true_category": "spam", "true_priority": "low", "expected_action": "ignore"},

                {"id": 3, "subject": "Wrong item delivered", "body": "Received wrong product",
                 "true_category": "support", "true_priority": "medium", "expected_action": "reply"},

                {"id": 4, "subject": "Discount inquiry", "body": "Any offers?",
                 "true_category": "business", "true_priority": "low", "expected_action": "reply"},

                {"id": 5, "subject": "Newsletter subscription", "body": "Subscribe me",
                 "true_category": "business", "true_priority": "low", "expected_action": "reply"}
            ]
        }

    elif task_name == "medium":
        return {
            "emails": [
                {"id": 1, "subject": "Late delivery", "body": "Order delayed",
                 "true_category": "support", "true_priority": "medium", "expected_action": "reply"},

                {"id": 2, "subject": "Partnership proposal", "body": "Let’s collaborate",
                 "true_category": "business", "true_priority": "medium", "expected_action": "escalate"},

                {"id": 3, "subject": "Login issue", "body": "Cannot login",
                 "true_category": "support", "true_priority": "high", "expected_action": "reply"},

                {"id": 4, "subject": "Fake lottery", "body": "You won money",
                 "true_category": "spam", "true_priority": "low", "expected_action": "ignore"},

                {"id": 5, "subject": "Bulk order", "body": "Need 500 units",
                 "true_category": "business", "true_priority": "high", "expected_action": "escalate"}
            ]
        }

    elif task_name == "hard":
        return {
            "emails": [
                {"id": 1, "subject": "Legal notice", "body": "We will sue",
                 "true_category": "legal", "true_priority": "high", "expected_action": "escalate"},

                {"id": 2, "subject": "Data breach", "body": "Data leaked",
                 "true_category": "security", "true_priority": "high", "expected_action": "escalate"},

                {"id": 3, "subject": "VIP complaint", "body": "Premium user unhappy",
                 "true_category": "support", "true_priority": "high", "expected_action": "escalate"},

                {"id": 4, "subject": "Phishing mail", "body": "Click link",
                 "true_category": "spam", "true_priority": "high", "expected_action": "ignore"},

                {"id": 5, "subject": "Security bug", "body": "System vulnerable",
                 "true_category": "security", "true_priority": "high", "expected_action": "escalate"},

                {"id": 6, "subject": "Regulatory issue", "body": "Policy violation",
                 "true_category": "legal", "true_priority": "high", "expected_action": "escalate"}
            ]
        }
