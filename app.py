import random
import streamlit as st


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

    return question, correct_answer, choices, explanation


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


st.set_page_config(page_title="Algebra Practice Tool", page_icon="⭐")

st.title("📘 Algebra Practice Tool")
st.subheader("Version 0.1: Combining Like Terms")

st.write("Enter your name and practice simplifying expressions by combining like terms.")

student_name = st.text_input("Student Name")

if "question_data" not in st.session_state:
    st.session_state.question_data = generate_combining_like_terms_question()

if student_name:
    question, correct_answer, choices, explanation = st.session_state.question_data

    st.divider()
    st.write(f"Welcome, **{student_name}**.")
    st.markdown(f"### {question}")

    student_answer = st.radio("Choose the correct answer:", choices, index=None)

    if st.button("Submit Answer"):
        if student_answer == correct_answer:
            st.success("Correct!")
        else:
            st.error("Not quite.")

        st.info(f"The correct answer is: **{correct_answer}**")
        st.write("### Explanation")
        st.write(explanation)

    if st.button("New Question"):
        st.session_state.question_data = generate_combining_like_terms_question()
        st.rerun()
else:
    st.warning("Please enter your name to begin.")