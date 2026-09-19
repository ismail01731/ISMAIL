import re
from typing import Optional
HOOK_WORDS = [
    "কেন",
    "কিভাবে",
    "কীভাবে",
    "কি",
    "সত্যি",
    "রহস্য",
    "দেখুন",
    "জানুন",
    "চমক",
    "অবশেষে",
    "শেষে",
    "how",
    "why",
    "what",
    "secret",
    "finally",
    "watch",
    "revealed",
]
def _clean_text(text: str) -> str:
    return str(text or "").strip()
def _split_sentences(text: str):
    text = _clean_text(text)
    if not text:
        return []
    parts = re.split(r"(?<=[.!?।!?])\s+|\n+", text)
    return [
        part.strip()
        for part in parts
        if part.strip()
    ]
def _word_count(text: str):
    return len(re.findall(r"\S+", _clean_text(text)))
def analyze_hook(hook: str):
    hook = _clean_text(hook)
    lower = hook.lower()
    score = 50
    word_count = _word_count(hook)
    has_question = "?" in hook or "?" in hook or "কি" in hook or "কেন" in hook
    has_exclamation = "!" in hook
    has_number = bool(re.search(r"\d+", hook))
    curiosity_count = sum(
        1 for word in HOOK_WORDS
        if word.lower() in lower
    )
    if 5 <= word_count <= 25:
        score += 10
    if has_question:
        score += 8
    if has_exclamation:
        score += 5
    if has_number:
        score += 5
    score += min(curiosity_count * 4, 12)
    if word_count > 35:
        score -= 12
    if word_count < 3:
        score -= 8
    score = max(0, min(100, score))
    return {
        "success": True,
        "hook": hook,
        "hook_score": score,
        "word_count": word_count,
        "has_question": has_question,
        "has_exclamation": has_exclamation,
        "has_number": has_number,
        "curiosity_word_count": curiosity_count,
    }
def analyze_script(script: str, video_type: str = "short"):
    script = _clean_text(script)
    video_type = _clean_text(video_type).lower() or "short"
    sentences = _split_sentences(script)
    if not sentences:
        return {
            "success": False,
            "error": "Script is empty",
        }
    total_words = _word_count(script)
    hook_text = sentences[0]
    hook_analysis = analyze_hook(hook_text)
    if video_type in {"short", "shorts"}:
        ideal_sentences = 6
        max_early_sentences = 3
    else:
        ideal_sentences = 12
        max_early_sentences = 5
    structure_score = 50
    if len(sentences) >= 3:
        structure_score += 10
    if len(sentences) >= ideal_sentences:
        structure_score += 8
    if len(sentences) <= ideal_sentences * 2:
        structure_score += 7
    if hook_analysis["hook_score"] >= 70:
        structure_score += 10
    if total_words >= 30:
        structure_score += 5
    if total_words > 1000:
        structure_score -= 10
    structure_score = max(0, min(100, structure_score))
    early_text = " ".join(sentences[:max_early_sentences])
    has_call_to_action = any(
        phrase in script.lower()
        for phrase in [
            "subscribe",
            "like",
            "comment",
            "follow",
            "শেয়ার",
            "সাবস্ক্রাইব",
            "লাইক",
            "কমেন্ট",
            "ফলো",
        ]
    )
    has_payoff_words = any(
        word in script.lower()
        for word in [
            "শেষে",
            "অবশেষে",
            "চমক",
            "দেখুন",
            "ফলাফল",
            "result",
            "finally",
            "revealed",
            "শেষ পর্যন্ত",
        ]
    )
    recommendations = []
    if hook_analysis["hook_score"] < 70:
        recommendations.append(
            "প্রথম লাইনে curiosity, প্রশ্ন বা unexpected result যোগ করুন।"
        )
    if len(sentences) < 3:
        recommendations.append(
            "স্ক্রিপ্টে আরও clear setup, development এবং payoff যোগ করুন।"
        )
    if not has_payoff_words:
        recommendations.append(
            "শেষের দিকে একটি clear payoff বা reveal রাখুন।"
        )
    if not has_call_to_action:
        recommendations.append(
            "প্রয়োজনে শেষে সংক্ষিপ্ত CTA যোগ করুন।"
        )
    if video_type in {"short", "shorts"} and len(sentences) > 20:
        recommendations.append(
            "Shorts-এর জন্য অপ্রয়োজনীয় অংশ কমিয়ে দ্রুত pacing রাখুন।"
        )
    return {
        "success": True,
        "video_type": video_type,
        "word_count": total_words,
        "sentence_count": len(sentences),
        "hook": hook_analysis,
        "structure_score": structure_score,
        "early_script": early_text,
        "has_call_to_action": has_call_to_action,
        "has_payoff": has_payoff_words,
        "recommendations": recommendations,
    }
def optimize_script(script: str, video_type: str = "short"):
    analysis = analyze_script(script, video_type)
    if not analysis.get("success"):
        return analysis
    sentences = _split_sentences(script)
    improved = list(sentences)
    hook_score = analysis["hook"]["hook_score"]
    if hook_score < 70 and improved:
        original_hook = improved[0]
        improved[0] = (
            f"আপনি কি জানেন? {original_hook}"
        )
    if not analysis["has_payoff"]:
        improved.append(
            "শেষ পর্যন্ত দেখুন—শেষে আসল চমকটি আছে!"
        )
    if (
        video_type.lower() in {"short", "shorts"}
        and not analysis["has_call_to_action"]
    ):
        improved.append(
            "ভিডিওটি ভালো লাগলে লাইক ও সাবস্ক্রাইব করুন!"
        )
    optimized_script = "\n".join(improved)
    return {
        "success": True,
        "video_type": video_type,
        "original_script": script,
        "optimized_script": optimized_script,
        "original_analysis": analysis,
        "optimized_word_count": _word_count(optimized_script),
    }
def analyze_video_structure(
    script: str,
    video_type: str = "short",
):
    analysis = analyze_script(script, video_type)
    if not analysis.get("success"):
        return analysis
    if video_type.lower() in {"short", "shorts"}:
        structure = [
            "HOOK",
            "SETUP",
            "DEVELOPMENT",
            "PAYOFF",
            "CTA",
        ]
    else:
        structure = [
            "HOOK",
            "INTRO",
            "SETUP",
            "DEVELOPMENT",
            "CONFLICT",
            "ESCALATION",
            "PAYOFF",
            "CTA",
        ]
    sentence_count = analysis["sentence_count"]
    return {
        "success": True,
        "video_type": video_type,
        "recommended_structure": structure,
        "script_sentence_count": sentence_count,
        "structure_score": analysis["structure_score"],
        "hook_score": analysis["hook"]["hook_score"],
        "has_payoff": analysis["has_payoff"],
        "has_call_to_action": analysis["has_call_to_action"],
    }
def generate_script_structure(
    topic: str,
    video_type: str = "short",
):
    topic = _clean_text(topic)
    video_type = _clean_text(video_type).lower() or "short"
    if video_type in {"short", "shorts"}:
        sections = [
            {
                "section": "HOOK",
                "purpose": "প্রথম কয়েক সেকেন্ডে attention নেওয়া",
                "example": f"আপনি কি জানেন {topic} নিয়ে আসল মজার ব্যাপারটা কী?",
            },
            {
                "section": "SETUP",
                "purpose": "বিষয়টি দ্রুত establish করা",
                "example": f"আজকে আমরা দেখবো {topic}.",
            },
            {
                "section": "DEVELOPMENT",
                "purpose": "মূল ঘটনা বা comedy escalation",
                "example": f"{topic} নিয়ে একের পর এক মজার ঘটনা ঘটতে থাকে!",
            },
            {
                "section": "PAYOFF",
                "purpose": "শেষে reveal বা punchline",
                "example": "কিন্তু শেষ মুহূর্তে যা হলো, সেটা কেউ ভাবেনি!",
            },
            {
                "section": "CTA",
                "purpose": "দর্শককে action নিতে বলা",
                "example": "ভালো লাগলে লাইক ও সাবস্ক্রাইব করুন!",
            },
        ]
    else:
        sections = [
            {
                "section": "HOOK",
                "purpose": "দর্শকের attention নেওয়া",
                "example": f"{topic} নিয়ে আজকের ঘটনাটা আলাদা!",
            },
            {
                "section": "INTRO",
                "purpose": "ভিডিওর context দেওয়া",
                "example": f"আজকের ভিডিওতে দেখানো হবে {topic}.",
            },
            {
                "section": "SETUP",
                "purpose": "ঘটনার ভিত্তি তৈরি করা",
                "example": "চলুন শুরু করি।",
            },
            {
                "section": "DEVELOPMENT",
                "purpose": "মূল content এগিয়ে নেওয়া",
                "example": f"{topic} ধীরে ধীরে আরও interesting হয়ে যায়।",
            },
            {
                "section": "CONFLICT",
                "purpose": "সমস্যা বা tension তৈরি করা",
                "example": "এরপর unexpected একটি সমস্যা দেখা দেয়।",
            },
            {
                "section": "ESCALATION",
                "purpose": "tension বাড়ানো",
                "example": "পরিস্থিতি আরও মজার ও challenging হয়ে যায়।",
            },
            {
                "section": "PAYOFF",
                "purpose": "শেষ ফলাফল বা reveal",
                "example": "শেষে আসল ফলাফল সামনে আসে!",
            },
            {
                "section": "CTA",
                "purpose": "দর্শকের engagement নেওয়া",
                "example": "কমেন্ট করে আপনার মতামত জানান।",
            },
        ]
    return {
        "success": True,
        "topic": topic,
        "video_type": video_type,
        "sections": sections,
    }
class YouTubeScriptOptimizer:
    def analyze_hook(self, hook: str):
        return analyze_hook(hook)
    def analyze(self, script: str, video_type: str = "short"):
        return analyze_script(script, video_type)
    def optimize(self, script: str, video_type: str = "short"):
        return optimize_script(script, video_type)
    def structure(self, script: str, video_type: str = "short"):
        return analyze_video_structure(script, video_type)
    def generate_structure(
        self,
        topic: str,
        video_type: str = "short",
    ):
        return generate_script_structure(topic, video_type)
script_optimizer = YouTubeScriptOptimizer()
