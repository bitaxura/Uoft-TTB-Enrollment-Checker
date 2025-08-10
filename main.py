import requests

# Format:
# Dvision: Campus/division code. Examples: "ERIN" (UTM), "ARTSC" (UTSG FAS).
# Sessions: Session codes as strings. Examples: "YYYY9" (Fall), "YYYY1" (Winter). Example: "20259".
# Course Code: Full name of course including campus suffix. Example: 'MAT224H5'
# Sections: A list of sections you want alerts for. Examples: ["TUT0103", "TUT0104", "PRA0119"].
# User ID: Discord user ID to mention in the message. Example: "700329119761448910".
# CHECK README.MD FOR FULL LIST

# Example:
# courses = [
#     {
#         'division': 'ERIN',
#         'sessions': '20259',
#         'course_code': 'MAT224H5',
#         'sections': ['TUT0103'],
#         'user_id': '700329119761448910'
#     }
# ]  # list of dicts

courses = [{'division': "", 'sessions': "", 'course_code': "", 'sections': [''], 'user_id': ''}]

url = "https://api.easi.utoronto.ca/ttb/getPageableCourses"

headers = {
    "Content-Type": "application/json",
    "Origin": "https://ttb.utoronto.ca",
    "Referer": "https://ttb.utoronto.ca/"
}

PAGE = 1
PAGE_SIZE = 20

START_MARKER = r'<courses><courses>'
END_MARKER = r'<cmCourseInfo>'

CURR_ENROL_STAG = "<currentEnrolment>"
CURR_ENROL_ETAG = "</currentEnrolment>"
MAX_ENROL_STAG = "<maxEnrolment>"
MAX_ENROL_ETAG = "</maxEnrolment>"


def send_discord_message(message: str, user: str):
    webhook_url = r"YOUR_DISCORD_WEBHOOK_URL_HERE" # Put your Discord webhook URL here, found in server settings under Integrations
    message += f"<@{user}>"
    data = {"content": message}
    requests.post(webhook_url, json=data)


for course in courses:
    payload = {
        "courseCodeAndTitleProps": {"courseCode": course['course_code'], "courseTitle": "", "courseSectionCode": ""},
        "departmentProps": [],
        "campuses": [],
        "sessions": [course['sessions']],
        "requirementProps": [],
        "instructor": "",
        "courseLevels": [],
        "deliveryModes": [],
        "dayPreferences": [],
        "timePreferences": [],
        "divisions": [course['division']],
        "creditWeights": [],
        "availableSpace": False,
        "waitListable": False,
        "page": PAGE,
        "pageSize": PAGE_SIZE,
        "direction": "asc"
    }

    response = requests.post(url, headers=headers, json=payload)
    text = response.text

    start_pos = text.find(START_MARKER)
    end_pos = text.find(END_MARKER, start_pos)

    extracted_snippet = text[start_pos:end_pos]

    for section in course['sections']:
        section_start_pos = text.find(section)
        curr_enrol_spos = text.find(CURR_ENROL_STAG, section_start_pos)
        curr_enrol_epos = text.find(CURR_ENROL_ETAG, curr_enrol_spos)

        max_enrol_spos = text.find(MAX_ENROL_STAG, curr_enrol_epos)
        max_enrol_epos = text.find(MAX_ENROL_ETAG, max_enrol_spos)

        current_enrollement = int(text[curr_enrol_spos + len(CURR_ENROL_STAG): curr_enrol_epos])
        max_enrollement = int(text[max_enrol_spos + len(MAX_ENROL_STAG): max_enrol_epos])

        if current_enrollement < max_enrollement:
            message = f"There are {max_enrollement - current_enrollement} spots available in section {section} in course {course['course_code']}."
            send_discord_message(message, course['user_id'])
        # Not really useful but just in case you want a message of its full
        # else:
        #     message = f"Section {section} of course {course['course_code']} is full."
        #     send_discord_message(message, course['user_id'])
