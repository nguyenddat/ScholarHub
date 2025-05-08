from typing import *

def cal_weights(weights: Optional[Dict[int, str]] = None):
    criteria_weights = {
        "education": 0,
        "experience": 0,
        "research": 0,
        "achievement": 0,
        "certification": 0,
        "personal": 0
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
            "education": 1 / 6,
            "experience": 1 / 6,
            "research": 1 / 6,
            "achievement": 1 / 6,
            "certification": 1 / 6,
            "personal": 1 / 6
        }
    
    return criteria_weights
    
    