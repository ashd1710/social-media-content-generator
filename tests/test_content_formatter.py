import json
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from content_formatter import format_content_for_platform

def test_content_formatting():
    """
    Test the content formatter with sample content for different platforms.
    """
    # Sample content from Perplexity API
    sample_content = """
Artificial Intelligence is rapidly transforming the way businesses operate in 2025. The integration of generative AI models into everyday workflows has created new opportunities for automation and innovation.

Companies that leverage AI effectively are seeing significant productivity gains. According to recent studies, businesses using AI-powered tools report an average productivity increase of 35%.

The rise of specialized AI models trained for specific industries is another key trend. These domain-specific models outperform general-purpose models on industry tasks while requiring less computational resources.

Responsible AI development remains critical. Organizations are increasingly adopting transparent AI governance frameworks to address ethical concerns and regulatory requirements.
    """
    
    topic = "ai_trends"
    content_type = "trend_analysis"
    
    # Format content for each platform
    platforms = ["linkedin", "twitter", "bluesky", "threads"]
    formatted_results = {}
    
    for platform in platforms:
        formatted_content = format_content_for_platform(
            content=sample_content,
            topic=topic,
            content_type=content_type,
            platform=platform
        )
        formatted_results[platform] = {
            "content": formatted_content,
            "char_count": len(formatted_content)
        }
    
    # Print results
    print("Content Formatting Results:\n")
    for platform, result in formatted_results.items():
        print(f"=== {platform.upper()} ({result['char_count']} chars) ===")
        print(result["content"])
        print("\n" + "-" * 50 + "\n")

if __name__ == "__main__":
    test_content_formatting()