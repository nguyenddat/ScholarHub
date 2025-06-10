from typing import *

def cal_weights(weights: Optional[Dict[int, str]] = None):
    criteria_weights = {
        "education_criteria": 0.0,
        "personal_criteria": 0.0,
        "experience_criteria": 0.0,
        "research_criteria": 0.0,
        "achievement_criteria": 0.0,
        "certification_criteria": 0.0
    }

    if weights:
        # Sắp xếp thứ tự ưu tiên từ 0,1,2,...
        sorted_items = sorted(weights.items(), key=lambda x: x[0])
        total = 0.0

        for i, (_, key) in enumerate(sorted_items):
            if key not in criteria_weights:
                raise ValueError(f"Không tìm thấy key: {key}")

            weight = 1 / (2 ** i)
            criteria_weights[key] = weight
            total += weight

        # Chuẩn hóa tổng trọng số = 1
        for k in criteria_weights:
            if criteria_weights[k] > 0:
                criteria_weights[k] /= total
    else:
        # Trọng số mặc định chia đều
        criteria_weights = {
            "education_criteria": 1 / 6,
            "personal_criteria": 1 / 6,
            "experience_criteria": 1 / 6,
            "research_criteria": 1 / 6,
            "achievement_criteria": 1 / 6,
            "certification_criteria": 1 / 6
        }

    return criteria_weights
    
    