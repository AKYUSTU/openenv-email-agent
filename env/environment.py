class EmailEnv:

    def __init__(self, task_name="easy"):
        self.task_name = task_name
        self.reset()

    def reset(self):
        from env.tasks import load_task
        self.state_data = load_task(self.task_name)
        self.current_index = 0
        self.total_reward = 0
        self.history = []
        return self._get_obs()

    def _get_obs(self):
        email = self.state_data["emails"][self.current_index]
        return {
            "email_id": email["id"],
            "subject": email["subject"],
            "body": email["body"],
            "history": self.history
        }

    def step(self, action):
        from env.grader import compute_reward

        email = self.state_data["emails"][self.current_index]

        reward = compute_reward(email, action)
        self.total_reward += reward

        self.history.append(f"Handled email {email['id']}")

        self.current_index += 1
        done = self.current_index >= len(self.state_data["emails"])

        obs = None if done else self._get_obs()

        return obs, reward, done, {
            "total_reward": self.total_reward
        }

    def state(self):
        return self.state_data