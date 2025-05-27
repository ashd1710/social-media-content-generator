# 🚀 Social Media Content Generator
## Powered by Perplexity Sonar API

[![Demo Video](https://img.shields.io/badge/▶️_Demo-YouTube-r)](]https://youtu.be/JRp7JAR7ifo)
[![Perplexity API](https://img.shields.io/badge/Powered_by-Perplexity_Sonar-blue)](https://www.perplexity.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> **Transform your social media strategy with AI-powered content generation and refinement**

An intelligent content generator that leverages **Perplexity's Sonar Reasoning API** to create, refine, and publish platform-optimized content for LinkedIn, Twitter/X, Bluesky, and Threads. Built for the **Perplexity Global Hackathon 2025**.

---

## ✨ **Key Features**

### 🤖 **Advanced AI Content Generation**
- **Research-Driven Content**: Uses Perplexity Sonar API for real-time research and current information
- **Custom Topic Support**: Generate content on any topic with intelligent context understanding
- **Platform Optimization**: Content automatically formatted for LinkedIn, Twitter/X, Bluesky, and Threads
- **Multiple Content Types**: Trend analysis, news summaries, deep dives, and custom formats

### 🔄 **Innovative Iterative Refinement**
- **AI-Powered Improvement**: Unique refinement system using Perplexity for iterative content enhancement
- **Quick Suggestions**: One-click refinement with pre-built prompts ("Make more engaging", "Add statistics")
- **Custom Refinement**: Unlimited custom improvement prompts with progress tracking
- **Refinement History**: Track changes and revert to previous versions

### 📱 **Multi-Platform Publishing**
- **Live Bluesky Integration**: Real posting capability via AT Protocol
- **Professional Demo Modes**: LinkedIn, Twitter/X, and Threads with realistic workflows
- **Platform-Specific Formatting**: Character limits, hashtags, and tone optimization
- **Tiered Platform Access**: Free and premium integration levels

### 📊 **Professional Analytics Dashboard**
- **AI-Generated Insights**: Performance recommendations powered by data analysis
- **5-Tab Analytics Suite**: Overview, AI Insights, Timing Analysis, Hashtag Performance, Detailed Metrics
- **Visual Performance Tracking**: Interactive charts and trend analysis
- **Optimization Recommendations**: Data-driven suggestions for content improvement

### 🎨 **Beautiful User Experience**
- **Modern Interface**: Professional Streamlit design with custom CSS and animations
- **Smooth Workflows**: Intuitive content creation to publishing pipeline
- **Progress Tracking**: Visual feedback with celebration animations
- **Mobile Responsive**: Works seamlessly across devices

---

## 🏆 **Hackathon Innovation Highlights**

### **Advanced Perplexity Integration**
This project pushes beyond basic content generation to showcase the full potential of Perplexity's Sonar API:

- **Sophisticated Prompt Engineering**: Custom system and user prompts optimized for each platform and content type
- **Chain-of-Thought Reasoning**: Leverages Sonar Reasoning for complex analysis and insights
- **Iterative AI Improvement**: Unique refinement workflow that uses Perplexity to progressively enhance content quality
- **Real-Time Research**: Incorporates current events and trending information for timely, relevant content

### **Production-Ready Architecture**
- **Modular Design**: Clean separation of concerns with dedicated modules for API integration, formatting, and platform management
- **Error Handling**: Comprehensive error management with user-friendly feedback
- **Session Management**: Persistent state management for smooth user experience
- **Scalable Foundation**: Ready for production deployment with proper security and optimization

---

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8 or higher
- Perplexity API key ([Get yours here](https://www.perplexity.ai/))

### **Installation**
```bash
# Clone the repository
git clone https://github.com/ashd1710/social-media-content-generator.git
cd social-media-content-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your PERPLEXITY_API_KEY
```

### **Run the Application**
```bash
streamlit run app.py
```

Visit `http://localhost:8501` to access the application.

---

## 🏗️ **Architecture Overview**

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface (Streamlit)               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌────────┐ │
│  │  Generate   │ │ Preview &   │ │  Connect    │ │ Analytics│ │
│  │  Content    │ │ Refine      │ │ Accounts    │ │Dashboard │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                Content Processing Engine                     │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐│
│  │ Perplexity API  │ │ Content         │ │ Platform        ││
│  │ Integration     │ │ Formatter       │ │ Adapters        ││
│  │ • Generation    │ │ • LinkedIn      │ │ • Bluesky       ││
│  │ • Refinement    │ │ • Twitter/X     │ │ • LinkedIn      ││
│  │ • Research      │ │ • Bluesky       │ │ • Twitter/X     ││
│  │                 │ │ • Threads       │ │ • Threads       ││
│  └─────────────────┘ └─────────────────┘ └─────────────────┘│
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data & Analytics Layer                   │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐│
│  │ SQLite Database │ │ Performance     │ │ Session State   ││
│  │ • Content       │ │ Analytics       │ │ Management      ││
│  │ • Metrics       │ │ • Engagement    │ │ • User Prefs    ││
│  │ • History       │ │ • Optimization  │ │ • Connections   ││
│  └─────────────────┘ └─────────────────┘ └─────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

---

## 🔌 **Perplexity API Usage**

### **Content Generation**
```python
# Example of our sophisticated Perplexity integration
response = client.generate_content(
    topic="AI in Healthcare",
    content_type="trend_analysis", 
    platform="linkedin",
    model="sonar-reasoning"
)
```

### **Iterative Refinement** *(Innovation)*
```python
# Unique refinement workflow using Perplexity
refined_content = client.refine_content(
    original_content=content,
    refinement_prompt="Make this more engaging with a specific example from a major hospital",
    platform="linkedin"
)
```

**Why This Matters**: Our refinement system represents a novel approach to AI content creation, using Perplexity's reasoning capabilities to iteratively improve content quality through multiple AI-driven enhancement rounds.

---

## 📱 **Platform Support**

| Platform | Status | Features | Character Limit |
|----------|--------|----------|----------------|
| **Bluesky** | ✅ Live Integration | Real posting, AT Protocol | 300 chars |
| **LinkedIn** | 🎭 Professional Demo | Formatted posts, hashtags | 1300 chars |
| **Twitter/X** | 🎭 Professional Demo | Optimized threads, engagement | 280 chars |
| **Threads** | 🎭 Professional Demo | Visual-first content | Variable |

*Live integrations require API access. Demo modes provide realistic publishing workflows.*

---

## 🎯 **Use Cases**

- **Content Creators**: Generate consistent, high-quality posts across multiple platforms
- **Marketing Teams**: Create data-driven content with real-time research backing
- **Thought Leaders**: Develop insightful analysis on trending topics in your industry
- **Small Businesses**: Maintain active social media presence without dedicated resources
- **Developers**: Understand advanced AI integration patterns and multi-platform optimization

---

## 📊 **Analytics Features**

### **AI-Powered Insights**
- Performance trend analysis with recommendations
- Optimal posting time suggestions
- Hashtag effectiveness tracking
- Content type performance comparison

### **Visual Dashboards**
- Real-time metrics with interactive charts
- 7-day performance trends
- Platform-specific analytics
- Engagement pattern analysis

---

## 🛠️ **Technical Stack**

- **Frontend**: Streamlit with custom CSS and animations
- **AI Engine**: Perplexity Sonar Reasoning API
- **Backend**: Python with modular architecture
- **Database**: SQLite for analytics and history
- **APIs**: Bluesky AT Protocol, platform-specific integrations
- **Deployment**: Streamlit Cloud ready

---

## 📁 **Project Structure**

```
social-media-content-generator/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Dependencies
├── .env.example                    # Environment variables template
├── README.md                       # This file
├── LICENSE                         # MIT License
│
├── src/                           # Source code modules
│   ├── perplexity_client.py       # Perplexity API integration
│   ├── content_formatter.py       # Platform-specific formatting
│   ├── platform_preview.py        # Content preview components  
│   ├── social_integrations.py     # Social media API integrations
│   └── utils.py                   # Utility functions
│
├── data/                          # Data storage
│   └── content_generator.db       # SQLite database
│
├── docs/                          # Documentation
│   ├── setup.md                   # Detailed setup guide
│   ├── api_integration.md         # Perplexity API usage details
│   └── user_guide.md              # User documentation
│
└── tests/                         # Test suite
    └── test_*.py                  # Test files
```

---

## 🎬 **Demo Video**

[![Demo Thumbnail](https://img.shields.io/badge/▶️_Watch_Demo-3_minutes-red?style=for-the-badge)](https://youtu.be/JRp7JAR7ifo)

**Demo Highlights:**
- Live content generation with real-time research
- Iterative AI refinement workflow demonstration
- Multi-platform formatting and publishing
- Analytics dashboard walkthrough
- End-to-end content creation pipeline

---

## 🏅 **Awards & Recognition**

**Built for Perplexity Global Hackathon 2025**
- **Category**: Most Fun / Creative Project
- **Innovation**: Advanced iterative refinement using Sonar API
- **Technical Excellence**: Production-ready architecture with beautiful UX

---

## 🤝 **Contributing**

We welcome contributions! Please see our contributing guidelines for details.

### **Development Setup**
```bash
# Clone and setup development environment
git clone https://github.com/ashd1710/social-media-content-generator.git
cd social-media-content-generator
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **Running Tests**
```bash
# Run the test suite
python -m pytest tests/
```

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 **Links**

- **[Perplexity AI](https://www.perplexity.ai/)** - Powering our content generation
- **[Demo Video](https://youtu.be/JRp7JAR7ifo)** - 3-minute demonstration
- **[Documentation](docs/)** - Comprehensive guides and API details
- **[Issues](https://github.com/ashd1710/social-media-content-generator/issues)** - Bug reports and feature requests

---

## 🙏 **Acknowledgments**

- **Perplexity AI** for providing the powerful Sonar API that makes this innovation possible
- **Streamlit** for the excellent framework that enables rapid UI development
- **Open Source Community** for the incredible tools and libraries that support this project

---

<div align="center">

### **Ready to revolutionize your social media content strategy?**

**[🚀 Get Started](#-quick-start) • [📖 Read the Docs](docs/) • [🎬 Watch Demo](https://youtu.be/JRp7JAR7ifo)**

*Built with ❤️ for the Perplexity Global Hackathon 2025*

</div>
