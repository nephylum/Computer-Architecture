"""CPU functionality."""

import sys
"""Set Instructions"""
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
ADD = 0b10100000
SUB = 0b10100001
DIV = 0b10100011
PUSH = 0b01000101
POP = 0b01000110
SP = 7
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0,0,0,0,0,0,0,0]
        self.pc = 0
        self.reg[SP] = 0xF4
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
                # print(type(instruction))
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
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
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
                print('Store:', operand_b, 'in', operand_a)
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif instruction == SUB:
                print('Subtract:', self.reg[operand_a], 'and', self.reg[operand_b])
                self.alu('SUB', operand_a, operand_b)
                print('Result:', self.reg[operand_a])
                self.pc += 3
            elif instruction == ADD:
                print('Add:', self.reg[operand_a], 'and', self.reg[operand_b])
                self.alu('ADD', operand_a, operand_b)
                print('Result:', self.reg[operand_a])
                self.pc += 3
            elif instruction == MUL:
                print('Multiply:',self.reg[operand_a], "and", self.reg[operand_b])
                self.alu('MUL', operand_a, operand_b)
                print('Result:', self.reg[operand_a])
                self.pc += 3
            elif instruction == DIV:
                print('Divide:', self.reg[operand_a], 'by', self.reg[operand_b])
                self.alu('DIV', operand_a, operand_b)
                print('Result:', self.reg[operand_a])
                self.pc += 3
            elif instruction == PRN:
                print("Print", self.reg[operand_a])
                self.pc += 2
            elif instruction == PUSH:
                if self.reg[SP]!=0x00:

                    self.reg[SP] -= 1
                    self.ram_write(self.reg[SP], self.reg[operand_a])
                    print('Push:', self.reg[operand_a], 'to', self.reg[SP])
                else:
                    print("stack full!")
                self.pc += 2
            elif instruction == POP:
                if self.reg[SP] == 0xF4:
                    print("can't pop without a stack!")
                else:
                    print('Pop:', self.ram_read(self.reg[SP]), 'from', self.reg[SP])
                    self.reg[operand_a] = self.ram_read(self.reg[SP])
                    self.reg[SP] +=1
                self.pc +=2
            else:
                print("Unknown Instruction:", instruction, "at address:", self.pc)
                sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Incorrect number of arguments. Only one file path accepted')
        sys.exit(1)
    try:
        file = sys.argv[1]
        print(file)
    except:
        Print(sys.argv[1], 'File not found!')
        sys.exit(1)

    prog = open(file, 'r')
    test = CPU()
    test.load(prog)
    test.run()
    #print([x for x in prog])
