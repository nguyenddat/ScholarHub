from schemas.CRUD.Scholarship import PostScholarshipRequest

def scholarship_to_description(scholarship: PostScholarshipRequest) -> str:
    parts = []

    # Thông tin cơ bản
    if scholarship.title:
        parts.append(f"Học bổng: \"{scholarship.title}\"")
    if scholarship.provider:
        parts.append(f"do {scholarship.provider} cung cấp")
    if scholarship.type:
        parts.append(f"({scholarship.type})")
    if scholarship.country or scholarship.region:
        location = f"tại {scholarship.country}" if scholarship.country else f"ở khu vực {scholarship.region}"
        parts.append(location)
    if scholarship.major:
        parts.append(f"dành cho ngành: {scholarship.major}")
    if scholarship.funding_level:
        parts.append(f"Hỗ trợ tài chính: {scholarship.funding_level}")
    if scholarship.degree_level:
        parts.append(f"Trình độ học vấn: {scholarship.degree_level}")
    if scholarship.deadline:
        parts.append(f"Hạn nộp: {scholarship.deadline}")

    # Tiêu chí đánh giá
    criteria_details = []
    if scholarship.education_criteria:
        criteria_details.append(f"Giáo dục: {scholarship.education_criteria}")
    if scholarship.experience_criteria:
        criteria_details.append(f"Kinh nghiệm: {scholarship.experience_criteria}")
    if scholarship.research_criteria:
        criteria_details.append(f"Nghiên cứu: {scholarship.research_criteria}")
    if scholarship.achievement_criteria:
        criteria_details.append(f"Thành tích: {scholarship.achievement_criteria}")
    if scholarship.certification_criteria:
        criteria_details.append(f"Chứng chỉ: {scholarship.certification_criteria}")
    if scholarship.personal_criteria:
        criteria_details.append(f"Yếu tố cá nhân: {scholarship.personal_criteria}")

    if criteria_details:
        parts.append("Tiêu chí đánh giá bao gồm: " + "; ".join(criteria_details) + ".")

    return ". ".join(parts) + "."