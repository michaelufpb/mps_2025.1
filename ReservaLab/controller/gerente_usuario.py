import re
from typing import List
from entity.user import User
from repository.json_repository import JSONRepository

class GerenteUsuario:
    def __init__(self, repository: JSONRepository):
        self.repository = repository
    
    def cadastrar_usuario(self, user_id: str, name: str, role: str, password: str) -> bool:
        """Cadastra um novo usuário"""
        try:
            # Verifica se já existe um usuário com esse ID
            if self.repository.get_user_by_id(user_id):
                print(f"Erro: Usuário com ID '{user_id}' já existe.")
                return False
            
            # Validações
            if not self._validate_user_id(user_id):
                return False
            
            if not self._validate_password(password):
                return False
            
            if role not in ["admin", "usuario"]:
                print("Erro: Role deve ser 'admin' ou 'usuario'.")
                return False
            
            user = User(user_id, name, role, password)
            self.repository.add_user(user)
            print(f"Usuário '{name}' cadastrado com sucesso!")
            return True
            
        except Exception as e:
            print(f"Erro ao cadastrar usuário: {e}")
            return False
    
    def _validate_user_id(self, user_id: str) -> bool:
        """Valida o ID do usuário"""
        if len(user_id) > 12:
            print("Erro: Login deve ter no máximo 12 caracteres")
            return False
        if not user_id:
            print("Erro: Login não pode ser vazio")
            return False
        if any(char.isdigit() for char in user_id):
            print("Erro: Login não pode conter números")
            return False
        return True
    
    def _validate_password(self, password: str) -> bool:
        """Valida a senha do usuário"""
        if len(password) < 8 or len(password) > 128:
            print("Erro: Password deve ter entre 8 e 128 caracteres")
            return False
        if not re.search("[a-z]", password):
            print("Erro: Password deve conter pelo menos uma letra minúscula")
            return False
        if not re.search("[A-Z]", password):
            print("Erro: Password deve conter pelo menos uma letra maiúscula")
            return False
        if not re.search("[0-9]", password):
            print("Erro: Password deve conter pelo menos um dígito")
            return False
        if not re.search("[@#$%^&+=]", password):
            print("Erro: Password deve conter pelo menos um caractere especial")
            return False
        return True
    
    def listar_usuarios(self) -> List[User]:
        """Lista todos os usuários"""
        return self.repository.get_all_users()
    
    def buscar_usuario(self, user_id: str) -> User:
        """Busca um usuário por ID"""
        return self.repository.get_user_by_id(user_id)
    
    def autenticar_usuario(self, user_id: str, password: str) -> User:
        """Autentica um usuário"""
        user = self.repository.get_user_by_id(user_id)
        if user and user.password == password:
            return user
        return None
    
    def criar_usuario_admin_padrao(self):
        """Cria usuário admin padrão para testes"""
        admin_id = "admin"
        if not self.repository.get_user_by_id(admin_id):
            admin = User(admin_id, "Administrador", "admin", "Admin123!")
            self.repository.add_user(admin)
            print("Usuário admin padrão criado (login: admin, senha: Admin123!)")
