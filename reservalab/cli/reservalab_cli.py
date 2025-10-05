from controller.facade_singleton import FacadeSingleton
from entity.user import User
from cli.login_cli import LoginCLI
from cli.admin_cli import AdminCLI
from cli.usuario_menu_cli import UsuarioMenuCLI

class ReservaLabCLI:
    """CLI principal do sistema ReservaLab"""
    
    def __init__(self):
        self.facade = FacadeSingleton()
        self.usuario_logado = None
        self.login_cli = LoginCLI(self.facade)
        self.admin_cli = None
        self.usuario_menu_cli = None
    
    def iniciar(self):
        """Inicia o sistema ReservaLab"""
        print("=" * 50)
        print("    SISTEMA RESERVALAB")
        print("    Gerenciamento de Reservas de Laboratórios")
        print("=" * 50)
        
        while True:
            if not self.usuario_logado:
                self.processar_login()
            else:
                self.processar_menu_logado()
    
    def processar_login(self):
        """Processa login do usuário"""
        usuario, deve_continuar = self.login_cli.processar_menu_login()
        
        if not deve_continuar:
            exit()
        
        if usuario:
            self.usuario_logado = usuario
            # Inicializa CLIs específicos baseados no role do usuário
            if usuario.role == "admin":
                self.admin_cli = AdminCLI(self.facade, usuario)
            else:  # professor ou aluno
                self.usuario_menu_cli = UsuarioMenuCLI(self.facade, usuario)
    
    def processar_menu_logado(self):
        """Processa menu do usuário logado"""
        if self.usuario_logado.role == "admin":
            deve_continuar = self.admin_cli.processar_menu_admin()
            if not deve_continuar:
                self.usuario_logado = None
                self.admin_cli = None
        else:
            deve_continuar = self.usuario_menu_cli.processar_menu_usuario()
            if not deve_continuar:
                self.usuario_logado = None
                self.usuario_menu_cli = None
