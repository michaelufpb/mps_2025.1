import json
import os
from typing import List, Dict, Any
from entity.user import User
from entity.lab import Lab
from entity.reserva import Reserva
from repository.dao import UserDAO, LabDAO, ReservaDAO

class JSONUserDAO(UserDAO):
    def __init__(self, data: Dict):
        self.data = data

    def add_user(self, user: User):
        self.data["usuarios"].append(user.to_dict())

    def get_all_users(self) -> List[User]:
        return [User.from_dict(user_data) for user_data in self.data["usuarios"]]

    def get_user_by_id(self, user_id: str) -> User:
        for user_data in self.data["usuarios"]:
            if user_data["user_id"] == user_id:
                return User.from_dict(user_data)
        return None

class JSONLabDAO(LabDAO):
    def __init__(self, data: Dict):
        self.data = data

    def add_lab(self, lab: Lab):
        self.data["labs"].append(lab.to_dict())

    def get_all_labs(self) -> List[Lab]:
        return [Lab.from_dict(lab_data) for lab_data in self.data["labs"]]

    def get_lab_by_id(self, lab_id: str) -> Lab:
        for lab_data in self.data["labs"]:
            if lab_data["id"] == lab_id:
                return Lab.from_dict(lab_data)
        return None

    def update_lab(self, lab: Lab) -> bool:
        for i, lab_data in enumerate(self.data["labs"]):
            if lab_data["id"] == lab.id:
                self.data["labs"][i] = lab.to_dict()
                return True
        return False

    def delete_lab(self, lab_id: str) -> bool:
        for i, lab_data in enumerate(self.data["labs"]):
            if lab_data["id"] == lab_id:
                del self.data["labs"][i]
                return True
        return False

class JSONReservaDAO(ReservaDAO):
    def __init__(self, data: Dict):
        self.data = data

    def add_reserva(self, reserva: Reserva):
        self.data["reservas"].append(reserva.to_dict())

    def get_all_reservas(self) -> List[Reserva]:
        return [Reserva.from_dict(reserva_data) for reserva_data in self.data["reservas"]]

    def get_reserva_by_id(self, reserva_id: str) -> Reserva:
        for reserva_data in self.data["reservas"]:
            if reserva_data["id"] == reserva_id:
                return Reserva.from_dict(reserva_data)
        return None

    def get_reservas_by_lab(self, lab_id: str) -> List[Reserva]:
        return [Reserva.from_dict(reserva_data) for reserva_data in self.data["reservas"] 
                if reserva_data["lab_id"] == lab_id]

    def get_reservas_by_user(self, user_id: str) -> List[Reserva]:
        return [Reserva.from_dict(reserva_data) for reserva_data in self.data["reservas"] 
                if reserva_data["usuario_id"] == user_id]

    def update_reserva(self, reserva: Reserva) -> bool:
        for i, reserva_data in enumerate(self.data["reservas"]):
            if reserva_data["id"] == reserva.id:
                self.data["reservas"][i] = reserva.to_dict()
                return True
        return False

    def cancel_reserva(self, reserva_id: str) -> bool:
        for i, reserva_data in enumerate(self.data["reservas"]):
            if reserva_data["id"] == reserva_id:
                self.data["reservas"][i]["status"] = "cancelada"
                return True
        return False

class JSONRepository:
    def __init__(self, data_file: str = "reservalab_data.json"):
        self.data_file = data_file
        self.data = self._load_data()
        self.user_dao = JSONUserDAO(self.data)
        self.lab_dao = JSONLabDAO(self.data)
        self.reserva_dao = JSONReservaDAO(self.data)
    
    def _load_data(self) -> Dict[str, Any]:
        """Carrega dados do arquivo JSON ou cria estrutura vazia"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Erro ao carregar dados: {e}")
                return self._create_empty_data()
        else:
            return self._create_empty_data()
    
    def _create_empty_data(self) -> Dict[str, Any]:
        """Cria estrutura de dados vazia"""
        return {
            "usuarios": [],
            "labs": [],
            "reservas": []
        }
    
    def _save_data(self):
        """Salva dados no arquivo JSON"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Erro ao salvar dados: {e}")
    
    # Métodos delegados para DAOs, com save após modificações
    def add_user(self, user: User):
        self.user_dao.add_user(user)
        self._save_data()
    
    def get_all_users(self) -> List[User]:
        return self.user_dao.get_all_users()
    
    def get_user_by_id(self, user_id: str) -> User:
        return self.user_dao.get_user_by_id(user_id)
    
    def add_lab(self, lab: Lab):
        self.lab_dao.add_lab(lab)
        self._save_data()
    
    def get_all_labs(self) -> List[Lab]:
        return self.lab_dao.get_all_labs()
    
    def get_lab_by_id(self, lab_id: str) -> Lab:
        return self.lab_dao.get_lab_by_id(lab_id)
    
    def update_lab(self, lab: Lab) -> bool:
        result = self.lab_dao.update_lab(lab)
        if result:
            self._save_data()
        return result
    
    def delete_lab(self, lab_id: str) -> bool:
        result = self.lab_dao.delete_lab(lab_id)
        if result:
            self._save_data()
        return result
    
    def add_reserva(self, reserva: Reserva):
        self.reserva_dao.add_reserva(reserva)
        self._save_data()
    
    def get_all_reservas(self) -> List[Reserva]:
        return self.reserva_dao.get_all_reservas()
    
    def get_reserva_by_id(self, reserva_id: str) -> Reserva:
        return self.reserva_dao.get_reserva_by_id(reserva_id)
    
    def get_reservas_by_lab(self, lab_id: str) -> List[Reserva]:
        return self.reserva_dao.get_reservas_by_lab(lab_id)
    
    def get_reservas_by_user(self, user_id: str) -> List[Reserva]:
        return self.reserva_dao.get_reservas_by_user(user_id)
    
    def update_reserva(self, reserva: Reserva) -> bool:
        result = self.reserva_dao.update_reserva(reserva)
        if result:
            self._save_data()
        return result
    
    def cancel_reserva(self, reserva_id: str) -> bool:
        result = self.reserva_dao.cancel_reserva(reserva_id)
        if result:
            self._save_data()
        return result