#!/usr/bin/env python3
import json
import base64

from litellm import completion
from tqdm import tqdm

def load_puzzles(filename='puzzles.json'):
    with open(filename, 'r') as f:
        return json.load(f)

def get_mime_type(image_path):
    """Get MIME type from file extension"""
    mime_types = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'webp': 'image/webp'
    }
    ext = image_path.lower().split('.')[-1]
    return mime_types.get(ext, 'image/jpeg')

def encode_image(image_path):
    """Encode image to base64 data URL"""
    with open(image_path, 'rb') as img_file:
        image_data = base64.standard_b64encode(img_file.read()).decode('utf-8')
        mime_type = get_mime_type(image_path)
        return f"data:{mime_type};base64,{image_data}"

def build_system_prompt():
    """Build system prompt for mathematical puzzle solving"""
    return """You are an expert mathematical puzzle solver.
Your task is to:
1. Carefully read and understand the mathematical puzzle
2. If an image is provided, analyze it thoroughly before answering
3. Break down the problem step by step
4. Show your reasoning and work
5. Provide a clear, concise final answer

Be precise and logical in your approach."""

def build_message_content(puzzle):
    """Build message content with text and optional image"""
    content = []

    if 'image' in puzzle and puzzle['image']:
        image_url = encode_image(puzzle['image'])
        content.append({
            "type": "image_url",
            "image_url": {"url": image_url}
        })

    if 'question' in puzzle:
        content.append({"type": "text", "text": puzzle['question']})

    return content

def get_answer(puzzle):
    """Get answer to a question using Gemini 2.5 Flash via LiteLLM"""
    try:
        content = build_message_content(puzzle)
        messages = [
            {"role": "system", "content": build_system_prompt()},
            {"role": "user", "content": content}
        ]

        response = completion(
            model="gemini-2.5-flash",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting answer: {str(e)}"

def solve_puzzles(output_filename='puzzles_answer.json'):
    """Load puzzles, get answers, and save to JSON file"""
    puzzles = load_puzzles()

    with open(output_filename, 'w') as f:
        f.write('[\n')

        for idx, puzzle in enumerate(tqdm(puzzles, desc="Processing puzzles")):
            answer_data = {
                'id': puzzle['id'],
                'title': puzzle['title'],
                'question': puzzle['question'],
                'answer': get_answer(puzzle)
            }
            json.dump(answer_data, f, indent=2)

            if idx < len(puzzles) - 1:
                f.write(',\n')
            else:
                f.write('\n')

        f.write(']')

    print(f"\nAnswers saved to {output_filename}")

if __name__ == "__main__":
    solve_puzzles()
