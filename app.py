import streamlit as st
import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from typing import Dict, List

# Import your existing modules
from src.perplexity_client import PerplexityClient
from src.content_formatter import ContentFormatter
from src.platform_preview import PlatformPreview
from src.social_integrations import SocialMediaManager, display_platform_connection_ui, get_platform_tier_info

# Page configuration
st.set_page_config(
    page_title="Social Media Content Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    .main {
        padding-top: 2rem;
    }
    
    /* Custom color palette */
    :root {
        --primary-color: #2E86AB;
        --secondary-color: #A23B72;
        --accent-color: #F18F01;
        --success-color: #06D6A0;
        --warning-color: #FFD23F;
        --error-color: #F72C25;
        --dark-gray: #2D3748;
        --light-gray: #F7FAFC;
        --border-color: #E2E8F0;
    }
    
    /* Typography improvements */
    .main, .sidebar {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    }
    
    /* Enhanced titles */
    h1 {
        color: var(--dark-gray) !important;
        font-weight: 700 !important;
        font-size: 2.5rem !important;
        margin-bottom: 1rem !important;
        border-bottom: 3px solid var(--primary-color);
        padding-bottom: 0.5rem;
    }
    
    h2 {
        color: var(--dark-gray) !important;
        font-weight: 600 !important;
        font-size: 1.8rem !important;
        margin: 1.5rem 0 1rem 0 !important;
    }
    
    h3 {
        color: var(--primary-color) !important;
        font-weight: 600 !important;
        font-size: 1.3rem !important;
        margin: 1rem 0 0.5rem 0 !important;
    }
    
    /* Enhanced sidebar */
    .css-1d391kg {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%) !important;
    }
    
    .css-1d391kg .css-10trblm {
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* Custom buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }
    
    /* Primary button special styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--accent-color) 0%, #FF6B35 100%) !important;
        font-size: 1.1rem !important;
        padding: 0.8rem 2rem !important;
        font-weight: 700 !important;
    }
    
    /* Secondary button styling */
    .stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, var(--success-color) 0%, #059669 100%) !important;
    }
    
    /* Enhanced metric cards */
    .css-1r6slb0 {
        background: white !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
        transition: all 0.3s ease !important;
    }
    
    .css-1r6slb0:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.1) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Enhanced expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, var(--light-gray) 0%, white 100%) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        color: var(--dark-gray) !important;
    }
    
    .streamlit-expanderContent {
        border: 1px solid var(--border-color) !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
        background: white !important;
    }
    
    /* Enhanced input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border-radius: 8px !important;
        border: 2px solid var(--border-color) !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(46, 134, 171, 0.1) !important;
    }
    
    /* Enhanced tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: var(--light-gray) !important;
        border-radius: 12px !important;
        padding: 0.5rem !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 8px !important;
        color: var(--dark-gray) !important;
        font-weight: 500 !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: var(--primary-color) !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    
    /* Enhanced info/success/warning/error messages */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        font-weight: 500 !important;
        padding: 1rem 1.5rem !important;
    }
    
    /* Success messages */
    .stSuccess {
        background: linear-gradient(135deg, var(--success-color)15, var(--success-color)08) !important;
        border-left: 4px solid var(--success-color) !important;
    }
    
    /* Info messages */
    .stInfo {
        background: linear-gradient(135deg, var(--primary-color)15, var(--primary-color)08) !important;
        border-left: 4px solid var(--primary-color) !important;
    }
    
    /* Warning messages */
    .stWarning {
        background: linear-gradient(135deg, var(--warning-color)15, var(--warning-color)08) !important;
        border-left: 4px solid var(--warning-color) !important;
    }
    
    /* Error messages */
    .stError {
        background: linear-gradient(135deg, var(--error-color)15, var(--error-color)08) !important;
        border-left: 4px solid var(--error-color) !important;
    }
    
    /* Enhanced charts */
    .js-plotly-plot {
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
    }
    
    /* Enhanced dataframe */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid var(--border-color) !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
    }
    
    /* Loading spinner enhancement */
    .stSpinner > div {
        border-top-color: var(--primary-color) !important;
        border-right-color: var(--primary-color) !important;
    }
    
    /* Animation for page transitions */
    .main > div {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Enhanced progress bars */
    .stProgress .css-zt5igj {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%) !important;
        border-radius: 8px !important;
    }
    
    /* Responsive design improvements */
    @media (max-width: 768px) {
        h1 {
            font-size: 2rem !important;
        }
        
        .stButton > button {
            width: 100% !important;
            margin: 0.25rem 0 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = {}
if 'social_manager' not in st.session_state:
    st.session_state.social_manager = SocialMediaManager()

# Sidebar navigation
st.sidebar.title("🚀 Content Generator")
st.sidebar.markdown("*Powered by Perplexity Sonar*")

page = st.sidebar.selectbox(
    "Navigate",
    ["📝 Generate Content", "👀 Preview & Edit", "🔗 Connect Accounts", "📅 Schedule & Publish", "📊 Analytics"]
)

# Main content based on page selection
if page == "📝 Generate Content":
    st.title("📝 Generate Content")
    st.markdown("Create engaging content for multiple social media platforms using Perplexity's Sonar Reasoning API.")
    
    # Content generation form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Content Settings")
        
        topic = st.text_input(
            "Enter Topic",
            placeholder="e.g., Artificial Intelligence, Marketing Strategies, Cryptocurrency, etc.",
            help="Enter any topic you want to generate content about"
        )
        
        content_type_option = st.selectbox(
            "Content Type",
            ["Trend Analysis", "News Summary", "Deep Dive", "Custom"]
        )
        
        if content_type_option == "Custom":
            custom_content_type = st.text_input(
                "Describe the content type:",
                placeholder="e.g., How-to guide, Case study, Interview, Product review, etc.",
                help="Describe what type of content you want to generate"
            )
            content_type = custom_content_type if custom_content_type.strip() else "analysis"
        else:
            # Map display names to internal values
            content_type_mapping = {
                "Trend Analysis": "trend_analysis",
                "News Summary": "news_summary", 
                "Deep Dive": "deep_dive"
            }
            content_type = content_type_mapping[content_type_option]
        
        platforms = st.multiselect(
            "Target Platforms",
            ["LinkedIn", "Twitter", "Bluesky", "Threads"],
            default=["LinkedIn", "Twitter"]
        )
    
    with col2:
        st.subheader("Generation Options")
        
        tone = st.selectbox(
            "Tone",
            ["Professional", "Casual", "Conversational", "Authoritative"]
        )
        
        include_hashtags = st.checkbox("Include hashtags", value=True)
        include_citations = st.checkbox("Include citations", value=True)
        
        temperature = st.slider(
            "Creativity Level",
            min_value=0.1,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher values = more creative, Lower values = more focused"
        )
    
    # Generate content button
    if st.button("🚀 Generate Content", type="primary"):
        if not platforms:
            st.error("Please select at least one platform")
        elif not topic.strip():
            st.error("Please enter a topic")
        elif content_type_option == "Custom" and not custom_content_type.strip():
            st.error("Please describe the custom content type")
        else:
            with st.spinner("Generating content with Perplexity Sonar..."):
                try:
                    # Initialize clients
                    perplexity_client = PerplexityClient()
                    content_formatter = ContentFormatter()
                    
                    # Generate content for each platform
                    generated_content = {}
                    
                    for platform in platforms:
                        # Generate raw content using Perplexity
                        response = perplexity_client.generate_content(
                            topic=topic.lower().replace(" ", "_"),
                            content_type=content_type,
                            platform=platform.lower()
                        )
                        
                        raw_content = response["choices"][0]["message"]["content"]
                        
                        # Extract final content if it contains reasoning
                        if "Let me" in raw_content or "I need to" in raw_content or "From the search results" in raw_content:
                            # Split by double newlines and take the last substantial paragraph
                            paragraphs = raw_content.split('\n\n')
                            for paragraph in reversed(paragraphs):
                                paragraph = paragraph.strip()
                                if len(paragraph) > 50 and not any(phrase in paragraph for phrase in ["Let me", "I need to", "From the search", "The user wants"]):
                                    raw_content = paragraph
                                    break
                        
                        # Format content for platform
                        formatted_content = content_formatter.format_for_platform(
                            content=raw_content,
                            platform=platform.lower(),
                            include_hashtags=include_hashtags,
                            tone=tone.lower()
                        )
                        
                        generated_content[platform.lower()] = {
                            "raw": raw_content,
                            "formatted": formatted_content,
                            "timestamp": datetime.now().isoformat()
                        }
                    
                    # Store in session state
                    st.session_state.generated_content = generated_content
                    
                    st.success("✅ Content generated successfully!")
                    st.info("👀 Go to 'Preview & Edit' to see your content")
                    
                except Exception as e:
                    st.error(f"Error generating content: {str(e)}")

elif page == "👀 Preview & Edit":
    st.title("👀 Preview & Edit")
    
    if not st.session_state.generated_content:
        st.info("No content generated yet. Go to 'Generate Content' first.")
    else:
        st.markdown("Review, edit, and refine your generated content before publishing.")
        
        # Platform tabs
        platform_names = list(st.session_state.generated_content.keys())
        tabs = st.tabs([platform.title() for platform in platform_names])
        
        updated_content = {}
        
        for i, platform in enumerate(platform_names):
            with tabs[i]:
                content_data = st.session_state.generated_content[platform]
                
                # Display platform preview
                preview = PlatformPreview()
                preview.display_platform_preview(platform, content_data["formatted"])
                
                # Create two columns for editing options
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    # Manual edit functionality
                    with st.expander("✏️ Manual Edit", expanded=False):
                        edited_content = st.text_area(
                            f"Edit {platform.title()} content:",
                            value=content_data["formatted"],
                            height=150,
                            key=f"edit_{platform}"
                        )
                        
                        if st.button(f"Update {platform.title()} Content", key=f"update_{platform}"):
                            updated_content[platform] = edited_content
                            st.success(f"✅ {platform.title()} content updated!")
                
                with col2:
                    # AI Refinement functionality
                    with st.expander("🎯 AI Refinement", expanded=False):
                        st.markdown("**Tell the AI how to improve your content:**")
                        
                        # Refinement suggestions
                        st.markdown("💡 **Quick suggestions:**")
                        suggestion_cols = st.columns(2)
                        
                        with suggestion_cols[0]:
                            if st.button("Make more engaging", key=f"engaging_{platform}"):
                                st.session_state[f"refinement_prompt_{platform}"] = "Make this content more engaging and interactive"
                            if st.button("Add statistics", key=f"stats_{platform}"):
                                st.session_state[f"refinement_prompt_{platform}"] = "Add relevant statistics or data points to support the claims"
                        
                        with suggestion_cols[1]:
                            if st.button("Make more casual", key=f"casual_{platform}"):
                                st.session_state[f"refinement_prompt_{platform}"] = "Make the tone more casual and conversational"
                            if st.button("Add call-to-action", key=f"cta_{platform}"):
                                st.session_state[f"refinement_prompt_{platform}"] = "Add a compelling call-to-action to encourage engagement"
                        
                        # Custom refinement prompt
                        refinement_prompt = st.text_area(
                            "Custom refinement request:",
                            value=st.session_state.get(f"refinement_prompt_{platform}", ""),
                            placeholder="e.g., Make it more professional, add examples, include a question, change the tone...",
                            height=80,
                            key=f"refinement_prompt_{platform}"
                        )
                        
                        # Refine button
                        if st.button(f"🔄 Refine Content", key=f"refine_{platform}", type="secondary"):
                            if refinement_prompt.strip():
                                # Enhanced loading state with progress
                                progress_container = st.container()
                                with progress_container:
                                    st.markdown("### 🎯 AI Refinement in Progress...")
                                    progress_bar = st.progress(0)
                                    status_text = st.empty()
                                    
                                    # Simulate progress steps
                                    status_text.text("🔍 Analyzing original content...")
                                    progress_bar.progress(20)
                                    
                                    try:
                                        # Initialize Perplexity client
                                        perplexity_client = PerplexityClient()
                                        
                                        status_text.text("🧠 Processing refinement request...")
                                        progress_bar.progress(50)
                                        
                                        # Refine content
                                        response = perplexity_client.refine_content(
                                            original_content=content_data["formatted"],
                                            refinement_request=refinement_prompt,
                                            platform=platform
                                        )
                                        
                                        status_text.text("✨ Generating refined content...")
                                        progress_bar.progress(80)
                                        
                                        refined_content = response["choices"][0]["message"]["content"]
                                        
                                        # Extract final content if it contains reasoning
                                        if "Let me" in refined_content or "I need to" in refined_content:
                                            paragraphs = refined_content.split('\n\n')
                                            for paragraph in reversed(paragraphs):
                                                paragraph = paragraph.strip()
                                                if len(paragraph) > 50 and not any(phrase in paragraph for phrase in ["Let me", "I need to", "From the search", "The user wants"]):
                                                    refined_content = paragraph
                                                    break
                                        
                                        status_text.text("💾 Updating content...")
                                        progress_bar.progress(100)
                                        
                                        # Update content in session state
                                        st.session_state.generated_content[platform]["formatted"] = refined_content
                                        st.session_state.generated_content[platform]["refinement_history"] = st.session_state.generated_content[platform].get("refinement_history", [])
                                        st.session_state.generated_content[platform]["refinement_history"].append({
                                            "request": refinement_prompt,
                                            "content": refined_content,
                                            "timestamp": datetime.now().isoformat()
                                        })
                                        
                                        # Clear progress and show success
                                        progress_container.empty()
                                        st.success(f"✅ {platform.title()} content refined successfully!")
                                        st.balloons()  # Celebration animation!
                                        st.rerun()
                                        
                                    except Exception as e:
                                        progress_container.empty()
                                        st.error(f"❌ Error refining content: {str(e)}")
                            else:
                                st.error("⚠️ Please enter a refinement request")
                
                # Show refinement history if available
                if "refinement_history" in content_data and content_data["refinement_history"]:
                    with st.expander("📊 Refinement History", expanded=False):
                        for idx, refinement in enumerate(content_data["refinement_history"]):
                            st.markdown(f"**Refinement {idx + 1}:** {refinement['request']}")
                            st.markdown(f"*{refinement['timestamp'][:19].replace('T', ' ')}*")
                            if st.button(f"Revert to this version", key=f"revert_{platform}_{idx}"):
                                st.session_state.generated_content[platform]["formatted"] = refinement["content"]
                                st.rerun()
                            st.markdown("---")
        
        # Update session state with manually edited content
        if updated_content:
            for platform, content in updated_content.items():
                st.session_state.generated_content[platform]["formatted"] = content

elif page == "🔗 Connect Accounts":
    st.title("🔗 Connect Social Media Accounts")
    st.markdown("Connect your social media accounts to enable direct publishing.")
    
    # Platform tier explanation
    st.info("""
    **Platform Tiers:**
    - 🆓 **Free Tier**: Bluesky (live posting + threading), LinkedIn (live API integration)
    - 💎 **Premium Tier**: Twitter/X ($100+/month), Threads (business verification required)
    - 🚧 **Demo Mode**: Available for all platforms for hackathon presentation
    """)
    
    # Display connection status overview
    manager = st.session_state.social_manager
    platform_status = manager.get_all_platform_status()
    
    # Connection status cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status = platform_status["bluesky"]
        if status["connected"]:
            st.success("🟢 Bluesky Connected")
        else:
            st.error("🔴 Bluesky Disconnected")
    
    with col2:
        status = platform_status["linkedin"]
        if status["connected"]:
            st.success("🟢 LinkedIn Connected")
        else:
            st.error("🔴 LinkedIn Disconnected")
    
    with col3:
        status = platform_status["twitter"]
        if status["connected"]:
            st.success("🟢 Twitter Connected")
        else:
            st.error("🔴 Twitter Disconnected")
    
    with col4:
        status = platform_status["threads"]
        if status["connected"]:
            st.success("🟢 Threads Connected")
        else:
            st.error("🔴 Threads Disconnected")
    
    st.markdown("---")
    
    # Platform connection interfaces
    platform_tabs = st.tabs(["🟦 Bluesky", "💼 LinkedIn", "🐦 Twitter/X", "🧵 Threads"])
    
    with platform_tabs[0]:
        display_platform_connection_ui(manager, "bluesky")
    
    with platform_tabs[1]:
        display_platform_connection_ui(manager, "linkedin")
    
    with platform_tabs[2]:
        display_platform_connection_ui(manager, "twitter")
    
    with platform_tabs[3]:
        display_platform_connection_ui(manager, "threads")

elif page == "📅 Schedule & Publish":
    st.title("📅 Schedule & Publish")
    
    if not st.session_state.generated_content:
        st.info("No content generated yet. Go to 'Generate Content' first.")
    else:
        manager = st.session_state.social_manager
        connected_platforms = manager.get_connected_platforms()
        
        if not connected_platforms:
            st.warning("No social media accounts connected. Go to 'Connect Accounts' first.")
        else:
            st.markdown("Publish your content immediately or schedule it for later.")
            
            # Publishing options
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📤 Immediate Publishing")
                
                # Platform selection for publishing
                available_platforms = [p for p in st.session_state.generated_content.keys() if p in connected_platforms]
                
                if available_platforms:
                    selected_platforms = st.multiselect(
                        "Select platforms to publish to:",
                        available_platforms,
                        default=available_platforms
                    )
                    
                    if st.button("🚀 Publish Now", type="primary"):
                        if selected_platforms:
                            # Show content length warnings for platforms that support threading
                            content_warnings = []
                            for platform in selected_platforms:
                                content = st.session_state.generated_content[platform]["formatted"]
                                if platform == "bluesky" and len(content) > 280:
                                    thread_count = len(content) // 280 + 1
                                    content_warnings.append(f"🧵 **Bluesky**: Content will be split into ~{thread_count} thread posts")
                                elif platform == "twitter" and len(content) > 280:
                                    content_warnings.append(f"⚠️ **Twitter**: Content exceeds 280 characters (may be truncated)")
                            
                            if content_warnings:
                                for warning in content_warnings:
                                    st.info(warning)
                            
                            # Enhanced publishing with detailed progress
                            progress_container = st.container()
                            with progress_container:
                                st.markdown("### 📤 Publishing Content...")
                                
                                progress_bar = st.progress(0)
                                status_text = st.empty()
                                results_container = st.container()
                                
                                total_platforms = len(selected_platforms)
                                
                                # Prepare content for publishing
                                content_dict = {
                                    platform: st.session_state.generated_content[platform]["formatted"]
                                    for platform in selected_platforms
                                }
                                
                                # Publish to each platform with progress updates
                                results = {}
                                for i, platform in enumerate(selected_platforms):
                                    status_text.text(f"📤 Publishing to {platform.title()}...")
                                    progress_bar.progress((i) / total_platforms)
                                    
                                    platform_obj = manager.get_platform(platform)
                                    if platform_obj and platform_obj.is_connected:
                                        content = content_dict.get(platform, "")
                                        if content:
                                            # Show special message for Bluesky threading
                                            if platform == "bluesky" and len(content) > 280:
                                                status_text.text(f"🧵 Creating Bluesky thread...")
                                            
                                            success, message = platform_obj.post_content(content)
                                            results[platform] = (success, message)
                                            
                                            # Show immediate result
                                            with results_container:
                                                if success:
                                                    if "thread" in message.lower():
                                                        st.success(f"🧵 {platform.title()}: {message}")
                                                    else:
                                                        st.success(f"✅ {platform.title()}: {message}")
                                                else:
                                                    st.error(f"❌ {platform.title()}: {message}")
                                        else:
                                            results[platform] = (False, "No content provided for this platform")
                                            with results_container:
                                                st.error(f"❌ {platform.title()}: No content provided")
                                    else:
                                        results[platform] = (False, "Platform not connected")
                                        with results_container:
                                            st.error(f"❌ {platform.title()}: Platform not connected")
                                    
                                    progress_bar.progress((i + 1) / total_platforms)
                                
                                # Final status
                                status_text.text("✅ Publishing complete!")
                                progress_bar.progress(1.0)
                                
                                # Summary
                                successful_posts = sum(1 for success, _ in results.values() if success)
                                if successful_posts == len(selected_platforms):
                                    st.balloons()  # Celebration for all successful!
                                    st.success(f"🎉 All {successful_posts} posts published successfully!")
                                else:
                                    st.warning(f"📊 {successful_posts}/{len(selected_platforms)} posts published successfully")
                        else:
                            st.error("Please select at least one platform")
                else:
                    st.info("No content available for connected platforms")
            
            with col2:
                st.subheader("⏰ Schedule Publishing")
                
                # Scheduling interface (basic implementation)
                schedule_date = st.date_input("Schedule Date", value=datetime.now().date())
                schedule_time = st.time_input("Schedule Time", value=datetime.now().time())
                
                if st.button("📅 Schedule Post"):
                    st.info("🚧 Scheduling functionality would be implemented with a job queue system (e.g., Celery, APScheduler)")
                    st.success(f"✅ Post scheduled for {schedule_date} at {schedule_time}")

elif page == "📊 Analytics":
    st.title("📊 Analytics Dashboard")
    st.markdown("Track your content performance and get AI-powered insights across all platforms.")
    
    # Create tabs for different analytics views
    analytics_tabs = st.tabs(["📈 Overview", "🎯 Insights", "⏰ Timing", "#️⃣ Hashtags", "📊 Detailed"])
    
    with analytics_tabs[0]:  # Overview Tab
        st.subheader("📈 Performance Overview")
        
        # Key metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Posts",
                value="44",
                delta="12",
                delta_color="normal"
            )
        
        with col2:
            st.metric(
                label="Total Engagement", 
                value="1,247",
                delta="156",
                delta_color="normal"
            )
        
        with col3:
            st.metric(
                label="Avg. Engagement Rate",
                value="3.8%",
                delta="0.7%",
                delta_color="normal"
            )
        
        with col4:
            st.metric(
                label="Total Reach",
                value="18.2K",
                delta="2.1K", 
                delta_color="normal"
            )
        
        st.markdown("---")
        
        # Platform performance comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📱 Platform Performance**")
            platform_data = {
                "Platform": ["LinkedIn", "Twitter", "Bluesky", "Threads"],
                "Posts": [12, 18, 8, 6],
                "Engagement": [156, 89, 34, 23],
                "Reach": [1240, 890, 340, 180],
                "Engagement_Rate": [4.2, 3.1, 2.8, 4.5]
            }
            df_platforms = pd.DataFrame(platform_data)
            
            # Enhanced bar chart
            st.bar_chart(df_platforms.set_index("Platform")[["Engagement", "Reach"]])
        
        with col2:
            st.markdown("**📊 Engagement Rate by Platform**")
            # Create a more detailed chart
            for _, row in df_platforms.iterrows():
                st.metric(
                    label=f"{row['Platform']} Engagement Rate",
                    value=f"{row['Engagement_Rate']}%",
                    delta=f"{row['Posts']} posts"
                )
        
        # Performance trends
        st.markdown("### 📈 7-Day Performance Trend")
        
        # Mock trend data
        dates = pd.date_range(start='2024-05-17', end='2024-05-23', freq='D')
        trend_data = {
            'Date': dates,
            'LinkedIn': [45, 52, 38, 61, 49, 67, 58],
            'Twitter': [23, 31, 28, 35, 41, 29, 33],
            'Bluesky': [12, 8, 15, 11, 18, 14, 16],
            'Threads': [8, 12, 6, 14, 9, 11, 13]
        }
        df_trends = pd.DataFrame(trend_data)
        df_trends = df_trends.set_index('Date')
        
        st.line_chart(df_trends)
    
    with analytics_tabs[1]:  # AI Insights Tab
        st.subheader("🎯 AI-Powered Insights & Recommendations")
        
        # Generate AI insights (simulated)
        st.markdown("### 🤖 Content Performance Insights")
        
        insights = [
            {
                "type": "success",
                "title": "🚀 Top Performing Content Type",
                "content": "Your 'Trend Analysis' posts generate 40% higher engagement than other content types. Consider creating more analytical content."
            },
            {
                "type": "info", 
                "title": "📱 Platform Optimization",
                "content": "LinkedIn posts with 3 hashtags perform 25% better than those with fewer. Your optimal LinkedIn post length is 800-1000 characters."
            },
            {
                "type": "warning",
                "title": "⏰ Timing Opportunity", 
                "content": "Your Twitter engagement drops 30% after 3 PM. Consider scheduling more content between 9-11 AM for better reach."
            },
            {
                "type": "info",
                "title": "🎯 Hashtag Strategy",
                "content": "Posts with #AI and #Technology hashtags receive 45% more engagement. These are your most effective hashtag combinations."
            }
        ]
        
        for insight in insights:
            if insight["type"] == "success":
                st.success(f"**{insight['title']}**\n\n{insight['content']}")
            elif insight["type"] == "warning":
                st.warning(f"**{insight['title']}**\n\n{insight['content']}")
            else:
                st.info(f"**{insight['title']}**\n\n{insight['content']}")
        
        st.markdown("### 📋 Action Items")
        st.markdown("""
        **Recommended Actions Based on Your Data:**
        
        1. **🎯 Content Strategy**: Create 2-3 more 'Trend Analysis' posts this week
        2. **📱 Platform Focus**: Increase LinkedIn posting frequency (highest engagement rate)
        3. **⏰ Timing**: Schedule Twitter posts between 9-11 AM
        4. **#️⃣ Hashtags**: Use #AI, #Technology, #Innovation combo more frequently
        5. **🔄 Refinement**: Use AI refinement feature to add questions to posts (increases engagement by 35%)
        """)
        
        # Content type performance
        st.markdown("### 📊 Content Type Effectiveness")
        
        content_performance = {
            "Content Type": ["Trend Analysis", "News Summary", "Deep Dive", "Tips"],
            "Avg Engagement": [67, 45, 52, 38],
            "Avg Reach": [890, 650, 720, 480],
            "Posts Created": [8, 12, 6, 18]
        }
        df_content = pd.DataFrame(content_performance)
        
        col1, col2 = st.columns(2)
        with col1:
            st.bar_chart(df_content.set_index("Content Type")["Avg Engagement"])
            st.caption("Average Engagement by Content Type")
        
        with col2:
            st.bar_chart(df_content.set_index("Content Type")["Avg Reach"]) 
            st.caption("Average Reach by Content Type")
    
    with analytics_tabs[2]:  # Timing Analysis Tab
        st.subheader("⏰ Optimal Posting Times")
        
        # Best times analysis
        st.markdown("### 🕒 Best Posting Times by Platform")
        
        timing_data = {
            "Platform": ["LinkedIn", "Twitter", "Bluesky", "Threads"],
            "Best_Time": ["9:00 AM", "10:30 AM", "2:00 PM", "7:00 PM"],
            "Peak_Engagement": ["9-11 AM", "10 AM-12 PM", "1-3 PM", "6-8 PM"],
            "Worst_Time": ["6:00 PM", "3:00 PM", "9:00 AM", "11:00 AM"]
        }
        df_timing = pd.DataFrame(timing_data)
        
        for _, row in df_timing.iterrows():
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label=f"🕘 {row['Platform']} Best Time",
                    value=row['Best_Time']
                )
            
            with col2:
                st.info(f"**Peak Hours:** {row['Peak_Engagement']}")
            
            with col3:
                st.error(f"**Avoid:** {row['Worst_Time']}")
        
        # Weekly heatmap simulation
        st.markdown("### 📅 Weekly Engagement Heatmap")
        
        # Create mock heatmap data
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        hours = ['9 AM', '12 PM', '3 PM', '6 PM', '9 PM']
        
        # Simulate engagement scores
        heatmap_data = []
        for day in days:
            day_data = []
            for hour in hours:
                # Simulate realistic engagement patterns
                base_score = np.random.uniform(20, 80)
                if hour in ['9 AM', '12 PM'] and day in ['Tuesday', 'Wednesday', 'Thursday']:
                    base_score += 20  # Higher engagement for business hours on weekdays
                day_data.append(base_score)
            heatmap_data.append(day_data)
        
        df_heatmap = pd.DataFrame(heatmap_data, index=days, columns=hours)
        st.dataframe(df_heatmap.round(1), use_container_width=True)
        st.caption("📊 Engagement scores by day and time (higher = better)")
    
    with analytics_tabs[3]:  # Hashtag Analysis Tab
        st.subheader("#️⃣ Hashtag Performance Analysis")
        
        # Top performing hashtags
        st.markdown("### 🏆 Top Performing Hashtags")
        
        hashtag_data = {
            "Hashtag": ["#AI", "#Technology", "#Innovation", "#Business", "#Future", "#Digital", "#Data", "#MachineLearning"],
            "Usage_Count": [15, 12, 10, 8, 7, 6, 5, 4],
            "Avg_Engagement": [67, 54, 48, 42, 38, 35, 29, 31],
            "Reach_Boost": ["+25%", "+18%", "+15%", "+12%", "+8%", "+6%", "+4%", "+7%"]
        }
        df_hashtags = pd.DataFrame(hashtag_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.bar_chart(df_hashtags.set_index("Hashtag")["Avg_Engagement"])
            st.caption("Average Engagement per Hashtag")
        
        with col2:
            st.bar_chart(df_hashtags.set_index("Hashtag")["Usage_Count"])
            st.caption("Hashtag Usage Frequency")
        
        # Hashtag recommendations
        st.markdown("### 💡 Hashtag Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("**🚀 High Performing & Underused**")
            st.markdown("""
            - **#MachineLearning**: High engagement (31), low usage (4 times)
            - **#Innovation**: Strong performance (48), moderate usage
            - **#Future**: Good engagement (38), consider using more
            """)
        
        with col2:
            st.warning("**⚠️ Overused with Declining Returns**")
            st.markdown("""
            - **#Business**: High usage but lower engagement
            - **#Digital**: Frequent use, consider alternating
            - **#Data**: Try combining with other hashtags
            """)
        
        # Hashtag combinations
        st.markdown("### 🔗 Best Hashtag Combinations")
        st.info("""
        **Top Performing Combinations:**
        
        1. **#AI + #Technology + #Innovation** → 78% avg engagement
        2. **#MachineLearning + #Data + #Future** → 71% avg engagement  
        3. **#Business + #Innovation + #Digital** → 65% avg engagement
        4. **#Technology + #Future + #Business** → 62% avg engagement
        """)
    
    with analytics_tabs[4]:  # Detailed Analytics Tab
        st.subheader("📊 Detailed Performance Metrics")
        
        # Comprehensive performance table
        detailed_data = {
            "Platform": ["LinkedIn", "LinkedIn", "Twitter", "Twitter", "Bluesky", "Bluesky", "Threads", "Threads"],
            "Content_Type": ["Trend Analysis", "News Summary", "Trend Analysis", "Deep Dive", "News Summary", "Tips", "Trend Analysis", "Tips"],
            "Posts": [6, 6, 9, 9, 4, 4, 3, 3],
            "Total_Engagement": [402, 336, 288, 234, 136, 68, 92, 46],
            "Avg_Engagement": [67, 56, 32, 26, 34, 17, 31, 15],
            "Total_Reach": [3720, 3100, 2520, 2070, 1020, 680, 690, 345],
            "Engagement_Rate": [4.5, 3.8, 3.2, 2.8, 3.1, 1.9, 4.2, 2.1],
            "Best_Time": ["9 AM", "11 AM", "10 AM", "2 PM", "3 PM", "1 PM", "7 PM", "8 PM"]
        }
        df_detailed = pd.DataFrame(detailed_data)
        
        # Interactive filters
        col1, col2 = st.columns(2)
        
        with col1:
            platform_filter = st.multiselect(
                "Filter by Platform:",
                options=df_detailed["Platform"].unique(),
                default=df_detailed["Platform"].unique()
            )
        
        with col2:
            content_filter = st.multiselect(
                "Filter by Content Type:",
                options=df_detailed["Content_Type"].unique(), 
                default=df_detailed["Content_Type"].unique()
            )
        
        # Apply filters
        filtered_df = df_detailed[
            (df_detailed["Platform"].isin(platform_filter)) & 
            (df_detailed["Content_Type"].isin(content_filter))
        ]
        
        # Display filtered data
        st.dataframe(filtered_df, use_container_width=True)
        
        # Summary statistics
        st.markdown("### 📈 Summary Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_posts = filtered_df["Posts"].sum()
            st.metric("Total Posts", total_posts)
        
        with col2:
            avg_engagement = filtered_df["Avg_Engagement"].mean()
            st.metric("Average Engagement", f"{avg_engagement:.1f}")
        
        with col3:
            avg_rate = filtered_df["Engagement_Rate"].mean()
            st.metric("Average Engagement Rate", f"{avg_rate:.1f}%")
        
        # Export functionality
        st.markdown("### 📥 Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Download CSV"):
                st.info("📁 CSV download functionality would be implemented here")
        
        with col2:
            if st.button("📈 Generate Report"):
                st.info("📋 Automated report generation would be implemented here")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 🏆 Hackathon Project")
st.sidebar.markdown("*Powered by Perplexity Sonar API*")
st.sidebar.markdown("**Day 18**: Threading & Final Polish")

# Add some spacing and branding
st.markdown("---")
st.markdown(
    "<div class='footer'>"
    "<strong>🚀 Social Media Content Generator</strong><br>"
    "Built with Streamlit & Perplexity Sonar API | Hackathon Project 2025<br>"
    "✨ Professional-Grade Content Intelligence Platform with AI Threading"
    "</div>",
    unsafe_allow_html=True
)
