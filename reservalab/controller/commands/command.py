from abc import ABC, abstractmethod
from controller.gerente_lab import GerenteLab
from controller.gerente_usuario import GerenteUsuario
from controller.gerente_reserva import GerenteReserva
from datetime import datetime

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

# Comandos para Labs
class CadastrarLabCommand(Command):
    def __init__(self, gerente_lab: GerenteLab, lab_id: str, nome: str, capacidade: int, equipamentos: list):
        self.gerente_lab = gerente_lab
        self.lab_id = lab_id
        self.nome = nome
        self.capacidade = capacidade
        self.equipamentos = equipamentos

    def execute(self):
        return self.gerente_lab.cadastrar_lab(self.lab_id, self.nome, self.capacidade, self.equipamentos)

class ListarLabsCommand(Command):
    def __init__(self, gerente_lab: GerenteLab):
        self.gerente_lab = gerente_lab

    def execute(self):
        return self.gerente_lab.listar_labs()

class BuscarLabCommand(Command):
    def __init__(self, gerente_lab: GerenteLab, lab_id: str):
        self.gerente_lab = gerente_lab
        self.lab_id = lab_id

    def execute(self):
        return self.gerente_lab.buscar_lab(self.lab_id)

class AtualizarLabCommand(Command):
    def __init__(self, gerente_lab: GerenteLab, lab_id: str, nome: str, capacidade: int, equipamentos: list):
        self.gerente_lab = gerente_lab
        self.lab_id = lab_id
        self.nome = nome
        self.capacidade = capacidade
        self.equipamentos = equipamentos

    def execute(self):
        return self.gerente_lab.atualizar_lab(self.lab_id, self.nome, self.capacidade, self.equipamentos)

class RemoverLabCommand(Command):
    def __init__(self, gerente_lab: GerenteLab, lab_id: str):
        self.gerente_lab = gerente_lab
        self.lab_id = lab_id

    def execute(self):
        return self.gerente_lab.remover_lab(self.lab_id)

# Comandos para Usuários
class CadastrarUsuarioCommand(Command):
    def __init__(self, gerente_usuario: GerenteUsuario, user_id: str, name: str, role: str, password: str):
        self.gerente_usuario = gerente_usuario
        self.user_id = user_id
        self.name = name
        self.role = role
        self.password = password

    def execute(self):
        return self.gerente_usuario.cadastrar_usuario(self.user_id, self.name, self.role, self.password)

class ListarUsuariosCommand(Command):
    def __init__(self, gerente_usuario: GerenteUsuario):
        self.gerente_usuario = gerente_usuario

    def execute(self):
        return self.gerente_usuario.listar_usuarios()

# Comandos para Reservas
class CriarReservaCommand(Command):
    def __init__(self, gerente_reserva: GerenteReserva, lab_id: str, usuario_id: str, data_inicio: datetime, data_fim: datetime, motivo: str):
        self.gerente_reserva = gerente_reserva
        self.lab_id = lab_id
        self.usuario_id = usuario_id
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.motivo = motivo

    def execute(self):
        return self.gerente_reserva.criar_reserva(self.lab_id, self.usuario_id, self.data_inicio, self.data_fim, self.motivo)

class ListarTodasReservasCommand(Command):
    def __init__(self, gerente_reserva: GerenteReserva):
        self.gerente_reserva = gerente_reserva

    def execute(self):
        return self.gerente_reserva.listar_todas_reservas()

class ListarReservasUsuarioCommand(Command):
    def __init__(self, gerente_reserva: GerenteReserva, usuario_id: str):
        self.gerente_reserva = gerente_reserva
        self.usuario_id = usuario_id

    def execute(self):
        return self.gerente_reserva.listar_reservas_usuario(self.usuario_id)

class CancelarReservaCommand(Command):
    def __init__(self, gerente_reserva: GerenteReserva, reserva_id: str, usuario_id: str):
        self.gerente_reserva = gerente_reserva
        self.reserva_id = reserva_id
        self.usuario_id = usuario_id

    def execute(self):
        return self.gerente_reserva.cancelar_reserva(self.reserva_id, self.usuario_id)

class ConsultarDisponibilidadeCommand(Command):
    def __init__(self, gerente_reserva: GerenteReserva, lab_id: str, data_inicio: datetime, data_fim: datetime):
        self.gerente_reserva = gerente_reserva
        self.lab_id = lab_id
        self.data_inicio = data_inicio
        self.data_fim = data_fim

    def execute(self):
        return self.gerente_reserva.consultar_disponibilidade(self.lab_id, self.data_inicio, self.data_fim)