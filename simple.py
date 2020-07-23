PRINT_TIM = 0b01
HALT      = 0b10
PRINT_NUM = 0b11

memory = [
    PRINT_TIM,
    PRINT_TIM,
    PRINT_NUM,
    42,
    HALT,
]


def load_memory(file_name):
    pass

if len(sys.argv) < 2:
    pass


# register aka memory
registers = [0] * 8
registers[7] = 0xA



# Write a program to pull eah command out of memory and execute
# We can loop over it!
#

pc = 0
running = True

while running:
    command = memory[pc]

    if commmand == PRINT_TIM:
        print('Tim!')

    if command == HALT:
        running = False

    if command == PRINT_NUM:
        num_to_print = 2
        pass
