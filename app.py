
# flask imports
from flask import Flask, request

# json formatting imports
from json2html import *
import json
import pandas as pd

# retrieve env
import os

# limiting the number of pages to fetch
import time

# error handling import
import traceback

# codeacademy import
from codeacademy_search import find_codeacademy_courses

# coursera import
from coursera_search import search_coursera

app = Flask(__name__)

# ---------------------------------------------------------------------------- #
@app.route('/search')
def search():

    keywords = request.args.get('keywords')
    pageNum = request.args.get('page')
    FETCH_ALL_JOBS = False

    start = time.time()
    """
    if not pageNum:
        print("No page number specified; fetching all jobs...")
        FETCH_ALL_JOBS = True
    """

    if keywords is not None:
        # Codeacademy Courses
        codeacademy_courses = find_codeacademy_courses(keywords)
        if type(codeacademy_courses) is list:
            num_codeacademy_courses = len(codeacademy_courses)
            print("Num Codeacademy courses:", num_codeacademy_courses)

        else:
            num_codeacademy_courses = 0

    else:
        codeacademy_courses = {'error': "Error Code 1: No keywords given; remember to use 'keywords' as your search parameter"}
        num_codeacademy_courses = 0

    # Coursera courses
    coursera_response = search_coursera(keywords, pageNum)
    if 'error' not in coursera_response:
        coursera_courses = coursera_response['Item']
        num_coursera_courses = len(coursera_courses)

    else:
        num_coursera_courses = 0

    total_courses = num_codeacademy_courses + num_coursera_courses

    print("\nTotal courses:", total_courses)
    jobs = {'coursera courses': coursera_courses, 'codeacademy jobs': codeacademy_courses, 'total hits': f'{total_courses}'}

    response = json.dumps(jobs, indent=4)

    print("\nTotal time:", time.time() - start)
    return response

# ---------------------------------------------------------------------------- #
if __name__ == "__main__":
	# setting debug to True enables hot reload
	# and also provides a debugger shell
	# if you hit an error while running the server
	app.run(debug = True)
