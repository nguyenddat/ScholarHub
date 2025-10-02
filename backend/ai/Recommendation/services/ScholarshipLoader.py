import ast
import json
import numpy as np

from database.init_db import get_db
from models.Scholarship import Scholarship

criterias = ["education", "experience", "research", "certification", "achievement"]
def load_scholarships(db):
    scholarships = Scholarship.get(db = db, limit = None, offset = None)
    
    scholarship_criterias = []
    criteria_weights = []

    for scholarship in scholarships:
        tmp = scholarship["scholarship_criteria"]
        scholarship_criteria = []
        criteria_weight = []

        try:
            tmp = ast.literal_eval(tmp)
            for criteria in criterias:
                scholarship_criteria.append(tmp["ordinal_criteria"][criteria]["score"])
                criteria_weight.append(scholarship[f"{criteria}_weights"])
            
            scholarship_criterias.append(np.array(scholarship_criteria, dtype=float))
            criteria_weights.append(np.array(criteria_weight, dtype=float))
        
        except Exception as err:
            print(f"Học bổng {scholarship["title"]} lỗi: {str(err)}")
            print(f"\t{tmp}")
            scholarship_criterias.append(np.zeros((5, 5), dtype=float))
            criteria_weights.append(np.zeros((5,), dtype=float))

    return scholarship_criterias, criteria_weights, scholarships
