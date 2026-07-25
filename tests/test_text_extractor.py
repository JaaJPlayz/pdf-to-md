"""Tests for the text extractor module."""



from pdf_to_md.text_extractor import TextExtractor, _avg_weight, _median


class TestTextExtractor:
    """Tests for TextExtractor."""

    def test_median_empty(self) -> None:
        assert _median([]) == 0.0

    def test_median_odd(self) -> None:
        assert _median([1, 3, 2]) == 2.0

    def test_median_even(self) -> None:
        assert _median([1, 2, 3, 4]) == 2.5

    def test_avg_weight_empty(self) -> None:
        assert _avg_weight([]) == 400.0

    def test_avg_weight(self) -> None:
        spans = [{"weight": 400}, {"weight": 700}]
        assert _avg_weight(spans) == 550.0

    def test_size_to_heading_level(self) -> None:
        extractor = TextExtractor()
        assert extractor._size_to_heading_level(24.0, 12.0) == 1
        assert extractor._size_to_heading_level(18.0, 12.0) == 2
        assert extractor._size_to_heading_level(16.0, 12.0) == 3
        assert extractor._size_to_heading_level(14.0, 12.0) == 4
