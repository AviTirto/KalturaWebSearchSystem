import sys
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory to the system path
sys.path.append(os.path.dirname(current_dir))

import streamlit as st
from api_calls import fetch_clips, fetch_slides
import asyncio
from dotenv import load_dotenv



load_dotenv()


async def main():
    tab1, tab2 = st.tabs(["Lecture Clip Search 📹", "PowerPoint Search 🎒"])

    tab1.subheader("Econ 301 Lecture Clip Search")
    tab2.subheader("Econ 301 PowerPoint Search")

    if 'clips_query' not in st.session_state:
        st.session_state.clips_query = None
    if 'clips' not in st.session_state:
        st.session_state.clips = None
    if 'slides_query' not in st.session_state:
        st.session_state.slides_query = None
    if 'slides' not in st.session_state:
        st.session_state.slides = {'titles': [], 'page_nums': [], 'texts': []}
    if 'images' not in st.session_state:
        st.session_state.images = {}
    if 'slider_value' not in st.session_state:
        st.session_state.slider_value = None

    with tab1:
        clips_search_bar = st.text_input("Find me clips about...")

        if clips_search_bar and clips_search_bar != st.session_state.clips_query:
            st.session_state.clips_query = clips_search_bar
            st.session_state.clips = None

        if st.session_state.clips_query:
            if st.session_state.clips is None:  # Fetch clips only if not already fetched
                with st.spinner("Searching for clips..."):
                    try:
                        st.session_state.clips = await fetch_clips(st.session_state.clips_query)
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

    # with tab2:
    #     loader = Loader()
    #     slides_search_bar = st.text_input("Searching for slides...")

    #     if slides_search_bar and slides_search_bar != st.session_state.slides_query:
    #         st.session_state.slides_query = slides_search_bar
        

    #         with st.spinner("Searching for slides..."):
    #             try:
    #                 response = await fetch_slides(st.session_state.slides_query)
    #                 if response:
    #                     st.session_state.slides = response  # Save valid response
    #             except Exception as e:
    #                 st.error(f"An error occurred: {e}")

    #     slides = st.session_state.slides
    #     titles = slides['titles']
    #     page_nums = slides['page_nums']
    #     texts = slides['texts'] 


    #     if titles and page_nums and texts:
    #         unique_titles = list(set(titles))  # Get unique file paths

    #         for pdf_path in unique_titles:
    #             slide_indices = [i for i, title in enumerate(titles) if title == pdf_path]

    #             # Cache images for this file if not already loaded
    #             if pdf_path not in st.session_state.images:
    #                 with st.spinner(f"Loading slides from {pdf_path}..."):
    #                     images = loader.pdf_to_images('.' + pdf_path) or []
    #                     st.session_state.images[pdf_path] = images

    #             images = st.session_state.images.get(pdf_path, [])

    #             with st.expander(pdf_path.split("/")[-1]):  # Expander for each PDF
    #                 if images:
    #                     # Default to the first slide mentioned in the search results
    #                     start_page = min([page_nums[i] for i in slide_indices])
    #                     st.session_state.slider_value = start_page if st.session_state.slider_value is None else st.session_state.slider_value

    #                     # Slider for navigating slides (now properly adjusted)
    #                     slide_number = st.slider(f"Slide from {pdf_path.split('/')[-1]}", 
    #                                             min_value=1, 
    #                                             max_value=len(images), 
    #                                             value=st.session_state.slider_value)  # Use session state slider value

    #                     # Display the selected slide image
    #                     st.image(images[slide_number - 1], caption=f"Slide {slide_number}", use_container_width=True)

    #                     # Create buttons only for slides that haven't been added already
    #                     button_displayed = set()  # To track already displayed slide page numbers
    #                     for idx, i in enumerate(slide_indices):
    #                         # Add button only if it's not already displayed for this slide
    #                         if page_nums[i] not in button_displayed:
    #                             button_key = f"button_{pdf_path}_{page_nums[i]}_{idx}"
    #                             if st.button(f"Go to Slide {page_nums[i]} from {pdf_path.split('/')[-1]}", key=button_key, help=f"Jump to Slide {page_nums[i]}"):
    #                                 st.session_state.slider_value = page_nums[i]  # Update slider value when button clicked
    #                                 button_displayed.add(page_nums[i])  # Mark this slide as having a button

    #                     # Custom CSS to style the button
    #                     st.markdown("""
    #                         <style>
    #                             .stButton>button {
    #                                 background-color: #007BFF;
    #                                 color: white;
    #                                 font-size: 16px;
    #                                 padding: 10px 20px;
    #                                 border-radius: 5px;
    #                                 box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    #                             }
    #                             .stButton>button:hover {
    #                                 background-color: #0056b3;
    #                             }
    #                         </style>
    #                         """, unsafe_allow_html=True)

    #                 # Show extracted text in a separate text area for the selected page
    #                 for i in slide_indices:
    #                     if page_nums[i] == slide_number:  # Compare correctly (1-indexed comparison)
    #                         st.text_area(f"Extracted Text from Slide {page_nums[i]}", texts[i], height=150)
    #     else:
    #         st.warning("No slides found.")



if __name__ == "__main__":
    print(f"Current Working Directory: {os.getcwd()}")
    asyncio.run(main())




