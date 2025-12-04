import streamlit as st
from datetime import datetime
import json

st.set_page_config(page_title="Indelible Frame", page_icon="🎬", layout="wide")

# Art Deco Hollywood Theme CSS
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
    h2, h3 {
        color: #f5f5dc !important;
        font-family: 'Didot', 'Bodoni MT', serif !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
    }
    
    /* Text color */
    p, span, label {
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
    
    /* Success messages */
    .stSuccess {
        background-color: rgba(76, 175, 80, 0.2) !important;
        border-left: 4px solid #4caf50 !important;
        color: #a8e6a1 !important;
    }
    
    /* Warning messages */
    .stWarning {
        background-color: rgba(255, 193, 7, 0.2) !important;
        border-left: 4px solid #d4af37 !important;
        color: #f5f5dc !important;
    }
    
    /* Info messages */
    .stInfo {
        background-color: rgba(79, 195, 247, 0.2) !important;
        border-left: 4px solid #4fc3f7 !important;
        color: #b3e5fc !important;
    }
    
    /* Checkboxes */
    .stCheckbox {
        color: #f5f5dc !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #d4af37 !important;
    }
    
    /* Metric values */
    [data-testid="stMetricValue"] {
        color: #d4af37 !important;
        font-family: 'Didot', serif !important;
    }
    
    /* Caption text */
    .caption {
        color: #c0c0c0 !important;
        font-style: italic;
    }
    
    /* Sidebar title special styling */
    [data-testid="stSidebar"] h1 {
        text-align: center;
        font-size: 28px !important;
        margin-bottom: 5px !important;
        text-shadow: 0 0 20px rgba(212, 175, 55, 0.5);
    }
    
    /* Add film strip decoration */
    .main::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 10px;
        background: repeating-linear-gradient(
            90deg,
            #d4af37 0px,
            #d4af37 20px,
            #1a1a1a 20px,
            #1a1a1a 40px
        );
        z-index: 1000;
    }
    
    .main::after {
        content: "";
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 10px;
        background: repeating-linear-gradient(
            90deg,
            #d4af37 0px,
            #d4af37 20px,
            #1a1a1a 20px,
            #1a1a1a 40px
        );
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

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
            type_instruction = "Find 15 diverse sources: mix of articles, images, videos, and PDFs."
        elif content_type == "images":
            type_instruction = "Find 15 IMAGE sources only. Look for: photo archives, museum collections, Pinterest boards, Flickr albums, historical image databases, Google Images results."
        elif content_type == "articles":
            type_instruction = "Find 15 ARTICLE sources only. Look for: historical articles, blog posts, encyclopedia entries, news archives, educational websites."
        elif content_type == "videos":
            type_instruction = "Find 15 VIDEO sources only. Look for: YouTube videos, documentaries, educational channels, PBS content, historical footage archives."
        elif content_type == "pdfs":
            type_instruction = "Find 15 PDF DOCUMENT sources only. Look for: research papers on Google Scholar, academic journals, historical documents, museum reports."
        
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

CRITICAL: URLs must be DIRECT LINKS to the actual content, NOT just homepage URLs.
- For images: Link to the specific image page or gallery, not just the site homepage
- For articles: Link to the specific article URL, not just the domain
- For videos: Link to the specific video URL (e.g., youtube.com/watch?v=abc123)
- For PDFs: Link to the actual PDF file or document page

Return ONLY a valid JSON array (no markdown, no preamble, no explanation):
[
  {{
    "id": "1",
    "title": "Specific descriptive title",
    "url": "https://complete-direct-url-to-actual-content.com/specific-page",
    "description": "1-2 sentence description of what this source contains",
    "type": "{content_type if content_type != 'all' else 'article'}"
  }}
]

Use the web_search tool to find REAL, WORKING, DIRECT URLs. Double-check that URLs are complete and specific."""
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
            # Ensure each has an id and validate URLs
            for i, r in enumerate(results):
                if 'id' not in r:
                    r['id'] = str(i + 1)
                # Basic URL validation
                if not r.get('url', '').startswith('http'):
                    r['url'] = 'https://' + r.get('url', '')
            
            if len(results) > 0:
                return results
            else:
                raise Exception("No results returned")
        else:
            raise Exception("Could not parse JSON response")
            
    except Exception as e:
        st.warning(f"AI search encountered an issue. Showing curated {content_type} results instead.")
        return generate_demo_results(query, content_type)

def generate_demo_results(query, content_type):
    """Fallback demo results with realistic direct URLs"""
    
    # Create search-friendly query
    search_query = query.replace(' ', '+')
    
    all_results = {
        "images": [
            {"id": "1", "title": f"{query} - Library of Congress Photos", "url": f"https://www.loc.gov/pictures/?q={search_query}", "description": "Historical photographs from the Library of Congress archive", "type": "image"},
            {"id": "2", "title": f"{query} - Victoria & Albert Museum", "url": f"https://collections.vam.ac.uk/search/?q={search_query}", "description": "Museum collection images and artifacts", "type": "image"},
            {"id": "3", "title": f"{query} - Getty Images Archive", "url": f"https://www.gettyimages.com/photos/{search_query}", "description": "Professional historical photography collection", "type": "image"},
            {"id": "4", "title": f"{query} - Wikimedia Commons", "url": f"https://commons.wikimedia.org/w/index.php?search={search_query}", "description": "Free historical images and illustrations", "type": "image"},
            {"id": "5", "title": f"{query} - National Archives", "url": f"https://catalog.archives.gov/search?q={search_query}", "description": "U.S. government historical photographs", "type": "image"},
            {"id": "6", "title": f"{query} - Europeana Collections", "url": f"https://www.europeana.eu/en/search?query={search_query}", "description": "European cultural heritage images", "type": "image"},
            {"id": "7", "title": f"{query} - British Library Images", "url": f"https://www.bl.uk/catalogues-and-collections/digital-collections", "description": "Digitized manuscripts and historical images", "type": "image"},
            {"id": "8", "title": f"{query} - Smithsonian Collections", "url": f"https://www.si.edu/search/collection-images?edan_q={search_query}", "description": "Smithsonian Institution image archive", "type": "image"},
            {"id": "9", "title": f"{query} - Pinterest Boards", "url": f"https://www.pinterest.com/search/pins/?q={search_query}", "description": "Curated historical image boards", "type": "image"},
            {"id": "10", "title": f"{query} - Flickr Commons", "url": f"https://www.flickr.com/search/?text={search_query}", "description": "Community historical photo collection", "type": "image"},
            {"id": "11", "title": f"{query} - NYPL Digital", "url": f"https://digitalcollections.nypl.org/search/index?utf8=%E2%9C%93&keywords={search_query}", "description": "New York Public Library digital images", "type": "image"},
            {"id": "12", "title": f"{query} - Met Museum Collection", "url": f"https://www.metmuseum.org/art/collection/search#{search_query}", "description": "Metropolitan Museum artwork and artifacts", "type": "image"},
            {"id": "13", "title": f"{query} - Old Book Illustrations", "url": f"https://www.oldbookillustrations.com/?s={search_query}", "description": "Vintage book illustrations and engravings", "type": "image"},
            {"id": "14", "title": f"{query} - Harvard Art Museums", "url": f"https://harvardartmuseums.org/collections?q={search_query}", "description": "Harvard university art collection", "type": "image"},
            {"id": "15", "title": f"{query} - Internet Archive Images", "url": f"https://archive.org/search.php?query={search_query}&and[]=mediatype:image", "description": "Digital library historical images", "type": "image"},
        ],
        "articles": [
            {"id": "1", "title": f"{query} - History Extra", "url": f"https://www.historyextra.com/?s={search_query}", "description": "Historical analysis from expert historians", "type": "article"},
            {"id": "2", "title": f"{query} - Britannica", "url": f"https://www.britannica.com/search?query={search_query}", "description": "Encyclopedia entry with scholarly references", "type": "article"},
            {"id": "3", "title": f"{query} - Wikipedia", "url": f"https://en.wikipedia.org/wiki/Special:Search?search={search_query}", "description": "Comprehensive overview with citations", "type": "article"},
            {"id": "4", "title": f"{query} - BBC History", "url": f"https://www.bbc.co.uk/search?q={search_query}", "description": "Educational articles with expert commentary", "type": "article"},
            {"id": "5", "title": f"{query} - Smithsonian Magazine", "url": f"https://www.smithsonianmag.com/?s={search_query}", "description": "In-depth cultural and historical articles", "type": "article"},
            {"id": "6", "title": f"{query} - History Today", "url": f"https://www.historytoday.com/search?s={search_query}", "description": "Scholarly historical exploration", "type": "article"},
            {"id": "7", "title": f"{query} - National Geographic", "url": f"https://www.nationalgeographic.com/search?q={search_query}", "description": "Historical and cultural research articles", "type": "article"},
            {"id": "8", "title": f"{query} - Ancient History Encyclopedia", "url": f"https://www.worldhistory.org/search/?q={search_query}", "description": "Academic historical reference", "type": "article"},
            {"id": "9", "title": f"{query} - The Public Domain Review", "url": f"https://publicdomainreview.org/?s={search_query}", "description": "Essays on historical culture and artifacts", "type": "article"},
            {"id": "10", "title": f"{query} - JSTOR Daily", "url": f"https://daily.jstor.org/?s={search_query}", "description": "Academic research made accessible", "type": "article"},
            {"id": "11", "title": f"{query} - Historic UK", "url": f"https://www.historic-uk.com/?s={search_query}", "description": "British history and heritage articles", "type": "article"},
            {"id": "12", "title": f"{query} - Khan Academy", "url": f"https://www.khanacademy.org/search?page_search_query={search_query}", "description": "Educational historical content", "type": "article"},
            {"id": "13", "title": f"{query} - Oxford Reference", "url": f"https://www.oxfordreference.com/search?q={search_query}", "description": "Academic reference material", "type": "article"},
            {"id": "14", "title": f"{query} - ThoughtCo", "url": f"https://www.thoughtco.com/search?q={search_query}", "description": "Educational history guides", "type": "article"},
            {"id": "15", "title": f"{query} - History.com", "url": f"https://www.history.com/search?q={search_query}", "description": "Historical documentaries and articles", "type": "article"},
        ],
        "videos": [
            {"id": "1", "title": f"{query} - Documentary", "url": f"https://www.youtube.com/results?search_query={search_query}+documentary", "description": "Full-length historical documentary", "type": "video"},
            {"id": "2", "title": f"{query} - Crash Course", "url": f"https://www.youtube.com/results?search_query={search_query}+crash+course", "description": "Educational video series", "type": "video"},
            {"id": "3", "title": f"{query} - TED-Ed", "url": f"https://www.youtube.com/results?search_query={search_query}+TED-Ed", "description": "Animated educational content", "type": "video"},
            {"id": "4", "title": f"{query} - PBS Documentary", "url": f"https://www.pbs.org/search/?q={search_query}", "description": "Public broadcasting historical content", "type": "video"},
            {"id": "5", "title": f"{query} - History Channel", "url": f"https://www.youtube.com/results?search_query={search_query}+history+channel", "description": "Historical documentary series", "type": "video"},
            {"id": "6", "title": f"{query} - British Pathé Archive", "url": f"https://www.youtube.com/c/britishpathe/search?query={search_query}", "description": "Historical newsreel footage", "type": "video"},
            {"id": "7", "title": f"{query} - Khan Academy Video", "url": f"https://www.youtube.com/results?search_query={search_query}+khan+academy", "description": "Educational lecture series", "type": "video"},
            {"id": "8", "title": f"{query} - BBC Documentary", "url": f"https://www.youtube.com/results?search_query={search_query}+BBC+documentary", "description": "BBC historical programming", "type": "video"},
            {"id": "9", "title": f"{query} - Smithsonian Channel", "url": f"https://www.youtube.com/results?search_query={search_query}+smithsonian", "description": "Museum video content", "type": "video"},
            {"id": "10", "title": f"{query} - Timeline Documentary", "url": f"https://www.youtube.com/results?search_query={search_query}+timeline+documentary", "description": "World history documentaries", "type": "video"},
            {"id": "11", "title": f"{query} - National Geographic", "url": f"https://www.youtube.com/results?search_query={search_query}+national+geographic", "description": "Historical exploration videos", "type": "video"},
            {"id": "12", "title": f"{query} - CrashCourse History", "url": f"https://www.youtube.com/results?search_query={search_query}+crashcourse+history", "description": "Fast-paced history lessons", "type": "video"},
            {"id": "13", "title": f"{query} - Extra Credits", "url": f"https://www.youtube.com/results?search_query={search_query}+extra+credits+history", "description": "Animated history series", "type": "video"},
            {"id": "14", "title": f"{query} - Oversimplified", "url": f"https://www.youtube.com/results?search_query={search_query}+oversimplified", "description": "Humorous history animations", "type": "video"},
            {"id": "15", "title": f"{query} - Yale Courses", "url": f"https://www.youtube.com/results?search_query={search_query}+yale+courses", "description": "University lecture recordings", "type": "video"},
        ],
        "pdfs": [
            {"id": "1", "title": f"{query} - Google Scholar", "url": f"https://scholar.google.com/scholar?q={search_query}", "description": "Academic research papers and theses", "type": "pdf"},
            {"id": "2", "title": f"{query} - JSTOR", "url": f"https://www.jstor.org/action/doBasicSearch?Query={search_query}", "description": "Peer-reviewed journal articles", "type": "pdf"},
            {"id": "3", "title": f"{query} - Academia.edu", "url": f"https://www.academia.edu/search?q={search_query}", "description": "Academic papers and research", "type": "pdf"},
            {"id": "4", "title": f"{query} - ResearchGate", "url": f"https://www.researchgate.net/search/publication?q={search_query}", "description": "Scientific research publications", "type": "pdf"},
            {"id": "5", "title": f"{query} - Internet Archive", "url": f"https://archive.org/search.php?query={search_query}&and[]=mediatype:texts", "description": "Digital library books and documents", "type": "pdf"},
            {"id": "6", "title": f"{query} - ProQuest", "url": f"https://www.proquest.com/search/{search_query}", "description": "Dissertations and theses", "type": "pdf"},
            {"id": "7", "title": f"{query} - National Archives", "url": f"https://catalog.archives.gov/search?q={search_query}", "description": "Historical government documents", "type": "pdf"},
            {"id": "8", "title": f"{query} - Library of Congress", "url": f"https://www.loc.gov/search/?q={search_query}&fo=json", "description": "Primary source documents", "type": "pdf"},
            {"id": "9", "title": f"{query} - Google Books", "url": f"https://www.google.com/search?tbm=bks&q={search_query}", "description": "Digitized book excerpts", "type": "pdf"},
            {"id": "10", "title": f"{query} - Project Gutenberg", "url": f"https://www.gutenberg.org/ebooks/search/?query={search_query}", "description": "Free historical texts", "type": "pdf"},
            {"id": "11", "title": f"{query} - HathiTrust", "url": f"https://catalog.hathitrust.org/Search/Home?lookfor={search_query}", "description": "Digital library partnership", "type": "pdf"},
            {"id": "12", "title": f"{query} - ERIC Database", "url": f"https://eric.ed.gov/?q={search_query}", "description": "Education research documents", "type": "pdf"},
            {"id": "13", "title": f"{query} - SSRN Papers", "url": f"https://papers.ssrn.com/sol3/results.cfm?q={search_query}", "description": "Social science research network", "type": "pdf"},
            {"id": "14", "title": f"{query} - arXiv", "url": f"https://arxiv.org/search/?query={search_query}", "description": "Scientific preprint archive", "type": "pdf"},
            {"id": "15", "title": f"{query} - PubMed Central", "url": f"https://www.ncbi.nlm.nih.gov/pmc/?term={search_query}", "description": "Biomedical research articles", "type": "pdf"},
        ]
    }
    
    if content_type == "all":
        return all_results["articles"][:5] + all_results["images"][:4] + all_results["videos"][:3] + all_results["pdfs"][:3]
    else:
        return all_results.get(content_type, all_results["articles"])

with st.sidebar:
    st.title("🎬 INDELIBLE FRAME")
    st.caption("✦ Research Engine ✦")
    st.divider()
    
    st.subheader("⬥ Project Boards")
    board = st.selectbox("", st.session_state.boards, label_visibility="collapsed")
    st.session_state.current_board = board
    
    new = st.text_input("New board name")
    if st.button("Create Board") and new:
        if new not in st.session_state.boards:
            st.session_state.boards.append(new)
            st.rerun()
    
    if st.session_state.selected_items:
        st.divider()
        st.write(f"**✦ {len(st.session_state.selected_items)} Selected**")
        st.caption("Pin to board:")
        for b in st.session_state.boards:
            if st.button(f"📌 {b}", key=f"pin_{b}"):
                items = [r for r in st.session_state.search_results if r['id'] in st.session_state.selected_items]
                if b not in st.session_state.pinned_items:
                    st.session_state.pinned_items[b] = []
                for item in items:
                    st.session_state.pinned_items[b].append({}
                        'title': item['title'], 'url': item['url'], 'type': item['type'],
                        'description': item.get('description', ''), 'added': datetime
