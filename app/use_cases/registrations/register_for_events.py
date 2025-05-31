from app.repositories.event_repository import EventRepository
from app.repositories.registration import RegistrationRepository
from app.repositories.user_repository import UserRepository


class RegisterForEvent:
    def __init__(self, registration_repository: RegistrationRepository, event_repository: EventRepository):
        self.registration_repository: RegistrationRepository = registration_repository
        self.event_repository: EventRepository = event_repository

    def execute(self, user_id: int, event_id: int):

        event = self.event_repository.get_event_by_id(event_id)
        if not event:
            raise ValueError("Event not found")

        existing_registration = self.registration_repository.get_registration(user_id, event_id)
        if existing_registration:
            raise ValueError("User is already registered for this event")

        current_registrations = self.registration_repository.get_event_current_registrations_count(event_id)
        if current_registrations >= event.capacity:
            raise ValueError("Event is full")

        registration = self.registration_repository.create_registration(user_id, event_id)
        return registration