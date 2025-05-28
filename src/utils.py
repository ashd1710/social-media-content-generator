import hashlib
from datetime import datetime

def get_platform_info(platform):
    """Get platform-specific information"""
    platform_info = {
        'linkedin': {
            'icon': '💼',
            'char_limit': 1300,
            'name': 'LinkedIn',
            'color': '#0077B5'
        },
        'twitter': {
            'icon': '🐦', 
            'char_limit': 280,
            'name': 'Twitter/X',
            'color': '#1DA1F2'
        },
        'bluesky': {
            'icon': '🦋',
            'char_limit': 300, 
            'name': 'Bluesky',
            'color': '#00D4FF'
        },
        'threads': {
            'icon': '🧵',
            'char_limit': 500,
            'name': 'Threads', 
            'color': '#000000'
        }
    }
    
    return platform_info.get(platform, {
        'icon': '📱',
        'char_limit': 280,
        'name': platform.title(),
        'color': '#666666'
    })

def generate_content_hash(content):
    """Generate hash for content identification"""
    return hashlib.md5(content.encode()).hexdigest()[:8]

def format_timestamp(timestamp):
    """Format timestamp for display"""
    if isinstance(timestamp, str):
        try:
            timestamp = datetime.fromisoformat(timestamp)
        except:
            return timestamp
    
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def truncate_text(text, max_length=100):
    """Truncate text with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def validate_platform(platform):
    """Validate if platform is supported"""
    supported_platforms = ['linkedin', 'twitter', 'bluesky', 'threads']
    return platform.lower() in supported_platforms
