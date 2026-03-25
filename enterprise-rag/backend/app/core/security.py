INJECTION_PATTERNS = [
    "ignore previous instructions",
    "reveal system prompt",
    "显示系统提示词",
    "忽略以上规则",
]


def is_prompt_injection_risk(query: str) -> bool:
    content = query.lower()
    return any(pattern in content for pattern in INJECTION_PATTERNS)


def mask_text(text: str) -> str:
    if not text:
        return text
    if len(text) <= 4:
        return "*" * len(text)
    return text[:2] + "***" + text[-2:]
