# 🛠️ Installation Guide

## Prerequisites

Before installing the Social Media Content Generator, ensure you have the following:

### **System Requirements**
- **Python**: Version 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: At least 4GB RAM recommended
- **Storage**: 500MB free disk space

### **Required Accounts**
- **Perplexity API Key**: [Sign up here](https://www.perplexity.ai/) (Required)
- **Social Media Accounts**: For platform integration (Optional)

---

## 🚀 Quick Installation

### **Method 1: Standard Installation**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ashd1710/social-media-content-generator.git
   cd social-media-content-generator
   ```

2. **Create Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit the .env file with your API keys
   # Add your Perplexity API key:
   # PERPLEXITY_API_KEY=pplx-your-api-key-here
   ```

5. **Run the Application**
   ```bash
   streamlit run app.py
   ```

6. **Access the Application**
   - Open your browser and go to: `http://localhost:8501`

---

## 🔐 API Configuration

### **Required: Perplexity API Key**

1. **Get Your API Key**:
   - Visit [Perplexity AI](https://www.perplexity.ai/)
   - Sign up for an account
   - Navigate to API section
   - Generate your API key

2. **Add to Environment**:
   ```bash
   # In your .env file
   PERPLEXITY_API_KEY=pplx-your-actual-api-key-here
   ```

### **Optional: Social Media Platform APIs**

#### **Bluesky (Live Integration Available)**
```bash
# In your .env file
BLUESKY_USERNAME=your-username.bsky.social
BLUESKY_PASSWORD=your-app-password
```

To get Bluesky app password:
1. Go to Bluesky Settings → App Passwords
2. Create new app password
3. Use this password (not your main account password)

#### **LinkedIn (Demo Mode)**
```bash
# In your .env file
LINKEDIN_CLIENT_ID=your-linkedin-client-id
LINKEDIN_CLIENT_SECRET=your-linkedin-client-secret
```

#### **Twitter/X (Demo Mode)**
```bash
# In your .env file
TWITTER_BEARER_TOKEN=your-twitter-bearer-token
TWITTER_API_KEY=your-twitter-api-key
TWITTER_API_SECRET=your-twitter-api-secret
```

---

## 🐳 Docker Installation (Alternative)

If you prefer using Docker:

1. **Build Docker Image**
   ```bash
   docker build -t social-media-content-generator .
   ```

2. **Run Container**
   ```bash
   docker run -p 8501:8501 -e PERPLEXITY_API_KEY=your-key social-media-content-generator
   ```

---

## 🔧 Development Setup

For contributors and developers who want to modify the code:

### **Additional Development Dependencies**
```bash
pip install -r requirements-dev.txt
```

### **Pre-commit Hooks**
```bash
# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/

# Format code
black src/
flake8 src/
```

### **Environment Variables for Development**
```bash
# In your .env file
DEBUG=True
LOG_LEVEL=DEBUG
```

---

## 📁 File Structure After Installation

```
social-media-content-generator/
├── app.py                      # ✅ Main application entry point
├── .env                        # ✅ Your environment variables (created)
├── .env.example               # ✅ Template for environment variables
├── requirements.txt           # ✅ Python dependencies
├── venv/                      # ✅ Virtual environment (created)
│
├── src/                       # ✅ Source code modules
│   ├── perplexity_client.py   # ✅ Perplexity API integration
│   ├── content_formatter.py   # ✅ Platform formatting logic
│   ├── social_integrations.py # ✅ Social media APIs
│   └── utils.py              # ✅ Utility functions
│
├── data/                      # ✅ Data storage (auto-created)
│   └── content_generator.db   # ✅ SQLite database (auto-created)
│
└── docs/                      # ✅ Documentation
    ├── setup.md               # ✅ This file
    ├── api_integration.md     # ✅ API usage details
    └── user_guide.md          # ✅ User documentation
```

---

## ✅ Verification Steps

After installation, verify everything is working:

### **1. Test Application Launch**
```bash
streamlit run app.py
```
- ✅ Application should open in browser at `http://localhost:8501`
- ✅ You should see the "Generate Content" page

### **2. Test Perplexity API Connection**
1. Navigate to "Generate Content" page
2. Enter any topic (e.g., "AI trends")
3. Select content type and platform
4. Click "Generate Content"
5. ✅ You should see generated content within 10-15 seconds

### **3. Test Platform Integration**
1. Go to "Connect Accounts" page
2. ✅ You should see platform connection options
3. For Bluesky: Test connection if credentials are configured

### **4. Test Analytics Dashboard**
1. Navigate to "Analytics" page
2. ✅ You should see 5 tabs with demo data
3. ✅ Charts and metrics should load properly

---

## 🐛 Troubleshooting

### **Common Issues and Solutions**

#### **"ModuleNotFoundError" when running**
```bash
# Solution: Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Then reinstall dependencies
pip install -r requirements.txt
```

#### **"Invalid API Key" error**
```bash
# Solution: Check your .env file
cat .env | grep PERPLEXITY_API_KEY

# Ensure format is correct:
# PERPLEXITY_API_KEY=pplx-your-actual-key-here
```

#### **Streamlit won't start**
```bash
# Solution: Check if port 8501 is available
netstat -an | grep 8501

# Or use different port
streamlit run app.py --server.port 8502
```

#### **Content generation fails**
1. **Check API Key**: Ensure Perplexity API key is valid and has credits
2. **Check Internet**: Application needs internet access for API calls
3. **Check Logs**: Look at terminal output for specific error messages

#### **Platform connections fail**
- **Bluesky**: Verify username format (must include .bsky.social)
- **Other Platforms**: Ensure you're using app passwords, not main passwords

### **Getting Help**

If you encounter issues not covered here:

1. **Check the logs**: Terminal output often shows helpful error messages
2. **Verify environment**: Ensure all environment variables are set correctly
3. **Test internet connection**: API calls require active internet
4. **Create an issue**: [Report bugs on GitHub](https://github.com/ashd1710/social-media-content-generator/issues)

---

## 🚀 Next Steps

After successful installation:

1. **Read the [User Guide](user_guide.md)** for detailed feature walkthroughs
2. **Explore [API Integration docs](api_integration.md)** to understand Perplexity usage
3. **Watch the [Demo Video](../README.md#-demo-video)** for feature overview
4. **Start generating content** and experience the AI-powered workflow!

---

## 📞 Support

- **Documentation**: Check other files in the `docs/` folder
- **Issues**: [GitHub Issues](https://github.com/ashd1710/social-media-content-generator/issues)
- **API Support**: [Perplexity Documentation](https://docs.perplexity.ai/)

---

*Installation guide last updated: Day 18 of Perplexity Hackathon 2025*
