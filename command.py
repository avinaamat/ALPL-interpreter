from enum import Enum


class Command(Enum):
    LET = 0
    IF = 1
    JUMP = 2
    CALL = 3
    RETURN = 4
    PRINT = 5