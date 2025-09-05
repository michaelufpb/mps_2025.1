from repository.json_repository import JSONRepository
from controller.gerente_lab import GerenteLab
from controller.gerente_usuario import GerenteUsuario
from controller.gerente_reserva import GerenteReserva
from entity.user import User

class FacadeSingleton:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FacadeSingleton, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.repository = JSONRepository()
            self.gerente_lab = GerenteLab(self.repository)
            self.gerente_usuario = GerenteUsuario(self.repository)
            self.gerente_reserva = GerenteReserva(self.repository)
            
            # Cria usuário admin padrão se não existir
            self.gerente_usuario.criar_usuario_admin_padrao()
            
            self._initialized = True
    
    def get_gerente_lab(self) -> GerenteLab:
        """Retorna o gerente de laboratórios"""
        return self.gerente_lab
    
    def get_gerente_usuario(self) -> GerenteUsuario:
        """Retorna o gerente de usuários"""
        return self.gerente_usuario
    
    def get_gerente_reserva(self) -> GerenteReserva:
        """Retorna o gerente de reservas"""
        return self.gerente_reserva
    
    def autenticar_usuario(self, user_id: str, password: str) -> User:
        """Autentica um usuário"""
        return self.gerente_usuario.autenticar_usuario(user_id, password)
