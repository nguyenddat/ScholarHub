from sqlalchemy.orm import Session

from models import Profile
from ai.core.chain import get_chat_completion
from repositories import ProfileRepository, UserRepository
from repositories import EducationRepository, ExperienceRepository, PublicationRepository, ReferenceRepository, AchievementRepository

class ProfileService:
    @staticmethod
    def getByUserId(id: int, db: Session):
        return ProfileRepository.getByUserId(id, db)

    @staticmethod
    def create(profile: Profile, db: Session):
        return ProfileRepository.create(profile, db)
    
    @staticmethod
    def update(id: int, update_data: dict, db: Session):
        return ProfileRepository.update(id, update_data, db)
    
    @staticmethod
    def deleteById(id: int, db: Session):
        ProfileRepository.deleteById(id, db)

    @staticmethod
    def updateCriteria(user_id: int, db: Session):
        user = UserRepository.getById(user_id, db)
        profile = ProfileRepository.getByUserId(user_id, db)

        educations = EducationRepository.getByUserId(user_id, db)
        experiences = ExperienceRepository.getByUserId(user_id, db)
        publications = PublicationRepository.getByUserId(user_id, db)
        references = ReferenceRepository.getByUserId(user_id, db)
        achievements = AchievementRepository.getByUserId(user_id, db)

        educations = [EducationRepository.toDict(a) for a in educations]
        experiences = [ExperienceRepository.toDict(a) for a in experiences]
        publications = [PublicationRepository.toDict(a) for a in publications]
        references = [ReferenceRepository.toDict(a) for a in references]
        achievements = [AchievementRepository.toDict(a) for a in achievements]

        resume_text = ""
        if educations:
            resume_text += "## Education\n"
            for edu in educations:
                degree_type = edu.get('degree_type', '')
                major = edu.get('major', '')
                institution = edu.get('institution', '')
                graduation_year = edu.get('graduation_year', '')
                gpa = edu.get('gpa', '')
                resume_text += f"- {degree_type} in {major} at {institution}"
                if graduation_year or gpa:
                    resume_text += f", Graduation: {graduation_year}" if graduation_year else ""
                    resume_text += f", GPA: {gpa}" if gpa else ""
                resume_text += "\n"

        if experiences:
            resume_text += "\n## Experience\n"
            for exp in experiences:
                title = exp.get('title', '')
                organization = exp.get('organization', '')
                start_date = exp.get('start_date', '')
                end_date = exp.get('end_date', 'Present')
                location = exp.get('location', '')
                description = exp.get('description', '')

                resume_text += f"- {title} at {organization} ({start_date} - {end_date})\n"
                if location:
                    resume_text += f"  Location: {location}\n"
                if description:
                    resume_text += f"  Description: {description}\n"

        if publications:
            resume_text += "\n## Publications\n"
            for pub in publications:
                title = pub.get('title', '')
                pub_type = pub.get('type', '')
                venue_name = pub.get('venue_name', '')
                publish_date = pub.get('publish_date', '')
                resume_text += f"- {title} ({pub_type}), {venue_name}, {publish_date}\n"

        if achievements:
            resume_text += "\n## Achievements\n"
            for ach in achievements:
                title = ach.get('title', '')
                issuer = ach.get('issuer', '')
                award_date = ach.get('award_date', '')
                description = ach.get('description', '')

                resume_text += f"- {title} awarded by {issuer}"
                if award_date:
                    resume_text += f" on {award_date}"
                resume_text += "\n"
                if description:
                    resume_text += f"  Description: {description}\n"

        if references:
            resume_text += "\n## References\n"
            for ref in references:
                name = ref.get('name', '')
                job_title = ref.get('job_title', '')
                organization = ref.get('organization', '')
                relationship = ref.get('relationship', '')
                email = ref.get('email', '')

                resume_text += f"- {name} ({job_title} at {organization}), {relationship}"
                if email:
                    resume_text += f", Email: {email}"
                resume_text += "\n"
                
        # Gửi đến LLM để đánh giá
        criteria_result = get_chat_completion(
            task="resume_extract",
            params={
                "resume": resume_text,
                "question": "Evaluate the information from the CV against these criteria."
            }
        )

        profile.criteria = criteria_result["criteria"]
        db.commit()
        db.refresh(profile)
        return True


