import streamlit as st
from api_calls import fetch_clips
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

async def main():
    tab1, tab2 = st.tabs(["Lecture Clip Search 📹", "PowerPoint Search 🎒"])

    tab1.subheader("Econ 301 Lecture Clip Search")
    tab2.subheader("Econ 301 PowerPoint Search")

    if 'clips_query' not in st.session_state:
        st.session_state.clips_query = None
    if 'clips' not in st.session_state:
            st.session_state.clips = None

    with tab1:
        clips_search_bar = st.text_input("Find me clips about...")

        if clips_search_bar and clips_search_bar != st.session_state.clips_query:
            st.session_state.clips_query = clips_search_bar
            st.session_state.clips = None

        if st.session_state.clips_query:
            if st.session_state.clips is None:  # Fetch clips only if not already fetched
                with st.spinner("Searching for clips..."):
                    try:
                        st.session_state.clips = await fetch_clips(st.session_state.clips_query, os.getenv('GEMINI_API_KEY'))
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                        st.session_state.clips = []

            clips = st.session_state.clips
            if clips:
                st.success(f"Found {len(clips)} clips!")
                for idx, clip in enumerate(clips):
                    with st.expander(f"{clip['start_time']} - {clip['end_time']}"):
                        st.markdown(clip['embed_link'], unsafe_allow_html=True)
                        st.write(f'**Explanation**')
                        st.write(clip['explanation'])
            else:
                st.warning("No clips found for your query.")

if __name__ == "__main__":
    asyncio.run(main())

