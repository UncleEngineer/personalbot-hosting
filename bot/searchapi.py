import requests
from decouple import config

# Load Zenserp API key from environment
ZENSERP_API = config('ZENSERP_API')

def search_zenserp(search_query, location="Bangkok,Thailand"):
    # search หาตามที่ user พิมพ์ top 3 ผลลัพธ์ ถ้า error printout
    headers = { 
        "apikey": ZENSERP_API
    }

    params = (
        ("q", search_query),
        ("location", location),
    )
    response = requests.get('https://app.zenserp.com/api/v2/search', headers=headers, params=params)
    results_list = []

    if response.status_code == 200:
        # Parse the response to JSON
        data = response.json()

        # Check if there are any organic search results
        if 'organic' in data:
            results = data['organic'][:3]  # top 3 ผลลัพธ์

            # Prettify the results for display
            for i, item in enumerate(results, 1):
                title = item.get('title')
                url = item.get('url')
                description = item.get('description') or item.get('snippet')  # Fallback to snippet

                # Construct the formatted result string
                result_str = f"Result {i}:\n"
                result_str += f"Title: {title}\n"
                result_str += f"URL: {url}\n"
                result_str += f"Description: {description}\n"
                result_str += "-" * 50  # **** 50 ตัว
                
                results_list.append(result_str)
            
            # Join results to a single string
            return "\n\n".join(results_list)
        else:
            # Return if no results were found
            return "No search results found."
    else:
        # Return an error message if the API call fails
        return f"Error {response.status_code}: Unable to perform search."
