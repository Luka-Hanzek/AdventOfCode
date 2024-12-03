from typing import Tuple, List
import re


class ExecutionError(Exception):
    pass


class _Memory:
    def __init__(self):
        self._instructions = []
        self._result = 0

    def clear(self):
        self.clear_instructions()
        self.clear_result()

    def clear_instructions(self):
        self._instructions.clear()

    def clear_result(self):
        self._result = 0

    def load_instructions(self, instructions):
        self._instructions.clear()
        self._instructions.extend(instructions)

    def fetch_instruction(self, loc: int) -> str:
        return self._instructions[loc]

    def instruction_count(self) -> int:
        return len(self._instructions)

    def store_result(self, result: int):
        self._result = result

    def get_result(self) -> int:
        return self._result


class _State:
    def __init__(self):
        self.__set_initial_state()

    def __set_initial_state(self):
        self.IP = 0
        self.do = True

        self.error = False
        self.error_message = ""

    def reset(self):
        self.__set_initial_state()

    def set_error(self, msg: str):
        self.error = True
        self.error_message = msg

    def clear_error(self):
        self.error = False
        self.error_message = ""


class Computer:
    def __init__(self):
        self._state = _State()
        self._memory = _Memory()

    def restart(self):
        self._state.reset()
        self._memory.clear()

    def load_program(self, instructions: List[str]):
        self._memory.load_instructions(instructions)

    def done(self) -> bool:
        return self._state.error or self._state.IP == self._memory.instruction_count()

    def clock(self) -> bool:
        """Returns True not done, False if done."""
        if self._state.error:
            return False

        if self.done():
            return False

        if self._memory.instruction_count() == 0:
            raise Exception("No program loaded.")

        instruction = self._memory.fetch_instruction(self._state.IP)
        pattern = "mul\([\d]+,[\d]+\)|do\(\)|don't\(\)"
        if not re.match(pattern, instruction):
            self._state.set_error(f"Invalid instruction encountered.\n"
                                  f"INSTRUCTION: {instruction}\n"
                                  f"Current IP: {self._state.IP}")
            return False
        if instruction == "do()":
            self._state.do = True
        elif instruction == "don't()":
            self._state.do = False
        else:
            if self._state.do:
                a, b = self._extract_operands(instruction)
                self._memory.store_result(self._memory.get_result() + a * b)

        self._state.IP += 1

        return not self.done()

    def get_result(self) -> int:
        return self._memory.get_result()

    def check_error(self) -> None:
        """Raises "ExecutionError" if computer is in error state."""
        if self._state.error:
            raise ExecutionError(self._state.error_message)

    def _extract_operands(self, instruction: str) -> Tuple[int, int] | None:
        match = re.match('mul\(([\d]+),([\d]+)\)', instruction)
        if not match:
            return None
        groups = match.groups()
        if len(groups) != 2:
            return None
        a, b = [int(x) for x in match.groups()]
        return a, b
