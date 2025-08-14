def format_hashtags(*tags: str) -> str:
    cleaned = ["#" + t.strip().replace(" ", "") for t in tags if t.strip()]
    return " ".join(cleaned)
