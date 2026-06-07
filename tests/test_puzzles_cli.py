import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from puzzles_cli import (
    build_message_content,
    build_system_prompt,
    encode_image,
    get_mime_type,
    load_puzzles,
)


class TestGetMimeType:
    def test_jpg(self):
        assert get_mime_type("photo.jpg") == "image/jpeg"

    def test_jpeg(self):
        assert get_mime_type("photo.jpeg") == "image/jpeg"

    def test_png(self):
        assert get_mime_type("photo.png") == "image/png"

    def test_gif(self):
        assert get_mime_type("photo.gif") == "image/gif"

    def test_webp(self):
        assert get_mime_type("photo.webp") == "image/webp"

    def test_unknown_extension_defaults_to_jpeg(self):
        assert get_mime_type("photo.bmp") == "image/jpeg"

    def test_case_insensitive(self):
        assert get_mime_type("photo.PNG") == "image/png"
        assert get_mime_type("photo.JPG") == "image/jpeg"

    def test_path_with_directories(self):
        assert get_mime_type("images/sdevi_q33.png") == "image/png"


class TestBuildSystemPrompt:
    def test_returns_non_empty_string(self):
        prompt = build_system_prompt()
        assert isinstance(prompt, str)
        assert len(prompt) > 0

    def test_mentions_puzzle_solving(self):
        prompt = build_system_prompt()
        assert "puzzle" in prompt.lower()


class TestLoadPuzzles:
    def test_loads_all_puzzles(self):
        puzzles = load_puzzles()
        assert len(puzzles) == 150

    def test_first_puzzle_is_correct(self):
        puzzles = load_puzzles()
        assert puzzles[0]["id"] == 1
        assert "TALL" in puzzles[0]["title"]

    def test_load_from_custom_path(self, tmp_path):
        data = [{"id": 1, "title": "Test", "question": "Test question"}]
        f = tmp_path / "custom.json"
        f.write_text(json.dumps(data))
        assert load_puzzles(str(f)) == data


class TestEncodeImage:
    def test_missing_file_returns_none(self):
        assert encode_image("nonexistent.png") is None

    def test_valid_image_returns_data_url(self, tmp_path):
        img = tmp_path / "test.png"
        img.write_bytes(b"fake png content")
        result = encode_image(str(img))
        assert result.startswith("data:image/png;base64,")
        assert len(result) > len("data:image/png;base64,")


class TestBuildMessageContent:
    def test_text_only_puzzle(self):
        puzzle = {"id": 1, "title": "Test", "question": "What is 2+2?"}
        content = build_message_content(puzzle)
        assert len(content) == 1
        assert content[0]["type"] == "text"
        assert content[0]["text"] == "What is 2+2?"

    def test_puzzle_with_image(self, tmp_path):
        img = tmp_path / "test.png"
        img.write_bytes(b"fake png")
        puzzle = {"id": 1, "title": "Test", "question": "Q", "image": str(img)}
        content = build_message_content(puzzle)
        assert len(content) == 2
        assert content[0]["type"] == "image_url"
        assert content[1]["type"] == "text"

    def test_puzzle_with_missing_image_skips_image(self):
        puzzle = {"id": 1, "title": "Test", "question": "Q", "image": "missing.png"}
        content = build_message_content(puzzle)
        assert len(content) == 1
        assert content[0]["type"] == "text"

    def test_puzzle_with_empty_image_string(self):
        puzzle = {"id": 1, "title": "Test", "question": "Q", "image": ""}
        content = build_message_content(puzzle)
        assert len(content) == 1
        assert content[0]["type"] == "text"

    def test_puzzle_missing_question(self):
        puzzle = {"id": 1, "title": "Test"}
        content = build_message_content(puzzle)
        assert len(content) == 0
