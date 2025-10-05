from typing import List
from entity.user import User
from entity.lab import Lab
from entity.reserva import Reserva

class UserDAO:
    def add_user(self, user: User):
        pass

    def get_all_users(self) -> List[User]:
        pass

    def get_user_by_id(self, user_id: str) -> User:
        pass

class LabDAO:
    def add_lab(self, lab: Lab):
        pass

    def get_all_labs(self) -> List[Lab]:
        pass

    def get_lab_by_id(self, lab_id: str) -> Lab:
        pass

    def update_lab(self, lab: Lab) -> bool:
        pass

    def delete_lab(self, lab_id: str) -> bool:
        pass

class ReservaDAO:
    def add_reserva(self, reserva: Reserva):
        pass

    def get_all_reservas(self) -> List[Reserva]:
        pass

    def get_reserva_by_id(self, reserva_id: str) -> Reserva:
        pass

    def get_reservas_by_lab(self, lab_id: str) -> List[Reserva]:
        pass

    def get_reservas_by_user(self, user_id: str) -> List[Reserva]:
        pass

    def update_reserva(self, reserva: Reserva) -> bool:
        pass

    def cancel_reserva(self, reserva_id: str) -> bool:
        pass