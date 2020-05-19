"""CPU functionality."""

import sys
"""Set Instructions"""
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0,0,0,0,0,0,0,0]
        self.pc = 0
        pass

    def load(self, program = None):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        if program == None:
            program = [
                # From print8.ls8
                0b10000010, # LDI R0,8
                0b00000000,
                0b00001000,
                0b01000111, # PRN R0
                0b00000000,
                0b00000001, # HLT
            ]


        for instruction in program:

            instruction = instruction.replace(',', '')
            instruction = instruction.replace(' ', '')
            instruction = instruction.replace('\n', '')
            commentspot = instruction.find('#')
            if commentspot > -1:
                instruction = instruction[:commentspot]
            if len(instruction) > 0:
                print(type(instruction))
                self.ram[address] = int(instruction, 2)
                address += 1
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, data):
            self.ram[address] = data


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

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
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        run = True
        #self.pc = 0 #program counter

        while run == True:
            instruction = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if instruction == HLT:
                run = False
                print('halt!')
            elif instruction == LDI:
                #print(operand_a, operand_b)
                print('set value:', operand_b, 'to location:', operand_a)
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif instruction == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            else:
                print("Unknown Instruction:", instruction, "at address:", self.pc)
                sys.exit(1)

if __name__ == "__main__":
    file = sys.argv[1]
    print(file)
    prog = open(file, 'r')
    test = CPU()
    test.load(prog)
    test.run()
    #print([x for x in prog])
