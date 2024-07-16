import os
import json
import requests
from crewai_tools import tool


class SocialTools:

    @tool
    def create_medium_draft_post(title: str, content: str, tags: list=None):
        """
        Upload a draft post to Medium using the Medium API.
        
        Args:
            title: The title of the Medium post
            content: The post content in markdown format
            tags: The list of tags

        Returns:
            Response from Medium API.
        """
        headers = {
            "Authorization": f"Bearer {os.getenv('MEDIUM_TOKEN')}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # Replace 'your_user_id' with your actual Medium user ID if known, otherwise you need to fetch it
        user_id = SocialTools.get_user_id(os.getenv('MEDIUM_TOKEN'))
        url = f"https://api.medium.com/v1/users/{user_id}/posts"

        data = {
            "title": title,
            "contentFormat": 'markdown',
            "content": content,
            "tags": None,
            "publishStatus": 'draft'
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 201:
            print("Draft post created successfully!")
            print("Response:", response.json())
        else:
            print("Failed to create draft post. Status code:", response.status_code)
            print("Response:", response.json())

    def get_user_id(access_token):
        url = "https://api.medium.com/v1/me"
        headers = {
            "Authorization": f"Bearer {os.getenv('MEDIUM_TOKEN')}",
            "Accept": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            print(user_data['data']['id'])
            return user_data['data']['id']
        else:
            print("Failed to fetch user ID. Status code:", response.status_code)
            print("Response:", response.json())
            return None