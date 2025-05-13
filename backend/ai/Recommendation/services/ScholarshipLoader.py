import numpy as np

from database.init_db import get_db
from models.Scholarship import Scholarship

criterias = ["education", "personal", "experience", "research", "certification", "achievement"]
def load_scholarships():
    db = next(get_db())
    scholarships = Scholarship.get(db = db, limit = None, offset = None)
    
    scholarship_criterias = []
    criteria_weights = []

    for scholarship in scholarships:
        scholarship_criteria = []
        criteria_weight = []

        for criteria in criterias:
            scholarship_criteria.append(scholarship[f"{criteria}_criteria"])
            criteria_weight.append(scholarship[f"{criteria}_weights"])
        
        scholarship_criterias.append(np.array(scholarship_criteria))
        criteria_weights.append(np.array(criteria_weight))
    
    db.close()
    return scholarship_criterias, criteria_weights, scholarships

scholarship_criterias, criteria_weights, scholarships = load_scholarships()