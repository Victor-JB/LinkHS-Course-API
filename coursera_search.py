
# handling calls to endpoint
import requests

# formatting results
import json
import xmltodict

# error handling import
import traceback

# for env variable handling
import os

# for time-keeping and debugging
import time

account_sid = 'IR7FdTDStn9y3560855gpgkhPoZX8TtgX1'
auth_token = 'kPsxR-WH9hiSbhmeF-CcXmNxQPK6iuEk'

# ---------------------------------------------------------------------------- #
def search_coursera(search_terms, pageNum):

    # credentials
    # account_sid = os.getenv('ACCOUNT_SID')
    # auth_token = os.getenv('COURSERA_AUTH_TOKEN')

    start = time.time()

    # api endpoint
    url = f"https://api.impact.com/Mediapartners/{account_sid}/Catalogs/ItemSearch?PageSize=200&Keyword={search_terms}"
    pUrl = f"https://api.impact.com/Mediapartners/<AccountSID>/Catalogs/ItemSearch?PageSize=200&Keyword={search_terms}"

    # searching for specific page if pageNum is given
    try:
        pageNum = int(pageNum)
        if pageNum > 1:
            print("\nPage number given:", pageNum)
            url += f"&Page={pageNum}"
            pUrl += f"&Page={pageNum}"
    except:
        pageNum = 1

    print(f"Hitting '{pUrl}' for coursera courses...")

    try:
        response = requests.get(url, auth=(account_sid, auth_token))

    except Exception as e:
        traceback.print_exc()
        return {'error': f'Error Code 4: Failed to request the API endpoint at url: {pUrl}, given keywords={search_terms}'}

    if response.status_code != 200:
        return {'error': f'Error Code 3: Received response code of {response.status_code}; perhaps our API keys have expired?'}

    else:
        print("Success! Received response code of 200")

    results = xmltodict.parse(response.content)
    print("Request finished in", time.time() - start, "seconds\n")

    results_info = results['ImpactRadiusResponse']['Items']

    if 'Item' in results_info:
        if len(results_info['Item']) == 200:
            print("Over 200 courses were returned; grabbing next batch...")
            next_courses = search_coursera(search_terms, pageNum+1)
            results_info['Item'] += next_courses['Item']
            return results_info

        return results_info

    else:
        return {'error': f'Error Code 1: No courses available for search term(s) {search_terms} at page {pageNum}'}

# ---------------------------------------------------------------------------- #
if __name__ == "__main__":

    search_terms = "python"
    coursera_response = search_coursera(search_terms, '2')
    print(coursera_response)

    if 'error' not in coursera_response:
        coursera_courses = coursera_response['Item']

    else:
        coursera_courses = {}

    print(coursera_courses)
    print(f"\nNumber of courses for {search_terms}: {len(coursera_courses)}")
