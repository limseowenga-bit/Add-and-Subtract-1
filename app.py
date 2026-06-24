import random
import streamlit as st

# Set up the page with a fun title and icon
st.set_page_config(page_title="Math Wizards!", page_icon="🧮", layout="centered")

# --- Custom Styling for Kids ---
st.markdown(
    """
    <style>
    .big-title { font-size: 40px !important; font-weight: bold; color: #FF4B4B; text-align: center; }
    .score-box { font-size: 24px !important; font-weight: bold; color: #1E88E5; text-align: center; background-color: #E3F2FD; padding: 10px; border-radius: 10px; }
    .question-box { font-size: 48px !important; font-weight: bold; text-align: center; margin: 20px 0; color: #2E7D32; }
    </style>
    """,
    unsafe_style_allowed=True,
)

st.markdown("<div class='big-title'>✨ Math Wizards! ✨</div>", unsafe_style_allowed=True)
st.write("### Can you solve the mystery math puzzles? Let's find out!")
st.write("---")

# --- Initialize Game State ---
if "score" not in st.session_state:
    st.session_state.score = 0
if "total_questions" not in st.session_state:
    st.session_state.total_questions = 0
if "num1" not in st.session_state:
    # First time setup
    st.session_state.operation = random.choice(["+", "-"])
    if st.session_state.operation == "+":
        st.session_state.num1 = random.randint(0, 10)
        st.session_state.num2 = random.randint(0, 10 - st.session_state.num1)  # Ensure sum <= 10
    else:
        st.session_state.num1 = random.randint(0, 10)
        st.session_state.num2 = random.randint(0, st.session_state.num1)  # Ensure no negative results

# --- Helper Function to Generate a New Question ---
def next_question():
    st.session_state.operation = random.choice(["+", "-"])
    if st.session_state.operation == "+":
        st.session_state.num1 = random.randint(0, 10)
        st.session_state.num2 = random.randint(0, 10 - st.session_state.num1)
    else:
        st.session_state.num1 = random.randint(0, 10)
        st.session_state.num2 = random.randint(0, st.session_state.num1)
    # Clear the text input field by resetting its key if needed, or letting form handling take care of it
    if "user_answer" in st.session_state:
        st.session_state.user_answer = ""

# --- Display Score ---
st.markdown(
    f"<div class='score-box'>🏆 Score: {st.session_state.score} / {st.session_state.total_questions}</div>",
    unsafe_style_allowed=True,
)

# --- Display Current Question ---
n1 = st.session_state.num1
n2 = st.session_state.num2
op = st.session_state.operation

st.markdown(f"<div class='question-box'>{n1} {op} {n2} = ?</div>", unsafe_style_allowed=True)

# --- Answer Form ---
# Using a form so pressing "Enter" or clicking "Submit" handles the logic neatly
with st.form(key="math_form", clear_on_submit=True):
    user_input = st.number_input("Type your answer here:", min_value=0, max_value=20, step=1, format="%d")
    submit_button = st.form_submit_button(label="Submit Answer! 🚀")

if submit_button:
    st.session_state.total_questions += 1
    
    # Calculate correct answer
    if op == "+":
        correct_answer = n1 + n2
        explanation_visual = "🍎" * n1 + "  +  " + "🍎" * n2
    else:
        correct_answer = n1 - n2
        explanation_visual = "🍏" * n1 + f" (take away {n2})"

    # Check Answer
    if user_input == correct_answer:
        st.balloons()
        st.success(f"🎉 Correct! Amazing job! {n1} {op} {n2} is exactly {correct_answer}!")
        st.session_state.score += 1
    else:
        st.error(f"💥 Not quite! Let's look at it together.")
        if op == "+":
            st.info(f"**Explanation:**\n\nIf you have {n1} apples: { '🍎' * n1 }\n\nAnd you add {n2} more: { '🍎' * n2 }\n\nCount them all together to get **{correct_answer}**!")
        else:
            remaining = n1 - n2
            st.info(f"**Explanation:**\n\nYou start with {n1} apples: { '🍏' * n1 }\n\nCross out {n2} of them... You have **{remaining}** left over!")

    # Add a button to move to the next question
    st.button("Next Question ➡️", on_click=next_question)

# --- Reset Game Option ---
st.write("---")
if st.button("Reset Game 🔄"):
    st.session_state.score = 0
    st.session_state.total_questions = 0
    next_question()
    st.rerun()
