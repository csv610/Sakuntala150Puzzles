import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent

def test_puzzles_json_exists():
    assert (DATA_DIR / "puzzles.json").exists()

def test_all_150_puzzles_present():
    with open(DATA_DIR / "puzzles.json") as f:
        puzzles = json.load(f)
    assert len(puzzles) == 150

def test_puzzle_ids_are_sequential():
    with open(DATA_DIR / "puzzles.json") as f:
        puzzles = json.load(f)
    ids = [p["id"] for p in puzzles]
    assert ids == list(range(1, 151))

def test_each_puzzle_has_required_fields():
    with open(DATA_DIR / "puzzles.json") as f:
        puzzles = json.load(f)
    for p in puzzles:
        assert "title" in p, f"Puzzle {p['id']} missing title"
        assert "question" in p, f"Puzzle {p['id']} missing question"
        assert isinstance(p["title"], str) and p["title"], f"Puzzle {p['id']} has empty title"
        msg = f"Puzzle {p['id']} has empty question"
        assert isinstance(p["question"], str) and p["question"], msg

def test_no_duplicate_ids():
    with open(DATA_DIR / "puzzles.json") as f:
        puzzles = json.load(f)
    ids = [p["id"] for p in puzzles]
    assert len(ids) == len(set(ids))

def test_referenced_images_exist():
    with open(DATA_DIR / "puzzles.json") as f:
        puzzles = json.load(f)
    for p in puzzles:
        if "image" in p and p["image"]:
            img_path = DATA_DIR / p["image"]
            assert img_path.exists(), f"Missing image: {p['image']} (puzzle {p['id']})"

def test_no_duplicate_image_references():
    with open(DATA_DIR / "puzzles.json") as f:
        puzzles = json.load(f)
    image_refs = [p["image"] for p in puzzles if "image" in p and p["image"]]
    assert len(image_refs) == len(set(image_refs))

def test_all_image_formats_are_supported():
    with open(DATA_DIR / "puzzles.json") as f:
        puzzles = json.load(f)
    supported = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
    for p in puzzles:
        if "image" in p and p["image"]:
            ext = Path(p["image"]).suffix.lower()
            assert ext in supported, f"Unsupported image format {ext} in puzzle {p['id']}"

def test_prepopulated_answers_are_valid():
    with open(DATA_DIR / "puzzles.json") as f:
        puzzles = json.load(f)
    for p in puzzles:
        if "answer" in p:
            assert isinstance(p["answer"], (int, float, str))
