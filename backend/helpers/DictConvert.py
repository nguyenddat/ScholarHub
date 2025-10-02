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
    if not scholarship:
        return "No scholarship information available."

    lines = []

    # General information
    title = getattr(scholarship, "title", None)
    lines.append(f"Scholarship Title: {title or 'N/A'}.")

    provider = getattr(scholarship, "provider", None)
    if provider:
        lines.append(f"Provided by: {provider}.")

    type_ = getattr(scholarship, "type", None)
    if type_:
        lines.append(f"Type: {type_}.")

    funding_level = getattr(scholarship, "funding_level", None)
    if funding_level:
        lines.append(f"Funding Level: {funding_level}.")

    degree_level = getattr(scholarship, "degree_level", None)
    if degree_level:
        lines.append(f"Degree Level: {degree_level}.")

    region = getattr(scholarship, "region", None)
    if region:
        lines.append(f"Region: {region}.")

    country = getattr(scholarship, "country", None)
    if country:
        lines.append(f"Country: {country}.")

    major = getattr(scholarship, "major", None)
    if major:
        lines.append(f"Field of Study: {major}.")

    deadline = getattr(scholarship, "deadline", None)
    if deadline:
        lines.append(f"Application Deadline: {deadline}.")

    original_url = getattr(scholarship, "original_url", None)
    if original_url:
        lines.append(f"More Information: {original_url}")

    # Criteria
    criteria_lines = []

    education_criteria = getattr(scholarship, "education_criteria", None)
    if education_criteria:
        criteria_lines.append(f"- Education: {education_criteria}")

    personal_criteria = getattr(scholarship, "personal_criteria", None)
    if personal_criteria:
        criteria_lines.append(f"- Personal qualities: {personal_criteria}")

    experience_criteria = getattr(scholarship, "experience_criteria", None)
    if experience_criteria:
        criteria_lines.append(f"- Experience: {experience_criteria}")

    research_criteria = getattr(scholarship, "research_criteria", None)
    if research_criteria:
        criteria_lines.append(f"- Research: {research_criteria}")

    certification_criteria = getattr(scholarship, "certification_criteria", None)
    if certification_criteria:
        criteria_lines.append(f"- Certifications: {certification_criteria}")

    achievement_criteria = getattr(scholarship, "achievement_criteria", None)
    if achievement_criteria:
        criteria_lines.append(f"- Achievements: {achievement_criteria}")

    if criteria_lines:
        lines.append("Eligibility Criteria:")
        lines.extend(criteria_lines)

    # Description
    description = getattr(scholarship, "description", None)
    if description:
        lines.append(f"\nDescription:\n{description}")

    return "\n".join(lines)


def convert_candidate_to_text(profile, educations, experiences, achievements, publications):
    text = ""

    # === Personal Info ===
    if profile:
        full_name = f"{profile.get('first_name', '')} {profile.get('middle_name', '')} {profile.get('last_name', '')}".strip()
        text += f"Candidate Name: {full_name or 'Unknown'}.\n"
        if profile.get("job_title"):
            text += f"Current Job Title: {profile.get('job_title')}.\n"
        if profile.get("contact_email"):
            text += f"Email: {profile.get('contact_email')}.\n"
        if profile.get("gender"):
            text += f"Gender: {profile.get('gender')}.\n"
        if profile.get("date_of_birth"):
            text += f"Date of Birth: {profile.get('date_of_birth')}.\n"
        if profile.get("nationality"):
            text += f"Nationality: {profile.get('nationality')}.\n"
        if profile.get("country_of_residence"):
            text += f"Country of Residence: {profile.get('country_of_residence')}.\n"
        if profile.get("self_introduction"):
            text += f"Self Introduction: {profile.get('self_introduction')}.\n"

    # === Education ===
    if educations:
        text += "\nEducational Background:\n"
        for edu in educations:
            degree = edu.get('degree_type', 'Degree')
            major = edu.get('major', 'Unknown Major')
            institution = edu.get('institution', 'Unknown Institution')
            line = f"- {degree} in {major} at {institution}"
            if edu.get("graduation_year"):
                line += f", graduated in {edu.get('graduation_year')}"
            if edu.get("gpa") is not None:
                line += f", GPA: {edu.get('gpa')}"
            text += line + ".\n"

    # === Work Experience ===
    if experiences:
        text += "\nWork Experience:\n"
        for exp in experiences:
            title = exp.get('title', 'Unknown Title')
            organization = exp.get('organization', 'Unknown Organization')
            start = exp.get("start_date", "N/A")
            end = exp.get("end_date") or ("Present" if exp.get("is_ongoing") else "N/A")
            text += f"- {title} at {organization} ({start} - {end}).\n"
            if exp.get("location"):
                text += f"  Location: {exp.get('location')}.\n"
            if exp.get("description"):
                text += f"  Description: {exp.get('description')}.\n"

    # === Achievements ===
    if achievements:
        text += "\nAchievements:\n"
        for ach in achievements:
            title = ach.get('title', 'Unknown Achievement')
            text += f"- {title}"
            if ach.get("description"):
                text += f": {ach.get('description')}"
            text += "\n"

    # === Publications ===
    if publications:
        text += "\nPublications:\n"
        for pub in publications:
            title = pub.get('title', 'Untitled')
            text += f"- \"{title}\""
            if pub.get("venue_name"):
                text += f", published at {pub.get('venue_name')}"
            if pub.get("publish_date"):
                text += f" on {pub.get('publish_date')}"
            text += ".\n"

    return text.strip()