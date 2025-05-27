import streamlit as st
from .content_formatter import ContentFormatter

class PlatformPreview:
    """Display platform-specific content previews."""
    
    def __init__(self):
        self.formatter = ContentFormatter()
    
    def display_platform_preview(self, platform: str, content: str):
        """Display a preview of content formatted for a specific platform."""
        
        platform_configs = {
            "linkedin": {
                "name": "LinkedIn",
                "icon": "💼",
                "color": "#0077b5",
                "char_limit": 1300,
                "description": "Professional network"
            },
            "twitter": {
                "name": "Twitter/X", 
                "icon": "🐦",
                "color": "#1da1f2",
                "char_limit": 280,
                "description": "Microblogging platform"
            },
            "bluesky": {
                "name": "Bluesky",
                "icon": "🟦", 
                "color": "#00a8e8",
                "char_limit": 300,
                "description": "Decentralized social network"
            },
            "threads": {
                "name": "Threads",
                "icon": "🧵",
                "color": "#000000", 
                "description": "Text-based conversation app"
            }
        }
        
        config = platform_configs.get(platform.lower(), platform_configs["linkedin"])
        
        # Platform header
        st.markdown(f"""
        <div style="
            background: linear-gradient(90deg, {config['color']}22, {config['color']}11);
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid {config['color']};
            margin: 10px 0;
        ">
            <h3>{config['icon']} {config['name']}</h3>
            <p style="margin: 0; color: #666;">{config['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Character count and content preview
        char_count = len(content)
        char_limit = config.get("char_limit", 1000)
        
        # Character count display
        if char_count <= char_limit:
            char_color = "green"
        elif char_count <= char_limit * 1.1:
            char_color = "orange" 
        else:
            char_color = "red"
            
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**Content Preview:**")
        
        with col2:
            if "char_limit" in config:
                st.markdown(f"<span style='color: {char_color}; font-weight: bold;'>{char_count}/{char_limit} chars</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color: green; font-weight: bold;'>{char_count} chars</span>", unsafe_allow_html=True)
        
        # Content preview box
        st.markdown(f"""
        <div style="
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #e9ecef;
            margin: 10px 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.4;
        ">
            {content.replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)
        
        # Platform-specific tips
        if platform.lower() == "twitter":
            if char_count > 280:
                st.warning("⚠️ Content exceeds Twitter's 280 character limit")
            st.info("💡 Twitter tip: Use engaging hooks and clear calls-to-action")
            
        elif platform.lower() == "linkedin":
            st.info("💡 LinkedIn tip: Professional tone works best. Consider adding industry insights")
            
        elif platform.lower() == "bluesky":
            if char_count > 300:
                st.warning("⚠️ Content exceeds Bluesky's 300 character limit")
            st.info("💡 Bluesky tip: Community-focused content performs well")
            
        elif platform.lower() == "threads":
            st.info("💡 Threads tip: Visual content and conversation starters work great")
