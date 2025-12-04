import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="Indelible Frame Research Engine", page_icon="🎬", layout="wide")

st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #1e1b4b 0%, #581c87 50%, #1e1b4b 100%);}
</style>
""", unsafe_allow_html=True)

if 'boards' not in st.session_state:
    st.session_state.boards = ['1860s Ireland', 'Sci-Fi Dystopia']
if 'current_board' not in st.session_state:
    st.session_state.current_board = '1860s Ireland'
if 'pinned_items' not in st.session_state:
    st.session_state.pinned_items = {}
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'selected_items' not in st.session_state:
    st.session_state.selected_items = set()

def generate_demo_results(query, content_type):
    results = [
        {"title": f"{query} - Historical Archive", "url": "https://historyextra.com/period/victorian/", "description": "Comprehensive historical documentation with primary sources", "type": "article"},
        {"title": f"Visual Guide: {query}", "url": "https://vam.ac.uk/collections/fashion", "description": "Museum collection with detailed photographs", "type": "image"},
        {"title": f"{query} Research Paper", "url": "https://jstor.org", "description": "Academic research with citations", "type": "pdf"},
        {"title": f"Documentary: {query}", "url": "https://youtube.com", "description": "Educational video content", "type": "video"},
        {"title": f"Understanding {query}", "url": "https://britannica.com", "description": "Encyclopedia entry with references", "type": "article"},
        {"title": f"{query} Photo Collection", "url": "https://flickr.com", "description": "Curated historical images", "type": "image"},
    ]
    
    if content_type != "all":
        results = [r for r in results if r['type'] == content_type]
    
    for i, r in enumerate(results):
        r['id'] = f"result_{i}"
    
    return results

with st.sidebar:
    st.title("🎬 Indelible Frame")
    st.caption("AI Research Engine")
    st.divider()
    
    st.subheader("Project Boards")
    selected = st.selectbox("Select Board", st.session_state.boards, key="board_select")
    st.session_state.current_board = selected
    
    with st.expander("➕ Create New Board"):
        new_board = st.text_input("Board Name")
        if st.button("Create"):
            if new_board and new_board not in st.session_state.boards:
                st.session_state.boards.append(new_board)
                st.session_state.current_board = new_board
                st.rerun()
    
    if len(st.session_state.boards) > 1:
        if st.button("🗑️ Delete Current Board"):
            st.session_state.boards.remove(st.session_state.current_board)
            st.session_state.current_board = st.session_state.boards[0]
            if st.session_state.current_board in st.session_state.pinned_items:
                del st.session_state.pinned_items[st.session_state.current_board]
            st.rerun()
    
    if st.session_state.selected_items:
        st.divider()
        st.write(f"**{len(st.session_state.selected_items)} selected**")
        st.write("Pin to board:")
        for board in st.session_state.boards:
            if st.button(f"📌 {board}", key=f"pin_{board}"):
                items_to_pin = [r for r in st.session_state.search_results if r['id'] in st.session_state.selected_items]
                if board not in st.session_state.pinned_items:
                    st.session_state.pinned_items[board] = []
                for item in items_to_pin:
                    st.session_state.pinned_items[board].append({
                        'title': item['title'], 'url': item['url'], 'type': item['type'],
                        'description': item['description'], 'added': datetime.now().strftime('%Y-%m-%d')
                    })
                st.session_state.selected_items.clear()
                st.success(f"Pinned {len(items_to_pin)} items!")
                st.rerun()
    
    st.divider()
    if st.button("📥 Export Board"):
        items = st.session_state.pinned_items.get(st.session_state.current_board, [])
        md = f"# {st.session_state.current_board}\n\n"
        for item in items:
            md += f"## {item['title']}\n- Type: {item['type']}\n- URL: {item['url']}\n"
            if item.get('description'):
                md += f"- Description: {item['description']}\n"
            md += f"- Added: {item['added']}\n\n---\n\n"
        st.download_button("Download", md, file_name=f"{st.session_state.current_board.replace(' ', '_')}.md")

tab1, tab2 = st.tabs(["🔍 AI Search", f"📋 {st.session_state.current_board}"])

with tab1:
    st.title("AI-Powered Research Search")
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("What are you researching?", placeholder="e.g., 1860s Ireland women's fashion")
    with col2:
        content_type = st.selectbox("Type", ["all", "article", "image", "video", "pdf"])
    
    if st.button("🔍 Search", type="primary", use_container_width=True):
        if query:
            with st.spinner("Searching..."):
                results = generate_demo_results(query, content_type)
                st.session_state.search_results = results
                st.session_state.selected_items.clear()
                st.rerun()
    
    if st.session_state.search_results:
        st.subheader(f"Found {len(st.session_state.search_results)} sources")
        for result in st.session_state.search_results:
            is_selected = result['id'] in st.session_state.selected_items
            with st.container(border=True):
                col1, col2 = st.columns([4, 1])
                with col1:
                    emoji = {'article': '📄', 'image': '🖼️', 'video': '🎬', 'pdf': '📕'}.get(result['type'], '📄')
                    st.markdown(f"{emoji} **{result['title']}**")
                    st.caption(result['description'])
                    st.markdown(f"[View Source]({result['url']})")
                with col2:
                    if st.checkbox("Select", value=is_selected, key=f"cb_{result['id']}"):
                        st.session_state.selected_items.add(result['id'])
                    else:
                        st.session_state.selected_items.discard(result['id'])

with tab2:
    st.title(st.session_state.current_board)
    items = st.session_state.pinned_items.get(st.session_state.current_board, [])
    
    if not items:
        st.info("No items yet. Use AI Search to find and pin content.")
    else:
        filter_type = st.selectbox("Filter", ["all", "article", "image", "video", "pdf"])
        if filter_type != "all":
            items = [i for i in items if i['type'] == filter_type]
        st.write(f"**{len(items)} items**")
        
        cols = st.columns(3)
        for idx, item in enumerate(items):
            with cols[idx % 3]:
                with st.container(border=True):
                    emoji = {'article': '📄', 'image': '🖼️', 'video': '🎬', 'pdf': '📕'}.get(item['type'], '📄')
                    st.markdown(f"### {emoji} {item['title']}")
                    st.caption(f"{item['type']} • {item['added']}")
                    if item.get('description'):
                        st.write(item['description'])
                    st.markdown(f"[Open]({item['url']})")
                    if st.button("🗑️", key=f"del_{idx}"):
                        st.session_state.pinned_items[st.session_state.current_board].remove(item)
                        st.rerun()
```

4. Click **"Commit changes"**

**Create requirements.txt:**
1. Click **"Add file"** → **"Create new file"**
2. Filename: `requirements.txt`
3. Paste just this:
```
streamlit>=1.32.0
