from enum import Enum

class Status(Enum):
    ATTENDANCE = "online"
    CHECKOUT = "offline"
    AWAY = "away"
    RETURN = "return" 