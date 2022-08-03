
# selenium webscraper imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# error handling import
import traceback

# .env handling
import os

# ---------------------------------------------------------------------------- #
def find_codeacademy_courses(search_terms):

    # initialize list
    course_list = []

    # construct url
    base_url = "https://www.codecademy.com/search?query="
    query_url = "%20".join(search_terms.split())
    full_url = base_url + query_url

    print(f"Hitting '{full_url}' to retrieve codeacademy courses...")

    try:
        # initialize webdriver
        options = webdriver.ChromeOptions()
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        options.add_argument('--headless')
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        # service = ChromeService(executable_path = ChromeDriverManager().install())
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
    except Exception as e:
        traceback.print_exc()
        return {'error': f'Error Code 2: Failed to initialize webdriver, given keywords={search_terms}'}

    # with webdriver.Chrome(service = service, options = options) as driver:

    try:
        # load webpage
        driver.get(full_url)

        # wait until results are loaded
        results_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "ol")))
    except Exception as e:
        traceback.print_exc()
        return {'error': f'Error Code 3: Failed to load (retrieve) webpage, given keywords={search_terms}'}

    # find courses
    courses = results_list.find_elements(By.TAG_NAME, 'li')
    print("\nParsing results...")
    for course in courses:

        # extract details
        url = course.find_element(By.TAG_NAME, 'a').get_attribute("href")
        title = course.find_element(By.TAG_NAME, 'h3').text
        description = course.find_element(By.XPATH, "a/div/div/span[2]").text

        # add course details to list
        course_list.append({'title': title, 'description': description, 'url': url})

    return course_list

# ---------------------------------------------------------------------------- #
if __name__ == "__main__":

    search_terms = "dfkjghsldfkgh"
    course_list = find_courses(search_terms)
    print("Found len(course_list)) courses matching", search_terms)
