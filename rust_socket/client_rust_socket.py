
from rustplus import RustSocket

from rust_socket.rate_limit_manager import RateLimitManager

class ClientRustSocket:
    def __init__(self, steam_id: int, socket: RustSocket) -> None:
        self._steam_id: int = steam_id
        self._socket: RustSocket = socket
        self.rate_limit_manager: RateLimitManager = RateLimitManager()
        
    @property
    def socket(self) -> RustSocket:
        return self._socket
    
    @property
    def steam_id(self) -> int:
        return self._steam_id
    
    def tokens_available(self) -> int:
        return self.rate_limit_manager.tokens_available()
