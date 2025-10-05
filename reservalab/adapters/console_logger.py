from adapters.ilogger import ILogger

class ConsoleLogger(ILogger):
    """Implementação original de logging no console"""
    
    def log_erro(self, mensagem: str):
        print(f"Erro: {mensagem}")
    
    def log_sucesso(self, mensagem: str):
        print(f"{mensagem}")