from models.Scholarship import Scholarship

def scholarship_recommended(profile, db):
    scholarships = Scholarship.get(
        db = db,
        model = "all",
        limit = None,
        offset = None
    )

    