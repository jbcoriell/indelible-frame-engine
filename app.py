import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Indelible Frame", page_icon="🎬", layout="wide")

if 'boards' not in st.session_state:
    st.session_state.boards = ['1860s Ireland', 'Sci-Fi Dystopia']
    st.session_state.current_board = '1860s Ireland'
    st.session_state.pinned_items = {}
    st.session_state.search_results = []
    st.session_state.selected_items = set()

def generate_results(query):
    return [
        {"id": "1", "title": f"{query} - Historical Archive", "url": "https://historyextra.com", "description": "Comprehensive historical documentation", "type": "article"},
        {"id": "2", "title": f"Visual Guide: {query}", "url": "https://vam.ac.uk", "description": "Museum collection with photographs", "type": "image"},
        {"id": "3", "title": f"{query} Research Paper", "url": "https://jstor.org", "description": "Academic research with citations", "type": "pdf"},
        {"id": "4", "title": f"Documentary: {query}", "url": "https://youtube.com", "description": "Educational video", "type": "video"},
    ]

with st.sidebar:
    st.title("🎬 Indelible Frame")
    st.divider()
    
    board = st.selectbox("Project Boards", st.session_state.boards)
    st.session_state.current_board = board
    
    new = st.text_input("New board name")
    if st.button("Create") and new:
        st.session_state.boards.append(new)
        st.rerun()
    
    if st.session_state.selected_items:
        st.write(f"**{len(st.session_state.selected_items)} selected**")
        for b in st.session_state.boards:
            if st.button(f"Pin to {b}", key=f"pin_{b}"):
                items = [r for r in st.session_state.search_results if r['id'] in st.session_state.selected_items]
                if b not in st.session_state.pinned_items:
                    st.session_state.pinned_items[b] = []
                for item in items:
                    st.session_state.pinned_items[b].append({
                        'title': item['title'], 'url': item['url'], 'type': item['type'],
                        'description': item['description'], 'added': datetime.now().strftime('%Y-%m-%d')
                    })
                st.session_state.selected_items.clear()
                st.success("Pinned!")
                st.rerun()

tab1, tab2 = st.tabs(["🔍 Search", f"📋 {st.session_state.current_board}"])

with tab1:
    st.title("AI Research Search")
    query = st.text_input("What are you researching?", placeholder="e.g., 1860s Ireland fashion")
    
    if st.button("🔍 Search", type="primary"):
        if query:
            st.session_state.search_results = generate_results(query)
            st.session_state.selected_items.clear()
            st.rerun()
    
    if st.session_state.search_results:
        st.subheader(f"Found {len(st.session_state.search_results)} sources")
        for result in st.session_state.search_results:
            with st.container(border=True):
                col1, col2 = st.columns([4, 1])
                with col1:
                    emoji = {'article': '📄', 'image': '🖼️', 'video': '🎬', 'pdf': '📕'}
                    st.markdown(f"{emoji.get(result['type'], '📄')} **{result['title']}**")
                    st.caption(result['description'])
                    st.markdown(f"[View]({result['url']})")
                with col2:
                    checked = result['id'] in st.session_state.selected_items
                    if st.checkbox("Select", value=checked, key=f"cb_{result['id']}"):
                        st.session_state.selected_items.add(result['id'])
                    else:
                        st.session_state.selected_items.discard(result['id'])

with tab2:
    st.title(st.session_state.current_board)
    items = st.session_state.pinned_items.get(st.session_state.current_board, [])
    
    if not items:
        st.info("No items yet. Use Search to find content.")
    else:
        st.write(f"**{len(items)} items**")
        cols = st.columns(3)
        for idx, item in enumerate(items):
            with cols[idx % 3]:
                with st.container(border=True):
                    emoji = {'article': '📄', 'image': '🖼️', 'video': '🎬', 'pdf': '📕'}
                    st.markdown(f"### {emoji.get(item['type'], '📄')} {item['title']}")
                    st.caption(f"{item['type']} • {item['added']}")
                    st.write(item['description'])
                    st.markdown(f"[Open]({item['url']})")
