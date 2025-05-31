from typing import List
from app.repositories.registration import RegistrationRepository
from app.schemas.registration import RegistrationResponse

class GetUserEventRegistrations:
    def __init__(self, registration_repository: RegistrationRepository):
        self.registration_repository = registration_repository

    def execute(self, user_id: int) -> List[RegistrationResponse]:
        registrations = self.registration_repository.get_registrations_by_user(user_id)
        return [RegistrationResponse.model_validate(reg) for reg in registrations]