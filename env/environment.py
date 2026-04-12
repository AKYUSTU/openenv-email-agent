from env.tasks import load_task
from env.grader import compute_reward

class EmailEnv:
    def __init__(self, task_name):
        self.task_name = task_name
        self.task_data = load_task(task_name)

        self.emails = self.task_data["emails"]
        self.current_index = 0
        self.history = []

    def reset(self):
        self.current_index = 0
        self.history = []

        email = self.emails[self.current_index]

        return {
            "subject": email["subject"],
            "body": email["body"],
            "history": self.history
        }

    def step(self, action):
        email = self.emails[self.current_index]

        # ✅ compute reward
        reward = compute_reward(email, action)

        # ✅ store history
        self.history.append({
            "email_id": email["id"],
            "action": action
        })

        # ✅ move to next email
        self.current_index += 1

        done = self.current_index >= len(self.emails)

        if not done:
            next_email = self.emails[self.current_index]

            observation = {
                "subject": next_email["subject"],
                "body": next_email["body"],
                "history": self.history
            }
        else:
            observation = {}

        return observation, reward, done, {}
