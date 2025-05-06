import os
import requests
from dotenv import load_dotenv
load_dotenv()


def scrape_linkedin_profile(linkedin_profile: str):
    """Scrape information from LinkedIn profile.
        Manually scrape the information from the LinkedIn profile.
    """
    
    response = requests.get(linkedin_profile,timeout=10)
    
    data = response.json().get("person")
    data = {k: v 
            for k, v in data.items()
            if v not in ([],"","",None)
            and k not in ["certifications","languages"]
            }
    return data

def scrape_linkedin_profile_with_proxy(linkedin_profile: str, mock_proxy: bool = False):
    """Scrape information from LinkedIn profile.
        Manually scrape the information from the LinkedIn profile.
    """
    
    if mock_proxy:
        linkedin_profile = "https://gist.githubusercontent.com/emarco177/859ec7d786b45d8e3e3f688c6c9139d8/raw/5eaf8e46dc29a98612c8fe0c774123a7a2ac4575/eden-marco-scrapin.json"
        response = requests.get(linkedin_profile,timeout=10)
        return response.json()
    else:
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        headers = {'Authorization': f'Bearer {os.getenv("PROXYCURL_API_KEY")}'}
        response = requests.get(api_endpoint,
                        params={'url': linkedin_profile},
                        headers=headers)

        data = response.json()
        data = {k: v 
            for k, v in data.items()
            if v not in ([],"","",None)
            and k not in ["certifications","languages"]
            }
        if data.get("groups"):
            for group_dict in data.get("groups"):
                group_dict.pop("profile_pic_url")
        return data




if __name__ == "__main__":
    linkedin_profile_url = "https://www.linkedin.com/in/eden-marco/"
    data_information = scrape_linkedin_profile_with_proxy(linkedin_profile_url, mock_proxy=False)
    print(data_information)