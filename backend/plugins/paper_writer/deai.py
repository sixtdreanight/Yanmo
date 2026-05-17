"""De-AI text — remove common AI writing patterns from academic text."""

import re

# Patterns to detect and fix
AI_PATTERNS = [
    # Overused AI vocabulary (Chinese)
    (r"此外[，,]\s*", ""),
    (r"至关重要", "重要"),
    (r"深入探讨", "讨论"),
    (r"值得注意的是[，,]?\s*", ""),
    (r"毋庸置疑[，,]?\s*", ""),
    (r"换言之[，,]?\s*", "即"),
    (r"不仅[，,]?\s*而且[，,]?\s*", ""),
    (r"这不仅仅是[^，,]+[，,]而是", ""),
    # English AI vocabulary
    (r"\bFurthermore[,]?\s*", ""),
    (r"\bMoreover[,]?\s*", ""),
    (r"\bIt is worth noting that\s*", ""),
    (r"\bIt should be noted that\s*", ""),
    (r"\bNot only\s+(\w+)\s+but also\s+", r"\1 "),
    # Dummy subjects
    (r"\bIt is (important|crucial|essential|vital|critical) to\b", "You should"),
    (r"\bIt can be (seen|observed|noted) that\b", ""),
    # Over-qualification
    (r"\bpotentially\s+potentially\b", "potentially"),
    (r"\bit may be possible that\b", "it may"),
    (r"\bit could potentially be argued that\b", "it could be that"),
    # Vague attribution
    (r"\bexperts believe that\b", ""),
    (r"\bindustry reports show that\b", ""),
    (r"\bobservers note that\b", ""),
    (r"\bsome critics argue that\b", ""),
    # Overused emphasis
    (r"\bplays? a (crucial|critical|vital|pivotal|key) role in\b", "is important in"),
    (r"\bserves as a testament to\b", "demonstrates"),
    (r"\bin the ever-evolving landscape of\b", "in"),
    # Triple patterns → break into two
    (r"(\w+)、(\w+)和(\w+)", r"\1 和 \2"),
    (r"(\w+),\s*(\w+),\s*and\s*(\w+)", r"\1 and \2"),
]

# Sentence starts that sound like a chatbot
CHATBOT_STARTS = [
    "当然",
    "让我来",
    "以下是",
    "这是一个",
    "希望这",
    "请告诉我",
    "基于上述",
]


def deai_text(text: str) -> str:
    """Remove common AI writing patterns from text."""
    result = text

    # Apply pattern replacements
    for pattern, replacement in AI_PATTERNS:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

    # Remove chatbot-style sentence openers
    sentences = re.split(r"(?<=[。！？.!?])\s*", result)
    filtered = []
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        # Skip sentences that start with chatbot phrases
        if any(s.startswith(prefix) for prefix in CHATBOT_STARTS):
            continue
        filtered.append(s)
    result = "。".join(filtered)

    # Clean up multiple spaces and repeated punctuation
    result = re.sub(r"\s{2,}", " ", result)
    result = re.sub(r"[，,]{2,}", "，", result)
    result = re.sub(r"[。.]{2,}", "。", result)
    result = re.sub(r"！{2,}", "！", result)
    result = result.replace("。。", "。")
    result = result.replace("，，", "，")

    # Remove empty parenthetical asides
    result = re.sub(r"\(\s*\)", "", result)
    result = re.sub(r"（\s*）", "", result)

    return result.strip()


def detect_ai_score(text: str) -> dict:
    """Score how likely a text is AI-generated. Lower = more human."""
    if not text.strip():
        return {"score": 0, "flags": [], "summary": "空文本"}

    flags = []
    score = 0

    # Check AI vocabulary density
    ai_words = [
        "此外", "至关重要", "深入探讨", "值得注意的是", "毋庸置疑",
        "Furthermore", "Moreover", "It is worth noting",
        "serves as", "plays a crucial role", "ever-evolving landscape",
        "pivotal", "testament", "showcases", "underscores",
        "不仅如此", "与此同时", "在此背景下",
    ]
    word_count = 0
    for word in ai_words:
        count = len(re.findall(re.escape(word), text, re.IGNORECASE))
        if count > 0:
            word_count += count
            flags.append(f"AI词汇: '{word}' 出现 {count} 次")
    score += min(word_count * 2, 20)

    # Check for em-dash overuse
    em_dash_count = text.count("—") + text.count("--")
    if em_dash_count > 2:
        flags.append(f"破折号过多: {em_dash_count} 处")
        score += min(em_dash_count, 10)

    # Check for three-item lists
    triple_count = len(re.findall(r"[^,，]+[,，][^,，]+[,，][^,，和]+和", text))
    triple_count += len(re.findall(r"\w+, \w+, and \w+", text))
    if triple_count > 1:
        flags.append(f"三段式列举: {triple_count} 处")
        score += min(triple_count * 3, 10)

    # Check for chatbot openers
    for s in re.split(r"(?<=[。！？.!?])\s*", text):
        for prefix in CHATBOT_STARTS:
            if s.strip().startswith(prefix):
                flags.append(f"聊天机器人开头: '{s.strip()[:20]}...'")
                score += 3
                break

    # Sentence length uniformity
    lengths = [len(s.strip()) for s in re.split(r"(?<=[。！？.!?])\s*", text) if s.strip()]
    if len(lengths) >= 3:
        avg = sum(lengths) / len(lengths)
        uniform = sum(1 for l in lengths if abs(l - avg) < 10) / len(lengths)
        if uniform > 0.7:
            flags.append("句子长度过于均匀")
            score += 5

    score = min(score, 100)

    summary = "读起来自然" if score < 15 else ("有些AI痕迹" if score < 30 else "AI痕迹较重")
    return {"score": score, "flags": flags[:8], "summary": summary}
