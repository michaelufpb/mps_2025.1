from datetime import datetime
from typing import List

class Lab:
    def __init__(self, id: str, nome: str, capacidade: int, equipamentos: List[str] = None):
        self.id = id
        self.nome = nome
        self.capacidade = capacidade
        self.equipamentos = equipamentos or []
    
    def __str__(self):
        equipamentos_str = ", ".join(self.equipamentos) if self.equipamentos else "Nenhum"
        return f"Lab {self.id}: {self.nome} | Capacidade: {self.capacidade} | Equipamentos: {equipamentos_str}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "capacidade": self.capacidade,
            "equipamentos": self.equipamentos
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            nome=data["nome"],
            capacidade=data["capacidade"],
            equipamentos=data.get("equipamentos", [])
        )
