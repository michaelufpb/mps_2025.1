from abc import ABC, abstractmethod

class ILogger(ABC):
    """Interface para logging no sistema"""
    
    @abstractmethod
    def log_erro(self, mensagem: str):
        pass
    
    @abstractmethod
    def log_sucesso(self, mensagem: str):
        pass