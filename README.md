# Sakuntala 150 Puzzles

A command-line tool that solves mathematical puzzles using Google's Gemini 2.5 Flash AI model.

## Overview

This project reads mathematical puzzles from a JSON file and uses the Gemini 2.5 Flash API (via LiteLLM) to generate solutions. The answers are then saved to a JSON file for easy reference.

## Features

- Loads puzzles from `puzzles.json`
- Supports image-based puzzles (embedded as base64)
- Uses Google's Gemini 2.5 Flash model for solving
- Displays progress with a progress bar (tqdm)
- Saves answers to `puzzles_answer.json`

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Google API key:
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```

## Usage

Run the script to process all puzzles and save answers:

```bash
python puzzles_cli.py
```

This will:
1. Load puzzles from `puzzles.json`
2. Process each puzzle with Gemini AI
3. Save the results to `puzzles_answer.json`

## File Structure

- `puzzles.json` - Input file containing puzzles with the following structure:
  ```json
  [
    {
      "id": 1,
      "title": "Puzzle Title",
      "question": "Puzzle description",
      "image": "path/to/image.png" (optional)
    }
  ]
  ```

- `puzzles_answer.json` - Output file containing puzzles with AI-generated answers:
  ```json
  [
    {
      "id": 1,
      "title": "Puzzle Title",
      "question": "Puzzle description",
      "answer": "AI-generated answer"
    }
  ]
  ```

## Configuration

The script uses LiteLLM to communicate with the Gemini API. Ensure your API credentials are properly configured before running.
