from ai.core.chain import get_chat_completion

def profile_match(profile, scholarship):
    return get_chat_completion(
        task = "profile_matching",
        params = {
            "resume": format_dict(profile),
            "description": format_dict(scholarship),
            "question": "For each requirement, determine whether it is satisfied, and provide evidence from the resume to justify the decision."
        }
    )

def format_dict(dict):
    resp = ""
    for key, values in dict.items():
        text = f"{key}\n"

        if len(values) == 0:
            text += "- None\n"
            continue

        for value in values:
            text += f"- {value}\n"
        resp += text
    return resp

