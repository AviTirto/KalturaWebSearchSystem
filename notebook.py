import asyncio
import httpx
import streamlit as st
import requests
import aiohttp

async def fetch_data(query: str):
    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:8000/", params={"query": query}) as response:
            return await response.json()

async def main():
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