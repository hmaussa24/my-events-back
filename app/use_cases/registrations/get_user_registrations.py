from typing import List
from app.repositories.registration import RegistrationRepository
from app.schemas.registration import RegistrationResponse

class GetUserRegistrations:
    def __init__(self, registration_repository: RegistrationRepository):
        self.registration_repository = registration_repository

    def execute(self, event_id: int) -> List[RegistrationResponse]:
        registrations = self.registration_repository.get_registrations_by_event(event_id)
        return [RegistrationResponse.model_validate(reg) for reg in registrations]