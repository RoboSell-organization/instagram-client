from os import access
from urllib.parse import urlencode
from instagram_client.api.base_api import BaseAPI
from instagram_client.exceptions.http_exceptions import ForbiddenApiException
from instagram_client.schemes.conversation_schemes import Conversation, ConversationsResponse, UserConversationResponse, \
    MessagesListResponse, Messages, MessageItem, SendMessageScheme
from instagram_client.schemes.user_schemes import LoginResponse, TokenResponse, UserResponse, UserProfile
from dateutil.parser import parse


class InstagramClient(BaseAPI):
    """
        A Python instagram_client for interacting with the official Instagram Graph API.

        This instagram_client handles authentication, token management, and API requests
        for retrieving user information, managing conversations, and more.

        Official Instagram Graph API documentation:
        https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/

       Attributes:
        BASE_URL (str): The base URL for Instagram's Graph API.
    """

    BASE_URL = "https://graph.instagram.com/v22.0" # instagram base url of api

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str, scopes: list[str]):
        """
            Initializes the InstagramClient with authentication credentials and configuration.

            :param client_id: The instagram_client ID assigned by Instagram app.
            :param client_secret: The instagram_client secret assigned by Instagram app.
            :param redirect_uri: The URI to which Instagram will redirect after authentication.
            :param scopes: A list of OAuth scopes defining the access permissions.

            for more detail info visit:
            https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/business-login
        """
        super().__init__(base_url=self.BASE_URL)
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = ','.join(scopes)
        self.redirect_uri = redirect_uri
        self.access_token = ""
        self.headers = {"Accept": "application/json", "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.access_token}"}

    def set_access_token(self, access_token: str) -> None:
        """
            Upgrades the access token for this InstagramClient instance.

            This method updates the access token used for authenticating API requests and
            refreshes the HTTP headers to include the new token.

            :param access_token: The new access token to be used for authentication.
            :return: None
        """
        self.access_token = access_token
        self.headers["Authorization"] = f"Bearer {access_token}"


    def get_auth_url(self, enable_fb_login: int = 1, force_authentication: int = 0, state: str = None):
        """
           Constructs the Instagram OAuth authorization URL.

           This method builds the URL that directs users to Instagram's OAuth authorization page,
           where they can grant access to the application. The URL includes required query parameters
           such as client_id, redirect_uri, scope, and response type. Optionally, parameters for Facebook login
           and forced re-authentication can be specified.

           :param enable_fb_login: Flag to enable Facebook login (1 to enable, default is 1).
           :param force_authentication: Flag to force re-authentication (1 to force, default is 0).
           :param state: Optional state parameter to provide custom data
           :return: A URL string directing the user to the Instagram OAuth authorization page.
           """
        query_params = {'client_id': self.client_id, 'redirect_uri': self.redirect_uri, 'scope': self.scope,
        'response_type': 'code', 'enable_fb_login': enable_fb_login, 'force_authentication': force_authentication}

        if state:
            query_params['state'] = state

        return 'https://www.instagram.com/oauth/authorize?' + urlencode(query_params)


    def retrieve_access_token(self, code: str) -> LoginResponse:
        """
           Retrieves an access token using the provided authorization code.

           This method sends a POST request to Instagram's access token endpoint with the necessary
           credentials and authorization code to exchange it for an access token. If the response does
           not contain an 'access_token', it raises a ForbiddenApiException.

           :param code: The authorization code returned by Instagram after user authorization.
           :return: An instance of LoginResponse containing the access token and related data.
           :raises ForbiddenApiException: If the access token is not present in the response.
       """
        payload = {'client_id': self.client_id, 'client_secret': self.client_secret, 'grant_type': 'authorization_code',
        'redirect_uri': self.redirect_uri, 'code': code}

        response = self._post("https://www.instagram.com/oauth/access_token", data=payload,
                              reset_base_url=True, form_encoded=True)
        data = response.json()

        if 'access_token' not in data:
            raise ForbiddenApiException("Access denied!", 401)

        self.set_access_token(access_token=data['access_token'])
        return LoginResponse(**data)

    def exchange_long_lived_token(self) -> TokenResponse:
        """
           Exchanges a short-lived access token for a long-lived access token.

           This method sends a GET request to the Instagram Graph API endpoint for token exchange.
           It uses the current access token and the instagram_client secret to request a long-lived token.
           The response is parsed into a TokenResponse object.

           :return: An instance of TokenResponse containing the long-lived access token and its details.
       """
        query_params = {"grant_type": "ig_exchange_token", "client_secret": self.client_secret, "access_token": self.access_token}
        response = self._get(f'/access_token?' + urlencode(query_params))
        token = TokenResponse(**response.json())

        self.set_access_token(access_token=token.access_token)
        return token

    def get_me(self) -> UserResponse:
        """
           Retrieves the authenticated user's profile information.

           This method calls the Instagram Graph API endpoint to obtain details about the
           authenticated user. It requests specific fields such as user_id, username, name,
           profile_picture_url, followers_count, follows_count, and media_count.

           :return: An instance of UserResponse containing user profile details.
       """
        allowed_fields = "user_id,username,name,profile_picture_url,followers_count,follows_count,media_count"
        response = self._get(f'/me?fields={allowed_fields}&access_token={self.access_token}')
        return UserResponse(**response.json())

    def get_profile_info(self, user_id: int) -> UserProfile:
        """
           Retrieves detailed profile information for a specified user.

           This method sends a GET request to the Instagram Graph API to retrieve profile
           details for the user with the given user_id. It requests fields like id, name,
           username, profile_pic, follower_count, is_user_follow_business, and is_business_follow_user.

           :param user_id: The unique identifier of the user whose profile is to be retrieved.
           :return: An instance of UserProfile containing the user's profile information.
       """
        allowed_fields = "id, name,username,profile_pic,follower_count,is_user_follow_business,is_business_follow_user"
        response = self._get(f'/{user_id}?fields={allowed_fields}&access_token={self.access_token}')
        return UserProfile(**response.json())

    def get_conversations(self) -> list[Conversation]:
        """
            Retrieves the list of conversations for the authenticated Instagram user.

            This method sends a GET request to the Instagram Graph API endpoint for retrieving
            conversations associated with the authenticated user on the Instagram platform.
            It requests participant details for each conversation.

            :return: A list of Conversation objects.
        """
        response = self._get(f'/me/conversations?platform=instagram&access_token={self.access_token}&fields=participants')
        return ConversationsResponse(**response.json()).data

    def get_user_conversation(self, user_id: int) -> list[Conversation]:
        """
            Retrieves conversations involving a specific user.

            This method sends a GET request to the Instagram Graph API endpoint to fetch
            conversations for the authenticated user that involve the specified user_id.
            It includes participant details in the response.

            :param user_id: The unique identifier of the user to filter conversations.
            :return: A list of Conversation objects that include the specified user.
            """
        response = self._get(f'/me/conversations?platform=instagram&access_token={self.access_token}&user_id={user_id}&fields=participants')
        return UserConversationResponse(**response.json()).data

    def get_conversation_messages(self, conversation_id: str, desired_limit: int = 100) -> list[MessageItem]:
        """
            Retrieves messages from a specific conversation with pagination support.

            This method retrieves messages from a conversation identified by conversation_id.
            It iterates through paginated results until the desired number of messages is collected
            or no additional messages are available. The messages are then sorted in ascending order
            by their creation time.

            :param conversation_id: The unique identifier of the conversation.
            :param desired_limit: The maximum number of messages to retrieve (default is 100).
            :return: A list of MessageItem objects sorted by creation time.
        """

        messages = []
        url = f'{self.BASE_URL}/{conversation_id}?access_token={self.access_token}&fields=messages{{message,from,created_time}}'
        cycle = 1

        while url and len(messages) < desired_limit:
            response = self._get(url, reset_base_url=True)
            json_data = response.json()

            if cycle > 1:
                if not json_data.get('data'):
                    break
                messages_page = Messages(**json_data).data
            else:
                messages_page = MessagesListResponse(**json_data).messages.data

            messages.extend(messages_page)

            paging = json_data.get("messages", {}).get("paging", {})
            url = paging.get("next")
            cycle += 1

        return sorted(messages[:desired_limit], key=lambda m: parse(m.created_time))

    def send_message(self, instagram_id: str, payload: SendMessageScheme) -> dict:
        """
           Sends a message to a specified Instagram user.

           This method posts a message to the Instagram API for the given Instagram user ID.
           The payload should conform to the SendMessageScheme, defining the structure of the message.
           The method returns the JSON response from the API.

           :param instagram_id: The Instagram user ID to which the message will be sent.
           :param payload: An instance of SendMessageScheme containing the message details.
           :return: A dictionary containing the API's JSON response.
       """
        response = self._post(f'/{instagram_id}/messages', headers=self.headers, data=payload.model_dump())
        return response.json()


    def subscribe_to_webhook(self, user_id: int, subscribed_fields: str = "messages"):
        """
        Subscribes a specific user to webhook events for designated fields.
        The function constructs the API endpoint URL using the provided user_id, subscribed_fields, and the instance's access token.
        It then sends a POST request to subscribe the user to the webhook events, and returns the response in JSON format.

        :param user_id:
        :param subscribed_fields:
        :return: dict
        """
        response = self._post(f'/{user_id}/subscribed_apps?subscribed_fields={subscribed_fields}&access_token={self.access_token}', headers=self.headers,
                              data={})
        return response.json()