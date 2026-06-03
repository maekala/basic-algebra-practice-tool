import random
import streamlit as st

def format_expression(x_coefficient, constant):
    if x_coefficient == 0:
        return str(constant)

    if x_coefficient == 1:
        x_part = "x"
    elif x_coefficient == -1:
        x_part = "-x"
    else:
        x_part = f"{x_coefficient}x"

    if constant == 0:
        return x_part
    elif constant > 0:
        return f"{x_part} + {constant}"
    else:
        return f"{x_part} - {abs(constant)}"

def generate_combining_like_terms_question():
    a = random.randint(2, 9)
    b = random.randint(1, 9)
    c = random.randint(1, 8)
    d = random.randint(1, 9)

    # Question: ax + b - cx + d
    x_coefficient = a - c
    constant = b + d

    question = f"Simplify: {a}x + {b} - {c}x + {d}"

    correct_answer = format_expression(x_coefficient, constant)

    choices = list(set([
        correct_answer,
        format_expression(a + c, constant),
        format_expression(x_coefficient, b - d),
        format_expression(a + c, b + d),
    ]))

    while len(choices) < 4:
        fake_x = random.randint(-5, 12)
        fake_constant = random.randint(-10, 20)
        choices.append(format_expression(fake_x, fake_constant))
        choices = list(set(choices))

    random.shuffle(choices)

    explanation = (
        f"Combine the x-terms: {a}x - {c}x = {x_coefficient}x\n\n"
        f"Combine the constants: {b} + {d} = {constant}\n\n"
        f"Final answer: {correct_answer}"
    )

    return {
        "skill": "Combining Like Terms",
        "question": question,
        "correct_answer": correct_answer,
        "choices": choices,
        "explanation": explanation,
    }


def start_new_question():
    st.session_state.question_data = generate_combining_like_terms_question()
    st.session_state.answered = False
    st.session_state.selected_answer = None

st.set_page_config(page_title="Algebra Practice Tool", page_icon="⭐")

st.title("⭐ Algebra Practice Tool")
st.subheader("Version 0.2: Combining Like Terms")

st.write("Practice simplifying expressions by combining like terms.")

if "question_data" not in st.session_state:
    st.session_state.question_data = generate_combining_like_terms_question()

if "answered" not in st.session_state:
    st.session_state.answered = False

if "correct_count" not in st.session_state:
    st.session_state.correct_count = 0

if "total_answered" not in st.session_state:
    st.session_state.total_answered = 0

if "student_name" not in st.session_state:
    st.session_state.student_name = ""

student_name = st.text_input("Student Name", value=st.session_state.student_name)

if student_name:
    st.session_state.student_name = student_name

    question_data = st.session_state.question_data

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Student", student_name)

    with col2:
        st.metric("Questions Answered", st.session_state.total_answered)

    with col3:
        if st.session_state.total_answered == 0:
            accuracy = 0
        else:
            accuracy = round(
                st.session_state.correct_count / st.session_state.total_answered * 100
            )
        st.metric("Accuracy", f"{accuracy}%")

    st.markdown(f"### {question_data['question']}")

    selected_answer = st.radio(
        "Choose the correct answer:",
        question_data["choices"],
        index=None,
        disabled=st.session_state.answered,
    )

    if st.button("Submit Answer", disabled=st.session_state.answered):
        if selected_answer is None:
            st.warning("Please choose an answer before submitting.")
        else:
            st.session_state.answered = True
            st.session_state.selected_answer = selected_answer
            st.session_state.total_answered += 1

            if selected_answer == question_data["correct_answer"]:
                st.session_state.correct_count += 1

            st.rerun()

    if st.session_state.answered:
        if st.session_state.selected_answer == question_data["correct_answer"]:
            st.success("Correct!")
        else:
            st.error("Not quite.")

        st.info(f"The correct answer is: **{question_data['correct_answer']}**")

        st.write("### Explanation")
        st.write(question_data["explanation"])

        if st.button("New Question"):
            start_new_question()
            st.rerun()

    st.divider()

    if st.session_state.total_answered > 0:
        st.write("### Session Summary")
        st.write(
            f"{student_name} has answered "
            f"{st.session_state.total_answered} question(s) with "
            f"{st.session_state.correct_count} correct."
        )

        if accuracy < 70:
            st.warning("Keep practicing. This skill may need more review.")
        elif accuracy < 90:
            st.info("Good progress. A little more practice could help.")
        else:
            st.success("Strong work on this skill!")

else:
    st.warning("Please enter your name to begin.")