from models import Action, Observation, Email


class EmailEnvironment:
    def __init__(self):
        self.step_count = 0
        self.max_steps = 5
        self.emails = []

    def generate_emails(self):
        return [
            Email(id="1", subject="Urgent: Server down", body="Fix ASAP", category="urgent"),
            Email(id="2", subject="Win lottery", body="Click here", category="spam"),
            Email(id="3", subject="Meeting request", body="Schedule call", category="normal"),
        ]

    # RESET
    async def reset_async(self):
        self.step_count = 0
        self.emails = self.generate_emails()

        obs = Observation(
            emails=self.emails,
            step=self.step_count,
            reward=0.0,
            done=False
        )

        return {
            "observation": obs,
            "reward": 0.0,
            "done": False,
            "info": {}
        }

    # STEP
    async def step_async(self, action: Action):
        reward = 0

        email = next((e for e in self.emails if e.id == action.email_id), None)

        if email is None:
            reward -= 0.2
        else:
            if email.category == "urgent" and action.action_type == "escalate":
                reward += 0.3
            elif email.category == "spam" and action.action_type == "ignore":
                reward += 0.2
            elif email.category == "normal" and action.action_type == "reply":
                reward += 0.2
            else:
                reward -= 0.1

        self.step_count += 1
        done = self.step_count >= self.max_steps

        obs = Observation(
            emails=self.emails,
            step=self.step_count,
            reward=reward,
            done=done
        )

        return {
            "observation": obs,
            "reward": reward,
            "done": done,
            "info": {}
        }

    def close(self):
        pass

    async def state(self):
        return {
            "emails": self.emails,
            "step": self.step_count
        }