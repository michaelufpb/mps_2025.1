import logging
from adapters.ilogger import ILogger

class LoggingAdapter(ILogger):
    """Adapter que adapta a biblioteca logging para a interface ILogger"""
    
    def __init__(self):
        self.logger = logging.getLogger("ReservaLab")
        handler = logging.FileHandler("reservalab.log")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def log_erro(self, mensagem: str):
        self.logger.error(mensagem)
    
    def log_sucesso(self, mensagem: str):
        self.logger.info(mensagem)