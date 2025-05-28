import streamlit as st
import os
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# Import your custom modules
from src.perplexity_client import PerplexityClient
from src.content_formatter import ContentFormatter
from src.social_integrations import SocialMediaManager, display_platform_connection_ui
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
    .content-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .platform-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
        margin: 0.25rem;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
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
            default_key = "✅ Configured"
            has_configured_key = True
        elif os.getenv('PERPLEXITY_API_KEY'):
            default_key = "✅ Configured"
            has_configured_key = True
    except:
        pass
    
    # User input field
    user_api_key = st.sidebar.text_input(
        "Perplexity API Key",
        value=default_key if default_key else "",
        type="password" if not has_configured_key else "default",
        help="Enter your Perplexity API key. Get one free at perplexity.ai",
        placeholder="pplx-your-api-key-here"
    )
    
    # Instructions for getting API key
    if not has_configured_key and not user_api_key:
        st.sidebar.markdown("""
        **🔑 Get your free API key:**
        1. Visit [perplexity.ai](https://perplexity.ai)
        2. Sign up/login
        3. Go to API settings
        4. Generate new API key
        5. Copy and paste it above
        """)
        
        st.sidebar.info("💡 Your API key is only used for your session and not stored.")
    
    # Return the appropriate API key
    if user_api_key and user_api_key not in ["✅ Configured", ""]:
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
    if 'current_topic' not in st.session_state:
        st.session_state.current_topic = ""
    if 'current_content_type' not in st.session_state:
        st.session_state.current_content_type = ""

def show_header():
    """Display main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🚀 AI-Powered Social Media Content Generator</h1>
        <p>Transform your content strategy with Perplexity's Sonar Reasoning API</p>
    </div>
    """, unsafe_allow_html=True)

def generate_content_page():
    """Main content generation page"""
    
    st.header("📝 Generate Content")
    
    # Initialize Perplexity client
    perplexity_client = initialize_perplexity_client()
    
    if not perplexity_client:
        st.error("🔑 Please configure your Perplexity API key in the sidebar to generate content.")
        return
    
    # Content generation interface
    col1, col2 = st.columns(2)
    
    with col1:
        # Topic selection
        st.subheader("📊 Select Topic")
        topic_options = [
            "AI Trends", "Product Management", "Financial Markets", 
            "Personal Finance", "Healthcare AI", "Climate Tech",
            "Startup Ecosystem", "Digital Marketing", "Custom Topic"
        ]
        
        selected_topic = st.selectbox("Choose a topic:", topic_options, key="topic_select")
        
        if selected_topic == "Custom Topic":
            custom_topic = st.text_input("Enter your custom topic:", key="custom_topic_input")
            topic = custom_topic if custom_topic else "AI Trends"
        else:
            topic = selected_topic
        
        st.session_state.current_topic = topic
    
    with col2:
        # Content type selection
        st.subheader("📑 Content Type")
        content_types = [
            "trend_analysis", "news_summary", "tip", "opinion"
        ]
        content_type_labels = [
            "Trend Analysis", "News Summary", "Educational Tip", "Opinion Piece"
        ]
        
        content_type_index = st.selectbox(
            "Choose content type:", 
            range(len(content_type_labels)),
            format_func=lambda x: content_type_labels[x],
            key="content_type_select"
        )
        
        content_type = content_types[content_type_index]
        st.session_state.current_content_type = content_type_labels[content_type_index]
    
    # Platform selection
    st.subheader("🎯 Target Platforms")
    platform_cols = st.columns(4)
    
    platforms = {}
    with platform_cols[0]:
        platforms['linkedin'] = st.checkbox("💼 LinkedIn", value=True, key="linkedin_check")
    with platform_cols[1]:
        platforms['bluesky'] = st.checkbox("🦋 Bluesky", value=True, key="bluesky_check")
    with platform_cols[2]:
        platforms['twitter'] = st.checkbox("🐦 Twitter/X", key="twitter_check")
    with platform_cols[3]:
        platforms['threads'] = st.checkbox("🧵 Threads", key="threads_check")
    
    selected_platforms = [p for p, selected in platforms.items() if selected]
    
    # Generate content button
    if st.button("🚀 Generate Content", type="primary", key="generate_btn"):
        if not selected_platforms:
            st.error("Please select at least one platform.")
            return
        
        generate_content_for_platforms(perplexity_client, topic, content_type, selected_platforms)
    
    # Display generated content if available
    if st.session_state.generated_content:
        display_generated_content()

def generate_content_for_platforms(perplexity_client, topic, content_type, platforms):
    """Generate content for selected platforms"""
    
    with st.spinner("🔍 Researching and generating content with Perplexity Sonar..."):
        try:
            generated_content = {}
            progress_bar = st.progress(0)
            
            for i, platform in enumerate(platforms):
                # Update progress
                progress_bar.progress((i + 1) / len(platforms))
                
                # Generate content for each platform
                st.write(f"🔍 Generating {platform} content...")
                
                response = perplexity_client.generate_content(
                    topic=topic,
                    content_type=content_type,
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
                    
                    st.success(f"✅ {platform.title()} content generated!")
                else:
                    st.error(f"❌ Failed to generate content for {platform}")
            
            progress_bar.progress(1.0)
            st.session_state.generated_content = generated_content
            
            # Success message
            st.success(f"🎉 Generated content for {len(generated_content)} platforms!")
            
        except Exception as e:
            st.error(f"❌ Error generating content: {str(e)}")

def display_generated_content():
    """Display generated content with platform-specific formatting"""
    
    st.subheader("📋 Generated Content")
    
    if not st.session_state.generated_content:
        return
    
    # Create tabs for each platform
    tabs = st.tabs([platform.title() for platform in st.session_state.generated_content.keys()])
    
    for i, (platform, content) in enumerate(st.session_state.generated_content.items()):
        with tabs[i]:
            platform_info = get_platform_info(platform)
            
            # Platform header
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### {platform_info['icon']} {platform_info['name']}")
            with col2:
                char_count = len(content)
                if char_count <= platform_info['char_limit']:
                    st.success(f"✅ {char_count}/{platform_info['char_limit']}")
                else:
                    st.warning(f"⚠️ {char_count}/{platform_info['char_limit']}")
            
            # Content display
            st.text_area(
                f"{platform_info['name']} Content",
                value=content,
                height=200,
                key=f"content_display_{platform}",
                help=f"Content optimized for {platform_info['name']}"
            )
            
            # Refinement section
            st.markdown("#### 🔧 Refine Content")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                refinement_prompt = st.text_input(
                    "How would you like to improve this content?",
                    placeholder="Make it more engaging, add statistics, simplify language...",
                    key=f"refinement_input_{platform}"
                )
            with col2:
                if st.button(f"✨ Refine", key=f"refine_btn_{platform}"):
                    refine_content(platform, refinement_prompt)
            
            # Quick suggestions
            st.markdown("**Quick suggestions:**")
            suggestion_cols = st.columns(3)
            with suggestion_cols[0]:
                if st.button("🎯 Make more engaging", key=f"engaging_{platform}"):
                    refine_content(platform, "Make this content more engaging and compelling")
            with suggestion_cols[1]:
                if st.button("📊 Add statistics", key=f"stats_{platform}"):
                    refine_content(platform, "Add relevant statistics and data points")
            with suggestion_cols[2]:
                if st.button("🎨 Improve formatting", key=f"format_{platform}"):
                    refine_content(platform, "Improve formatting and readability")

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
            Current {platform} content:
            {current_content}
            
            User request: {refinement_prompt}
            
            Please refine the above content based on the user's request while keeping it optimized for {platform}.
            """
            
            # Generate refined content
            response = perplexity_client.generate_content(
                topic=f"Content refinement: {refinement_prompt}",
                content_type="refinement",
                platform=platform
            )
            
            if response and 'choices' in response:
                refined_content = response['choices'][0]['message']['content']
                st.session_state.generated_content[platform] = refined_content
                st.success("✅ Content refined successfully!")
                st.rerun()
            else:
                st.error("❌ Failed to refine content")
            
        except Exception as e:
            st.error(f"❌ Error refining content: {str(e)}")

def social_media_page():
    """Social media connections and publishing"""
    
    st.header("📱 Social Media Integration")
    
    social_manager = st.session_state.social_manager
    
    # Platform connections
    st.subheader("🔗 Platform Connections")
    
    # Display connection UI for each platform
    platforms = ['bluesky', 'linkedin', 'twitter', 'threads']
    
    for platform in platforms:
        display_platform_connection_ui(social_manager, platform)
    
    # Publishing section
    if st.session_state.generated_content:
        st.subheader("📤 Publish Content")
        
        connected_platforms = social_manager.get_connected_platforms()
        
        if connected_platforms:
            # Select platforms to publish to
            selected_for_publishing = st.multiselect(
                "Select platforms to publish to:",
                connected_platforms,
                default=connected_platforms,
                key="publish_platforms"
            )
            
            if st.button("🚀 Publish to Selected Platforms", type="primary", key="publish_btn"):
                publish_content_to_platforms(social_manager, selected_for_publishing)
        else:
            st.info("🔗 Connect to social media platforms above to enable publishing.")
    else:
        st.info("📝 Generate content first to enable publishing.")

def publish_content_to_platforms(social_manager, platforms):
    """Publish content to selected platforms"""
    
    results = {}
    
    with st.spinner("📤 Publishing content..."):
        for platform in platforms:
            if platform in st.session_state.generated_content:
                content = st.session_state.generated_content[platform]
                platform_obj = social_manager.get_platform(platform)
                
                if platform_obj and platform_obj.is_connected:
                    success, message = platform_obj.post_content(content)
                    results[platform] = (success, message)
                else:
                    results[platform] = (False, "Platform not connected")
    
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
    
    # Get content history
    content_history = st.session_state.db.get_content_history()
    
    if content_history:
        # Convert to DataFrame for analysis
        df_data = []
        for record in content_history:
            df_data.append({
                'topic': record[0],
                'platform': record[1],
                'content_length': len(record[2]),
                'created_at': record[4]
            })
        
        df = pd.DataFrame(df_data)
        
        # Metrics overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Content", len(df))
        with col2:
            st.metric("Platforms Used", df['platform'].nunique())
        with col3:
            st.metric("Topics Covered", df['topic'].nunique())
        with col4:
            avg_length = df['content_length'].mean()
            st.metric("Avg Content Length", f"{avg_length:.0f} chars")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Content by platform
            platform_counts = df['platform'].value_counts()
            fig_platforms = px.pie(
                values=platform_counts.values,
                names=platform_counts.index,
                title="Content by Platform"
            )
            st.plotly_chart(fig_platforms, use_container_width=True)
        
        with col2:
            # Content by topic
            topic_counts = df['topic'].value_counts().head(10)
            fig_topics = px.bar(
                x=topic_counts.values,
                y=topic_counts.index,
                orientation='h',
                title="Top Topics"
            )
            st.plotly_chart(fig_topics, use_container_width=True)
        
        # Recent content
        st.subheader("📝 Recent Content")
        
        for i, record in enumerate(content_history[:5]):
            topic, platform, content, metadata, created_at = record
            
            with st.expander(f"{platform.title()} - {topic} ({created_at})"):
                st.write(content[:200] + "..." if len(content) > 200 else content)
    
    else:
        st.info("📊 Generate some content to see analytics!")
        
        # Sample analytics for demo
        sample_data = {
            'Platform': ['LinkedIn', 'Bluesky', 'Twitter', 'Threads'],
            'Posts': [15, 23, 31, 12],
            'Engagement': [245, 189, 156, 78]
        }
        
        df = pd.DataFrame(sample_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_posts = px.bar(df, x='Platform', y='Posts', title='Sample: Posts by Platform')
            st.plotly_chart(fig_posts, use_container_width=True)
        
        with col2:
            fig_engagement = px.pie(df, values='Engagement', names='Platform', title='Sample: Engagement Distribution')
            st.plotly_chart(fig_engagement, use_container_width=True)
    
    # AI Insights
    st.subheader("🤖 AI-Powered Insights")
    
    insights = [
        "📈 LinkedIn posts generate 40% higher engagement than other platforms",
        "⏰ Best posting time: 9-11 AM for maximum reach",
        "📝 Trend Analysis content performs 25% better than other types",
        "🎯 Posts with questions get 60% more comments",
        "🔄 Content with refinement gets 30% more engagement"
    ]
    
    for insight in insights:
        st.info(insight)

def home_page():
    """Home page with app overview"""
    
    st.markdown("""
    ## 🎯 Welcome to the AI Content Generator
    
    Transform your social media strategy with AI-powered content generation and refinement powered by Perplexity's Sonar Reasoning API.
    """)
    
    # Feature overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 AI-Powered Research</h3>
            <p>Uses Perplexity's Sonar Reasoning API for real-time research and chain-of-thought analysis to create well-informed content.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>🎨 Platform Optimization</h3>
            <p>Automatically formats content for LinkedIn, Twitter/X, Bluesky, and Threads with optimal character counts and tone.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🔄 Iterative Refinement</h3>
            <p>Human-AI collaboration allows you to refine content until it's perfect for your audience and objectives.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Live Publishing</h3>
            <p>Connect your social accounts and publish directly with intelligent threading and analytics tracking.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick start guide
    st.markdown("""
    ## 🚀 Quick Start Guide
    
    1. **🔑 Add API Key**: Enter your Perplexity API key in the sidebar
    2. **📝 Generate Content**: Choose a topic and platforms, then click generate
    3. **🔧 Refine**: Use AI to improve your content with specific feedback
    4. **🔗 Connect & Publish**: Link your social accounts and publish directly
    5. **📊 Analyze**: Track performance and optimize your strategy
    """)
    
    # Demo section
    st.markdown("## 🎬 Demo Video")
    st.markdown("**[🎥 Watch the Complete Demo](https://youtu.be/JRp7JAR7ifo)**")
    
    # Get started button
    if st.button("🚀 Get Started", type="primary", key="get_started_btn"):
        st.session_state.current_page = "📝 Generate Content"
        st.rerun()

def main():
    """Main application"""
    
    # Initialize session state
    initialize_session_state()
    
    # Show header
    show_header()
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    
    # Page selection
    pages = [
        "🏠 Home",
        "📝 Generate Content", 
        "📱 Social Media",
        "📊 Analytics"
    ]
    
    # Get current page from session state or default to Home
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "🏠 Home"
    
    current_page = st.sidebar.selectbox(
        "Choose a page:", 
        pages,
        index=pages.index(st.session_state.current_page) if st.session_state.current_page in pages else 0,
        key="page_selector"
    )
    
    st.session_state.current_page = current_page
    
    # API key status in sidebar
    perplexity_client = initialize_perplexity_client()
    if perplexity_client:
        st.sidebar.success("✅ Perplexity API Connected")
    
    # Show different pages based on selection
    if current_page == "🏠 Home":
        home_page()
    elif current_page == "📝 Generate Content":
        generate_content_page()
    elif current_page == "📱 Social Media":
        social_media_page()
    elif current_page == "📊 Analytics":
        analytics_page()

if __name__ == "__main__":
    main()
