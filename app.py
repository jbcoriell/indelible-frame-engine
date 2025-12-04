import streamlit as st
from datetime import datetime
import json
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Indelible Frame", page_icon="🎬", layout="wide")

# --- CUSTOM CSS (ART DECO THEME) ---
st.markdown("""
<style>
    /* Main background - Art Deco inspired */
    .main {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2416 50%, #1a1a1a 100%);
        background-image: 
            repeating-linear-gradient(45deg, transparent, transparent 35px, rgba(218, 165, 32, 0.03) 35px, rgba(218, 165, 32, 0.03) 70px),
            linear-gradient(135deg, #1a1a1a 0%, #2d2416 50%, #1a1a1a 100%);
    }
    
    /* Sidebar - Elegant gold and black */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a1a 0%, #2a2216 100%);
        border-right: 3px solid #d4af37;
        box-shadow: 5px 0 15px rgba(212, 175, 55, 0.2);
    }
    
    /* Main title styling */
    h1 {
        color: #d4af37 !important;
        font-family: 'Didot', 'Bodoni MT', serif !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
        letter-spacing: 3px;
        border-bottom: 2px solid #d4af37;
        padding-bottom: 10px;
    }
    
    /* Subtitles */
    h2, h3, h4 {
        color: #f5f5dc !important;
        font-family: 'Didot', 'Bodoni MT', serif !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
    }
    
    /* Text color */
    p, span, label, div {
        color: #f5f5dc !important;
    }
    
    /* Input boxes - Art Deco style */
    .stTextInput > div > div > input {
        background-color: rgba(26, 26, 26, 0.8) !important;
        color: #f5f5dc !important;
        border: 2px solid #d4af37 !important;
        border-radius: 0px !important;
        font-family: 'Garamond', serif !important;
        box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.5);
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background-color: rgba(26, 26, 26, 0.8) !important;
        color: #f5f5dc !important;
        border: 2px solid #d4af37 !important;
        border-radius: 0px !important;
    }
    
    /* Buttons - Hollywood glamour */
    .stButton > button {
        background: linear-gradient(135deg, #d4af37 0%, #c9a829 100%) !important;
        color: #1a1a1a !important;
        border: none !important;
        border-radius: 0px !important;
        font-weight: bold !important;
        font-family: 'Didot', serif !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        box-shadow: 0 4px 8px rgba(212, 175, 55, 0.4) !important;
        transition: all 0.3s ease !important;
        padding: 12px 24px !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #ffd700 0%, #d4af37 100%) !important;
        box-shadow: 0 6px 12px rgba(212, 175, 55, 0.6) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Primary button (Search button) */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #b8860b 0%, #d4af37 100%) !important;
        border: 2px solid #ffd700 !important;
    }
    
    /* Containers/Cards - Art Deco frames */
    [data-testid="stVerticalBlock"] > div > div[data-testid="stContainer"] {
        background: linear-gradient(135deg, rgba(26, 26, 26, 0.95) 0%, rgba(45, 36, 22, 0.95) 100%) !important;
        border: 3px solid #d4af37 !important;
        border-radius: 0px !important;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.6), inset 0 0 20px rgba(212, 175, 55, 0.1) !important;
        padding: 20px !important;
        position: relative;
    }
    
    /* Add decorative corner elements to containers */
    [data-testid="stVerticalBlock"] > div > div[data-testid="stContainer"]::before,
    [data-testid="stVerticalBlock"] > div > div[data-testid="stContainer"]::after {
        content: "◆";
        position: absolute;
        color: #d4af37;
        font-size: 16px;
    }
    
    [data-testid="stVerticalBlock"] > div > div[data-testid="stContainer"]::before {
        top: 10px;
        left: 10px;
    }
    
    [data-testid="stVerticalBlock"] > div > div[data-testid="stContainer"]::after {
        top: 10px;
        right: 10px;
    }
    
    /* Tabs - Art Deco style */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(26, 26, 26, 0.6);
        border-bottom: 3px solid #d4af37;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #c0c0c0 !important;
        background-color: transparent;
        border: none;
        font-family: 'Didot', serif !important;
        letter-spacing: 2px;
        padding: 15px 30px;
    }
    
    .stTabs [aria-selected="true"] {
        color: #d4af37 !important;
        background: linear-gradient(180deg, transparent 0%, rgba(212, 175, 55, 0.2) 100%);
        border-bottom: 4px solid #d4af37 !important;
    }
    
    /* Links - Gold accent */
    a {
        color: #d4af37 !important;
        text-decoration: none !important;
        transition: all 0.3s ease;
    }
    
    a:hover {
        color: #ffd700 !important;
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.6);
    }
    
    /* Divider lines */
    hr {
        border-color: #d4af37 !important;
        opacity: 0.3;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #d4af37 !important;
    }
    
    /* Caption text */
    .caption {
        color: #c0c0c0 !important;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'boards' not in st.session_state:
    st.session_state.boards = ['1860s Ireland', 'Sci-Fi Dystopia']
    st.session_state.current_board = '1860s Ireland'
    st.session_state.pinned_items = {}
    st.session_state.search_results = []
    st.session_state.selected_items = set()

# --- HELPER FUNCTIONS ---

def generate_demo_results(query, content_type):
    """Fallback demo results with realistic direct URLs"""
    search_query = query.replace(' ', '+')
    
    all_results = {
        "images": [
            {"id": "1", "title": f"{query} - Library of Congress", "url": f"https://www.loc.gov/pictures/?q={search_query}", "description": "Historical photographs from the LOC archive", "type": "image"},
            {"id": "2", "title": f"{query} - V&A Museum", "url": f"https://collections.vam.ac.uk/search/?q={search_query}", "description": "Museum collection images", "type": "image"},
            {"id": "3", "title": f"{query} - Getty Images", "url": f"https://www.gettyimages.com/photos/{search_query}", "description": "Historical photography collection", "type": "image"},
            {"id": "4", "title": f"{query} - Wikimedia Commons", "url": f"https://commons.wikimedia.org/w/index.php?search={search_query}", "description": "Free historical images", "type": "image"},
        ],
        "articles": [
            {"id": "5", "title": f"{query} - History Extra", "url": f"https://www.historyextra.com/?s={search_query}", "description": "Historical analysis", "type": "article"},
            {"id": "6", "title": f"{query} - Britannica", "url": f"https://www.britannica.com/search?query={search_query}", "description": "Encyclopedia entry", "type": "article"},
            {"id": "7", "title": f"{query} - Smithsonian Mag", "url": f"https://www.smithsonianmag.com/?s={search_query}", "description": "Cultural articles", "type": "article"},
        ],
        "videos": [
            {"id": "8", "title": f"{query} - Documentary", "url": f"https://www.youtube.com/results?search_query={search_query}+documentary", "description": "Full-length documentary", "type": "video"},
            {"id": "9", "title": f"{query} - British Pathé", "url": f"https://www.youtube.com/c/britishpathe/search?query={search_query}", "description": "Historical newsreels", "type": "video"},
        ],
        "pdfs": [
            {"id": "10", "title": f"{query} - Google Scholar", "url": f"https://scholar.google.com/scholar?q={search_query}", "description": "Academic papers", "type": "pdf"},
            {"id": "11", "title": f"{query} - JSTOR", "url": f"https://www.jstor.org/action/doBasicSearch?Query={search_query}", "description": "Journal articles", "type": "pdf"},
        ]
    }
    
    if content_type == "all":
        results = []
        for key in all_results:
            results.extend(all_results[key])
        return results
    else:
        return all_results.get(content_type, all_results["articles"])

def search_with_ai(query, content_type):
    """
    Simulated AI Search - In a real deployment, 
    this would use the Anthropic API code you had earlier.
    For the class demo, we use the robust demo generator to ensure it always works.
    """
    # NOTE: If you have a working API key, uncomment the Anthropic code block here.
    # For now, we return demo results to guarantee the UI works.
    return generate_demo_results(query, content_type)


# --- SIDEBAR (BOARD MANAGEMENT) ---
with st.sidebar:
    st.title("🎬 INDELIBLE FRAME")
    st.caption("✦ Research Engine ✦")
    st.divider()
    
    st.subheader("⬥ Project Boards")
    # This stores the user's choice in session state
    board_choice = st.selectbox("Select Board", st.session_state.boards, label_visibility="collapsed")
    st.session_state.current_board = board_choice
    
    st.write("") # Spacer
    new_board_name = st.text_input("Create New Board", placeholder="Name...")
    if st.button("➕ Create Board") and new_board_name:
        if new_board_name not in st.session_state.boards:
            st.session_state.boards.append(new_board_name)
            st.rerun()
    
    # If items are selected in the main view, show the "Pin" buttons here
    if st.session_state.selected_items:
        st.divider()
        st.write(f"**✦ {len(st.session_state.selected_items)} Items Selected**")
        st.caption("Pin selection to:")
        
        for b in st.session_state.boards:
            if st.button(f"📌 {b}", key=f"pin_btn_{b}"):
                # Find the full item details for the selected IDs
                items_to_pin = [r for r in st.session_state.search_results if r['id'] in st.session_state.selected_items]
                
                # Initialize list if board is empty
                if b not in st.session_state.pinned_items:
                    st.session_state.pinned_items[b] = []
                
                # Add items to the board
                count = 0
                for item in items_to_pin:
                    # Check if already pinned to avoid duplicates
                    current_urls = [x['url'] for x in st.session_state.pinned_items[b]]
                    if item['url'] not in current_urls:
                        st.session_state.pinned_items[b].append({
                            'title': item['title'], 
                            'url': item['url'], 
                            'type': item['type'],
                            'description': item.get('description', ''), 
                            'added': datetime.now().strftime("%Y-%m-%d")
                        })
                        count += 1
                
                st.success(f"Pinned {count} items to {b}!")
                # Clear selection after pinning
                st.session_state.selected_items.clear()
                st.rerun()

# --- MAIN PAGE LAYOUT ---

st.title("THE INDELIBLE FRAME")
st.markdown("### *Deconstructing Emotional Impact in Film & Media*")

# Create Tabs for the two main modes
tab1, tab2 = st.tabs(["🔍 RESEARCH AGENT", "📌 MY COLLECTIONS"])

# --- TAB 1: SEARCH INTERFACE ---
with tab1:
    st.write("")
    st.markdown("#### ⬥ AI Research Assistant")
    
    # Search Bar Layout
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input(
            "Search Query", 
            placeholder="e.g., 1860s Ireland fashion, Sci-Fi corridor lighting...", 
            label_visibility="collapsed"
        )
    with col2:
        content_type = st.selectbox(
            "Type",
            ["all", "images", "articles", "videos", "pdfs"],
            format_func=lambda x: {
                "all": "📚 All Types",
                "images": "🖼️ Images",
                "articles": "📄 Articles", 
                "videos": "🎬 Videos",
                "pdfs": "📕 PDFs"
            }[x],
            label_visibility="collapsed"
        )

    # Search Button
    if st.button("⬥ SEARCH WITH AI ⬥", type="primary", use_container_width=True):
        if query:
            with st.spinner(f"✦ Searching for {content_type}..."):
                st.session_state.search_results = search_with_ai(query, content_type)
                st.session_state.selected_items.clear() # Clear old selections on new search
                st.rerun()

    # Display Results
    if st.session_state.search_results:
        st.divider()
        st.subheader(f"✦ Found {len(st.session_state.search_results)} Sources")
        
        for result in st.session_state.search_results:
            with st.container(border=True):
                r_col1, r_col2 = st.columns([5, 1])
                
                with r_col1:
                    emoji_map = {'article': '📄', 'image': '🖼️', 'video': '🎬', 'pdf': '📕'}
                    icon = emoji_map.get(result['type'], '📄')
                    st.markdown(f"#### {icon} [{result['title']}]({result['url']})")
                    st.caption(result.get('description', ''))
                    
                with r_col2:
                    # Checkbox for selection
                    is_checked = result['id'] in st.session_state.selected_items
                    if st.checkbox("Select", value=is_checked, key=f"select_{result['id']}"):
                        st.session_state.selected_items.add(result['id'])
                    else:
                        st.session_state.selected_items.discard(result['id'])

# --- TAB 2: COLLECTIONS (PINTEREST BOARD VIEW) ---
with tab2:
    st.write("")
    current_b = st.session_state.current_board
    st.header(f"📂 PROJECT: {current_b.upper()}")
    
    saved_items = st.session_state.pinned_items.get(current_b, [])
    
    if not saved_items:
        st.info(f"This board is empty. Go to the 'Research Agent' tab to find and pin items to **{current_b}**.")
    else:
        st.write(f"*{len(saved_items)} Pins in this collection*")
        st.divider()
        
        # Grid Layout for Pins
        cols = st.columns(3)
        for idx, item in enumerate(saved_items):
            with cols[idx % 3]:
                with st.container(border=True):
                    emoji_map = {'article': '📄', 'image': '🖼️', 'video': '🎬', 'pdf': '📕'}
                    icon = emoji_map.get(item['type'], '📄')
                    
                    st.markdown(f"**{icon} {item['title']}**")
                    st.caption(f"Added: {item['added']}")
                    st.write(item.get('description', ''))
                    st.markdown(f"[⬥ Open Link]({item['url']})")
