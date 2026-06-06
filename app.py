import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API key
API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=API_KEY)

# Streamlit page settings
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🤖",
    layout="centered"
)

# App title
st.title("🤖 AI Study Assistant")

st.markdown("""
Welcome to the AI Study Assistant!

This app can:
- Explain concepts
- Summarize text
- Generate quiz questions
""")

# Chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Feature selection
feature = st.selectbox(
    "Choose a feature:",
    [
        "Explain a Concept",
        "Summarize Text",
        "Generate Quiz Questions"
    ]
)

# User input
user_input = st.text_area(
    "Enter your text:",
    height=200,
    placeholder="Type something here..."
)

# Generate button
if st.button("Generate Response"):

    # Empty input handling
    if user_input.strip() == "":
        st.warning("⚠️ Please enter some text.")

    else:

        # Prompt engineering
        if feature == "Explain a Concept":

            prompt = f"""
            Explain the following concept in simple beginner-friendly language:

            {user_input}
            """

        elif feature == "Summarize Text":

            prompt = f"""
            Summarize the following text into short bullet points:

            {user_input}
            """

        elif feature == "Generate Quiz Questions":

            prompt = f"""
            Generate 5 quiz questions from the following text:

            {user_input}
            """

        # Loading animation
        with st.spinner("Generating AI response..."):

            try:

                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                ai_response = response.choices[0].message.content

            except Exception as e:

                ai_response = f"❌ Error: {e}"

            # Save history
            st.session_state.history.append({
                "feature": feature,
                "input": user_input,
                "response": ai_response
            })

            # Display response
            st.subheader("AI Response")
            st.markdown(ai_response)

# Display chat history
if st.session_state.history:

    st.divider()

    st.subheader("📜 Chat History")

    for chat in reversed(st.session_state.history):

        with st.expander(chat["feature"]):

            st.markdown("### User Input")
            st.write(chat["input"])

            st.markdown("### AI Response")
            st.markdown(chat["response"])