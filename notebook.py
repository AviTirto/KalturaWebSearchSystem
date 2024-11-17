import streamlit as st
import asyncio
import httpx

# Define an async function to fetch data
async def fetch_data(query: str):
    async with httpx.AsyncClient() as client:
        response = await client.get("http://127.0.0.1:8000/", params={"query": query})
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()

# Main async function that Streamlit will call
async def main():
    search_bar = st.text_input("Find me clips about...")

    if search_bar:
        # Display a spinner while waiting for the response
        with st.spinner("Searching for clips..."):
            try:
                # Fetch clips using the async function
                clips = await fetch_data(search_bar)

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

    # Add iframe functionality
    if st.button("Add", type="primary"):
        iframe_html = '''
        <iframe id="kaltura_player" 
            src="https://cdnapisec.kaltura.com/p/1660902/embedPlaykitJs/uiconf_id/55063162?iframeembed=true&amp;entry_id=1_rroyad0t&amp;config%5Bprovider%5D=%7B%22widgetId%22%3A%221_z2zuabgx%22%7D&amp;config%5Bplayback%5D=%7B%22startTime%22%3A240%7D" 
            style="width: 576px; height: 324px; border: 0;" 
            allowfullscreen webkitallowfullscreen mozallowfullscreen allow="autoplay *; fullscreen *; encrypted-media *" 
            title="Embedded Player">
        </iframe>
        '''
        st.markdown(iframe_html, unsafe_allow_html=True)

# Streamlit runs the main function
if __name__ == "__main__":
    # Use asyncio to run the main async function
    asyncio.run(main())
