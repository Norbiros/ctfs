import struct

# Opcodes as defined in the specification
OPCODES = {
    0: 'push', 1: 'pop', 3: 'swp', 4: 'sub', 5: 'add', 6: 'mul', 7: 'div',
    8: 'xor', 9: '<<', 10: '>>', 11: 'write', 12: 'read', 13: 'je', 14: 'jne',
    15: 'jlz', 16: 'call', 17: 'goto', 18: 'ret', 19: 'dup', 20: 'jempt', 21: 'jnempt',
    22: 'wmem', 23: 'pmem', 24: 'ctfx', 25: 'drop'
}

class VMParser:
    def __init__(self, binary_file):
        self.binary_file = binary_file
        self.instructions = []
        self.stack = []
        self.call_stack = []
        self.ctf_stack = []
        self.memory = {}
        self.ip = 0  # Instruction pointer

    def read_binary(self):
        """Read the binary file and parse it into instructions."""
        with open(self.binary_file, 'rb') as f:
            # Read the entire file
            data = f.read()

            while self.ip < len(data):
                opcode = data[self.ip]
                self.ip += 1
                args = self.parse_arguments(opcode, data)
                self.instructions.append((opcode, args))
                self.execute(opcode, args)

    def parse_arguments(self, opcode, data):
        """Parse arguments based on the opcode."""
        if opcode == 0:  # push
            # A push is followed by a 4-byte integer (little endian)
            value = struct.unpack('<i', data[self.ip:self.ip + 4])[0]
            self.ip += 4
            return [value]

        elif opcode in [1, 3, 4, 5, 6, 7, 8, 9, 10, 11]:  # pop, swp, sub, add, mul, div, xor, <<, >>
            # These opcodes pop two values from the stack
            return []

        elif opcode in [17, 18, 19, 20, 21]:  # goto, ret, dup, jempt, jnempt
            # These opcodes involve a single argument
            value = struct.unpack('<i', data[self.ip:self.ip + 4])[0]
            self.ip += 4
            return [value]

        elif opcode == 22:  # wmem
            # Write to memory (2 arguments: address, value)
            address, value = struct.unpack('<ii', data[self.ip:self.ip + 8])
            self.ip += 8
            return [address, value]

        elif opcode == 23:  # pmem
            # Read from memory (1 argument: address)
            address = struct.unpack('<i', data[self.ip:self.ip + 4])[0]
            self.ip += 4
            return [address]

        elif opcode == 24:  # ctfx
            # Push to CTF stack (1 argument)
            value = struct.unpack('<B', data[self.ip:self.ip + 1])[0]
            self.ip += 1
            return [value]

        else:
            return []

    def execute(self, opcode, args):
        """Execute the parsed opcode with its arguments."""
        if opcode == 0:  # push
            value = args[0]
            self.stack.append(value)
        elif opcode == 1:  # pop
            if self.stack:
                self.stack.pop()
            else:
                print("Error: Pop from an empty stack!")
                return
        elif opcode == 3:  # swp
            if len(self.stack) >= 2:
                self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
        elif opcode == 4:  # sub
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)
        elif opcode == 5:  # add
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
        elif opcode == 6:  # mul
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)
        elif opcode == 7:  # div
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                if b == 0:
                    print("Error: Division by zero!")
                    return
                self.stack.append(a // b)
        elif opcode == 8:  # xor
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a ^ b)
        elif opcode == 9:  # <<
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a << b)
        elif opcode == 10:  # >>
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a >> b)
        elif opcode == 11:  # write
            if self.stack:
                byte = self.stack.pop()
                print(f"Write: {byte}")
        elif opcode == 12:  # read
            value = int(input("Read a byte (0-255): "))
            self.stack.append(value)
        elif opcode == 17:  # goto
            address = args[0]
            self.ip = address
        elif opcode == 18:  # ret
            if self.call_stack:
                self.ip = self.call_stack.pop()
        elif opcode == 19:  # dup
            if self.stack:
                self.stack.append(self.stack[-1])
        elif opcode == 20:  # jempt
            if not self.stack:
                self.ip = args[0]
        elif opcode == 21:  # jnempt
            if self.stack:
                self.ip = args[0]
        elif opcode == 22:  # wmem
            address, value = args
            self.memory[address] = value
        elif opcode == 23:  # pmem
            address = args[0]
            if address in self.memory:
                self.stack.append(self.memory[address])
        elif opcode == 24:  # ctfx
            value = args[0]
            self.ctf_stack.append(value)
        elif opcode == 25:  # drop
            if self.stack:
                self.stack.pop()

    def print_state(self):
        """Print the current state of the VM."""
        print(f"IP: {self.ip}")
        print(f"Stack: {self.stack}")
        print(f"Call Stack: {self.call_stack}")
        print(f"CTF Stack: {self.ctf_stack}")
        print(f"Memory: {self.memory}")

# Example usage:
binary_file = "flag.bin"
parser = VMParser(binary_file)
parser.read_binary()
parser.print_state()
