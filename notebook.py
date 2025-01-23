import asyncio
import streamlit as st
import aiohttp

async def fetch_data(query: str, key: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://searchsystem.onrender.com/",
            params={"query": query, "key": key},
        ) as response:
            return await response.json()

async def main():
    # Initialize session state variables
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'gemini_key' not in st.session_state:
        st.session_state.gemini_key = None
    if 'clips' not in st.session_state:
        st.session_state.clips = None
    if 'query' not in st.session_state:
        st.session_state.query = None

    # Login Function
    def login(token, gemini_key):
        # Replace with your authentication logic
        valid_token = "admin"

        if token == valid_token:
            st.session_state.logged_in = True
            st.session_state.gemini_key = gemini_key  # Store Gemini key in session state
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

    # Show search bar only if logged in
    if st.session_state.logged_in:
        search_bar = st.text_input("Find me clips about...")

        # Reset clips and query if the user submits a new search
        if search_bar and search_bar != st.session_state.query:
            st.session_state.query = search_bar
            st.session_state.clips = None  # Reset stored clips for the new search

        if st.session_state.query:
            if st.session_state.clips is None:  # Fetch clips only if not already fetched
                with st.spinner("Searching for clips..."):
                    try:
                        st.session_state.clips = await fetch_data(st.session_state.query, st.session_state.gemini_key)
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                        st.session_state.clips = []

            # Display clips
            clips = st.session_state.clips
            if clips:
                st.success(f"Found {len(clips)} clips!")
                for idx, clip in enumerate(clips):
                    if st.button(f"{clip['start_time']} - {clip['end_time']}", key=f"clip_{idx}"):
                        st.markdown(clip['embed_link'], unsafe_allow_html=True)
                        st.write(f'**Explanation**')
                        st.write(clip['explanation'])
            else:
                st.warning("No clips found for your query.")

# Streamlit app execution
if __name__ == "__main__":
    asyncio.run(main())
