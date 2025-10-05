from datetime import datetime, timedelta
from typing import List
from entity.reserva import Reserva
from entity.lab import Lab
from repository.json_repository import JSONRepository
import uuid

class GerenteReserva:
    def __init__(self, repository: JSONRepository):
        self.dao = repository.reserva_dao
        self.repository = repository  # Manter para acesso a outros DAOs e _save_data
    
    def criar_reserva(self, lab_id: str, usuario_id: str, data_inicio: datetime, 
                     data_fim: datetime, motivo: str) -> bool:
        """Cria uma nova reserva"""
        try:
            # Verifica se o laboratório existe
            lab = self.repository.lab_dao.get_lab_by_id(lab_id)
            if not lab:
                print(f"Erro: Laboratório '{lab_id}' não encontrado.")
                return False
            
            # Verifica se o usuário existe
            usuario = self.repository.user_dao.get_user_by_id(usuario_id)
            if not usuario:
                print(f"Erro: Usuário '{usuario_id}' não encontrado.")
                return False
            
            # Validações de data
            if not self._validate_datetime(data_inicio, data_fim):
                return False
            
            # Gera ID único para a reserva
            reserva_id = str(uuid.uuid4())[:8].upper()
            
            # Cria a reserva
            nova_reserva = Reserva(reserva_id, lab_id, usuario_id, data_inicio, data_fim, motivo)
            
            # Verifica conflitos
            if self._has_conflict(nova_reserva):
                print("Erro: Já existe uma reserva ativa para este laboratório no período solicitado.")
                return False
            
            self.dao.add_reserva(nova_reserva)
            self.repository._save_data()  # Salvar alterações
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
    
    def _has_conflict(self, reserva: Reserva) -> bool:
        """Verifica se há conflito de horário"""
        reservas_lab = self.dao.get_reservas_by_lab(reserva.lab_id)
        for r in reservas_lab:
            if r.tem_conflito(reserva):
                return True
        return False
    
    def cancelar_reserva(self, reserva_id: str, usuario_id: str) -> bool:
        """Cancela uma reserva"""
        try:
            reserva = self.dao.get_reserva_by_id(reserva_id)
            if not reserva:
                print(f"Erro: Reserva '{reserva_id}' não encontrada.")
                return False
            
            # Verifica se o usuário pode cancelar (própria reserva ou admin)
            usuario = self.repository.user_dao.get_user_by_id(usuario_id)
            if not usuario:
                print(f"Erro: Usuário '{usuario_id}' não encontrado.")
                return False
            
            if reserva.usuario_id != usuario_id and usuario.role != "admin":
                print("Erro: Você só pode cancelar suas próprias reservas.")
                return False
            
            if reserva.status == "cancelada":
                print("Erro: Esta reserva já foi cancelada.")
                return False
            
            self.dao.cancel_reserva(reserva_id)
            self.repository._save_data()  # Salvar alterações
            print(f"Reserva '{reserva_id}' cancelada com sucesso!")
            return True
            
        except Exception as e:
            print(f"Erro ao cancelar reserva: {e}")
            return False
    
    def listar_reservas_usuario(self, usuario_id: str) -> List[Reserva]:
        """Lista reservas de um usuário"""
        return self.dao.get_reservas_by_user(usuario_id)
    
    def listar_reservas_lab(self, lab_id: str) -> List[Reserva]:
        """Lista reservas de um laboratório"""
        return self.dao.get_reservas_by_lab(lab_id)
    
    def listar_todas_reservas(self) -> List[Reserva]:
        """Lista todas as reservas (apenas para admin)"""
        return self.dao.get_all_reservas()
    
    def consultar_disponibilidade(self, lab_id: str, data_inicio: datetime, data_fim: datetime) -> bool:
        """Consulta disponibilidade de um laboratório em um período"""
        try:
            # Verifica se o laboratório existe
            lab = self.repository.lab_dao.get_lab_by_id(lab_id)
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