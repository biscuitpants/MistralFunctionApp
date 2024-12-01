import streamlit as st
import requests

# Set page configuration
st.set_page_config(page_title="MistralMind: A Conversational AI App", layout="centered")

# Display the logo
st.image("mistral_logo.png", width=200)

# App Title and Description
st.title("MistralMind: A Conversational AI App")
st.markdown(
    """
    ### MistralMind is a serverless conversational AI application powered by Mistral's cutting-edge LLM technology, hosted on Azure.
    Built with ❤️ for conversational excellence.
    """
)

# API Configuration
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_API_KEY = "3si9UxhIFCU8I10T3MRBunmzjTKayLlX"

# Input Section
st.markdown("#### Enter your query below:")
user_input = st.text_input(label="", placeholder="Type your question here...")

# Output Section
if st.button("Submit"):
    if user_input.strip() == "":
        st.error("Please enter text to ask Mistral.")
    else:
        # Prepare API Request
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "open-mistral-7b",
            "messages": [{"role": "user", "content": user_input}]
        }

        # Make API Call
        try:
            response = requests.post(MISTRAL_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()

            # Display Result
            st.markdown("### Mistral's Response:")
            st.write(result["choices"][0]["message"]["content"])
        except Exception as e:
            st.error(f"An error occurred: {e}")
