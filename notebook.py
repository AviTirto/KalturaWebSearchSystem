import asyncio
import httpx
import streamlit as st
import requests
import aiohttp

async def fetch_data(query: str, key: str):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://searchsystem.onrender.com/", params={"query": query, "key": key}) as response:
            return await response.json()

async def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # Login Function
    def login(token, gemini_key):
        # Add your authentication logic here
        valid_token = "my_secure_token"  # Replace with your token validation logic
        valid_gemini_key = "my_gemini_key"  # Replace with your key validation logic

        if token == valid_token and gemini_key == valid_gemini_key:
            st.session_state.logged_in = True
            st.success("Login successful!")
        else:
            st.error("Invalid token or Gemini key. Please try again.")

    # Display Login Popup if not logged in
    if not st.session_state.logged_in:
        st.title("Login Required")
        with st.form("login_form"):
            token = st.text_input("Enter your Token", type="password")
            gemini_key = st.text_input("Enter your Gemini Key", type="password")
            submitted = st.form_submit_button("Login")
            
            if submitted:
                login(token, gemini_key)

    search_bar = st.text_input("Find me clips about...")

    if search_bar:
        # Display a spinner while waiting for the response
        with st.spinner("Searching for clips..."):
            try:
                # Fetch clips using the async function only once
                if "clips" not in st.session_state:  # Check if clips data is already stored
                    clips = await fetch_data(search_bar)
                    st.session_state.clips = clips  # Store the clips in session state
                else:
                    clips = st.session_state.clips  # Use stored clips
                
                # Handle the response
                if clips:
                    st.success(f"Found {len(clips)} clips!")
                    for clip in clips:
                        if st.button(f"{clip['start_time']} - {clip['end_time']}", use_container_width=True):
                            st.markdown(clip['embed_link'], unsafe_allow_html=True)
                else:
                    st.warning("No clips found for your query.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Streamlit app execution
if __name__ == "__main__":
    asyncio.run(main())