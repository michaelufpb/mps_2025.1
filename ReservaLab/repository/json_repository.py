import json
import os
from typing import List, Dict, Any
from entity.user import User
from entity.lab import Lab
from entity.reserva import Reserva

class JSONRepository:
    def __init__(self, data_file: str = "reservalab_data.json"):
        self.data_file = data_file
        self.data = self._load_data()
    
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
    
    # Métodos para Usuários
    def add_user(self, user: User):
        """Adiciona um usuário"""
        self.data["usuarios"].append(user.to_dict())
        self._save_data()
    
    def get_all_users(self) -> List[User]:
        """Retorna todos os usuários"""
        return [User.from_dict(user_data) for user_data in self.data["usuarios"]]
    
    def get_user_by_id(self, user_id: str) -> User:
        """Busca usuário por ID"""
        for user_data in self.data["usuarios"]:
            if user_data["user_id"] == user_id:
                return User.from_dict(user_data)
        return None
    
    # Métodos para Labs
    def add_lab(self, lab: Lab):
        """Adiciona um laboratório"""
        self.data["labs"].append(lab.to_dict())
        self._save_data()
    
    def get_all_labs(self) -> List[Lab]:
        """Retorna todos os laboratórios"""
        return [Lab.from_dict(lab_data) for lab_data in self.data["labs"]]
    
    def get_lab_by_id(self, lab_id: str) -> Lab:
        """Busca laboratório por ID"""
        for lab_data in self.data["labs"]:
            if lab_data["id"] == lab_id:
                return Lab.from_dict(lab_data)
        return None
    
    def update_lab(self, lab: Lab):
        """Atualiza um laboratório"""
        for i, lab_data in enumerate(self.data["labs"]):
            if lab_data["id"] == lab.id:
                self.data["labs"][i] = lab.to_dict()
                self._save_data()
                return True
        return False
    
    def delete_lab(self, lab_id: str) -> bool:
        """Remove um laboratório"""
        for i, lab_data in enumerate(self.data["labs"]):
            if lab_data["id"] == lab_id:
                del self.data["labs"][i]
                self._save_data()
                return True
        return False
    
    # Métodos para Reservas
    def add_reserva(self, reserva: Reserva):
        """Adiciona uma reserva"""
        self.data["reservas"].append(reserva.to_dict())
        self._save_data()
    
    def get_all_reservas(self) -> List[Reserva]:
        """Retorna todas as reservas"""
        return [Reserva.from_dict(reserva_data) for reserva_data in self.data["reservas"]]
    
    def get_reserva_by_id(self, reserva_id: str) -> Reserva:
        """Busca reserva por ID"""
        for reserva_data in self.data["reservas"]:
            if reserva_data["id"] == reserva_id:
                return Reserva.from_dict(reserva_data)
        return None
    
    def get_reservas_by_lab(self, lab_id: str) -> List[Reserva]:
        """Retorna reservas de um laboratório específico"""
        return [Reserva.from_dict(reserva_data) for reserva_data in self.data["reservas"] 
                if reserva_data["lab_id"] == lab_id]
    
    def get_reservas_by_user(self, user_id: str) -> List[Reserva]:
        """Retorna reservas de um usuário específico"""
        return [Reserva.from_dict(reserva_data) for reserva_data in self.data["reservas"] 
                if reserva_data["usuario_id"] == user_id]
    
    def update_reserva(self, reserva: Reserva):
        """Atualiza uma reserva"""
        for i, reserva_data in enumerate(self.data["reservas"]):
            if reserva_data["id"] == reserva.id:
                self.data["reservas"][i] = reserva.to_dict()
                self._save_data()
                return True
        return False
    
    def cancel_reserva(self, reserva_id: str) -> bool:
        """Cancela uma reserva"""
        for i, reserva_data in enumerate(self.data["reservas"]):
            if reserva_data["id"] == reserva_id:
                self.data["reservas"][i]["status"] = "cancelada"
                self._save_data()
                return True
        return False
