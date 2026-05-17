from backend.plugins.paper_writer.outline import generate_outline, OutlineSection
from backend.plugins.paper_writer.citation import parse_bibtex, BibEntry


def test_generate_outline_returns_sections():
    sections = generate_outline("基于Transformer的机器翻译改进研究")
    assert len(sections) >= 3
    assert any("引言" in s.title or "introduction" in s.title.lower() for s in sections)
    assert any("方法" in s.title or "method" in s.title.lower() for s in sections)


def test_sections_have_valid_structure():
    sections = generate_outline("Test Paper")
    for s in sections:
        assert isinstance(s.title, str)
        assert len(s.title) > 0
        assert isinstance(s.key_points, list)


def test_parse_bibtex_entry():
    entry = """@article{vaswani2017attention,
      title={Attention is All You Need},
      author={Vaswani, Ashish and Shazeer, Noam and Parmar, Niki},
      journal={NeurIPS},
      year={2017}
    }"""
    result = parse_bibtex(entry)
    assert len(result) == 1
    assert result[0].cite_key == "vaswani2017attention"
    assert result[0].title == "Attention is All You Need"
    assert result[0].year == "2017"


def test_parse_bibtex_multiple_entries():
    entries = """@article{a1, title={T1}, author={A}, journal={J}, year={2020}}
    @inproceedings{b1, title={T2}, author={B}, booktitle={C}, year={2021}}"""
    result = parse_bibtex(entries)
    assert len(result) == 2
