from controller.gerente_lab import GerenteLab
from controller.gerente_usuario import GerenteUsuario
from controller.gerente_reserva import GerenteReserva
from repository.json_repository import JSONRepository

class GerenteFactory:
    @staticmethod
    def create_gerente_lab(repository: JSONRepository):
        return GerenteLab(repository)

    @staticmethod
    def create_gerente_usuario(repository: JSONRepository):
        return GerenteUsuario(repository)

    @staticmethod
    def create_gerente_reserva(repository: JSONRepository):
        return GerenteReserva(repository)