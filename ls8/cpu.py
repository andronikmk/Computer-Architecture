"""CPU functionality."""

import sys

# stack pointer
SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0                 # program counter
        self.register = [0] * 8     # register
        self.ram = [0] * 256        # memory
        self.fl =  0b00000000       # 0 flags binary switch value
        self.register[7] = 0xF4     # 
        self.sp = self.register[7]  # stack pointer

    def load(self, program_filename):
        """Load a program into memory."""

        address = 0

        # open instruction and read line by line
        # like in beej's lecture code.
        with open(program_filename) as f:
            address = 0
            for line in f:
                line = line.split('#')
                line = line[0].strip()
                if line == '':
                    continue
                # print("##########",line, hex(int(line, 2)))
                value = int(line, 2)
                # memory[address] like in Beej's code
                self.ram[address] = value
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        # ADD
        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        # SUB
        elif op == "SUB":
            self.register[reg_a] -= self.register[reg_b]
        # MULTIPLICATION
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
        # Compare the values in two registers.
        elif op == "CMP":
            # If they are equal, set the Equal `E` flag to 1, otherwise set it to 0.
            if self.register[reg_a] == self.register[reg_b]:
                # EQ == 0b00000001
                self.fl = 0b00000001
            # If registerA is less than registerB, set the Less-than `L` flag to 1, otherwise set it to 0.
            elif self.register[reg_a] > self.register[reg_b]:
                # GT == 0b00000010
                self.fl = 0b00000010
            #  `L` Less-than: during a `CMP`, set to 1 if registerA is less than registerB,
            elif self.register[reg_a] < self.register[reg_b]:
                # LT = 0b00000100
                self.fl = 0b00000100
        else:
            raise Exception("Unsupported ALU operation")

    # `ram_read()` should accept the address to read and return the value stored there.
    def ram_read(self, address):
        return self.ram[address]

    # `ram_write()` should accept a value to write, and the address to write it to.
    def ram_write(self, value, address):
        self.ram[address] = value
    
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        
        while running:
            # instruction register
            # getting program from memory
            # ir = memory[pc]
            self.trace()
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # HALT
            if ir == 0b00000001:
                running = False
                self.pc += 1

            # LDI
            # This instruction sets a specified register to a specified value.
            elif ir == 0b10000010:
                self.register[operand_a] = operand_b
                self.pc += 3

            # PRN
            elif ir == 0b01000111:
                print(self.register[operand_a])
                self.pc += 2

            # MUL
            elif ir == 0b10100010:
                # result = self.register[operand_a] * self.register[operand_b]
                # self.register[operand_a] = result
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

            # ADD
            elif ir == 0b10100000:
                # result1 = self.register[operand_a] + self.register[operand_b]
                # self.register[operand_a] = result1
                self.alu("ADD", operand_a, operand_b) 
                self.pc += 3
            
            # PUSH
            elif ir == 0b01000101:
                # decrement the stack pointer
                self.register[7] -= 1
                 # copy the value to the given
                reg_slot_number = operand_a
                # the value we want to push onto the stack
                value = self.register[reg_slot_number]
                # push to stack layer that the address points at
                # store in memory
                address_to_push_to = self.register[7]
                # memory[address_to_push_to] = value
                self.ram[address_to_push_to] = value
                self.pc += 2

            # POP
            elif ir == 0b01000110:
                # get value from RAM
                # reg_slot_number = operand_a
                # value = memory[address_to_pop_from]
                # value = self.ram[reg_slot_number]

                address_to_pop_from = self.register[7]

                value = self.ram[address_to_pop_from]
                self.register[operand_a] = value
                # self.ram[address_to_pop_from] = value
                # increament sp
                # self.sp += 1
                self.register[7] += 1
                # beej referenced a two bit operation?
                self.pc += 2

            # CMP
            elif ir == 0b10100111:
                self.alu("CMP", operand_a, operand_b)
                self.pc += 3

            # JMP
            # Jump to the address stored in the given register.
            elif ir == 0b01010100:
                break
                self.pc = self.register[operand_a]
            
            # JEQ
            # If `equal` flag is set (true), jump to the address stored in the given register.
            elif ir == 0b01010101:
                # EQ = 0b00000001
                if (self.fl & 0b00000001) == 1:
                    self.pc = self.register[operand_a]
                else:
                    self.pc += 2
            
            #  JNE = 0b01010110
            elif ir == 0b01010110:
                # print(self.pc)
                # If `E` flag is clear (false, 0), jump to the address stored in the given register.
                # EQ = 0b00000001
                if (self.fl & 0b00000001) == 0:
                    self.pc = self.register[operand_a]
                else:
                    self.pc += 2
            
            # CALL
            elif ir == 0b01010000:
                
                # get address in the next instruction
                return_addr = self.pc + 2
                
                # push onto stack
                self.register[operand_a] -= 1
                
                address_to_push_to = self.register[operand_a]
                self.ram[address_to_push_to] = return_addr
                # set the PC to subroutine address
                reg_num = self.ram[self.pc + 1]
                subroutine_addr = self.register[reg_num]
                self.pc = subroutine_addr

            # RET
            elif ir == 0b00010001:
                # get the return address from the top of the stack
                address_to_pop_from = self.register[operand_a]
                return_addr = self.ram[address_to_pop_from]
                self.register[operand_a] += 1
                # set the PC to the return address.
                self.pc = return_addr

            else:
                print(f"Unknown instructions {ir} at address")
                self.trace()
                sys.exit(1)


            