from backend.plugins.evaluator.evaluate import evaluate_project, Evaluation


def test_evaluate_returns_structured_result():
    result = evaluate_project(
        title="Test Project",
        description="A novel approach to attention mechanisms in transformers.",
        field="machine_learning",
    )
    assert isinstance(result, Evaluation)
    assert 0 <= result.innovation_score <= 10
    assert 0 <= result.rationality_score <= 10
    assert 0 <= result.methodology_score <= 10
    assert len(result.strengths) >= 0
    assert len(result.weaknesses) >= 0


def test_evaluate_empty_description():
    result = evaluate_project(title="", description="", field="")
    assert isinstance(result, Evaluation)
    assert result.innovation_score == 0


def test_plugin_declaration():
    from backend.plugins.evaluator.plugin import EvaluatorPlugin
    plugin = EvaluatorPlugin()
    assert plugin.name == "evaluator"
    assert plugin.display_name == "审项目"
