import requests

division = "YOUR_CAMPUS_HERE" # "ERIN" for UTM and "ARTSC" for UTSG
sessions = ["SESSSIONS_LIST_HERE"] # Format is "YYYY9" for Fall, "YYYY1" for Winter, [20259, 20261]
course_code = ["COURSE_CODES_HERE"] # List of course codes to check, e.g., ["MAT223H5", "CSC207H5"]
sections = [['YOUR_SECTIONS_HERE']] # List of sections to check, e.g., [['PRA0101', 'PRA0119']] sections for each course is a nestedlist

url = "https://api.easi.utoronto.ca/ttb/getPageableCourses"

headers = {
    "Content-Type": "application/json",
    "Origin": "https://ttb.utoronto.ca",
    "Referer": "https://ttb.utoronto.ca/"
}

page = 1
page_size = 20
start_marker = r'<courses><courses>'
end_marker = r'<cmCourseInfo>'

def send_discord_message(message: str):
    webhook_url = r"YOUR_DISCORD_WEBHOOK_URL_HERE" # Put your Discord webhook URL here, found in server settings under Integrations
    data = {"content": message}
    requests.post(webhook_url, json=data)


for i in range(len(course_code)):
    payload = {
        "courseCodeAndTitleProps": {"courseCode": course_code[i], "courseTitle": "", "courseSectionCode": ""},
        "departmentProps": [],
        "campuses": [],
        "sessions": sessions,
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
        "page": 1,
        "pageSize": 20,
        "direction": "asc"
    }

    response = requests.post(url, headers=headers, json=payload)
    text = response.text

    start_pos = text.find(start_marker)
    end_pos = text.find(end_marker, start_pos)

    extracted_snippet = text[start_pos:end_pos]

    for section in sections[i]:
        section_start_pos = text.find(section)
        curr_enrol_pos = text.find("<currentEnrolment>", section_start_pos)
        max_enrol_pos = text.find("<maxEnrolment>", curr_enrol_pos)
        
        current_enrollement = int(text[curr_enrol_pos + len("<currentEnrolment>"):curr_enrol_pos + len("<currentEnrolment>") + 2].strip('<'))
        max_enrollement = int(text[max_enrol_pos + len("<maxEnrolment>"):max_enrol_pos + len("<maxEnrolment>") + 2].strip('<'))

        if current_enrollement < max_enrollement:
            message = f"There are {max_enrollement - current_enrollement} spots available in section {section} in course {course_code[i]}."
            send_discord_message(message)
        else:
            message = f"Section {section} of course {course_code[i]} is full."
            send_discord_message(message)
