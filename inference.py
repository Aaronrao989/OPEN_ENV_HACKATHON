import os
import asyncio
from typing import List

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from server.email_env_environment import EmailEnvironment
from models import Action

# ENV VARIABLES (MANDATORY)
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

MAX_STEPS = 5


# LOG FUNCTIONS (STRICT FORMAT)
def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool):
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
        flush=True,
    )


# SIMPLE BASELINE POLICY (IMPORTANT)
def choose_action(email):
    if email.category == "urgent":
        return "escalate"
    elif email.category == "spam":
        return "ignore"
    else:
        return "reply"


async def main():
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    env = EmailEnvironment()

    rewards = []
    steps_taken = 0

    log_start(task="email_task", env="email_env", model=MODEL_NAME)

    # RESET
    obs = await env.reset_async()

    try:
        for step in range(1, MAX_STEPS + 1):
            emails = obs.emails

            # pick first email (simple baseline)
            email = emails[step % len(emails)]

            action_type = choose_action(email)

            action = Action(
                email_id=email.id,
                action_type=action_type,
            )

            obs = await env.step_async(action)

            reward = obs.reward
            done = obs.done

            rewards.append(reward)
            steps_taken = step

            log_step(
                step=step,
                action=f"{email.id}:{action_type}",
                reward=reward,
                done=done,
            )

            if done:
                break

        # SCORE NORMALIZATION (0–1)
        score = max(0, min(1, sum(rewards) / (MAX_STEPS * 0.3)))
        success = score > 0.3

    finally:
        env.close()

        log_end(
            success=success,
            steps=steps_taken,
            score=score,
            rewards=rewards,
        )


if __name__ == "__main__":
    asyncio.run(main())