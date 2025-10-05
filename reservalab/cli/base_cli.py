from datetime import datetime
from controller.facade_singleton import FacadeSingleton
from entity.user import User
from adapters.console_logger import ConsoleLogger
from adapters.logging_adapter import LoggingAdapter

class BaseCLI:
    """Classe base com funcionalidades comuns para todas as telas CLI"""
    
    def __init__(self, facade: FacadeSingleton, usuario_logado: User = None):
        self.facade = facade
        self.usuario_logado = usuario_logado
        # Usar Adapter para logging: combina console e arquivo
        self.console_logger = ConsoleLogger()
        self.file_logger = LoggingAdapter()
    
    def exibir_cabecalho(self, titulo: str):
        """Exibe cabeçalho formatado"""
        print("\n" + "=" * 30)
        print(f"    {titulo}")
        print("=" * 30)
    
    def exibir_secao(self, titulo: str):
        """Exibe seção formatada"""
        print(f"\n--- {titulo} ---")
    
    def ler_opcao(self, prompt: str = "Escolha uma opção: ") -> str:
        """Lê opção do usuário"""
        return input(f"\n{prompt}").strip()
    
    def ler_texto(self, prompt: str) -> str:
        """Lê texto do usuário"""
        return input(f"{prompt}: ").strip()
    
    def ler_numero(self, prompt: str) -> int:
        """Lê número do usuário com validação"""
        while True:
            try:
                return int(input(f"{prompt}: ").strip())
            except ValueError:
                print("Valor deve ser um número!")
    
    def ler_data_hora(self, prompt: str) -> datetime:
        """Lê data e hora do usuário com validação"""
        while True:
            try:
                data_str = input(f"{prompt} (formato: DD/MM/AAAA HH:MM): ").strip()
                return datetime.strptime(data_str, "%d/%m/%Y %H:%M")
            except ValueError:
                print("Formato de data inválido! Use DD/MM/AAAA HH:MM")
    
    def confirmar_operacao(self, mensagem: str) -> bool:
        """Solicita confirmação do usuário"""
        confirmacao = input(f"{mensagem} (s/N): ").strip().lower()
        return confirmacao == 's'
    
    def exibir_lista_vazia(self, item: str):
        """Exibe mensagem quando lista está vazia"""
        print(f"Nenhum {item} encontrado.")
    
    def exibir_lista(self, itens: list, titulo: str = None):
        """Exibe lista de itens formatada"""
        if titulo:
            self.exibir_secao(titulo)
        
        if not itens:
            self.exibir_lista_vazia(titulo.lower() if titulo else "item")
        else:
            for item in itens:
                print(f"  {item}")
    
    def exibir_erro(self, mensagem: str):
        """Exibe mensagem de erro"""
        self.console_logger.log_erro(mensagem)  # Original: print
        self.file_logger.log_erro(mensagem)     # Adapter: log em arquivo
    
    def exibir_sucesso(self, mensagem: str):
        """Exibe mensagem de sucesso"""
        self.console_logger.log_sucesso(mensagem)  # Original: print
        self.file_logger.log_sucesso(mensagem)     # Adapter: log em arquivo
    
    def aguardar_enter(self, mensagem: str = "Pressione Enter para continuar..."):
        """Aguarda usuário pressionar Enter"""
        input(f"\n{mensagem}")