import re
from typing import Dict, List, Optional

class ContentFormatter:
    """Format content for different social media platforms."""
    
    def __init__(self):
        self.platform_configs = {
            "linkedin": {
                "char_limit": 1300,
                "hashtag_limit": 3,
                "tone": "professional",
                "features": ["long_form", "hashtags", "mentions"]
            },
            "twitter": {
                "char_limit": 280,
                "hashtag_limit": 2,
                "tone": "conversational",
                "features": ["short_form", "hashtags", "mentions"]
            },
            "bluesky": {
                "char_limit": 300,
                "hashtag_limit": 2,
                "tone": "community",
                "features": ["short_form", "hashtags"]
            },
            "threads": {
                "char_limit": 500,
                "hashtag_limit": 2,
                "tone": "casual",
                "features": ["medium_form", "hashtags"]
            }
        }
    
    def format_for_platform(self, content: str, platform: str, include_hashtags: bool = True, tone: str = "professional") -> str:
        """
        Format content for a specific platform.
        
        Args:
            content: Raw content to format
            platform: Target platform (linkedin, twitter, bluesky, threads)
            include_hashtags: Whether to include hashtags
            tone: Tone to use for formatting
            
        Returns:
            Formatted content for the platform
        """
        platform = platform.lower()
        config = self.platform_configs.get(platform, self.platform_configs["linkedin"])
        
        # Apply platform-specific formatting
        if platform == "linkedin":
            formatted = self._format_linkedin(content, config, include_hashtags, tone)
        elif platform == "twitter":
            formatted = self._format_twitter(content, config, include_hashtags, tone)
        elif platform == "bluesky":
            formatted = self._format_bluesky(content, config, include_hashtags, tone)
        elif platform == "threads":
            formatted = self._format_threads(content, config, include_hashtags, tone)
        else:
            formatted = self._format_generic(content, config, include_hashtags, tone)
        
        return formatted
    
    def _format_linkedin(self, content: str, config: Dict, include_hashtags: bool, tone: str) -> str:
        """Format content for LinkedIn."""
        # Clean and structure content
        formatted = self._clean_content(content)
        
        # Add professional formatting
        if not formatted.endswith('.'):
            formatted += '.'
        
        # Add line breaks for readability
        sentences = formatted.split('. ')
        if len(sentences) > 3:
            # Group sentences into paragraphs
            paragraphs = []
            current_para = []
            
            for i, sentence in enumerate(sentences):
                current_para.append(sentence)
                if len(current_para) >= 2 or i == len(sentences) - 1:
                    paragraphs.append('. '.join(current_para))
                    current_para = []
            
            formatted = '\n\n'.join(paragraphs)
        
        # Add hashtags if requested
        if include_hashtags:
            hashtags = self._generate_hashtags(content, config["hashtag_limit"], "professional")
            if hashtags:
                formatted += f"\n\n{' '.join(hashtags)}"
        
        # Trim to character limit
        formatted = self._trim_to_limit(formatted, config["char_limit"])
        
        return formatted
    
    def _format_twitter(self, content: str, config: Dict, include_hashtags: bool, tone: str) -> str:
        """Format content for Twitter/X."""
        formatted = self._clean_content(content)
        
        # Make it more conversational
        formatted = self._make_conversational(formatted)
        
        # Add hashtags first to see remaining space
        hashtags = []
        if include_hashtags:
            hashtags = self._generate_hashtags(content, config["hashtag_limit"], "casual")
        
        hashtag_text = ' '.join(hashtags)
        available_chars = config["char_limit"] - len(hashtag_text) - (2 if hashtags else 0)  # Space for hashtags
        
        # Trim content to fit with hashtags
        if len(formatted) > available_chars:
            formatted = formatted[:available_chars-3].strip() + "..."
        
        # Add hashtags
        if hashtags:
            formatted += f" {hashtag_text}"
        
        return formatted
    
    def _format_bluesky(self, content: str, config: Dict, include_hashtags: bool, tone: str) -> str:
        """Format content for Bluesky."""
        formatted = self._clean_content(content)
        
        # Community-focused tone
        formatted = self._make_community_focused(formatted)
        
        # Add hashtags
        hashtags = []
        if include_hashtags:
            hashtags = self._generate_hashtags(content, config["hashtag_limit"], "community")
        
        hashtag_text = ' '.join(hashtags)
        available_chars = config["char_limit"] - len(hashtag_text) - (2 if hashtags else 0)
        
        # Trim to fit
        if len(formatted) > available_chars:
            formatted = formatted[:available_chars-3].strip() + "..."
        
        if hashtags:
            formatted += f" {hashtag_text}"
        
        return formatted
    
    def _format_threads(self, content: str, config: Dict, include_hashtags: bool, tone: str) -> str:
        """Format content for Threads."""
        formatted = self._clean_content(content)
        
        # Casual, conversational tone
        formatted = self._make_conversational(formatted)
        
        # Add hashtags
        hashtags = []
        if include_hashtags:
            hashtags = self._generate_hashtags(content, config["hashtag_limit"], "casual")
        
        hashtag_text = ' '.join(hashtags)
        available_chars = config["char_limit"] - len(hashtag_text) - (2 if hashtags else 0)
        
        # Trim to fit
        if len(formatted) > available_chars:
            formatted = formatted[:available_chars-3].strip() + "..."
        
        if hashtags:
            formatted += f" {hashtag_text}"
        
        return formatted
    
    def _format_generic(self, content: str, config: Dict, include_hashtags: bool, tone: str) -> str:
        """Generic formatting for unknown platforms."""
        formatted = self._clean_content(content)
        
        if include_hashtags:
            hashtags = self._generate_hashtags(content, 2, tone)
            if hashtags:
                formatted += f"\n\n{' '.join(hashtags)}"
        
        return formatted
    
    def _clean_content(self, content: str) -> str:
        """Clean and normalize content."""
        # Remove extra whitespace
        content = re.sub(r'\s+', ' ', content.strip())
        
        # Remove markdown formatting that doesn't work on social media
        content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)  # Bold
        content = re.sub(r'\*(.*?)\*', r'\1', content)      # Italic
        content = re.sub(r'`(.*?)`', r'\1', content)        # Code
        
        return content
    
    def _make_conversational(self, content: str) -> str:
        """Make content more conversational."""
        # Add question marks for engagement
        if not content.endswith('?') and not content.endswith('!'):
            if "what" in content.lower() or "how" in content.lower() or "why" in content.lower():
                content = content.rstrip('.') + "?"
        
        return content
    
    def _make_community_focused(self, content: str) -> str:
        """Make content more community-focused."""
        # Similar to conversational but with community language
        return self._make_conversational(content)
    
    def _generate_hashtags(self, content: str, limit: int, style: str) -> List[str]:
        """Generate relevant hashtags from content."""
        # Extract key words/phrases for hashtags
        words = content.lower().split()
        
        # Common hashtag mappings
        hashtag_keywords = {
            "ai": "#AI",
            "artificial": "#AI",
            "intelligence": "#AI", 
            "machine": "#MachineLearning",
            "learning": "#MachineLearning",
            "technology": "#Technology",
            "tech": "#Tech",
            "data": "#Data",
            "analytics": "#DataAnalytics",
            "business": "#Business",
            "startup": "#Startup",
            "innovation": "#Innovation",
            "digital": "#Digital",
            "future": "#Future",
            "trends": "#Trends",
            "industry": "#Industry",
            "market": "#Market",
            "finance": "#Finance",
            "investment": "#Investment",
            "crypto": "#Crypto",
            "blockchain": "#Blockchain",
            "productivity": "#Productivity",
            "work": "#Work",
            "remote": "#RemoteWork",
            "social": "#SocialMedia",
            "marketing": "#Marketing",
            "content": "#Content",
            "strategy": "#Strategy",
            "growth": "#Growth",
            "leadership": "#Leadership",
            "management": "#Management"
        }
        
        # Find relevant hashtags
        hashtags = set()
        for word in words:
            clean_word = re.sub(r'[^\w]', '', word)
            if clean_word in hashtag_keywords:
                hashtags.add(hashtag_keywords[clean_word])
        
        # Add some general hashtags based on style
        if style == "professional":
            hashtags.add("#Business")
        elif style == "casual":
            hashtags.add("#Tech")
        elif style == "community":
            hashtags.add("#Community")
        
        # Convert to list and limit
        hashtag_list = list(hashtags)[:limit]
        
        return hashtag_list
    
    def _trim_to_limit(self, content: str, char_limit: int) -> str:
        """Trim content to character limit while preserving words."""
        if len(content) <= char_limit:
            return content
        
        # Find the last complete word that fits
        trimmed = content[:char_limit-3]
        last_space = trimmed.rfind(' ')
        
        if last_space > 0:
            trimmed = trimmed[:last_space]
        
        return trimmed + "..."
    
    def get_platform_info(self, platform: str) -> Dict:
        """Get platform configuration information."""
        return self.platform_configs.get(platform.lower(), {})


# Example usage and testing
if __name__ == "__main__":
    formatter = ContentFormatter()
    
    sample_content = """
    Artificial intelligence is transforming industries at an unprecedented pace. 
    Recent advances in machine learning algorithms have enabled breakthrough 
    applications in healthcare, finance, and autonomous systems. Companies 
    that embrace AI early are gaining significant competitive advantages.
    """
    
    platforms = ["linkedin", "twitter", "bluesky", "threads"]
    
    print("Content Formatter Test:")
    print("=" * 50)
    
    for platform in platforms:
        print(f"\n📱 {platform.upper()}:")
        formatted = formatter.format_for_platform(
            content=sample_content,
            platform=platform,
            include_hashtags=True,
            tone="professional"
        )
        print(f"Length: {len(formatted)} chars")
        print(f"Content: {formatted}")
        print("-" * 30)
