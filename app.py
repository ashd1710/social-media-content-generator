import streamlit as st
import os
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import hashlib

# Import your custom modules
from src.perplexity_client import PerplexityClient
from src.content_formatter import ContentFormatter
from src.social_integrations import SocialMediaManager
from src.database import ContentDatabase
from src.utils import get_platform_info, generate_content_hash

# Page config
st.set_page_config(
    page_title="AI Content Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def get_api_key_input():
    """Get Perplexity API key from user input or environment"""
    
    # Sidebar API key input
    st.sidebar.markdown("## 🔑 API Configuration")
    
    # Check if we have a key in secrets/env
    default_key = ""
    has_configured_key = False
    
    try:
        if hasattr(st, 'secrets') and 'PERPLEXITY_API_KEY' in st.secrets:
            default_key = "Using configured key"
            has_configured_key = True
        elif os.getenv('PERPLEXITY_API_KEY'):
            default_key = "Using configured key"
            has_configured_key = True
    except:
        pass
    
    # User input field
    user_api_key = st.sidebar.text_input(
        "Perplexity API Key",
        value=default_key if default_key else "",
        type="password",
        help="Enter your Perplexity API key. Get one free at perplexity.ai",
        placeholder="pplx-your-api-key-here"
    )
    
    # Instructions for getting API key
    if not has_configured_key and not user_api_key:
        st.sidebar.markdown("""
        **🔑 Get your free API key:**
        1. Visit [perplexity.ai](https://perplexity.ai)
        2. Sign up/login
        3. Go to API section  
        4. Generate new API key
        5. Copy and paste it above
        """)
        
        st.sidebar.info("💡 Your API key is only used for your session and not stored anywhere.")
    
    # Return the appropriate API key
    if user_api_key and user_api_key != "Using configured key":
        return user_api_key
    elif has_configured_key:
        try:
            if hasattr(st, 'secrets') and 'PERPLEXITY_API_KEY' in st.secrets:
                return st.secrets['PERPLEXITY_API_KEY']
            else:
                return os.getenv('PERPLEXITY_API_KEY')
        except:
            return None
    else:
        return None

def initialize_perplexity_client():
    """Initialize Perplexity client with API key"""
    api_key = get_api_key_input()
    
    if not api_key:
        st.sidebar.error("⚠️ Please enter your Perplexity API key to use the generator")
        return None
    
    try:
        return PerplexityClient(api_key=api_key)
    except Exception as e:
        st.sidebar.error(f"❌ Error initializing Perplexity client: {str(e)}")
        return None

def initialize_session_state():
    """Initialize session state variables"""
    if 'generated_content' not in st.session_state:
        st.session_state.generated_content = {}
    if 'content_history' not in st.session_state:
        st.session_state.content_history = []
    if 'social_manager' not in st.session_state:
        st.session_state.social_manager = SocialMediaManager()
    if 'db' not in st.session_state:
        st.session_state.db = ContentDatabase()

def show_header():
    """Display main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🚀 AI-Powered Social Media Content Generator</h1>
        <p>Transform your content strategy with Perplexity's Sonar Reasoning API</p>
    </div>
    """, unsafe_allow_html=True)

def content_generation_page(perplexity_client):
    """Main content generation interface"""
    
    st.header("📝 Generate Content")
    
    # Topic and content type selection
    col1, col2 = st.columns(2)
    
    with col1:
        # Topic selection
        topic_options = [
            "AI Trends", "Product Management", "Financial Markets", 
            "Personal Finance", "Healthcare AI", "Climate Tech",
            "Startup Ecosystem", "Digital Marketing", "Custom Topic"
        ]
        
        selected_topic = st.selectbox("📊 Select Topic", topic_options)
        
        if selected_topic == "Custom Topic":
            custom_topic = st.text_input("Enter your custom topic:")
            topic = custom_topic if custom_topic else "AI Trends"
        else:
            topic = selected_topic
    
    with col2:
        # Content type selection
        content_types = [
            "Trend Analysis", "News Summary", "Educational Tip", 
            "Opinion Piece", "Industry Insight", "How-to Guide"
        ]
        content_type = st.selectbox("📑 Content Type", content_types)
    
    # Platform selection
    st.subheader("🎯 Target Platforms")
    platform_cols = st.columns(4)
    
    platforms = {}
    with platform_cols[0]:
        platforms['linkedin'] = st.checkbox("💼 LinkedIn", value=True)
    with platform_cols[1]:
        platforms['bluesky'] = st.checkbox("🦋 Bluesky", value=True)
    with platform_cols[2]:
        platforms['twitter'] = st.checkbox("🐦 Twitter/X")
    with platform_cols[3]:
        platforms['threads'] = st.checkbox("🧵 Threads")
    
    selected_platforms = [p for p, selected in platforms.items() if selected]
    
    # Generate content button
    if st.button("🚀 Generate Content", type="primary"):
        if not selected_platforms:
            st.error("Please select at least one platform.")
            return
        
        with st.spinner("🔍 Researching and generating content..."):
            try:
                generated_content = {}
                progress_bar = st.progress(0)
                
                for i, platform in enumerate(selected_platforms):
                    # Update progress
                    progress_bar.progress((i + 1) / len(selected_platforms))
                    
                    # Generate content for each platform
                    response = perplexity_client.generate_content(
                        topic=topic,
                        content_type=content_type.lower().replace(" ", "_"),
                        platform=platform
                    )
                    
                    if response and 'choices' in response:
                        content = response['choices'][0]['message']['content']
                        generated_content[platform] = content
                        
                        # Store in database
                        st.session_state.db.store_content(
                            topic=topic,
                            platform=platform,
                            content=content,
                            metadata={'content_type': content_type}
                        )
                
                progress_bar.progress(1.0)
                st.session_state.generated_content = generated_content
                
                # Success message
                st.success(f"✅ Generated content for {len(generated_content)} platforms!")
                
                # Show generated content
                display_generated_content(generated_content)
                
            except Exception as e:
                st.error(f"❌ Error generating content: {str(e)}")

def display_generated_content(content_dict):
    """Display generated content with platform-specific formatting"""
    
    st.subheader("📋 Generated Content")
    
    # Create tabs for each platform
    if content_dict:
        tabs = st.tabs([platform.title() for platform in content_dict.keys()])
        
        for i, (platform, content) in enumerate(content_dict.items()):
            with tabs[i]:
                platform_info = get_platform_info(platform)
                
                # Platform header
                st.markdown(f"### {platform_info['icon']} {platform.title()}")
                st.markdown(f"**Character Limit:** {platform_info['char_limit']} characters")
                
                # Content display
                st.text_area(
                    f"{platform.title()} Content",
                    value=content,
                    height=200,
                    key=f"content_{platform}",
                    help=f"Content optimized for {platform}"
                )
                
                # Character count
                char_count = len(content)
                if char_count <= platform_info['char_limit']:
                    st.success(f"✅ {char_count}/{platform_info['char_limit']} characters")
                else:
                    st.warning(f"⚠️ {char_count}/{platform_info['char_limit']} characters (over limit)")
                
                # Refinement section
                st.markdown("#### 🔧 Refine Content")
                refinement_prompt = st.text_input(
                    "How would you like to improve this content?",
                    placeholder="Make it more engaging, add statistics, simplify language...",
                    key=f"refinement_{platform}"
                )
                
                if st.button(f"✨ Refine {platform.title()} Content", key=f"refine_{platform}"):
                    refine_content(platform, refinement_prompt)

def refine_content(platform, refinement_prompt):
    """Refine content based on user feedback"""
    
    if not refinement_prompt:
        st.error("Please enter refinement instructions.")
        return
    
    perplexity_client = initialize_perplexity_client()
    if not perplexity_client:
        return
    
    current_content = st.session_state.generated_content.get(platform, "")
    
    with st.spinner(f"🔄 Refining {platform} content..."):
        try:
            # Create refinement prompt
            refinement_request = f"""
            Please refine this {platform} content based on the user's request: "{refinement_prompt}"
            
            Current content:
            {current_content}
            
            Keep the content optimized for {platform} platform requirements.
            """
            
            # Call Perplexity API for refinement
            response = perplexity_client.generate_content(
                topic="content_refinement",
                content_type="refinement",
                platform=platform,
                custom_prompt=refinement_request
            )
            
            if response and 'choices' in response:
                refined_content = response['choices'][0]['message']['content']
                st.session_state.generated_content[platform] = refined_content
                st.success("✅ Content refined successfully!")
                st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error refining content: {str(e)}")

def social_media_page():
    """Social media connection and posting interface"""
    
    st.header("📱 Social Media Integration")
    
    social_manager = st.session_state.social_manager
    
    # Platform connection status
    st.subheader("🔗 Platform Connections")
    
    platforms = ['bluesky', 'linkedin', 'twitter', 'threads']
    
    for platform in platforms:
        platform_integration = social_manager.get_platform(platform)
        
        with st.expander(f"{platform.title()} - {'✅ Connected' if platform_integration.is_connected else '❌ Not Connected'}"):
            
            if platform_integration.is_connected:
                # Show connected user info
                user_info = platform_integration.user_info
                st.success(f"Connected as: {user_info.get('handle', user_info.get('name', 'User'))}")
                
                if st.button(f"Disconnect from {platform.title()}", key=f"disconnect_{platform}"):
                    platform_integration.disconnect()
                    social_manager.save_connections()
                    st.rerun()
            
            else:
                # Connection interface
                if platform == 'bluesky':
                    username = st.text_input(f"{platform.title()} Username/Email", key=f"{platform}_user")
                    password = st.text_input(f"{platform.title()} Password", type="password", key=f"{platform}_pass")
                    
                    if st.button(f"Connect to {platform.title()}", key=f"connect_{platform}"):
                        if username and password:
                            success, message = platform_integration.connect({
                                "username": username,
                                "password": password
                            })
                            if success:
                                st.success(message)
                                social_manager.save_connections()
                                st.rerun()
                            else:
                                st.error(message)
                
                else:
                    # Demo connection for other platforms
                    if st.button(f"Demo Connect to {platform.title()}", key=f"demo_{platform}"):
                        success, message = platform_integration.connect({"demo": True})
                        if success:
                            st.success(message)
                            social_manager.save_connections()
                            st.rerun()
    
    # Publishing interface
    if st.session_state.generated_content:
        st.subheader("📤 Publish Content")
        
        # Select platforms to publish to
        connected_platforms = social_manager.get_connected_platforms()
        
        if connected_platforms:
            selected_for_publishing = st.multiselect(
                "Select platforms to publish to:",
                connected_platforms,
                default=connected_platforms
            )
            
            if st.button("🚀 Publish to Selected Platforms", type="primary"):
                publish_content(social_manager, selected_for_publishing)
        else:
            st.info("Connect to social media platforms to enable publishing.")

def publish_content(social_manager, platforms):
    """Publish content to selected platforms"""
    
    if not st.session_state.generated_content:
        st.error("No content available to publish.")
        return
    
    results = {}
    
    with st.spinner("📤 Publishing content..."):
        for platform in platforms:
            if platform in st.session_state.generated_content:
                content = st.session_state.generated_content[platform]
                success, message = social_manager.get_platform(platform).post_content(content)
                results[platform] = (success, message)
    
    # Display results
    st.subheader("📊 Publishing Results")
    
    for platform, (success, message) in results.items():
        if success:
            st.success(f"✅ {platform.title()}: {message}")
        else:
            st.error(f"❌ {platform.title()}: {message}")

def analytics_page():
    """Analytics and insights dashboard"""
    
    st.header("📊 Analytics Dashboard")
    
    # Sample analytics data (replace with real data from your database)
    sample_data = {
        'Platform': ['LinkedIn', 'Bluesky', 'Twitter', 'Threads'],
        'Posts': [15, 23, 31, 12],
        'Engagement': [245, 189, 156, 78],
        'Reach': [1250, 890, 1100, 450]
    }
    
    df = pd.DataFrame(sample_data)
    
    # Metrics overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Posts", df['Posts'].sum())
    with col2:
        st.metric("Total Engagement", df['Engagement'].sum())
    with col3:
        st.metric("Total Reach", df['Reach'].sum())
    with col4:
        avg_engagement = df['Engagement'].sum() / df['Posts'].sum()
        st.metric("Avg Engagement/Post", f"{avg_engagement:.1f}")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Posts by platform
        fig_posts = px.bar(df, x='Platform', y='Posts', title='Posts by Platform')
        st.plotly_chart(fig_posts, use_container_width=True)
    
    with col2:
        # Engagement by platform
        fig_engagement = px.pie(df, values='Engagement', names='Platform', title='Engagement Distribution')
        st.plotly_chart(fig_engagement, use_container_width=True)
    
    # AI Insights
    st.subheader("🤖 AI-Powered Insights")
    
    insights = [
        "📈 LinkedIn posts generate 40% higher engagement than other platforms",
        "⏰ Best posting time: 9-11 AM for maximum reach",
        "📝 Trend Analysis content performs 25% better than other types",
        "🎯 Posts with questions get 60% more comments"
    ]
    
    for insight in insights:
        st.info(insight)

def main():
    """Main application"""
    
    # Initialize session state
    initialize_session_state()
    
    # Show header
    show_header()
    
    # Initialize Perplexity client
    perplexity_client = initialize_perplexity_client()
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.selectbox("Choose a page:", [
        "🏠 Home",
        "📝 Generate Content", 
        "📱 Social Media",
        "📊 Analytics"
    ])
    
    # API key status in sidebar
    if perplexity_client:
        st.sidebar.success("✅ Perplexity API Connected")
    else:
        st.sidebar.warning("⚠️ Perplexity API Key Required")
        st.sidebar.markdown("Add your API key above to use the content generator.")
    
    # Show different pages based on selection
    if page == "🏠 Home":
        show_home_page()
    elif page == "📝 Generate Content":
        if perplexity_client:
            content_generation_page(perplexity_client)
        else:
            st.error("Please configure your Perplexity API key to generate content.")
    elif page == "📱 Social Media":
        social_media_page()
    elif page == "📊 Analytics":
        analytics_page()

def show_home_page():
    """Display home page with app overview"""
    
    st.markdown("""
    ## 🎯 Welcome to the AI Content Generator
    
    Transform your social media strategy with AI-powered content generation and refinement.
    """)
    
    # Feature overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 AI-Powered Generation</h3>
            <p>Uses Perplexity's Sonar Reasoning API for research-backed content creation with real-time insights.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>🎨 Platform Optimization</h3>
            <p>Automatically formats content for LinkedIn, Twitter/X, Bluesky, and Threads with optimal character counts.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🔄 Iterative Refinement</h3>
            <p>Human-AI collaboration allows you to refine content until it's perfect for your audience.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Analytics Insights</h3>
            <p>Track performance and get AI-powered recommendations to improve your content strategy.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick start guide
    st.markdown("""
    ## 🚀 Quick Start Guide
    
    1. **Add API Key**: Enter your Perplexity API key in the sidebar
    2. **Generate Content**: Choose a topic and platforms, then click generate
    3. **Refine**: Use AI to improve your content with specific feedback
    4. **Connect & Publish**: Link your social accounts and publish directly
    5. **Analyze**: Track performance and optimize your strategy
    """)
    
    # Demo section
    if st.button("🎬 Watch Demo Video"):
        st.markdown("**[🎥 Watch the Complete Demo](https://youtu.be/JRp7JAR7ifo)**")

if __name__ == "__main__":
    main()
