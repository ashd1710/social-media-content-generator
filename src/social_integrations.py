import os
import json
import time
import requests
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import streamlit as st

class SocialMediaIntegrationBase:
    """Base class for social media platform integrations."""
    
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.is_connected = False
        self.user_info = {}
    
    def connect(self, credentials: Dict) -> Tuple[bool, str]:
        """Connect to the platform. Returns (success, message)"""
        raise NotImplementedError
    
    def disconnect(self):
        """Disconnect from the platform."""
        self.is_connected = False
        self.user_info = {}
    
    def post_content(self, content: str, media_urls: List[str] = None) -> Tuple[bool, str]:
        """Post content to the platform. Returns (success, message/post_id)"""
        raise NotImplementedError
    
    def get_connection_status(self) -> Dict:
        """Get current connection status and user info."""
        return {
            "platform": self.platform_name,
            "connected": self.is_connected,
            "user_info": self.user_info
        }

class BlueskyIntegration(SocialMediaIntegrationBase):
    """Bluesky (AT Protocol) integration - FREE TIER with Optimized Threading"""
    
    def __init__(self):
        super().__init__("Bluesky")
        self.base_url = "https://bsky.social"
        self.session = None
        self.access_jwt = None
        self.refresh_jwt = None
    
    def connect(self, credentials: Dict) -> Tuple[bool, str]:
        """Connect to Bluesky using username/password."""
        try:
            username = credentials.get("username", "")
            password = credentials.get("password", "")
            
            # DEBUG: Print username details
            print(f"🔍 DEBUG - Attempting Bluesky connection:")
            print(f"Username: '{username}'")
            print(f"Username length: {len(username)}")
            print(f"Username repr: {repr(username)}")
            print(f"Has @ symbol: {'@' in username}")
            print(f"Password length: {len(password)}")
            
            if not username or not password:
                return False, "Username and password are required"
            
            # Clean username: remove @ symbol if present and strip whitespace
            clean_username = username.strip()
            if clean_username.startswith('@'):
                clean_username = clean_username[1:]
            
            print(f"🧹 Cleaned username: '{clean_username}'")
            
            # Create session
            session_url = f"{self.base_url}/xrpc/com.atproto.server.createSession"
            session_data = {
                "identifier": clean_username,
                "password": password
            }
            
            print(f"🌐 Making request to: {session_url}")
            print(f"📤 Request data: {{'identifier': '{clean_username}', 'password': '[HIDDEN]'}}")
            
            response = requests.post(session_url, json=session_data)
            
            print(f"📥 Response status: {response.status_code}")
            if response.status_code != 200:
                print(f"❌ Response content: {response.text}")
            
            if response.status_code == 200:
                session_info = response.json()
                self.access_jwt = session_info.get("accessJwt")
                self.refresh_jwt = session_info.get("refreshJwt")
                self.user_info = {
                    "handle": session_info.get("handle"),
                    "did": session_info.get("did"),
                    "displayName": session_info.get("displayName", "")
                }
                self.is_connected = True
                print(f"✅ Connection successful! Handle: {self.user_info['handle']}")
                return True, f"Successfully connected to Bluesky as @{self.user_info['handle']}"
            else:
                error_msg = response.json().get("message", "Authentication failed")
                print(f"❌ Connection failed: {error_msg}")
                return False, f"Bluesky connection failed: {error_msg}"
                
        except Exception as e:
            print(f"💥 Exception during connection: {str(e)}")
            return False, f"Bluesky connection error: {str(e)}"
    
    def _split_content_intelligently(self, content: str, max_length: int = 300) -> List[str]:
        """Split content intelligently for threading with optimal character usage."""
        # First, clean any existing thread indicators from the content
        clean_content = self._clean_existing_thread_indicators(content)
        
        print(f"🧹 Cleaned content length: {len(clean_content)} characters")
        
        if len(clean_content) <= max_length:
            return [clean_content]
        
        # Account for thread indicators like "(1/3)" - reserve 8 chars to be safe
        effective_max = max_length - 8
        
        # First, try sentence-based splitting
        threads = self._split_by_sentences(clean_content, effective_max)
        
        # If we have a very short final thread (less than 50 chars), redistribute
        if len(threads) > 1 and len(threads[-1]) < 50:
            threads = self._redistribute_short_thread(threads, effective_max)
        
        # If sentence splitting creates too many short threads, try word-based splitting
        if len(threads) > 3 and any(len(thread) < 100 for thread in threads):
            word_threads = self._split_by_words(clean_content, effective_max)
            if len(word_threads) < len(threads):  # If word splitting is more efficient
                threads = word_threads
        
        # Add clean thread indicators at the start
        if len(threads) > 1:
            for i, thread in enumerate(threads):
                threads[i] = f"({i+1}/{len(threads)}) {thread}"
        
        return threads
    
    def _clean_existing_thread_indicators(self, content: str) -> str:
        """Remove any existing thread indicators from content."""
        import re
        
        # Remove patterns like "**Thread 1/3***", "Thread 1/2:", "(1/3)", etc.
        patterns = [
            r'\*\*Thread\s+\d+/\d+\*\*\*?',  # **Thread 1/3*** or **Thread 1/3**
            r'Thread\s+\d+/\d+:?',           # Thread 1/3: or Thread 1/3
            r'\(\d+/\d+\)',                  # (1/3)
            r'^\d+/\d+:?\s*',                # 1/3: or 1/3 at start
            r'^\(\d+/\d+\)\s*',              # (1/3) at start
        ]
        
        cleaned = content
        for pattern in patterns:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        
        # Clean up extra whitespace and line breaks
        cleaned = re.sub(r'\s+', ' ', cleaned)  # Multiple spaces to single space
        cleaned = cleaned.strip()
        
        return cleaned
    
    def _split_by_sentences(self, content: str, max_length: int) -> List[str]:
        """Split content by sentences."""
        sentences = content.split('. ')
        threads = []
        current_thread = ""
        
        for i, sentence in enumerate(sentences):
            # Add the period back (except for last sentence)
            sentence_with_period = sentence + ('.' if i < len(sentences) - 1 else '')
            
            # Check if adding this sentence would exceed limit
            test_content = current_thread + (' ' if current_thread else '') + sentence_with_period
            
            if len(test_content) <= max_length:
                current_thread = test_content
            else:
                # Current thread is full, start new one
                if current_thread:
                    threads.append(current_thread.strip())
                current_thread = sentence_with_period
        
        # Add the last thread
        if current_thread:
            threads.append(current_thread.strip())
        
        return threads
    
    def _split_by_words(self, content: str, max_length: int) -> List[str]:
        """Split content by words when sentence splitting isn't optimal."""
        words = content.split()
        threads = []
        current_thread = ""
        
        for word in words:
            test_content = current_thread + (' ' if current_thread else '') + word
            
            if len(test_content) <= max_length:
                current_thread = test_content
            else:
                if current_thread:
                    threads.append(current_thread.strip())
                current_thread = word
        
        if current_thread:
            threads.append(current_thread.strip())
        
        return threads
    
    def _redistribute_short_thread(self, threads: List[str], max_length: int) -> List[str]:
        """Redistribute content when the last thread is too short."""
        if len(threads) < 2:
            return threads
        
        # Combine the last two threads and try to split them more evenly
        last_thread = threads.pop()
        second_last = threads.pop()
        combined = f"{second_last} {last_thread}"
        
        # Split the combined content into two more balanced parts
        words = combined.split()
        mid_point = len(words) // 2
        
        # Find the best split point near the middle
        for offset in range(min(10, len(words) // 4)):  # Look within 10 words of midpoint
            for direction in [0, 1, -1]:  # Try exact midpoint, then +/- offset
                split_idx = mid_point + (direction * offset)
                if 0 < split_idx < len(words):
                    first_part = ' '.join(words[:split_idx])
                    second_part = ' '.join(words[split_idx:])
                    
                    # Check if both parts fit within limits
                    if len(first_part) <= max_length and len(second_part) <= max_length:
                        # Check if this is more balanced than before
                        old_min_length = min(len(second_last), len(last_thread))
                        new_min_length = min(len(first_part), len(second_part))
                        
                        if new_min_length > old_min_length:
                            threads.extend([first_part, second_part])
                            return threads
        
        # If redistribution didn't work better, keep original
        threads.extend([second_last, last_thread])
        return threads
    
    def post_content(self, content: str, media_urls: List[str] = None) -> Tuple[bool, str]:
        """Post content to Bluesky with intelligent threading for long content."""
        if not self.is_connected:
            return False, "Not connected to Bluesky"
        
        try:
            print(f"🔍 Original content length: {len(content)} characters")
            
            # Split content into threads if needed
            threads = self._split_content_intelligently(content)
            
            print(f"🧵 Content split into {len(threads)} thread(s)")
            for i, thread in enumerate(threads):
                print(f"   Thread {i+1}: {len(thread)} chars - '{thread[:50]}...'")
            
            if len(threads) == 1:
                print(f"📝 Posting as single message")
                return self._post_single(threads[0])
            else:
                print(f"🧵 Posting as {len(threads)}-part thread")
                return self._post_thread(threads)
                
        except Exception as e:
            print(f"💥 Bluesky post exception: {str(e)}")
            import traceback
            print(f"Full traceback: {traceback.format_exc()}")
            return False, f"Bluesky post error: {str(e)}"
    
    def _post_single(self, content: str) -> Tuple[bool, str]:
        """Post a single message to Bluesky."""
        try:
            post_url = f"{self.base_url}/xrpc/com.atproto.repo.createRecord"
            
            headers = {
                "Authorization": f"Bearer {self.access_jwt}",
                "Content-Type": "application/json"
            }
            
            post_record = {
                "text": content,
                "createdAt": datetime.utcnow().isoformat() + "Z"
            }
            
            post_data = {
                "repo": self.user_info["did"],
                "collection": "app.bsky.feed.post",
                "record": post_record
            }
            
            print(f"📤 Posting single message to Bluesky...")
            response = requests.post(post_url, headers=headers, json=post_data)
            
            if response.status_code == 200:
                result = response.json()
                post_uri = result.get("uri", "")
                return True, f"Posted successfully to Bluesky! URI: {post_uri}"
            else:
                error_msg = response.json().get("message", "Post failed")
                print(f"❌ Single post failed: {error_msg}")
                return False, f"Bluesky post failed: {error_msg}"
                
        except Exception as e:
            return False, f"Single post error: {str(e)}"
    
    def _post_thread(self, threads: List[str]) -> Tuple[bool, str]:
        """Post a thread to Bluesky."""
        try:
            posted_uris = []
            root_post = None
            parent_post = None
            
            for i, thread_content in enumerate(threads):
                print(f"📤 Posting thread {i+1}/{len(threads)}: {thread_content[:50]}...")
                
                # Add small delay between posts to avoid rate limiting
                if i > 0:
                    time.sleep(0.5)
                
                post_url = f"{self.base_url}/xrpc/com.atproto.repo.createRecord"
                
                headers = {
                    "Authorization": f"Bearer {self.access_jwt}",
                    "Content-Type": "application/json"
                }
                
                # Build post record
                post_record = {
                    "text": thread_content,
                    "createdAt": datetime.utcnow().isoformat() + "Z"
                }
                
                # Add reply structure for threaded posts (posts 2 and onwards)
                if i > 0 and root_post and parent_post:
                    post_record["reply"] = {
                        "root": {
                            "uri": root_post["uri"],
                            "cid": root_post["cid"]
                        },
                        "parent": {
                            "uri": parent_post["uri"],
                            "cid": parent_post["cid"]
                        }
                    }
                    print(f"🔗 Adding reply structure - Root: {root_post['uri'][:30]}...")
                
                post_data = {
                    "repo": self.user_info["did"],
                    "collection": "app.bsky.feed.post", 
                    "record": post_record
                }
                
                print(f"🌐 Making POST request to: {post_url}")
                response = requests.post(post_url, headers=headers, json=post_data)
                
                print(f"📥 Response status: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    current_uri = result.get("uri", "")
                    current_cid = result.get("cid", "")
                    
                    current_post = {
                        "uri": current_uri,
                        "cid": current_cid
                    }
                    
                    posted_uris.append(current_uri)
                    
                    # Set root and parent for next post
                    if i == 0:
                        root_post = current_post
                        print(f"🌳 Root post established: {current_uri}")
                    parent_post = current_post
                    
                    print(f"✅ Thread {i+1}/{len(threads)} posted successfully!")
                    print(f"   URI: {current_uri}")
                    print(f"   CID: {current_cid}")
                    
                else:
                    error_data = response.json() if response.content else {}
                    error_msg = error_data.get("message", "Post failed")
                    print(f"❌ Thread {i+1} failed: {error_msg}")
                    print(f"   Full response: {response.text}")
                    
                    # Return partial success if some posts succeeded
                    if posted_uris:
                        return True, f"Thread partially posted: {len(posted_uris)}/{len(threads)} posts successful. Check terminal for details."
                    else:
                        return False, f"Thread posting failed at post {i+1}: {error_msg}"
            
            # All posts successful
            print(f"🎉 Complete thread posted successfully!")
            return True, f"Thread posted successfully! {len(threads)} posts created as connected thread"
            
        except Exception as e:
            print(f"💥 Thread posting exception: {str(e)}")
            import traceback
            print(f"Full traceback: {traceback.format_exc()}")
            return False, f"Thread posting error: {str(e)}"
    
    def refresh_session(self) -> bool:
        """Refresh the access token."""
        if not self.refresh_jwt:
            return False
        
        try:
            refresh_url = f"{self.base_url}/xrpc/com.atproto.server.refreshSession"
            headers = {"Authorization": f"Bearer {self.refresh_jwt}"}
            
            response = requests.post(refresh_url, headers=headers)
            
            if response.status_code == 200:
                session_info = response.json()
                self.access_jwt = session_info.get("accessJwt")
                self.refresh_jwt = session_info.get("refreshJwt")
                return True
            
        except Exception:
            pass
        
        return False

class LinkedInIntegration(SocialMediaIntegrationBase):
    """LinkedIn integration - FREE TIER (Real API)"""
    
    def __init__(self):
        super().__init__("LinkedIn")
        self.api_base = "https://api.linkedin.com/v2"
        self.access_token = None
    
    def connect(self, credentials: Dict) -> Tuple[bool, str]:
        """Connect to LinkedIn using access token."""
        try:
            access_token = credentials.get("access_token", "")
            
            if not access_token and not credentials.get("demo"):
                return False, "LinkedIn access token is required"
            
            # Demo mode for hackathon
            if credentials.get("demo"):
                self.access_token = "demo_token"
                self.user_info = {
                    "name": "Demo User",
                    "profile_url": "https://linkedin.com/in/demo",
                    "firstName": "Demo",
                    "lastName": "User"
                }
                self.is_connected = True
                return True, "LinkedIn connected (Demo mode - Real OAuth integration available)"
            
            # Real LinkedIn API connection
            self.access_token = access_token
            
            # Verify token by getting user profile
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            print(f"🔍 DEBUG - LinkedIn API Request:")
            print(f"Token length: {len(access_token)}")
            print(f"Headers: Authorization: Bearer [HIDDEN]")
            
            # Get user profile to verify token
            profile_url = f"{self.api_base}/people/~?projection=(id,firstName,lastName,profilePicture(displayImage~:playableStreams))"
            
            response = requests.get(profile_url, headers=headers)
            
            print(f"📥 LinkedIn Response status: {response.status_code}")
            
            if response.status_code == 200:
                profile_data = response.json()
                self.user_info = {
                    "id": profile_data.get("id"),
                    "firstName": profile_data.get("firstName", {}).get("localized", {}).get("en_US", ""),
                    "lastName": profile_data.get("lastName", {}).get("localized", {}).get("en_US", ""),
                    "name": f"{profile_data.get('firstName', {}).get('localized', {}).get('en_US', '')} {profile_data.get('lastName', {}).get('localized', {}).get('en_US', '')}",
                    "profile_url": f"https://linkedin.com/in/{profile_data.get('id', '')}"
                }
                self.is_connected = True
                print(f"✅ LinkedIn connection successful! User: {self.user_info['name']}")
                return True, f"Successfully connected to LinkedIn as {self.user_info['name']}"
            else:
                error_data = response.json() if response.content else {}
                error_msg = error_data.get("message", "Invalid access token")
                print(f"❌ LinkedIn connection failed: {error_msg}")
                return False, f"LinkedIn connection failed: {error_msg}"
                
        except Exception as e:
            print(f"💥 LinkedIn exception: {str(e)}")
            return False, f"LinkedIn connection error: {str(e)}"
    
    def post_content(self, content: str, media_urls: List[str] = None) -> Tuple[bool, str]:
        """Post content to LinkedIn."""
        if not self.is_connected:
            return False, "Not connected to LinkedIn"
        
        # Demo mode posting
        if self.access_token == "demo_token":
            time.sleep(1)  # Simulate API call
            return True, "Posted to LinkedIn successfully (Demo mode)"
        
        try:
            # Real LinkedIn posting
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0"
            }
            
            # LinkedIn UGC (User Generated Content) API
            post_url = f"{self.api_base}/ugcPosts"
            
            post_data = {
                "author": f"urn:li:person:{self.user_info['id']}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": content
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            print(f"🌐 Posting to LinkedIn...")
            print(f"📤 Post data: {{'text': '{content[:50]}...', 'visibility': 'PUBLIC'}}")
            
            response = requests.post(post_url, headers=headers, json=post_data)
            
            print(f"📥 LinkedIn post response: {response.status_code}")
            
            if response.status_code == 201:
                result = response.json()
                post_id = result.get("id", "")
                return True, f"Posted successfully to LinkedIn! Post ID: {post_id}"
            else:
                error_data = response.json() if response.content else {}
                error_msg = error_data.get("message", "Post failed")
                print(f"❌ LinkedIn post failed: {error_msg}")
                return False, f"LinkedIn post failed: {error_msg}"
                
        except Exception as e:
            print(f"💥 LinkedIn post exception: {str(e)}")
            return False, f"LinkedIn post error: {str(e)}"

class TwitterIntegration(SocialMediaIntegrationBase):
    """Twitter/X integration - PREMIUM TIER (Expensive API)"""
    
    def __init__(self):
        super().__init__("Twitter/X")
        self.api_base = "https://api.twitter.com/2"
        self.bearer_token = None
        self.is_mock_mode = True  # For hackathon demo
    
    def connect(self, credentials: Dict) -> Tuple[bool, str]:
        """Twitter API connection (mock for hackathon)."""
        if self.is_mock_mode or credentials.get("demo"):
            # Mock connection for hackathon demo
            self.user_info = {
                "username": "demo_user",
                "name": "Demo User",
                "followers": "1.2K"
            }
            self.is_connected = True
            return True, "Twitter/X connected (Demo mode - $100+/month API tier required for live posting)"
        
        # Real implementation would use Twitter API v2
        bearer_token = credentials.get("bearer_token", "")
        if bearer_token:
            self.bearer_token = bearer_token
            # Validate token and get user info
            return True, "Twitter/X connected"
        
        return False, "Twitter API credentials required"
    
    def post_content(self, content: str, media_urls: List[str] = None) -> Tuple[bool, str]:
        """Post to Twitter (mock implementation for hackathon)."""
        if not self.is_connected:
            return False, "Not connected to Twitter/X"
        
        if self.is_mock_mode:
            time.sleep(1)  # Simulate API call
            return True, "Posted to Twitter/X successfully (Demo mode - Premium API tier required for live posting)"
        
        # Real implementation would use Twitter API v2
        return True, "Posted to Twitter/X"

class ThreadsIntegration(SocialMediaIntegrationBase):
    """Threads integration - PREMIUM TIER (Limited API)"""
    
    def __init__(self):
        super().__init__("Threads")
        self.api_base = "https://graph.threads.net"
        self.access_token = None
        self.is_mock_mode = True  # For hackathon demo
    
    def connect(self, credentials: Dict) -> Tuple[bool, str]:
        """Threads API connection (mock for hackathon)."""
        if self.is_mock_mode or credentials.get("demo"):
            # Mock connection for hackathon demo
            self.user_info = {
                "username": "demo_user",
                "name": "Demo User",
                "followers": "856"
            }
            self.is_connected = True
            return True, "Threads connected (Demo mode - Limited API access, business verification required)"
        
        access_token = credentials.get("access_token", "")
        if access_token:
            self.access_token = access_token
            return True, "Threads connected"
        
        return False, "Threads API credentials required"
    
    def post_content(self, content: str, media_urls: List[str] = None) -> Tuple[bool, str]:
        """Post to Threads (mock implementation for hackathon)."""
        if not self.is_connected:
            return False, "Not connected to Threads"
        
        if self.is_mock_mode:
            time.sleep(1)  # Simulate API call
            return True, "Posted to Threads successfully (Demo mode - Limited API requires business verification)"
        
        # Real implementation would use Threads API
        return True, "Posted to Threads"

class SocialMediaManager:
    """Manager class for all social media integrations."""
    
    def __init__(self):
        self.platforms = {
            "bluesky": BlueskyIntegration(),
            "linkedin": LinkedInIntegration(),
            "twitter": TwitterIntegration(),
            "threads": ThreadsIntegration()
        }
        self.load_connections()
    
    def get_platform(self, platform_name: str) -> Optional[SocialMediaIntegrationBase]:
        """Get platform integration by name."""
        return self.platforms.get(platform_name.lower())
    
    def get_connected_platforms(self) -> List[str]:
        """Get list of connected platform names."""
        return [name for name, platform in self.platforms.items() if platform.is_connected]
    
    def get_all_platform_status(self) -> Dict:
        """Get connection status for all platforms."""
        return {
            name: platform.get_connection_status() 
            for name, platform in self.platforms.items()
        }
    
    def post_to_multiple_platforms(self, content_dict: Dict[str, str], selected_platforms: List[str]) -> Dict[str, Tuple[bool, str]]:
        """Post content to multiple platforms simultaneously."""
        results = {}
        
        for platform_name in selected_platforms:
            platform = self.get_platform(platform_name)
            if platform and platform.is_connected:
                content = content_dict.get(platform_name, "")
                if content:
                    success, message = platform.post_content(content)
                    results[platform_name] = (success, message)
                else:
                    results[platform_name] = (False, "No content provided for this platform")
            else:
                results[platform_name] = (False, "Platform not connected")
        
        return results
    
    def save_connections(self):
        """Save connection states (for demo persistence)."""
        # In a real app, you'd save encrypted tokens to a secure database
        # For hackathon demo, we'll use Streamlit session state
        if 'social_connections' not in st.session_state:
            st.session_state.social_connections = {}
        
        for name, platform in self.platforms.items():
            st.session_state.social_connections[name] = {
                "connected": platform.is_connected,
                "user_info": platform.user_info
            }
    
    def load_connections(self):
        """Load saved connection states."""
        if 'social_connections' in st.session_state:
            for name, data in st.session_state.social_connections.items():
                if name in self.platforms:
                    platform = self.platforms[name]
                    platform.is_connected = data.get("connected", False)
                    platform.user_info = data.get("user_info", {})

# Utility functions for the UI
def get_platform_tier_info() -> Dict[str, Dict]:
    """Get platform tier information for UI display."""
    return {
        "bluesky": {
            "tier": "Free",
            "status": "Live posting + intelligent threading",
            "color": "green", 
            "icon": "🆓"
        },
        "linkedin": {
            "tier": "Free",
            "status": "Live API integration available",
            "color": "blue",
            "icon": "🆓"
        },
        "twitter": {
            "tier": "Premium", 
            "status": "$100+/month API required",
            "color": "orange",
            "icon": "💎"
        },
        "threads": {
            "tier": "Premium",
            "status": "Business verification required", 
            "color": "red",
            "icon": "💎"
        }
    }

def display_platform_connection_ui(manager: SocialMediaManager, platform_name: str):
    """Display connection UI for a specific platform."""
    platform = manager.get_platform(platform_name)
    tier_info = get_platform_tier_info()[platform_name]
    
    # Platform header
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        st.markdown(f"## {tier_info['icon']}")
    
    with col2:
        st.markdown(f"### {platform_name.title()}")
        st.markdown(f"**Tier:** {tier_info['tier']} | **Status:** {tier_info['status']}")
    
    with col3:
        if platform.is_connected:
            st.success("Connected")
        else:
            st.error("Not Connected")
    
    # Connection form
    if not platform.is_connected:
        with st.expander(f"Connect to {platform_name.title()}", expanded=False):
            if platform_name == "bluesky":
                st.markdown("**Enter your Bluesky credentials:**")
                st.info("💡 **Tip:** Use your email address instead of handle for better compatibility")
                
                username = st.text_input("Bluesky Email/Username", key=f"{platform_name}_username", 
                                        placeholder="your-email@domain.com or username.bsky.social")
                password = st.text_input("Bluesky Password", type="password", key=f"{platform_name}_password")
                
                if st.button(f"Connect to {platform_name.title()}", key=f"{platform_name}_connect"):
                    if username and password:
                        success, message = platform.connect({
                            "username": username,
                            "password": password
                        })
                        if success:
                            st.success(message)
                            manager.save_connections()
                            st.rerun()
                        else:
                            st.error(message)
                            st.info("🔧 **Troubleshooting:** Check the terminal/console for detailed debug information")
                    else:
                        st.error("Please enter both email/username and password")
            
            elif platform_name == "linkedin":
                st.markdown("**LinkedIn API Connection:**")
                
                # Option tabs for LinkedIn
                linkedin_tabs = st.tabs(["🔑 Use Access Token", "🎭 Demo Mode"])
                
                with linkedin_tabs[0]:
                    st.info("**How to get LinkedIn Access Token:**")
                    st.markdown("""
                    1. Go to [LinkedIn Developer Portal](https://developer.linkedin.com/)
                    2. Create a new app or use existing one
                    3. Get your Access Token from the app dashboard
                    4. Ensure your app has 'w_member_social' permission
                    """)
                    
                    access_token = st.text_input(
                        "LinkedIn Access Token", 
                        type="password", 
                        key=f"{platform_name}_access_token",
                        placeholder="Enter your LinkedIn access token here"
                    )
                    
                    if st.button(f"Connect with Real LinkedIn API", key=f"{platform_name}_real_connect"):
                        if access_token:
                            success, message = platform.connect({
                                "access_token": access_token
                            })
                            if success:
                                st.success(message)
                                manager.save_connections()
                                st.rerun()
                            else:
                                st.error(message)
                                st.info("🔧 **Check terminal for detailed error information**")
                        else:
                            st.error("Please enter your LinkedIn access token")
                
                with linkedin_tabs[1]:
                    st.info("Use demo mode for hackathon presentation without real LinkedIn API setup.")
                    
                    if st.button(f"Demo Connect to LinkedIn", key=f"{platform_name}_demo_connect"):
                        success, message = platform.connect({"demo": True})
                        if success:
                            st.success(message)
                            manager.save_connections()
                            st.rerun()
            
            else:
                st.info(f"This is a demo connection for {platform_name.title()}. Click to simulate connection.")
                if st.button(f"Demo Connect to {platform_name.title()}", key=f"{platform_name}_demo_connect"):
                    success, message = platform.connect({"demo": True})
                    if success:
                        st.success(message)
                        manager.save_connections()
                        st.rerun()
    
    else:
        # Show connected user info
        if platform_name == "linkedin" and platform.access_token != "demo_token":
            st.success(f"✅ **Connected as:** {platform.user_info.get('name', 'LinkedIn User')}")
            st.info(f"**Profile:** {platform.user_info.get('profile_url', 'N/A')}")
        else:
            st.info(f"Connected as: {platform.user_info.get('handle', platform.user_info.get('name', 'User'))}")
        
        if st.button(f"Disconnect from {platform_name.title()}", key=f"{platform_name}_disconnect"):
            platform.disconnect()
            manager.save_connections()
            st.rerun()
