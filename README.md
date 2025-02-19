# Instagram API Client Library

A Python library for interacting with the official Instagram Graph API. This client provides easy-to-use methods for authentication, user management, conversations, and messaging functionality.

[Official instagram documentation](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login)

## Demo
You can visit [robosell](https://robosell.uz) to test how instagram integration works and features have

## Features

- OAuth 2.0 Authentication
- Long-lived token exchange
- User profile management
- Conversation handling
- Message management
- Built-in pagination support

## Installation

```bash
pip install instagram-client
```

## Prerequisites

Before using this library, you need to:

1. Create an Instagram App in the [Meta for Developers Console](https://developers.facebook.com/)
2. Obtain your Client ID and Client Secret
3. Configure your OAuth redirect URI
4. Set up the required scopes for your application

## Quick Start

```python
from instagram_client import InstagramClient


# Initialize the client
client = InstagramClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    redirect_uri="your_redirect_uri",
    scopes=["instagram_business_basic", "instagram_business_manage_messages"]
)
# For more detailed information visit https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login

# Get the authorization URL
auth_url = client.get_auth_url()

# Also you can pass custom data to oauth url:
# auth_url = client.get_auth_url(state="user_{user_id}")

# Redirect user to auth_url for authorization

# After user authorization, exchange the code for an access token
login_response = client.retrieve_access_token(code="authorization_code")

# Exchange for a long-lived token
long_lived_token = client.exchange_long_lived_token() # long lived token expires in 60 days and short token expires in 30min

# Get authenticated user's profile
user_profile = client.get_me()
```

## Detailed Usage

### Authentication Flow

```python
# Create new endpoint to redirect oauth url

# 1. Generate authentication URL
auth_url = client.get_auth_url(
    enable_fb_login=1,
    force_authentication=0,
    state="optional_state_parameter"
)

# 2. After user authorization, exchange the code for an access token
login_response = client.retrieve_access_token(code="authorization_code")
print(f"Access Token: {login_response.access_token}")

# 3. Exchange for a long-lived token
long_lived_token = client.exchange_long_lived_token()
print(f"Long-lived Token: {long_lived_token.access_token}")
print(f"Token Expires in: {long_lived_token.expires_in} seconds")
```

### User Management

```python
# Get authenticated user's profile
me = client.get_me()
print(f"Username: {me.username}")
print(f"Followers: {me.followers_count}")
print(f"Following: {me.follows_count}")

# Get another user's profile
user_profile = client.get_profile_info(user_id="target_user_id")
print(f"Name: {user_profile.name}")
print(f"Is Following Business: {user_profile.is_user_follow_business}")
```

### Conversation Management

```python
# Get all conversations
conversations = client.get_conversations()
for conversation in conversations:
    print(f"Conversation ID: {conversation.id}")
    print(f"Participants: {conversation.participants}")

# Get conversation with specific user
user_conversations = client.get_user_conversation(
    user_id="target_user_id")

# Get messages from a conversation
messages = client.get_conversation_messages(
    conversation_id="conversation_id",
    desired_limit=100  # Optional: limit number of messages
)

for message in messages:
    print(f"From: {message.from_}")
    print(f"Message: {message.message}")
    print(f"Time: {message.created_time}")
```

### Sending Messages

```python
from instagram_client.schemes.conversation_schemes import SendMessageScheme

# Create message payload
message = SendMessageScheme(
    message="Hello from Instagram API Client!",
    recipient_id="target_user_id"
)

# Send message
response = client.send_message(
    instagram_id="target_user_id",
    payload=message
)
```

## Error Handling

The library includes built-in error handling for common API issues:

```python
from instagram_client.exceptions.http_exceptions import ForbiddenException

try:
    token = client.retrieve_access_token(code="invalid_code")
except ForbiddenException as e:
    print(f"Authentication failed: {e}")
```

## API Documentation

For detailed information about the Instagram Graph API endpoints and features, visit the [official Instagram Graph API documentation](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Security

Please note that this library handles sensitive authentication tokens. Always follow security best practices:
- Never commit tokens to version control
- Store sensitive credentials in environment variables
- Use secure methods to handle and store access tokens
- Implement proper token refresh mechanisms

## Support

If you encounter any issues or have questions, please file an issue on the GitHub repository.

## Contacts:
Email - erkinovabdulvoris101@gmail.com

Telegram - @abdulvoris_101