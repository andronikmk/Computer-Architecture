"""
Computer emulator
Software that pretends to be hardware.

Turing Complete - if can solve any problem for which there is an algorithms.

Memory -- is like a big array.
Index into the memory array == 'address' == 'pointer'
"""
import sys

program_filename = sys.argv[1]
# print(program_filename)
# sys.exit()

PRINT_ANDRONIK = 1
HALT = 2
SAVE_REG = 3
PRINT_REG = 4
ADD = 5

CALL = 7
RET = 8

# stack pointer --> magic value or has two meanings
SP = 7

# memory = [
#     SAVE_REG,
#     1,
#     99,
#     SAVE_REG,
#     2,
#     11,
#     ADD,
#     1,
#     2,
#     PRINT_REG,
#     1,
#     PRINT_ANDRONIK,
#     HALT
# ]

memory = [0] * 256 # my memory
register = [0] * 8 # 8 Registers, like varibales, R0, R1, R2,...R7

# load program into memory
# from beej lecture
address = 0
with open(program_filename) as f:
    for line in f:
        line = line.split('#')
        line = line[0].strip()
        if line == '':
            continue
        
        memory[address] = int(line)
        address += 1
# sys.exit()
pc = 0 # Program Counter, index of the current instructions
fl = 0

register[7] = 0xff # Anding an integer with 0xFF leaves only the least significant byte.
running = True

while running:
    # instruction register
    ir = memory[pc]

    # print andronik
    if ir == 1:
        print("Andronik!")
        pc += 1
    
    # halt
    elif ir == 2:
        running = False
    
    elif ir == 3:
        reg_num = memory[pc + 1]
        value = memory[pc + 2]
        register[reg_num] = value
        pc += 3

    # print register
    elif ir == 4:
        reg_num = memory[pc + 1]
        print("Reg num", reg_num)
        print(register[reg_num])
        pc += 2

    # push
    elif ir == 5:
        # decrement the stack pointer
        register[SP] -= 1
        # copy the value to the given
        reg_num = memory[pc + 1]
        # the value we want to push onto the stack
        value = register[reg_num]
        # push to stack layer that the address points at
        # store in memory
        address_to_push_to = register[7] 
        memory[address_to_push_to] = value
        pc += 2

    # pop
    elif ir == 6:
        # get value from RAM
        address_to_pop_from = register[SP]
        value = memory[address_to_pop_from]

        # store in the given register
        req_num = memory[pc + 1]
        register[req_num] = value

        # increament sp
        register[SP] += 1

        pc += 2


    # elif ir == ADD:
    #     req_num1 = memory[pc + 1]
    #     req_num2 = memory[pc + 2]
    #     register[req_num1] += register[req_num2]
    #     pc += 3
    
    
    elif ir == CALL: # Call
        # get address in the next instruction
        return_addr = pc + 2
        
        # push onto stack
        register[SP] -= 1
        
        
        address_to_push_to = register[SP]
        memory[address_to_push_to] = return_addr
        # set the PC to subroutine address
        reg_num = memory[pc + 1]
        subroutine_addr = register[reg_num]

        pc = subroutine_addr   

    elif ir == RET:
        # get the return address from the top of the stack
        address_to_pop_from = register[SP]
        return_addr = memory[address_to_pop_from]
        register[SP] += 1

        # set the PC to the return address.
        pc = return_addr
    
    else:
        print(f"Unknown instructions {ir} at address")
        sys.exit(1)


# register[SP] = 0xf4

####### CALL - calls the subroutine ########################
