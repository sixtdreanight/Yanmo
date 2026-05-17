from dataclasses import dataclass, field


@dataclass
class Evaluation:
    title: str
    innovation_score: float
    rationality_score: float
    methodology_score: float
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)


def evaluate_project(title: str, description: str, field: str = "") -> Evaluation:
    if not description.strip():
        return Evaluation(
            title=title,
            innovation_score=0,
            rationality_score=0,
            methodology_score=0,
            strengths=["请提供项目描述"],
            weaknesses=["无描述"],
            suggestions=["填写项目描述后重新评估"],
        )

    strengths: list[str] = []
    weaknesses: list[str] = []
    suggestions: list[str] = []

    novel_keywords = ["novel", "new", "改进", "首次", "first", "创新", "突破", "原创"]
    novel_count = sum(1 for kw in novel_keywords if kw.lower() in description.lower())

    method_keywords = ["实验", "证明", "验证", "theorem", "定理", "推导", "算法", "algorithm"]
    method_count = sum(1 for kw in method_keywords if kw.lower() in description.lower())

    if len(description) > 200:
        strengths.append("项目描述较为详细")
    else:
        weaknesses.append("项目描述过短，缺乏足够细节")

    if method_count >= 2:
        strengths.append(f"具备方法论意识（检测到 {method_count} 个方法论关键词）")
    else:
        weaknesses.append("缺少方法论描述，建议补充实验/验证方案")

    if novel_count >= 2:
        strengths.append(f"强调创新性（检测到 {novel_count} 个创新关键词）")
    else:
        suggestions.append("建议明确表达创新点和与现有工作的区别")

    desc_len = len(description)
    innovation_score = min(10, max(0, (novel_count * 2) + (desc_len / 200)))
    rationality_score = min(10, max(0, (method_count * 2) + (desc_len / 300)))
    methodology_score = min(10, max(0, method_count * 2.5))

    return Evaluation(
        title=title,
        innovation_score=round(innovation_score, 1),
        rationality_score=round(rationality_score, 1),
        methodology_score=round(methodology_score, 1),
        strengths=strengths,
        weaknesses=weaknesses,
        suggestions=suggestions,
    )
