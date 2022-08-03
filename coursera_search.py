
# handling calls to endpoint
import requests

# formatting results
import json
import xmltodict

# error handling import
import traceback

# for env variable handling
import os

# ---------------------------------------------------------------------------- #
def search_coursera(search_terms):

    # credentials
    account_sid = os.getenv('ACCOUNT_SID')
    auth_token = os.getenv('COURSERA_AUTH_TOKEN')

    # api endpoint
    url = f"https://api.impact.com/Mediapartners/{account_sid}/Ads"
    pUrl = "https://api.impact.com/Mediapartners/account_sid/Ads"
    print(f"Hitting '{pUrl}' for coursera courses...")

    try:
        response = requests.get(url, auth=(account_sid, auth_token))

    except Exception as e:
        traceback.print_exc()
        return {'error': f'Error Code 4: Failed to request the API endpoint at url: {pUrl}, given keywords={search_terms}'}

    if response.status_code != 200:
        return {'error': f'Error Code 3: Received response code of {response.status_code}; perhaps our API keys have expired?'}

    else:
        print("Success! Received response of 200")

    results = xmltodict.parse(response.content)

    return results['ImpactRadiusResponse']['Ads']

# ---------------------------------------------------------------------------- #
if __name__ == "__main__":

    search_terms = "javascript"
    coursera_courses = search_coursera(search_terms)

    print(coursera_courses)
    print(f"\nNumber of courses for {search_terms}: {len(coursera_courses)}")
