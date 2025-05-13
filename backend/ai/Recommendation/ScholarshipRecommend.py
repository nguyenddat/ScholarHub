import json

import numpy as np

from models.Scholarship import Scholarship
from models.Profile import Profile
from ai.Recommendation.services.ScholarshipLoader import criterias, scholarship_criterias, criteria_weights, scholarships

def recommend_scholarship(db, user):
    profile = db.query(Profile).filter(Profile.user_id == user.id).first()
    profile_criteria = json.loads(profile.criteria)
    
    profile_criteria_np = []
    for criteria in criterias:
        profile_criteria_np.append(profile_criteria[criteria]["score"])

    profile_criteria_np = np.array(profile_criteria_np)
    
    points = []
    for scholarship_criteria, criteria_weight in zip(scholarship_criterias, criteria_weights):
        points.append(
            (profile_criteria_np @ scholarship_criteria).dot(criteria_weight)
        )

    sorted_idx = np.argsort(points)[::-1]
    return scholarships[sorted_idx]

    




