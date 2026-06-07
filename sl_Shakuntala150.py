import json
import random

import streamlit as st
import vlc
from gtts import gTTS
from litellm import completion

# Map short names to LiteLLM model identifiers
MODEL_MAP = {
    'gemma4': 'ollama/gemma4',
    'llama3.2': 'ollama/llama3.2',
    'llama3.1': 'ollama/llama3.1',
    'gemma2': 'ollama/gemma2',
}

@st.cache_data
def load_questions():
    with open('puzzles.json') as f:
        questions = json.load(f)
    return questions

def initialize_remaining_questions(num_questions):
    """Initialize a list of remaining question indices."""
    return list(range(num_questions))  # Use a list to store indices

def generate_new_question(questions, remaining_questions, random_choice=True):
    """Generate a new question from the remaining questions."""
    if remaining_questions:
        if random_choice:
            # Select a random index from the remaining questions
            random_index = random.choice(remaining_questions)
            remaining_questions.remove(random_index)  # Remove the index from remaining questions
        else:
            # Select the first available question sequentially
            random_index = remaining_questions.pop(0)  # Get and remove the first available index

        selected_question = questions[random_index]
        return selected_question
    else:
        return None

def text_to_speech(text: str):
    """Convert text to speech and play it using VLC."""
    if not text:  # Check if the text is empty
        raise ValueError("Text cannot be empty.")

    tts = gTTS(text=text, lang='en')
    tts.save("answer.mp3")

    # Play the audio using VLC
    player = vlc.MediaPlayer("answer.mp3")
    player.play()

def reset_questions():
    """Reset the question and answer in session state."""
    st.session_state.question = None  # Reset question in session state
    st.session_state.answer = None  # Reset answer in session state

def main():
    st.sidebar.title("Shakuntala Puzzles")

    # Initialize a list to keep track of asked questions
    if 'question' not in st.session_state:
        st.session_state.question = None  # Initialize question in session state
    if 'answer' not in st.session_state:
        st.session_state.answer = None  # Initialize answer in session state

    model_names = list(MODEL_MAP.keys())
    default_idx = model_names.index('gemma4')
    model_name = st.sidebar.selectbox('Select a model', model_names, index=default_idx)

    questions = load_questions()

    st.sidebar.write(f"Total questions: {len(questions)}")

    # Initialize the remaining questions list
    if 'remaining_questions' not in st.session_state:
        st.session_state.remaining_questions = initialize_remaining_questions(len(questions))

    # Option to choose between random (True) or sequential (False) question
    random_choice = st.sidebar.checkbox("Random Question", value=True)  # Default to True

    # Add a button to generate a new question
    if st.sidebar.button("New Question"):
        remaining = st.session_state.remaining_questions
        st.session_state.question = generate_new_question(questions, remaining, random_choice)
        st.session_state.answer = None  # Reset answer when a new question is generated
        if st.session_state.question is None:
            st.write("No more questions available.")
            # Ask the user if they want to start over
            if st.button("Start Over"):
                n = len(questions)
                st.session_state.remaining_questions = initialize_remaining_questions(n)
                st.write("You can start asking questions again!")

    # Display the current question if it exists
    if st.session_state.question is not None:
        # Display the question text
        st.write(f"**Question#** {st.session_state.question['id']}")
        st.write(f"{st.session_state.question['question']}")

        # Check if there is an image associated with the question
        if 'image' in st.session_state.question and st.session_state.question['image']:
            img = st.session_state.question['image']
            st.image(img, caption='Question Image', use_column_width=True)

        # Create an "Ask LLM" button for the selected question
        enable_tts = st.checkbox("Read aloud", value=False)
        if st.button("Ask LLM"):
            with st.spinner("Generating answer..."):
                try:
                    response = completion(
                        model=MODEL_MAP[model_name],
                        messages=[
                            {
                                "role": "system",
                                "content": "Solve the puzzle step by step. Be precise.",
                            },
                            {"role": "user", "content": st.session_state.question['question']}
                        ]
                    )
                    st.session_state.answer = response.choices[0].message.content
                except Exception as e:
                    st.session_state.answer = f"Error: {e}"
                answer = st.session_state.answer
                if enable_tts and answer and not answer.startswith("Error:"):
                    try:
                        text_to_speech(st.session_state.answer)
                    except Exception as e:
                        st.warning(f"Text-to-speech failed: {e}")

    if st.session_state.answer is not None:
        st.write(f"**Answer:** {st.session_state.answer}")  # Ensure the answer is displayed

# Assuming this is the entry point for the Streamlit app
if __name__ == "__main__":
    main()

