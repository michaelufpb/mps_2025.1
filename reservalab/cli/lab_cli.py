from cli.base_cli import BaseCLI
from controller.commands.command import CadastrarLabCommand, ListarLabsCommand, BuscarLabCommand, AtualizarLabCommand, RemoverLabCommand

class LabCLI(BaseCLI):
    """CLI para gerenciamento de laboratórios"""
    
    def exibir_menu_labs(self) -> str:
        """Exibe menu para gerenciar laboratórios"""
        self.exibir_cabecalho("GERENCIAR LABORATÓRIOS")
        print("1. Cadastrar Laboratório")
        print("2. Listar Laboratórios")
        print("3. Atualizar Laboratório")
        print("4. Remover Laboratório")
        print("5. Desfazer Última Atualização")
        print("6. Voltar")
        
        return self.ler_opcao()
    
    def cadastrar_lab(self):
        """Cadastra novo laboratório"""
        self.exibir_secao("CADASTRO DE LABORATÓRIO")
        
        lab_id = self.ler_texto("ID do laboratório")
        nome = self.ler_texto("Nome do laboratório")
        capacidade = self.ler_numero("Capacidade")
        
        equipamentos_str = self.ler_texto("Equipamentos (separados por vírgula, ou Enter para nenhum)")
        equipamentos = [eq.strip() for eq in equipamentos_str.split(",")] if equipamentos_str else []
        
        command = CadastrarLabCommand(self.facade.get_gerente_lab(), lab_id, nome, capacidade, equipamentos)
        self.facade.execute_command(command)
    
    def listar_labs(self):
        """Lista todos os laboratórios"""
        command = ListarLabsCommand(self.facade.get_gerente_lab())
        labs = self.facade.execute_command(command)
        self.exibir_lista(labs, "LABORATÓRIOS CADASTRADOS")
    
    def atualizar_lab(self):
        """Atualiza um laboratório"""
        lab_id = self.ler_texto("ID do laboratório a ser atualizado")
        
        command_buscar = BuscarLabCommand(self.facade.get_gerente_lab(), lab_id)
        lab = self.facade.execute_command(command_buscar)
        if not lab:
            self.exibir_erro(f"Laboratório '{lab_id}' não encontrado.")
            return
        
        print(f"\nLaboratório atual: {lab}")
        print("Deixe em branco para manter o valor atual.")
        
        nome = self.ler_texto(f"Nome atual ({lab.nome})") or lab.nome
        
        try:
            capacidade_input = self.ler_texto(f"Capacidade atual ({lab.capacidade})")
            capacidade = int(capacidade_input) if capacidade_input else lab.capacidade
        except ValueError:
            self.exibir_erro("Capacidade deve ser um número!")
            return
        
        equipamentos_str = self.ler_texto(f"Equipamentos atuais ({', '.join(lab.equipamentos)})")
        equipamentos = [eq.strip() for eq in equipamentos_str.split(",")] if equipamentos_str else lab.equipamentos
        
        command = AtualizarLabCommand(self.facade.get_gerente_lab(), lab_id, nome, capacidade, equipamentos)
        self.facade.execute_command(command)
    
    def remover_lab(self):
        """Remove um laboratório"""
        lab_id = self.ler_texto("ID do laboratório a ser removido")
        
        if self.confirmar_operacao(f"Tem certeza que deseja remover o laboratório '{lab_id}'?"):
            command = RemoverLabCommand(self.facade.get_gerente_lab(), lab_id)
            self.facade.execute_command(command)
        else:
            self.exibir_sucesso("Operação cancelada.")
    
    def undo_update_lab(self):
        lab_id = self.ler_texto("ID do laboratório para desfazer atualização")
        self.facade.get_gerente_lab().undo_update_lab(lab_id)
    
    def processar_menu_labs(self):
        """Processa menu de gerenciamento de laboratórios"""
        while True:
            opcao = self.exibir_menu_labs()
            
            if opcao == "1":
                self.cadastrar_lab()
            elif opcao == "2":
                self.listar_labs()
            elif opcao == "3":
                self.atualizar_lab()
            elif opcao == "4":
                self.remover_lab()
            elif opcao == "5":
                self.undo_update_lab()
            elif opcao == "6":
                break
            else:
                self.exibir_erro("Opção inválida!")
            
            self.aguardar_enter()