from cli.base_cli import BaseCLI

class LabCLI(BaseCLI):
    """CLI para gerenciamento de laboratórios"""
    
    def exibir_menu_labs(self) -> str:
        """Exibe menu para gerenciar laboratórios"""
        self.exibir_cabecalho("GERENCIAR LABORATÓRIOS")
        print("1. Cadastrar Laboratório")
        print("2. Listar Laboratórios")
        print("3. Atualizar Laboratório")
        print("4. Remover Laboratório")
        print("5. Voltar")
        
        return self.ler_opcao()
    
    def cadastrar_lab(self):
        """Cadastra novo laboratório"""
        self.exibir_secao("CADASTRO DE LABORATÓRIO")
        
        lab_id = self.ler_texto("ID do laboratório")
        nome = self.ler_texto("Nome do laboratório")
        capacidade = self.ler_numero("Capacidade")
        
        equipamentos_str = self.ler_texto("Equipamentos (separados por vírgula, ou Enter para nenhum)")
        equipamentos = [eq.strip() for eq in equipamentos_str.split(",")] if equipamentos_str else []
        
        self.facade.get_gerente_lab().cadastrar_lab(lab_id, nome, capacidade, equipamentos)
    
    def listar_labs(self):
        """Lista todos os laboratórios"""
        labs = self.facade.get_gerente_lab().listar_labs()
        self.exibir_lista(labs, "LABORATÓRIOS CADASTRADOS")
    
    def atualizar_lab(self):
        """Atualiza um laboratório"""
        lab_id = self.ler_texto("ID do laboratório a ser atualizado")
        
        lab = self.facade.get_gerente_lab().buscar_lab(lab_id)
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
        
        self.facade.get_gerente_lab().atualizar_lab(lab_id, nome, capacidade, equipamentos)
    
    def remover_lab(self):
        """Remove um laboratório"""
        lab_id = self.ler_texto("ID do laboratório a ser removido")
        
        if self.confirmar_operacao(f"Tem certeza que deseja remover o laboratório '{lab_id}'?"):
            self.facade.get_gerente_lab().remover_lab(lab_id)
        else:
            self.exibir_sucesso("Operação cancelada.")
    
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
                break
            else:
                self.exibir_erro("Opção inválida!")
            
            self.aguardar_enter()
