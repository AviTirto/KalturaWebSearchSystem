import streamlit as st

if st.button("Add", type="primary"):
    oembed_url = "https://mediaspace.wisc.edu/media/Tyler%20Caraza-Harter-Noland%20132-09_13_23-13%3A17%3A00/1_rroyad0t"

    # Embed the video using markdown and iframe
    iframe_html = f'''
    <iframe id="kaltura_player" src='https://cdnapisec.kaltura.com/p/1660902/embedPlaykitJs/uiconf_id/55063162?iframeembed=true&amp;entry_id=1_rroyad0t&amp;config%5Bprovider%5D=%7B%22widgetId%22%3A%221_z2zuabgx%22%7D&amp;config%5Bplayback%5D=%7B%22startTime%22%3A240%7D'  style="width: 576px;height: 324px;border: 0;" allowfullscreen webkitallowfullscreen mozAllowFullScreen allow="autoplay *; fullscreen *; encrypted-media *"  title="Tyler Caraza-Harter-Noland 132-09/13/23-13:17:00"></iframe>
    '''

    st.markdown(iframe_html, unsafe_allow_html=True)