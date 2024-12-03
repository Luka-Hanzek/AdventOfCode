from typing import Tuple, List
import re
import computer

def read_input() -> str:
    with open('input.txt', 'r') as f:
        return f.read()


def extract_instructions(memory: str, syntax: str) -> List[str]:
    return re.findall(syntax, memory)


computer = computer.Computer()
memory = read_input()

program = extract_instructions(memory, syntax='mul\([\d]+,[\d]+\)')
program.append("asdsd")
computer.load_program(program)
while computer.clock():
    pass
else:
    computer.check_error()

print(f'Part 1: {computer.get_result()}')

program = extract_instructions(memory, syntax="mul\([\d]+,[\d]+\)|do\(\)|don't\(\)")
computer.restart()
computer.load_program(program)
while computer.clock():
    pass
else:
    computer.check_error()

print(f'Part 2: {computer.get_result()}')
