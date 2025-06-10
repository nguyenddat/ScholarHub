import numpy as np

from ai.ProfileMatching.services import ProfileMatch, ResumeExtract, ScholarshipExtract

async def resume_matching(profile, scholarship):
    return ProfileMatch.profile_match(profile, scholarship)


def preference_matching(profile, scholarship):
    pass


def success_rate(match_percentages, criteria_weights):
    if isinstance(match_percentages, list):
        match_percentages = np.array(match_percentages)
    if isinstance(criteria_weights, list):
        criteria_weights = np.array(criteria_weights)

    return np.sum(np.dot(match_percentages, criteria_weights))


def preference_rate():
    pass


def preference_rate(success_rate, preference):
    pass

