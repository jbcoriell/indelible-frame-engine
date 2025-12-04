import streamlit as st
from datetime import datetime
import json

st.set_page_config(page_title="Indelible Frame", page_icon="🎬", layout="wide")

if 'boards' not in st.session_state:
    st.session_state.boards = ['1860s Ireland', 'Sci-Fi Dystopia']
    st.session_state.current_board = '1860s Ireland'
    st.session_state.pinned_items = {}
    st.session_state.search_results = []
    st.session_state.selected_items = set()

def search_with_ai(query, content_type):
    """Real AI-powered web search with content type filtering"""
    try:
        import anthropic
        import os
        
        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        
        # Customize search instruction based on content type
        if content_type == "all":
            type_instruction = "Find 10 diverse sources: mix of articles, images, videos, and PDFs."
        elif content_type == "images":
            type_instruction = "Find 10 IMAGE sources only. Focus on photo archives, galleries, museum collections, historical image databases."
        elif content_type == "articles":
            type_instruction = "Find 10 ARTICLE sources only. Focus on historical articles, encyclopedia entries, blog posts, news archives."
        elif content_type == "videos":
            type_instruction = "Find 10 VIDEO sources only. Focus on documentaries, YouTube videos, educational content, interviews."
        elif content_type == "pdfs":
            type_instruction = "Find 10 PDF DOCUMENT sources only. Focus on research papers, academic journals, historical documents, reports."
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            tools=[{
                "type": "web_search_20250305",
                "name": "web_search"
            }],
            messages=[{
                "role": "user",
                "content": f"""Search the web for: "{query}"

{type_instruction}

Return ONLY a valid JSON array (no markdown, no preamble):
[{{"id": "1", "title": "Source Title", "url": "https://actual-url.com", "description": "Brief 1-2 sentence description", "type": "{content_type if content_type != 'all' else 'article'}"}}]

Important: 
- Use real, working URLs from your search
- For images, type should be "image"
- For articles/websites, type should be "article"  
- For videos, type should be "video"
- For PDFs, type should be "pdf"
- Make descriptions specific and informative"""
            }]
        )
        
        # Extract and parse response
        response_text = ""
        for block in message.content:
            if block.type == "text":
                response_text += block.text
        
        # Clean and parse JSON
        response_text = response_text.strip().replace("```json", "").replace("```", "")
        import re
        json_match = re.search(r'\[\s*\{[\s\S]*\}\s*\]', response_text)
        
        if json_match:
            results = json.loads(json_match.group(0))
            # Ensure each has an id
            for i, r in enumerate(results):
                if 'id' not in r:
                    r['id'] = str(i + 1)
            return results
        else:
            st.error("Could not parse search results. Using demo data.")
            return generate_demo_results(query, content_type)
            
    except Exception as e:
        st.error(f"Search error: {str(e)}. Using demo data.")
        return generate_demo_results(query, content_type)

def generate_demo_results(query, content_type):
    """Fallback demo results based on content type"""
    
    all_results = {
        "images": [
            {"id": "1", "title": f"{query} - Historical Photo Archive", "url": "https://loc.gov", "description": "Library of Congress historical photographs", "type": "image"},
            {"id": "2", "title": f"{query} - Museum Collection", "url": "https://vam.ac.uk", "description": "Victoria & Albert Museum image gallery", "type": "image"},
            {"id": "3", "title": f"{query} - Getty Images Archive", "url": "https://gettyimages.com", "description": "Professional historical photography", "type": "image"},
            {"id": "4", "title": f"{query} - Flickr Commons", "url": "https://flickr.com", "description": "Community historical image collection", "type": "image"},
            {"id": "5", "title": f"{query} - National Archives Photos", "url": "https://archives.gov", "description": "Government historical photo collection", "type": "image"},
            {"id": "6", "title": f"{query} - Europeana Gallery", "url": "https://europeana.eu", "description": "European cultural heritage images", "type": "image"},
            {"id": "7", "title": f"{query} - Smithsonian Images", "url": "https://si.edu", "description": "Smithsonian Institution collections", "type": "image"},
            {"id": "8", "title": f"{query} - British Library Images", "url": "https://bl.uk", "description": "Historical manuscripts and illustrations", "type": "image"},
        ],
        "articles": [
            {"id": "1", "title": f"{query} - Historical Overview", "url": "https://historyextra.com", "description": "Comprehensive historical analysis and context", "type": "article"},
            {"id": "2", "title": f"{query} - Encyclopedia Entry", "url": "https://britannica.com", "description": "Detailed encyclopedia article with references", "type": "article"},
            {"id": "3", "title": f"{query} - Academic Research", "url": "https://jstor.org", "description": "Scholarly article with citations", "type": "article"},
            {"id": "4", "title": f"{query} - BBC History", "url": "https://bbc.co.uk/history", "description": "Educational article with expert analysis", "type": "article"},
            {"id": "5", "title": f"{query} - Museum Article", "url": "https://metmuseum.org", "description": "Museum curator's perspective", "type": "article"},
            {"id": "6", "title": f"{query} - Historical Blog", "url": "https://historytoday.com", "description": "In-depth historical exploration", "type": "article"},
            {"id": "7", "title": f"{query} - Archive Article", "url": "https://archive.org", "description": "Historical documentation and sources", "type": "article"},
            {"id": "8", "title": f"{query} - Research Guide", "url": "https://loc.gov", "description": "Library of Congress research materials", "type": "article"},
        ],
        "videos": [
            {"id": "1", "title": f"Documentary: {query}", "url": "https://youtube.com", "description": "Full-length historical documentary", "type": "video"},
            {"id": "2", "title": f"{query} - Expert Interview", "url": "https://youtube.com", "description": "Interview with subject matter expert", "type": "video"},
            {"id": "3", "title": f"{query} - Educational Series", "url": "https://youtube.com", "description": "Multi-part educational video series", "type": "video"},
            {"id": "4", "title": f"{query} - Lecture", "url": "https://youtube.com", "description": "University lecture on the topic", "type": "video"},
            {"id": "5", "title": f"{query} - PBS Documentary", "url": "https://pbs.org", "description": "PBS historical documentary", "type": "video"},
            {"id": "6", "title": f"{query} - Archive Footage", "url": "https://britishpathe.com", "description": "Historical archive footage compilation", "type": "video"},
            {"id": "7", "title": f"{query} - Crash Course Video", "url": "https://youtube.com", "description": "Educational crash course episode", "type": "video"},
            {"id": "8", "title": f"{query} - Museum Tour", "url": "https://youtube.com", "description": "Virtual museum exhibition tour", "type": "video"},
        ],
        "pdfs": [
            {"id": "1", "title": f"{query} - Research Paper", "url": "https://scholar.google.com", "description": "Peer-reviewed academic research paper", "type": "pdf"},
            {"id": "2", "title": f"{query} - Thesis", "url": "https://proquest.com", "description": "Doctoral dissertation on the topic", "type": "pdf"},
            {"id": "3", "title": f"{query} - Historical Report", "url": "https://archives.gov", "description": "Government historical report", "type": "pdf"},
            {"id": "4", "title": f"{query} - Academic Journal", "url": "https://jstor.org", "description": "Journal article with extensive citations", "type": "pdf"},
            {"id": "5", "title": f"{query} - Museum Catalog", "url": "https://metmuseum.org", "description": "Exhibition catalog with scholarly essays", "type": "pdf"},
            {"id": "6", "title": f"{query} - Conference Paper", "url": "https://academia.edu", "description": "Academic conference presentation", "type": "pdf"},
            {"id": "7", "title": f"{query} - Book Chapter", "url": "https://googlebooks.com", "description": "Scanned book chapter excerpt", "type": "pdf"},
            {"id": "8", "title": f"{query} - Primary Document", "url": "https://loc.gov", "description": "Historical primary source document", "type": "pdf"},
        ]
    }
    
    if content_type == "all":
        return all_results["articles"][:3] + all_results["images"][:2] + all_results["videos"][:2] + all_results["pdfs"][:1]
    else:
        return all_results.get(content_type, all_results["articles"])

with st.sidebar:
    st.title("🎬 Indelible Frame")
    st.divider()
    
    board = st.selectbox("Project Boards", st.session_state.boards)
    st.session_state.current_board = board
    
    new = st.text_input("New board name")
    if st.button("Create") and new:
        if new not in st.session_state.boards:
            st.session_state.boards.append(new)
            st.rerun()
    
    if st.session_state.selected_items:
        st.write(f"**{len(st.session_state.selected_items)} selected**")
        st.write("Pin to board:")
        for b in st.session_state.boards:
            if st.button(f"📌 {b}", key=f"pin_{b}"):
                items = [r for r in st.session_state.search_results if r['id'] in st.session_state.selected_items]
                if b not in st.session_state.pinned_items:
                    st.session_state.pinned_items[b] = []
                for item in items:
                    st.session_state.pinned_items[b].append({
                        'title': item['title'], 'url': item['url'], 'type': item['type'],
                        'description': item.get('description', ''), 'added': datetime.now().strftime('%Y-%m-%d')
                    })
                st.session_state.selected_items.clear()
                st.success(f"Pinned {len(items)} items!")
                st.rerun()

tab1, tab2 = st.tabs(["🔍 Search", f"📋 {st.session_state.current_board}"])

with tab1:
    st.title("AI Research Search")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input("What are you researching?", placeholder="e.g., 1860s Ireland fashion")
    
    with col2:
        content_type = st.selectbox(
            "Content Type",
            ["all", "images", "articles", "videos", "pdfs"],
            format_func=lambda x: {
                "all": "📚 All Types",
                "images": "🖼️ Images Only",
                "articles": "📄 Articles Only", 
                "videos": "🎬 Videos Only",
                "pdfs": "📕 PDFs Only"
            }[x]
        )
    
    if st.button("🔍 Search with AI", type="primary", use_container_width=True):
        if query:
            with st.spinner(f"AI is searching for {content_type}..."):
                st.session_state.search_results = search_with_ai(query, content_type)
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
                    st.caption(result.get('description', ''))
                    st.markdown(f"[View Source]({result['url']})")
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
                    st.write(item.get('description', ''))
                    st.markdown(f"[Open]({item['url']})")
