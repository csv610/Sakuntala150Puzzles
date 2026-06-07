import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sl_Shakuntala150 import MODEL_MAP, generate_new_question, initialize_remaining_questions


class TestInitializeRemainingQuestions:
    def test_returns_list_of_length_n(self):
        result = initialize_remaining_questions(10)
        assert result == list(range(10))

    def test_zero_questions(self):
        result = initialize_remaining_questions(0)
        assert result == []

    def test_150_questions(self):
        result = initialize_remaining_questions(150)
        assert len(result) == 150


class TestGenerateNewQuestion:
    def test_returns_question_and_removes_index(self):
        questions = [
            {"id": 1, "title": "A", "question": "?"},
            {"id": 2, "title": "B", "question": "?"},
        ]
        remaining = [0, 1]
        result = generate_new_question(questions, remaining, random_choice=False)
        assert result == questions[0]
        assert remaining == [1]

    def test_sequential_order(self):
        questions = [{"id": i, "title": str(i), "question": "?"} for i in range(5)]
        remaining = list(range(5))
        for i in range(5):
            q = generate_new_question(questions, remaining, random_choice=False)
            assert q["id"] == i
        assert remaining == []

    def test_no_remaining_returns_none(self):
        result = generate_new_question([{"id": 1, "title": "A", "question": "?"}], [])
        assert result is None


class TestModelMap:
    def test_gemma4_is_present(self):
        assert "gemma4" in MODEL_MAP

    def test_gemma4_maps_to_ollama(self):
        assert MODEL_MAP["gemma4"] == "ollama/gemma4"

    def test_all_values_have_ollama_prefix(self):
        for key, value in MODEL_MAP.items():
            assert value.startswith("ollama/"), f"{key} -> {value} missing ollama/ prefix"
