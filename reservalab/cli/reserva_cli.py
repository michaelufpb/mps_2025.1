from cli.base_cli import BaseCLI
from controller.commands.command import ListarTodasReservasCommand

class ReservaCLI(BaseCLI):
    """CLI para gerenciamento de reservas"""
    
    def exibir_menu_reservas_admin(self) -> str:
        """Exibe menu para gerenciar reservas (admin)"""
        self.exibir_cabecalho("GERENCIAR RESERVAS")
        print("1. Listar Todas as Reservas")
        print("2. Voltar")
        
        return self.ler_opcao()
    
    def listar_todas_reservas(self):
        """Lista todas as reservas"""
        command = ListarTodasReservasCommand(self.facade.get_gerente_reserva())
        reservas = self.facade.execute_command(command)
        self.exibir_lista(reservas, "TODAS AS RESERVAS")
    
    def processar_menu_reservas_admin(self):
        """Processa menu de gerenciamento de reservas (admin)"""
        while True:
            opcao = self.exibir_menu_reservas_admin()
            
            if opcao == "1":
                self.listar_todas_reservas()
            elif opcao == "2":
                break
            else:
                self.exibir_erro("Opção inválida!")
            
            self.aguardar_enter()