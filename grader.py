def grade_hard(actions, emails):
    correct = 0
    penalties = 0

    for action in actions:
        email = next(e for e in emails if e.id == action["email_id"])

        if email.category == "urgent" and action["action_type"] == "escalate":
            correct += 1
        elif email.category == "spam" and action["action_type"] == "ignore":
            correct += 1
        elif email.category == "normal" and action["action_type"] == "reply":
            correct += 1
        else:
            penalties += 1

    score = (correct - 0.5 * penalties) / len(emails)
    return max(0, min(1, score))