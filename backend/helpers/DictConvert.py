import decimal

from schemas.CRUD.Scholarship import PostScholarshipRequest

def to_dict(model):
    resp = {}
    for key, value in vars(model).items():
        if value is None or key.startswith("_") or key == "is_public":
            continue

        if isinstance(value, decimal.Decimal):
            value = float(value)

        if (not isinstance(value, bool)) and \
            (not isinstance(value, int)) and \
            (not isinstance(value, float)):
            value = str(value)

        resp[key] = value 
    return resp

def convert_scholarship_to_text(scholarship: PostScholarshipRequest) -> str:
    lines = []

    # General information
    lines.append(f"Scholarship Title: {scholarship.title}.")
    if scholarship.provider:
        lines.append(f"Provided by: {scholarship.provider}.")
    if scholarship.type:
        lines.append(f"Type: {scholarship.type}.")
    if scholarship.funding_level:
        lines.append(f"Funding Level: {scholarship.funding_level}.")
    if scholarship.degree_level:
        lines.append(f"Degree Level: {scholarship.degree_level}.")
    if scholarship.region:
        lines.append(f"Region: {scholarship.region}.")
    if scholarship.country:
        lines.append(f"Country: {scholarship.country}.")
    if scholarship.major:
        lines.append(f"Field of Study: {scholarship.major}.")
    if scholarship.deadline:
        lines.append(f"Application Deadline: {scholarship.deadline}.")
    if scholarship.original_url:
        lines.append(f"More Information: {scholarship.original_url}")

    # Criteria
    criteria_lines = []
    if scholarship.education_criteria:
        criteria_lines.append(f"- Education: {scholarship.education_criteria}")
    if scholarship.personal_criteria:
        criteria_lines.append(f"- Personal qualities: {scholarship.personal_criteria}")
    if scholarship.experience_criteria:
        criteria_lines.append(f"- Experience: {scholarship.experience_criteria}")
    if scholarship.research_criteria:
        criteria_lines.append(f"- Research: {scholarship.research_criteria}")
    if scholarship.certification_criteria:
        criteria_lines.append(f"- Certifications: {scholarship.certification_criteria}")
    if scholarship.achievement_criteria:
        criteria_lines.append(f"- Achievements: {scholarship.achievement_criteria}")

    if criteria_lines:
        lines.append("Eligibility Criteria:")
        lines.extend(criteria_lines)

    # Description
    if scholarship.description:
        lines.append(f"\nDescription:\n{scholarship.description}")

    return "\n".join(lines)

def convert_candidate_to_text(profile, educations, experiences, achievements, publications):
    text = ""

    # === Personal Info ===
    if profile:
        full_name = f"{profile.get('first_name', '')} {profile.get('middle_name', '')} {profile.get('last_name', '')}".strip()
        text += f"Candidate Name: {full_name or 'Unknown'}.\n"
        if profile.get("job_title"):
            text += f"Current Job Title: {profile['job_title']}.\n"
        if profile.get("contact_email"):
            text += f"Email: {profile['contact_email']}.\n"
        if profile.get("gender"):
            text += f"Gender: {profile['gender']}.\n"
        if profile.get("date_of_birth"):
            text += f"Date of Birth: {profile['date_of_birth']}.\n"
        if profile.get("nationality"):
            text += f"Nationality: {profile['nationality']}.\n"
        if profile.get("country_of_residence"):
            text += f"Country of Residence: {profile['country_of_residence']}.\n"
        if profile.get("self_introduction"):
            text += f"Self Introduction: {profile['self_introduction']}.\n"

    # === Education ===
    if educations and educations[0]:
        text += "\nEducational Background:\n"
        for edu in educations[1]:
            line = f"- {edu['degree_type']} in {edu['major']} at {edu['institution']}"
            if edu.get("graduation_year"):
                line += f", graduated in {edu['graduation_year']}"
            if edu.get("gpa") is not None:
                line += f", GPA: {edu['gpa']}"
            text += line + ".\n"

    # === Work Experience ===
    if experiences and experiences[0]:
        text += "\nWork Experience:\n"
        for exp in experiences[1]:
            start = exp.get("start_date", "N/A")
            end = exp.get("end_date") or ("Present" if exp.get("is_ongoing") else "N/A")
            text += f"- {exp['title']} at {exp['organization']} ({start} - {end}).\n"
            if exp.get("location"):
                text += f"  Location: {exp['location']}.\n"
            if exp.get("description"):
                text += f"  Description: {exp['description']}.\n"

    # === Achievements ===
    if achievements:
        text += "\nAchievements:\n"
        for ach in achievements:
            text += f"- {ach['title']}"
            if ach.get("description"):
                text += f": {ach['description']}"
            text += "\n"

    # === Publications ===
    if publications and publications[0]:
        text += "\nPublications:\n"
        for pub in publications[1]:
            text += f"- \"{pub['title']}\""
            if pub.get("venue_name"):
                text += f", published at {pub['venue_name']}"
            if pub.get("publish_date"):
                text += f" on {pub['publish_date']}"
            text += ".\n"

    return text.strip()