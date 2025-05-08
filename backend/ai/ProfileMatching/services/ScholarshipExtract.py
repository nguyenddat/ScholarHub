from ai.core.chain import get_chat_completion

def extract_scholarship(description):
    return get_chat_completion(
        task = "scholarship_extract",
        params = {
            "question": "Extract specific fields of information from the provided scholarship description",
            "context": description
        }
    )
