import numpy as np

def profile_match(profile, scholarship):
    criteria_ws = scholarship["criteria_weights"]

    scholarship_ordinal = scholarship["ordinal_criteria"]
    profile_ordinal = profile["ordinal_criteria"]
    
    scholarship_binary = scholarship["binary_criteria"]
    profile_binary = profile["binary_criteria"]

    ordinal_point, ordinal_evidence = match_ordinal_criteria(profile_ordinal, scholarship_ordinal, criteria_ws)
    binary_point, binary_evidence = match_binary_criteria(profile_binary, scholarship_binary)
    
    evidence = {
        "criterias": ordinal_evidence,
        "personal_evidence": binary_evidence
    }

    return ordinal_point + binary_point, evidence

def match_ordinal_criteria(profile, scholarship, weights):
    point = 0
    evidence = {}
    for key in ["education", "experience", "research", "achievement", "certification"]:
        if not key in scholarship.keys() or not key in profile.keys():
            raise ValueError(f"Không tìm thấy key {key}")
        
        profile_ = np.array(profile[key])
        scholarship_ = np.array(scholarship[key])
        point += profile_.dot(scholarship_) * weights[key]
        evidence[key] = {
            "profile": profile_,
            "scholarship": scholarship_
        }

    return point, evidence

def match_binary_criteria(profile, scholarship, weight):
    point = 0
    evidence = []
    for key in ["gender", "nationality"]:
        gender_required = scholarship.get(key, "")
        if gender_required != "" and gender_required != profile[key]:
            evidence += f"{key.title()} required: {gender_required} and Profile: {profile[key]}"
            continue
            
        point += 1
        evidence += f"{key.title()} required: {gender_required} and Profile: {profile[key]}"
    
    return (point / 2) * weight, evidence
