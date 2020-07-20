"""
Computer emulator

Software that pretends to be hardward.

Turing Complete - if can solve any problem for which there is an algorithms.
"""

"""
Memory -- like a big array

"Index into the memory array" == "address" == "pointer"
#memory = [0] * 256 # Ram
"""

import sys

PRINT_ANDRONIK = 1
HALT = 2
SAVE_REG = 3            # SAVE_REG R1, 37 --> register[1] = 37
PRINT_REG = 4
ADD = 5           # PRINT_REG R1    --> print(register[1])

memory = [
    SAVE_REG,
    1,
    99,
    SAVE_REG,
    2,
    11,
    ADD,
    1,
    2,
    PRINT_REG,
    1,
    PRINT_ANDRONIK,
    HALT
]

register = [0] * 8 # 8 Registers, like varibales, R0, R1, R2,...R7

pc = 0 # Program Counter, index of the current instructions
running = True
while running:
    ir = memory[pc]
    
    if ir == PRINT_ANDRONIK:
        print("Andronik!")
        pc += 1
    
    elif ir == SAVE_REG:
        reg_num = memory[pc + 1]
        value = memory[pc + 2]
        register[reg_num] = value
        pc += 3
    
    elif ir == PRINT_REG:
        reg_num = memory[pc + 1]
        print(register[reg_num])
        pc += 2

    elif ir == ADD:
        req_num1 = memory[pc + 1]
        req_num2 = memory[pc + 2]
        register[req_num1] += register[req_num2]
        pc += 3
    
    elif ir == HALT:
        running = False
        pc += 1
    
    else:
        print(f"Unknown instructions {ir} at address")
        sys.exit(1)


