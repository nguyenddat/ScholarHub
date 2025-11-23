import json

import numpy as np

from models import Scholarship
from models import Profile
from ai.Recommendation.services.ScholarshipLoader import load_scholarships, criterias

def recommend_scholarship(db, user, limit: int = 10, offset: int = 0):
    scholarship_criterias, criteria_weights, scholarships = load_scholarships(db)

    profile = db.query(Profile).filter(Profile.user_id == user["id"]).first()
    profile_criteria = profile.criteria

    profile_criteria_np = []
    for criteria in criterias:
        profile_criteria_np.append(profile_criteria[criteria]["score"])

    print(profile_criteria_np, flush=True)

    profile_criteria_np = np.array(profile_criteria_np)

    points = []
    for scholarship_criteria, criteria_weight in zip(scholarship_criterias, criteria_weights):
        points.append(
            np.sum(profile_criteria_np @ scholarship_criteria, axis = 0).dot(criteria_weight)
        )

    sorted_idx = np.argsort(points)[::-1]
    resp_obj = []
    for i in sorted_idx:
        scholarships[i]["score"] = points[i] % 100
        for criteria in criterias:
            del scholarships[i][f"{criteria}_weights"]
        
        del scholarships[i]["scholarship_criteria"]
        
        resp_obj.append(scholarships[i])
    
    return resp_obj[offset:offset + limit]