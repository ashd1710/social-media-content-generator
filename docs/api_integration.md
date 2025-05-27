# 🔌 Perplexity API Integration

## Overview

This project showcases **advanced integration** with Perplexity's Sonar API, going beyond basic content generation to demonstrate sophisticated AI-driven workflows that leverage the full potential of Perplexity's reasoning capabilities.

---

## 🚀 **Core API Usage**

### **Primary Integration: Sonar Reasoning Model**

We use Perplexity's `sonar-reasoning` model, which provides:
- **Real-time web search** and current information access
- **Chain-of-thought reasoning** for complex analysis
- **Citation support** for factual accuracy
- **Multi-step problem solving** capabilities

```python
# Base API configuration
class PerplexityClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("PERPLEXITY_API_KEY")
        self.base_url = "https://api.perplexity.ai"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
```

---

## 🎯 **Innovation 1: Advanced Content Generation**

### **Sophisticated Prompt Engineering**

Our content generation uses **dual-prompt architecture** with specialized system and user prompts:

```python
def generate_content(self, topic: str, content_type: str, platform: str):
    # Create specialized system prompt for platform and content type
    system_prompt = self._create_system_prompt(content_type, platform)
    
    # Create research-focused user prompt
    user_prompt = self._create_user_prompt(topic, content_type, platform)
    
    payload = {
        "model": "sonar-reasoning",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
```

### **Platform-Specific System Prompts**

Each platform gets customized instructions:

```python
platform_guidelines = {
    "linkedin": """
    Write in a professional tone suitable for LinkedIn. 
    Content should be insightful, detailed (up to 1300 characters), 
    and include 2-3 relevant hashtags. Format with clear paragraphs 
    and bullet points when applicable.
    """,
    
    "twitter": """
    Create concise content for Twitter/X under 280 characters. 
    Use engaging language, 1-2 relevant hashtags, and a conversational tone. 
    Consider adding a question or call to action when appropriate.
    """,
    
    "bluesky": """
    Write for Bluesky with a community-focused approach under 300 characters. 
    Use a slightly more casual tone than Twitter while maintaining professionalism.
    """,
    
    "threads": """
    Create content for Threads with a visual-first mindset. 
    Write in a casual, conversational tone with short paragraphs.
    """
}
```

### **Research-Driven User Prompts**

```python
def _create_user_prompt(self, topic: str, content_type: str, platform: str):
    return f"""
    Research and create {content_type} content about {topic} for {platform}. 
    
    Focus on:
    - Recent developments and breakthrough technologies
    - Practical implications for professionals and businesses  
    - Current trends and market analysis
    - Actionable insights and recommendations
    
    Ensure the content is well-researched, engaging, and formatted 
    appropriately for the platform.
    """
```

---

## 🔄 **Innovation 2: Iterative AI Refinement** *(Hackathon Differentiator)*

### **The Refinement Breakthrough**

Our **most innovative feature** uses Perplexity API for iterative content improvement - a novel approach that treats content creation as an ongoing conversation with AI:

```python
def refine_content(self, original_content: str, refinement_prompt: str, platform: str):
    """
    Revolutionary refinement system using Perplexity for iterative improvement.
    This represents a new paradigm in AI content creation.
    """
    
    system_prompt = f"""
    You are an expert content optimizer specializing in {platform} content.
    
    Your task is to improve the provided content based on the specific 
    refinement request while:
    1. Maintaining the original intent and core message
    2. Preserving platform-specific formatting requirements
    3. Enhancing engagement and readability
    4. Adding value through the requested improvements
    
    Original content context: {platform} social media post
    Character limit: {self._get_platform_limit(platform)}
    """
    
    user_prompt = f"""
    Original Content:
    {original_content}
    
    Refinement Request:
    {refinement_prompt}
    
    Please provide the improved version that incorporates this refinement 
    while maintaining the content's effectiveness for {platform}.
    """
    
    # Use Perplexity's reasoning to iteratively improve content
    response = self._make_api_request(system_prompt, user_prompt)
    return response
```

### **Pre-Built Refinement Suggestions**

We offer one-click improvements that showcase Perplexity's versatility:

```python
REFINEMENT_SUGGESTIONS = {
    "engaging": "Make this content more engaging and attention-grabbing while maintaining professionalism",
    "statistics": "Add relevant statistics or data points to strengthen the arguments",
    "casual": "Make the tone more casual and conversational while keeping the key insights",
    "cta": "Add a compelling call-to-action that encourages audience engagement",
    "trending": "Incorporate current trending topics or recent developments in this field",
    "storytelling": "Transform this into a more narrative-driven format with storytelling elements"
}
```

### **Refinement History Tracking**

```python
class RefinementHistory:
    def __init__(self):
        self.history = []
        self.current_index = -1
    
    def add_refinement(self, content: str, prompt: str):
        """Track each refinement step with the ability to revert"""
        self.history.append({
            'content': content,
            'prompt': prompt,
            'timestamp': datetime.now()
        })
        self.current_index = len(self.history) - 1
    
    def revert_to_previous(self):
        """Revert to previous version in refinement chain"""
        if self.current_index > 0:
            self.current_index -= 1
            return self.history[self.current_index]['content']
```

---

## 📊 **Innovation 3: AI-Powered Analytics Insights**

### **Performance Analysis with Perplexity**

```python
def generate_performance_insights(self, content_metrics: dict):
    """
    Use Perplexity to analyze content performance and generate actionable insights
    """
    
    system_prompt = """
    You are a social media analytics expert. Analyze the provided content 
    performance data and generate specific, actionable recommendations for 
    content strategy improvement.
    """
    
    user_prompt = f"""
    Analyze this content performance data and provide insights:
    
    Metrics: {content_metrics}
    
    Please provide:
    1. Key performance patterns identified
    2. Specific recommendations for improvement
    3. Trending topics to focus on
    4. Optimal posting strategies
    5. Content format suggestions
    """
    
    insights = self._make_api_request(system_prompt, user_prompt)
    return insights
```

---

## 🛠️ **Technical Implementation Details**

### **API Request Architecture**

```python
def _make_api_request(self, system_prompt: str, user_prompt: str, model: str = "sonar-reasoning"):
    """
    Centralized API request handling with error management and optimization
    """
    
    endpoint = f"{self.base_url}/chat/completions"
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000,
        "stream": False  # For consistent response handling
    }
    
    try:
        response = requests.post(
            endpoint, 
            headers=self.headers, 
            json=payload,
            timeout=30  # Reasonable timeout for content generation
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise PerplexityAPIError(f"API request failed: {response.status_code}")
            
    except requests.exceptions.Timeout:
        raise PerplexityAPIError("Request timed out - please try again")
    except requests.exceptions.ConnectionError:
        raise PerplexityAPIError("Connection error - check internet connection")
```

### **Error Handling Strategy**

```python
class PerplexityAPIError(Exception):
    """Custom exception for Perplexity API errors"""
    pass

def handle_api_errors(func):
    """Decorator for consistent API error handling"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PerplexityAPIError as e:
            st.error(f"API Error: {str(e)}")
            return None
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            return None
    return wrapper
```

---

## 📈 **Performance Optimization**

### **Request Optimization**

1. **Smart Caching**: Cache recent API responses to avoid redundant calls
2. **Batch Processing**: Group related requests when possible
3. **Timeout Management**: Appropriate timeouts for user experience
4. **Rate Limiting**: Respect API limits with exponential backoff

```python
class APICache:
    def __init__(self, ttl_seconds=300):  # 5-minute cache
        self.cache = {}
        self.ttl = ttl_seconds
    
    def get_cached_response(self, cache_key: str):
        if cache_key in self.cache:
            timestamp, response = self.cache[cache_key]
            if time.time() - timestamp < self.ttl:
                return response
        return None
    
    def cache_response(self, cache_key: str, response: str):
        self.cache[cache_key] = (time.time(), response)
```

---

## 🔍 **API Usage Patterns**

### **Content Generation Flow**

1. **Research Phase**: Perplexity gathers current information on the topic
2. **Analysis Phase**: Chain-of-thought reasoning processes the information
3. **Creation Phase**: Platform-optimized content is generated
4. **Validation Phase**: Content is checked against platform requirements

### **Refinement Workflow**

1. **Context Preservation**: Original content maintains core message
2. **Enhancement Application**: Specific improvements are applied
3. **Quality Assurance**: Refined content meets platform standards
4. **Iteration Support**: Multiple refinement rounds supported

### **Analytics Integration**

1. **Data Collection**: Performance metrics are gathered
2. **Pattern Analysis**: Perplexity identifies trends and insights
3. **Recommendation Generation**: Actionable suggestions are created
4. **Strategy Optimization**: Content strategy is continuously improved

---

## 🎯 **Why This Integration Stands Out**

### **Beyond Basic Generation**

Most AI applications use APIs for simple request-response patterns. Our integration showcases:

1. **Sophisticated Prompt Engineering**: Multi-layered prompts for specialized outputs
2. **Iterative AI Conversations**: Using AI to improve AI-generated content
3. **Context-Aware Processing**: Platform and audience-specific optimization
4. **Real-Time Research Integration**: Current information for timely content

### **Production-Ready Architecture**

- **Error Resilience**: Comprehensive error handling and recovery
- **Performance Optimization**: Caching and request optimization
- **Scalability**: Modular design for easy extension
- **User Experience**: Smooth workflows with progress feedback

### **Innovation Showcase**

The **iterative refinement system** represents a novel approach to AI content creation that could inspire new product categories and workflows in the AI space.

---

## 📚 **API Documentation References**

- **Perplexity API Docs**: [https://docs.perplexity.ai/](https://docs.perplexity.ai/)
- **Sonar Models Overview**: [Model capabilities and specifications](https://docs.perplexity.ai/docs/model-cards)
- **API Rate Limits**: [Usage guidelines and limits](https://docs.perplexity.ai/docs/pricing)

---

## 🔮 **Future API Enhancements**

### **Planned Integrations**

1. **Sonar Deep Research**: For comprehensive topic research
2. **Multi-Modal Content**: Image and video content generation
3. **Real-Time Trends**: Dynamic topic suggestion based on current events
4. **Collaborative AI**: Multiple AI agents working together on content

### **Advanced Features**

1. **Sentiment Analysis**: Content tone optimization
2. **Audience Targeting**: Personalized content for different demographics
3. **A/B Testing**: AI-driven content variation testing
4. **Predictive Analytics**: AI-powered performance forecasting

---

*This integration demonstrates the cutting-edge potential of Perplexity's Sonar API in creating sophisticated, user-centric AI applications that go far beyond basic content generation.*
