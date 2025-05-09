from typing import *

def cal_weights(weights: Optional[Dict[int, str]] = None):
    criteria_weights = {
        "education_criteria": 0,
        "experience_criteria": 0,
        "research_criteria": 0,
        "achievement_criteria": 0,
        "certification_criteria": 0,
        "personal_criteria": 0
    }

    if weights:
        a = max([int(id) for id in weights.keys()]) + 1
        xi = (1 - (0.15 * (a - 1) * a) / 2) / a
        for i in range(a):
            key = weights[f"{i}"]
            if key not in criteria_weights.keys():
                raise ValueError(f"Không tìm thấy key: {key}")
            
            criteria_weights[key] = xi + i * 0.15
    
    else:
        criteria_weights = {
            "education_criteria": 1 / 6,
            "experience_criteria": 1 / 6,
            "research_criteria": 1 / 6,
            "achievement_criteria": 1 / 6,
            "certification_criteria": 1 / 6,
            "personal_criteria": 1 / 6
        }
    
    return criteria_weights
    
    