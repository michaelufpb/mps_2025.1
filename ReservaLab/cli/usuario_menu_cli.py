from cli.base_cli import BaseCLI
from cli.reserva_cli import ReservaCLI

class UsuarioMenuCLI(BaseCLI):
    """CLI para menu do usuário comum"""
    
    def __init__(self, facade, usuario_logado):
        super().__init__(facade, usuario_logado)
        self.reserva_cli = ReservaCLI(facade, usuario_logado)
    
    def exibir_menu_usuario(self) -> str:
        """Exibe menu do usuário comum"""
        self.exibir_cabecalho("MENU USUÁRIO")
        print("1. Consultar Laboratórios")
        print("2. Consultar Disponibilidade")
        print("3. Fazer Reserva")
        print("4. Minhas Reservas")
        print("5. Cancelar Reserva")
        print("6. Logout")
        
        return self.ler_opcao()
    
    def consultar_labs(self):
        """Consulta laboratórios disponíveis"""
        labs = self.facade.get_gerente_lab().listar_labs()
        self.exibir_lista(labs, "LABORATÓRIOS DISPONÍVEIS")
    
    def consultar_disponibilidade(self):
        """Consulta disponibilidade de um laboratório"""
        lab_id = self.ler_texto("ID do laboratório")
        
        print("Data e hora de início:")
        data_inicio = self.ler_data_hora("Exemplo: 15/12/2024 14:00")
        
        print("Data e hora de fim:")
        data_fim = self.ler_data_hora("Exemplo: 15/12/2024 16:00")
        
        self.facade.get_gerente_reserva().consultar_disponibilidade(lab_id, data_inicio, data_fim)
    
    def fazer_reserva(self):
        """Faz uma nova reserva"""
        self.exibir_secao("NOVA RESERVA")
        
        # Lista laboratórios disponíveis
        labs = self.facade.get_gerente_lab().listar_labs()
        if not labs:
            self.exibir_erro("Nenhum laboratório cadastrado.")
            return
        
        print("Laboratórios disponíveis:")
        for lab in labs:
            print(f"  {lab}")
        
        lab_id = self.ler_texto("\nID do laboratório")
        
        print("Data e hora de início:")
        data_inicio = self.ler_data_hora("Exemplo: 15/12/2024 14:00")
        
        print("Data e hora de fim:")
        data_fim = self.ler_data_hora("Exemplo: 15/12/2024 16:00")
        
        motivo = self.ler_texto("Motivo da reserva")
        
        self.facade.get_gerente_reserva().criar_reserva(
            lab_id, self.usuario_logado.user_id, data_inicio, data_fim, motivo
        )
    
    def minhas_reservas(self):
        """Lista reservas do usuário logado"""
        reservas = self.facade.get_gerente_reserva().listar_reservas_usuario(self.usuario_logado.user_id)
        self.exibir_lista(reservas, "MINHAS RESERVAS")
    
    def cancelar_reserva(self):
        """Cancela uma reserva"""
        reserva_id = self.ler_texto("ID da reserva a ser cancelada")
        
        if self.confirmar_operacao(f"Tem certeza que deseja cancelar a reserva '{reserva_id}'?"):
            self.facade.get_gerente_reserva().cancelar_reserva(reserva_id, self.usuario_logado.user_id)
        else:
            self.exibir_sucesso("Operação cancelada.")
    
    def processar_menu_usuario(self) -> bool:
        """
        Processa menu do usuário
        Retorna: True se deve continuar, False se deve fazer logout
        """
        opcao = self.exibir_menu_usuario()
        
        if opcao == "1":
            self.consultar_labs()
        elif opcao == "2":
            self.consultar_disponibilidade()
        elif opcao == "3":
            self.fazer_reserva()
        elif opcao == "4":
            self.minhas_reservas()
        elif opcao == "5":
            self.cancelar_reserva()
        elif opcao == "6":
            self.exibir_sucesso("Logout realizado!")
            return False
        else:
            self.exibir_erro("Opção inválida!")
        
        return True
