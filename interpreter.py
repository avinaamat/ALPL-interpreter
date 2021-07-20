from typing import List
from typing import Dict
from command import Command


def is_label(line: str) -> bool:
    return line[-1] == ":"


def is_call(line: str) -> bool:
    first_word: str = line.split(" ")[0]
    if Command[first_word].value == 3:
        return True
    else:
        return False


def is_return(line: str) -> bool:
    first_word: str = line.split(" ")[0]
    if Command[first_word].value == 4:
        return True
    else:
        return False


def is_print(line: str) -> bool:
    first_word: str = line.split(" ")[0]
    if Command[first_word].value == 5:
        return True
    else:
        return False


def is_jump(line: str) -> bool:
    first_word: str = line.split(" ")[0]
    if Command[first_word].value == 2:
        return True
    else:
        return False


def is_let(line: str) -> bool:
    first_word: str = line.split(" ")[0]
    if Command[first_word].value == 0:
        return True
    else:
        return False


def is_if(line: str) -> bool:
    first_word: str = line.split(" ")[0]
    if Command[first_word].value == 1:
        return True
    else:
        return False


def check_line(word: str):
    if word in Command._member_names_:
        return
    else:
        raise Exception("unknown command was given: {}".format(word))


def check_line_integrity(line, max, min=None):
    # check line integrity:
    if len(line.split(' ')) > max:
        raise Exception("unknown command was given: {}".format(line))
    if min is not None:
        if len(line.split(' ')) < min:
            raise Exception("unknown command was given: {}".format(line))


class Interpreter:
    def __init__(self, path: str):
        self.path: str = path
        self.file: List[str] = []
        self.labels: Dict[str, int] = {}
        self.registers = [None] * 10
        self.load_data()
        self.parse()

    # Read in file #and setup any input
    def load_data(self) -> None:
        self.file = [line.rstrip('\n').strip() for line in open(self.path)]

    # Iterate through code and pick out any labels and their locations
    def parse(self) -> None:
        for i in range(len(self.file)):
            print()
            if self.file[i] == '\n' or self.file[i] == '':
                pass
            elif is_label(self.file[i]):
                label = self.file[i][:-1]
                if label in self.labels:
                    raise Exception("Label {} already defined".format(label))
                else:
                    self.labels[label] = i

    # Iterate over the file, terminating when current_line reach the end of the file
    def run(self) -> None:
        current_line = 0
        return_list = []
        # Handle everything
        while True:
            if current_line >= len(self.file):
                break
            line: str = self.file[current_line]
            if line == '\n' or line == '' or is_label(line):
                check_line_integrity(line, 1)
                current_line += 1
                continue
            check_line(line.split(" ")[0])
            if is_call(line) or is_jump(line):
                check_line_integrity(line, 2)
                if is_call(line):
                    return_list.append(current_line)
                second_word: str = line.split(" ")[1]
                current_line = self.get_label(second_word)
            elif is_return(line):
                check_line_integrity(line, 1)
                if len(return_list) > 0:
                    current_line = return_list.pop(-1)
                else:
                    raise Exception("RETURN was issued but nowhere to return from")
            elif is_print(line):
                check_line_integrity(line, 2)
                print_arg = self.get_val(line.split(" ")[-1])
                print(print_arg)
            elif is_let(line):
                check_line_integrity(line, 6, 4)
                line_list = line.split(" ")
                if line_list[2] != ':=':
                    raise Exception("command {} is undefined".format(line))
                target_register = int(line_list[1][-1])
                self.check_reg(target_register, check_for_none=False)
                first_arg = self.get_val(line_list[3])
                if len(line_list) > 4:
                    second_arg = self.get_val(line_list[-1])
                    # check what type of operand to execute:
                    if line_list[4] == '+':
                        self.registers[target_register] = first_arg + second_arg
                    elif line_list[4] == '*':
                        self.registers[target_register] = first_arg * second_arg
                    else:
                        raise Exception("operation {} is undefined".format(line_list[4]))
                else:
                    self.registers[target_register] = first_arg
            elif is_if(line):
                check_line_integrity(line, 5, 5)
                line_list = line.split(" ")
                first_arg = self.get_val(line_list[1])
                second_arg = self.get_val(line_list[3])
                jump_occurred = False
                if line_list[2] == '=':
                    if first_arg == second_arg:
                        jump_occurred = True
                elif line_list[2] == '>':
                    if first_arg > second_arg:
                        jump_occurred = True
                elif line_list[2] == '<':
                    if first_arg == second_arg:
                        jump_occurred = True
                else:
                    raise Exception("operation {} is undefined".format(line_list[2]))
                if jump_occurred:
                    current_line = self.get_label(line_list[-1])
            else:
                raise Exception("command {} is undefined".format(line))
            current_line += 1

    # check a register if it's within the acceptable range and if it has a usable value other then None
    def check_reg(self, reg: int, check_for_none=True):
        if 0 <= reg <= 9:
            if check_for_none:
                if self.registers[reg] is None:
                    raise Exception(
                        "can't perform an operation on the requested register R{} since it's hasn't been initializes".format(
                            reg))
            return
        else:
            raise Exception("can't access the requested register R{}".format(reg))

    def get_val(self, arg):
        if arg[0] == 'R':
            if len(arg) == 2:
                reg_num = int(arg[-1])
                self.check_reg(reg_num)
                return self.registers[reg_num]
            else:
                raise Exception("can't access the requested register {}".format(arg))
        else:
            for s in arg:
                if '0' > s or s > '9':
                    raise Exception("the Value given here is wrong {}".format(arg))
            return int(arg)

    def get_label(self, label):
        if label in self.labels:
            return self.labels[label]
        else:
            raise Exception("Label {} is undefined".format(label))
