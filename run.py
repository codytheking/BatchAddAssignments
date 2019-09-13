#!/usr/bin/env python3

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import datetime

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/classroom.coursework.students']

def main():
    """Shows basic usage of the Classroom API.
    Prints the names of the first 10 courses the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('classroom', 'v1', credentials=creds)

    # Call the Classroom API
    #results = service.courses().list(pageSize=10).execute()
    #courses = results.get('courses', [])
    #
    #if not courses:
    #    print('No courses found.')
    #else:
    #    print('Courses:')
    #    for course in courses:
    #        print(course['name'])


    # Generate for the whole semester
    start_week = 6
    current_week = int(start_week)
    last_week = 17

    start_date = datetime.datetime.strptime("2019-09-19","%Y-%m-%d")
    post_date = start_date

    for i in range(start_week, last_week + 1):
        week_delta = datetime.timedelta(days=7)
        due_date_delta = datetime.timedelta(days=5)

        due_date = post_date + due_date_delta

        post_mon = post_date.month if post_date.month >= 10 else ('0' + str(post_date.month))
        post_day = post_date.day if post_date.day >= 10 else ('0' + str(post_date.day))
        due_mon = due_date.month if due_date.month >= 10 else ('0' + str(due_date.month))
        due_day = due_date.day if due_date.day >= 10 else ('0' + str(due_date.day))

        print('Post: {}, {}'.format(post_date.month, post_date.day))
        print('Due: {}, {}'.format(due_date.month, due_date.day))
        courseWork = {
            'title': 'Journal Week {}'.format(current_week),
            'description': 'Please attach a half page reflection explaining what work you completed for the week.\n\nPlease use 12pt Times (New Roman) font and double space the page. You do not need to put a heading.',
            'scheduledTime': '{}-{}-{}T{}:{}:{}Z'.format(post_date.year, post_mon, post_day, '23', '30' if int(due_mon) < 11 or int(due_day) <= 2 else 59, '00'),  # 23:30 UTC => 4:30pm PST (+1 hr for DST if after Nov 3, 2019)
            'dueDate': {
                "year": due_date.year,
                "month": due_mon,
                "day": due_day
            },
            'dueTime': {
                "hours": 19 if int(due_mon) < 11 or int(due_day) <= 2 else 20,
                "minutes": 0,
                "seconds": 0,
                "nanos": 0
            },  # 19 UTC => 12pm PST (+1 hr for DST if after Nov 3, 2019)
            'workType': 'ASSIGNMENT'
        }

        post_date += week_delta
        current_week = int(current_week) + 1

        courseWork = service.courses().courseWork().create(courseId='41073125665', body=courseWork).execute()
        print('Assignment created with ID {}'.format(courseWork.get('id')))



if __name__ == '__main__':
    main()
