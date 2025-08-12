import aiohttp
from collections import defaultdict

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
open_courses = []

def group_by_course_and_session(data):
    grouped = defaultdict(list)
    for item in data:
        key = (item['course_code'], item['sessions'], item['division'])
        grouped[key].append(item)
    return grouped

async def get_course_data(data: list[dict]):
    grouped_data = group_by_course_and_session(data)
    course_data = []

    for (course_code, session, division), courses in grouped_data.items():
        payload = {
            "courseCodeAndTitleProps": {"courseCode": course_code, "courseTitle": "", "courseSectionCode": ""},
            "departmentProps": [],
            "campuses": [],
            "sessions": [session],
            "requirementProps": [],
            "instructor": "",
            "courseLevels": [],
            "deliveryModes": [],
            "dayPreferences": [],
            "timePreferences": [],
            "divisions": [division],
            "creditWeights": [],
            "availableSpace": False,
            "waitListable": False,
            "page": PAGE,
            "pageSize": PAGE_SIZE,
            "direction": "asc"
        }
        text = await fetch_course_data(payload)


        start_pos = text.find(START_MARKER)
        end_pos = text.find(END_MARKER, start_pos)

        text = text[start_pos:end_pos]

        for course in courses:
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
                    open_courses.append(message + f" <@{course['user_id']}>")

    return open_courses


async def fetch_course_data(payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            return await response.text()