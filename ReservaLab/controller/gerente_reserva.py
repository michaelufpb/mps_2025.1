from datetime import datetime, timedelta
from typing import List
from entity.reserva import Reserva
from entity.lab import Lab
from repository.json_repository import JSONRepository

class GerenteReserva:
    def __init__(self, repository: JSONRepository):
        self.repository = repository
    
    def criar_reserva(self, lab_id: str, usuario_id: str, data_inicio: datetime, 
                     data_fim: datetime, motivo: str) -> bool:
        """Cria uma nova reserva"""
        try:
            # Verifica se o laboratório existe
            lab = self.repository.get_lab_by_id(lab_id)
            if not lab:
                print(f"Erro: Laboratório '{lab_id}' não encontrado.")
                return False
            
            # Verifica se o usuário existe
            usuario = self.repository.get_user_by_id(usuario_id)
            if not usuario:
                print(f"Erro: Usuário '{usuario_id}' não encontrado.")
                return False
            
            # Validações de data
            if not self._validate_datetime(data_inicio, data_fim):
                return False
            
            # Gera ID único para a reserva
            reserva_id = self._generate_reserva_id()
            
            # Cria a reserva
            nova_reserva = Reserva(reserva_id, lab_id, usuario_id, data_inicio, data_fim, motivo)
            
            # Verifica conflitos
            if self._has_conflict(nova_reserva):
                print("Erro: Já existe uma reserva ativa para este laboratório no período solicitado.")
                return False
            
            self.repository.add_reserva(nova_reserva)
            print(f"Reserva criada com sucesso! ID: {reserva_id}")
            return True
            
        except Exception as e:
            print(f"Erro ao criar reserva: {e}")
            return False
    
    def _validate_datetime(self, data_inicio: datetime, data_fim: datetime) -> bool:
        """Valida as datas da reserva"""
        agora = datetime.now()
        
        if data_inicio < agora:
            print("Erro: Data de início não pode ser no passado.")
            return False
        
        if data_fim <= data_inicio:
            print("Erro: Data de fim deve ser posterior à data de início.")
            return False
        
        # Limita reservas para no máximo 4 horas
        duracao = data_fim - data_inicio
        if duracao > timedelta(hours=4):
            print("Erro: Reserva não pode exceder 4 horas.")
            return False
        
        return True
    
    def _generate_reserva_id(self) -> str:
        """Gera um ID único para a reserva"""
        reservas = self.repository.get_all_reservas()
        return f"R{len(reservas) + 1:04d}"
    
    def _has_conflict(self, nova_reserva: Reserva) -> bool:
        """Verifica se há conflito com outras reservas"""
        reservas_lab = self.repository.get_reservas_by_lab(nova_reserva.lab_id)
        
        for reserva_existente in reservas_lab:
            if nova_reserva.tem_conflito(reserva_existente):
                return True
        
        return False
    
    def cancelar_reserva(self, reserva_id: str, usuario_id: str) -> bool:
        """Cancela uma reserva"""
        try:
            reserva = self.repository.get_reserva_by_id(reserva_id)
            if not reserva:
                print(f"Erro: Reserva '{reserva_id}' não encontrada.")
                return False
            
            # Verifica se o usuário pode cancelar (própria reserva ou admin)
            usuario = self.repository.get_user_by_id(usuario_id)
            if not usuario:
                print(f"Erro: Usuário '{usuario_id}' não encontrado.")
                return False
            
            if reserva.usuario_id != usuario_id and usuario.role != "admin":
                print("Erro: Você só pode cancelar suas próprias reservas.")
                return False
            
            if reserva.status == "cancelada":
                print("Erro: Esta reserva já foi cancelada.")
                return False
            
            self.repository.cancel_reserva(reserva_id)
            print(f"Reserva '{reserva_id}' cancelada com sucesso!")
            return True
            
        except Exception as e:
            print(f"Erro ao cancelar reserva: {e}")
            return False
    
    def listar_reservas_usuario(self, usuario_id: str) -> List[Reserva]:
        """Lista reservas de um usuário"""
        return self.repository.get_reservas_by_user(usuario_id)
    
    def listar_reservas_lab(self, lab_id: str) -> List[Reserva]:
        """Lista reservas de um laboratório"""
        return self.repository.get_reservas_by_lab(lab_id)
    
    def listar_todas_reservas(self) -> List[Reserva]:
        """Lista todas as reservas (apenas para admin)"""
        return self.repository.get_all_reservas()
    
    def consultar_disponibilidade(self, lab_id: str, data_inicio: datetime, data_fim: datetime) -> bool:
        """Consulta disponibilidade de um laboratório em um período"""
        try:
            # Verifica se o laboratório existe
            lab = self.repository.get_lab_by_id(lab_id)
            if not lab:
                print(f"Erro: Laboratório '{lab_id}' não encontrado.")
                return False
            
            # Cria uma reserva temporária para verificar conflitos
            reserva_temp = Reserva("temp", lab_id, "temp", data_inicio, data_fim, "consulta")
            
            if self._has_conflict(reserva_temp):
                print(f"Laboratório '{lab_id}' NÃO está disponível no período solicitado.")
                return False
            else:
                print(f"Laboratório '{lab_id}' está disponível no período solicitado.")
                return True
                
        except Exception as e:
            print(f"Erro ao consultar disponibilidade: {e}")
            return False
