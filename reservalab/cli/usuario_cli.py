from cli.base_cli import BaseCLI
from controller.commands.command import ListarUsuariosCommand

class UsuarioCLI(BaseCLI):
    """CLI para gerenciamento de usuários"""
    
    def exibir_menu_usuarios(self) -> str:
        """Exibe menu para gerenciar usuários"""
        self.exibir_cabecalho("GERENCIAR USUÁRIOS")
        print("1. Listar Usuários")
        print("2. Voltar")
        
        return self.ler_opcao()
    
    def listar_usuarios(self):
        """Lista todos os usuários"""
        command = ListarUsuariosCommand(self.facade.get_gerente_usuario())
        usuarios = self.facade.execute_command(command)
        self.exibir_lista(usuarios, "USUÁRIOS CADASTRADOS")
    
    def processar_menu_usuarios(self):
        """Processa menu de gerenciamento de usuários"""
        while True:
            opcao = self.exibir_menu_usuarios()
            
            if opcao == "1":
                self.listar_usuarios()
            elif opcao == "2":
                break
            else:
                self.exibir_erro("Opção inválida!")
            
            self.aguardar_enter()