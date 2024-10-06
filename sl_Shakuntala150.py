import json
import os
import random

import streamlit as st
from llama_model import LlamaModel

# Load questions from a JSON file
@st.cache_data
def load_questions():
    with open('puzzles.json', 'r') as f:
        questions = json.load(f)
    return questions
    
@st.cache_data
def get_llm_model(model_name):
    return LlamaModel(model_name)

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

    model_names = ['llama3.2', 'llama3.1', 'gemma2']
    model_name = st.sidebar.selectbox('Select a model', model_names)

    # Load questions (assuming this function is defined elsewhere)
    questions = load_questions()  # This should return a list of 150 questions
     
    st.sidebar.write(f"Total questions: {len(questions)}")

    llm = get_llm_model(model_name)

    # Initialize the remaining questions list
    if 'remaining_questions' not in st.session_state:
        st.session_state.remaining_questions = initialize_remaining_questions(len(questions))

    # Option to choose between random (True) or sequential (False) question
    random_choice = st.sidebar.checkbox("Random Question", value=True)  # Default to True 

    # Add a button to generate a new question
    if st.sidebar.button("New Question"):
        st.session_state.question = generate_new_question(questions, st.session_state.remaining_questions, random_choice)  # Store in session state
        st.session_state.answer = None  # Reset answer when a new question is generated
        if st.session_state.question is None:
            st.write("No more questions available.")
            # Ask the user if they want to start over
            if st.button("Start Over"):
                st.session_state.remaining_questions = initialize_remaining_questions(len(questions))  # Reset remaining questions
                st.write("You can start asking questions again!")

    # Display the current question if it exists
    if st.session_state.question is not None:
        # Display the question text
        st.write(f"**Question#** {st.session_state.question['id']}")
        st.write(f"{st.session_state.question['question']}")

        # Check if there is an image associated with the question
        if 'image' in st.session_state.question and st.session_state.question['image']:
            st.image(st.session_state.question['image'], caption='Question Image', use_column_width=True)

        # Create an "Ask LLM" button for the selected question
        if st.button("Ask LLM"):
            with st.spinner("Generating answer..."):  # Start spinner
                st.session_state.answer = llm.get_response(st.session_state.question['question'])  # Store answer in session state
    
    if st.session_state.answer is not None:
        st.write(f"**Answer:** {st.session_state.answer}")  # Ensure the answer is displayed

# Assuming this is the entry point for the Streamlit app
if __name__ == "__main__":
    main()

