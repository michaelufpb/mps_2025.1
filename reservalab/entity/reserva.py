from datetime import datetime
from typing import Optional

class Reserva:
    def __init__(self, id: str, lab_id: str, usuario_id: str, data_inicio: datetime, 
                 data_fim: datetime, motivo: str, status: str = "ativa"):
        self.id = id
        self.lab_id = lab_id
        self.usuario_id = usuario_id
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.motivo = motivo
        self.status = status  # ativa, cancelada
    
    def __str__(self):
        return f"Reserva {self.id}: Lab {self.lab_id} | Usuário {self.usuario_id} | " \
               f"{self.data_inicio.strftime('%d/%m/%Y %H:%M')} - {self.data_fim.strftime('%d/%m/%Y %H:%M')} | {self.status}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "lab_id": self.lab_id,
            "usuario_id": self.usuario_id,
            "data_inicio": self.data_inicio.isoformat(),
            "data_fim": self.data_fim.isoformat(),
            "motivo": self.motivo,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            lab_id=data["lab_id"],
            usuario_id=data["usuario_id"],
            data_inicio=datetime.fromisoformat(data["data_inicio"]),
            data_fim=datetime.fromisoformat(data["data_fim"]),
            motivo=data["motivo"],
            status=data.get("status", "ativa")
        )
    
    def tem_conflito(self, outra_reserva: 'Reserva') -> bool:
        """Verifica se há conflito de horário com outra reserva"""
        if self.lab_id != outra_reserva.lab_id or self.status != "ativa" or outra_reserva.status != "ativa":
            return False
        
        # Verifica se os intervalos se sobrepõem
        return (self.data_inicio < outra_reserva.data_fim and 
                self.data_fim > outra_reserva.data_inicio)
