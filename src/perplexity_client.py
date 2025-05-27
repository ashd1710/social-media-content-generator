import os
import requests
from typing import Dict, List, Optional, Union
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class PerplexityClient:
    """
    Client for interacting with Perplexity's Sonar Reasoning API.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the Perplexity API client.
        
        Args:
            api_key: Perplexity API key. If None, looks for PERPLEXITY_API_KEY environment variable.
        """
        self.api_key = api_key or os.environ.get("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise ValueError("Perplexity API key is required. Set it either as an argument or as PERPLEXITY_API_KEY environment variable.")
        
        self.base_url = "https://api.perplexity.ai"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_content(self, 
                        topic: str, 
                        content_type: str,
                        platform: str,
                        model: str = "sonar") -> Dict:
        """
        Generate content using Perplexity's Sonar API.
        
        Args:
            topic: The topic to generate content about
            content_type: Type of content (trend_analysis, news_summary, deep_dive, custom, etc.)
            platform: Target platform (linkedin, twitter, bluesky, threads)
            model: Perplexity model to use (default: sonar)
            
        Returns:
            Dict containing the API response with generated content
        """
        
        # Create a system prompt for the specified content type and platform
        system_prompt = self._create_system_prompt(content_type, platform)
        
        # Create user prompt based on the topic
        user_prompt = self._create_user_prompt(topic, content_type, platform)
        
        # Prepare the API request
        endpoint = f"{self.base_url}/chat/completions"
        payload = {
            "model": "sonar",  # Changed from sonar-reasoning to sonar
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 500  # Reduced for social media posts
        }
        
        # Make the API request
        response = requests.post(endpoint, headers=self.headers, json=payload)
        
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
        
        return response.json()
    
    def refine_content(self, original_content: str, refinement_request: str, platform: str) -> Dict:
        """
        Refine existing content based on user request.
        
        Args:
            original_content: The existing content to refine
            refinement_request: User's request for how to refine the content
            platform: Target platform (linkedin, twitter, bluesky, threads)
            
        Returns:
            Dict containing the API response with refined content
        """
        
        # Create refinement prompt
        system_prompt = self._create_refinement_system_prompt(platform)
        user_prompt = self._create_refinement_user_prompt(original_content, refinement_request, platform)
        
        # Prepare the API request
        endpoint = f"{self.base_url}/chat/completions"
        payload = {
            "model": "sonar",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        # Make the API request
        response = requests.post(endpoint, headers=self.headers, json=payload)
        
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
        
        return response.json()
    
    def _create_system_prompt(self, content_type: str, platform: str) -> str:
        """
        Create a system prompt based on content type and platform.
        """
        platform_guidelines = {
            "linkedin": "Write in a professional tone suitable for LinkedIn. Content should be insightful, detailed (up to 1300 characters), and include 2-3 relevant hashtags. Format with clear paragraphs and bullet points when applicable.",
            
            "twitter": "Create concise content for Twitter/X under 280 characters. Use engaging language, 1-2 relevant hashtags, and a conversational tone. Consider adding a question or call to action when appropriate.",
            
            "bluesky": "Write for Bluesky with a community-focused approach under 300 characters. Use a slightly more casual tone than Twitter while maintaining professionalism. Include 1-2 relevant hashtags.",
            
            "threads": "Create content for Threads with a visual-first mindset. Write in a casual, conversational tone. Content should be engaging and easy to read, with short paragraphs and an authentic voice."
        }
        
        content_type_guidelines = {
            "news_summary": "Summarize recent developments with factual accuracy. Include key points, implications, and proper citations.",
            
            "trend_analysis": "Analyze current trends, providing insights into patterns, potential future developments, and implications for professionals or consumers.",
            
            "deep_dive": "Provide comprehensive, in-depth analysis with multiple perspectives, detailed explanations, and actionable insights. Include background context and expert viewpoints.",
            
            "tip": "Provide actionable, practical advice that readers can implement. Be specific and include examples where helpful.",
            
            "opinion": "Offer an informed perspective on current developments, backed by facts and analysis.",
            
            # Handle custom content types
            "analysis": "Provide thoughtful analysis and insights on the topic.",
            "guide": "Create a helpful guide with step-by-step information.",
            "comparison": "Compare different aspects, options, or approaches related to the topic.",
            "case study": "Present a detailed case study with analysis and lessons learned.",
            "tutorial": "Create educational content that teaches something specific.",
            "review": "Provide a comprehensive review with pros, cons, and recommendations."
        }
        
        # Get the appropriate guideline, defaulting to general content creation
        content_guideline = content_type_guidelines.get(
            content_type.lower().replace(" ", "_"), 
            f"Create informative, engaging {content_type} content."
        )
        
        platform_guideline = platform_guidelines.get(platform, "Create appropriate social media content.")
        
        return f"""You are an expert social media content creator. Your task is to create ready-to-post content for social media platforms.

CONTENT TYPE: {content_guideline}

PLATFORM GUIDELINES: {platform_guideline}

CRITICAL: Respond ONLY with the final social media post content. Do not include:
- Your thinking process
- Explanations of your approach  
- Meta-commentary about the content
- Step-by-step reasoning

Your response should be:
1. Ready to copy and paste directly to social media
2. Well-researched with accurate, up-to-date information
3. Engaging and valuable to the target audience
4. Properly formatted for the specified platform
5. Include citations only if they fit naturally in the post format

Provide ONLY the final social media post content - nothing else."""
    
    def _create_refinement_system_prompt(self, platform: str) -> str:
        """Create system prompt for content refinement."""
        platform_guidelines = {
            "linkedin": "LinkedIn - Professional tone, up to 1300 characters, 2-3 hashtags",
            "twitter": "Twitter/X - Conversational tone, under 280 characters, 1-2 hashtags", 
            "bluesky": "Bluesky - Community-focused, under 300 characters, 1-2 hashtags",
            "threads": "Threads - Casual tone, engaging format, short paragraphs"
        }
        
        platform_guideline = platform_guidelines.get(platform, "Social media platform")
        
        return f"""You are an expert social media content refiner. Your task is to improve existing social media content based on specific user requests.

PLATFORM: {platform_guideline}

CRITICAL INSTRUCTIONS:
- Refine the content according to the user's specific request
- Maintain the platform's character limits and formatting requirements
- Keep the core message and key information intact
- Respond ONLY with the refined social media post content
- Do not include explanations, reasoning, or meta-commentary
- The output should be ready to copy-paste to social media

Your refined content should be an improved version that addresses the user's specific refinement request while staying true to the original message."""
    
    def _create_user_prompt(self, topic: str, content_type: str, platform: str) -> str:
        """
        Create a user prompt based on topic, content type, and platform.
        """
        # Handle different topic formats
        topic_key = topic.lower().replace(" ", "_")
        
        # Create a comprehensive prompt that works for any topic
        return f"""Create a {content_type} post about "{topic}" for {platform}. 

Requirements:
- Research current information about {topic}
- Include practical insights valuable to the audience
- Use platform-appropriate formatting and tone
- Make it engaging to encourage interaction

IMPORTANT: Provide ONLY the final social media post text - no explanations, no reasoning process, just the post content that's ready to publish."""
    
    def _create_refinement_user_prompt(self, original_content: str, refinement_request: str, platform: str) -> str:
        """Create user prompt for content refinement."""
        return f"""ORIGINAL CONTENT:
{original_content}

REFINEMENT REQUEST:
{refinement_request}

PLATFORM: {platform}

Please refine the original content according to the refinement request. Provide ONLY the improved social media post content - nothing else."""


# Example usage and testing
if __name__ == "__main__":
    try:
        # Initialize client
        client = PerplexityClient()
        print("✅ Perplexity client initialized successfully!")
        
        # Test content generation
        response = client.generate_content(
            topic="Artificial Intelligence",
            content_type="trend_analysis", 
            platform="linkedin"
        )
        
        print("✅ Content generation test successful!")
        original_content = response["choices"][0]["message"]["content"]
        print("Generated content preview:")
        print(original_content[:200] + "...")
        
        # Test content refinement
        print("\n🔄 Testing content refinement...")
        refinement_response = client.refine_content(
            original_content=original_content,
            refinement_request="Make this more engaging with a question for the audience",
            platform="linkedin"
        )
        
        refined_content = refinement_response["choices"][0]["message"]["content"]
        print("✅ Content refinement test successful!")
        print("Refined content preview:")
        print(refined_content[:200] + "...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Troubleshooting steps:")
        print("1. Make sure your .env file contains: PERPLEXITY_API_KEY=your-key-here")
        print("2. Check that your API key starts with 'pplx-'")
        print("3. Ensure the .env file is in the project root directory")
