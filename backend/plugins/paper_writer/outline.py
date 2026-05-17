from dataclasses import dataclass, field


@dataclass
class OutlineSection:
    title: str
    key_points: list[str] = field(default_factory=list)
    estimated_words: int = 0


def generate_outline(topic: str) -> list[OutlineSection]:
    return [
        OutlineSection(
            title="引言",
            key_points=["研究背景与动机", "现有工作的局限性", "本文的主要贡献"],
            estimated_words=800,
        ),
        OutlineSection(
            title="相关工作",
            key_points=["子领域A的综述", "子领域B的综述", "与本文方法的对比"],
            estimated_words=1000,
        ),
        OutlineSection(
            title="方法",
            key_points=["问题形式化定义", "模型/算法设计", "理论分析（如适用）"],
            estimated_words=1500,
        ),
        OutlineSection(
            title="实验",
            key_points=["实验设置（数据集、基线、评估指标）", "主实验结果与分析", "消融实验"],
            estimated_words=1200,
        ),
        OutlineSection(
            title="讨论",
            key_points=["结果的意义", "局限性", "未来方向"],
            estimated_words=600,
        ),
        OutlineSection(
            title="结论",
            key_points=["总结主要发现", "重申贡献"],
            estimated_words=300,
        ),
    ]
