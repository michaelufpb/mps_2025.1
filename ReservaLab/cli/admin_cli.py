from cli.base_cli import BaseCLI
from cli.lab_cli import LabCLI
from cli.usuario_cli import UsuarioCLI
from cli.reserva_cli import ReservaCLI

class AdminCLI(BaseCLI):
    """CLI para menu administrativo"""
    
    def __init__(self, facade, usuario_logado):
        super().__init__(facade, usuario_logado)
        self.lab_cli = LabCLI(facade, usuario_logado)
        self.usuario_cli = UsuarioCLI(facade, usuario_logado)
        self.reserva_cli = ReservaCLI(facade, usuario_logado)
    
    def exibir_menu_admin(self) -> str:
        """Exibe menu do administrador"""
        self.exibir_cabecalho("MENU ADMINISTRADOR")
        print("1. Gerenciar Laboratórios")
        print("2. Gerenciar Usuários")
        print("3. Gerenciar Reservas")
        print("4. Logout")
        
        return self.ler_opcao()
    
    def processar_menu_admin(self) -> bool:
        """
        Processa menu administrativo
        Retorna: True se deve continuar, False se deve fazer logout
        """
        opcao = self.exibir_menu_admin()
        
        if opcao == "1":
            self.lab_cli.processar_menu_labs()
        elif opcao == "2":
            self.usuario_cli.processar_menu_usuarios()
        elif opcao == "3":
            self.reserva_cli.processar_menu_reservas_admin()
        elif opcao == "4":
            self.exibir_sucesso("Logout realizado!")
            return False
        else:
            self.exibir_erro("Opção inválida!")
        
        return True
