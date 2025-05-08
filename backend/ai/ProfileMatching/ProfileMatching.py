from ai.ProfileMatching.services import ProfileMatch, ResumeExtract, ScholarshipExtract

async def ResumeMatching(file_path, description):
    pages = await ResumeExtract.read_resume(file_path)
    profile = ResumeExtract.extract_resume(pages)

    scholarship = ScholarshipExtract.extract_scholarship(description)

    return ProfileMatch.profile_match(profile, scholarship)
