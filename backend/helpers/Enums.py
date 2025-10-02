import enum

class AuthProviderEnum(str, enum.Enum):
    local = 'local'
    google = 'google'

class UserRoleEnum(str, enum.Enum):
    admin = "admin"
    user = "user"
    moderator = "moderator"


class ConnectionStatusEnum(str, enum.Enum):
    pending = 'pending'
    accepted = 'accepted'
    rejected = 'rejected'


class ScholarshipStatusEnum(str, enum.Enum):
    pending = 'pending'
    approved = 'approved'
    rejected = 'rejected'


class ApplicationStatusEnum(str, enum.Enum):
    draft = 'draft'
    submitted = 'submitted'
    under_review = 'under_review'
    accepted = 'accepted'
    rejected = 'rejected'
