import streamlit as st
import requests
import json

# Set up the Streamlit app
st.title("Mistral Function App UI")
st.write("This is a user-friendly interface to interact with the Mistral AI model.")

# Input text area
user_input = st.text_area("Enter your text below:", placeholder="Type something here...")

# Model settings
st.sidebar.title("Settings")
temperature = st.sidebar.slider("Set Temperature:", 0.0, 1.0, 0.7)
max_tokens = st.sidebar.number_input("Max Tokens:", min_value=1, max_value=512, value=50)

# Submit button
if st.button("Submit"):
    if not user_input:
        st.warning("Please enter some text before submitting!")
    else:
        with st.spinner("Processing..."):
            # Prepare the API request
            endpoint = "https://mistralfunctionapp123.azurewebsites.net/api/ProcessText"
            headers = {"Content-Type": "application/json"}
            payload = json.dumps({
                "input": user_input,
                "temperature": temperature,
                "max_tokens": max_tokens
            })

            try:
                response = requests.post(endpoint, headers=headers, data=payload)

                if response.status_code == 200:
                    result = response.json()
                    st.success("Response from Mistral:")
                    st.json(result)
                else:
                    st.error(f"Error from API: {response.status_code}")
                    st.error(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
