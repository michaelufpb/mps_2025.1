import re
from typing import List, Tuple
from entity.user import User
from repository.json_repository import JSONRepository

class GerenteUsuario:
    def __init__(self, repository: JSONRepository):
        self.dao = repository.user_dao
        self.repository = repository
    
    def cadastrar_usuario(self, user_id: str, name: str, role: str, password: str) -> Tuple[bool, str]:
        """Cadastra um novo usuário. Retorna (sucesso, mensagem de erro)"""
        try:
            # Verifica se já existe um usuário com esse ID
            if self.dao.get_user_by_id(user_id):
                return False, f"Usuário com ID '{user_id}' já existe."
            
            # Validações
            valid, msg = self._validate_user_id(user_id)
            if not valid:
                return False, msg
            
            valid, msg = self._validate_password(password)
            if not valid:
                return False, msg
            
            if role not in ["admin", "usuario"]:
                return False, "Role deve ser 'admin' ou 'usuario'."
            
            user = User(user_id, name, role, password)
            self.dao.add_user(user)
            self.repository._save_data()
            return True, "Usuário cadastrado com sucesso!"
            
        except Exception as e:
            return False, f"Erro ao cadastrar usuário: {e}"
    
    def _validate_user_id(self, user_id: str) -> Tuple[bool, str]:
        """Valida o ID do usuário. Retorna (valido, mensagem)"""
        if len(user_id) > 12:
            return False, "Login deve ter no máximo 12 caracteres"
        if not user_id:
            return False, "Login não pode ser vazio"
        if any(char.isdigit() for char in user_id):
            return False, "Login não pode conter números"
        return True, ""
    
    def _validate_password(self, password: str) -> Tuple[bool, str]:
        """Valida a senha do usuário. Retorna (valido, mensagem)"""
        if len(password) < 8 or len(password) > 128:
            return False, "Password deve ter entre 8 e 128 caracteres"
        if not re.search("[a-z]", password):
            return False, "Password deve conter pelo menos uma letra minúscula"
        if not re.search("[A-Z]", password):
            return False, "Password deve conter pelo menos uma letra maiúscula"
        if not re.search("[0-9]", password):
            return False, "Password deve conter pelo menos um dígito"
        if not re.search("[@#$%^&+=]", password):
            return False, "Password deve conter pelo menos um caractere especial"
        return True, ""
    
    def listar_usuarios(self) -> List[User]:
        """Lista todos os usuários"""
        return self.dao.get_all_users()
    
    def buscar_usuario(self, user_id: str) -> User:
        """Busca um usuário por ID"""
        return self.dao.get_user_by_id(user_id)
    
    def autenticar_usuario(self, user_id: str, password: str) -> User:
        """Autentica um usuário"""
        user = self.dao.get_user_by_id(user_id)
        if user and user.password == password:
            return user
        return None
    
    def criar_usuario_admin_padrao(self):
        """Cria usuário admin padrão para testes"""
        admin_id = "admin"
        if not self.dao.get_user_by_id(admin_id):
            admin = User(admin_id, "Administrador", "admin", "Admin123!")
            self.dao.add_user(admin)
            self.repository._save_data()