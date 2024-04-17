
import time

from log.loggable import Loggable

PLAYER_MAX_TOKENS = 25
PLAYER_TOKEN_REPLENISH_RATE = 3 # per second

# You get: 50 tokens max per IP address with 15 replenished per second 25 tokens max per PlayerID with 3 replenished per second

class RateLimitManager(Loggable):
    def __init__(self) -> None:
        self.tokens: int = PLAYER_MAX_TOKENS
        self.last_check_time: int = int(time.time())
        
    def update_bucket(self) -> None:
        now = int(time.time())
        time_since_last_check = now - self.last_check_time
        replenished = time_since_last_check * PLAYER_TOKEN_REPLENISH_RATE
        self.tokens = max(25, self.tokens + replenished)
        self.check_time = now
    
    def consume(self, amount) -> None:
        self.update_bucket()
        if self._can_consume(amount):
            self.tokens -= amount
        else:
            self.critical("Can't consume!?")
    
    def _can_consume(self, amount) -> bool:
        return self.tokens - amount >= 0
    
    def tokens_available(self) -> int:
        return self.tokens
