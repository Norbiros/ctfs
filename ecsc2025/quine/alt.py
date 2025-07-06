from hashlib import blake2b

def operand_value(arg1, arg2):
    if arg2 > 7:
        raise Exception("operand_value panic")
    if arg2 == 0: return 0
    if arg2 == 1: return 1
    if arg2 == 2: return 2
    if arg2 == 3: return 3
    if arg2 == 4: return 4
    if arg2 == 5: return arg1[7]
    if arg2 == 6: return arg1[8]
    if arg2 == 7: return arg1[9]

def ashr(arg1, arg2):
    val = arg1[7]
    shift = operand_value(arg1, arg2)
    if shift < 0x40:
        return val >> (shift & 0x3f)
    else:
        raise Exception("ashr panic")

def f1(arg1, arg2):
    h = blake2b(digest_size=8)
    h.update(arg2.to_bytes(8, 'little'))
    h.update((0x2a).to_bytes(8, 'little'))
    return int.from_bytes(h.digest(), 'little') & 7

def f2(arg1, arg2):
    h = blake2b(digest_size=8)
    h.update(arg2.to_bytes(8, 'little'))
    h.update((0x45).to_bytes(8, 'little'))
    return int.from_bytes(h.digest(), 'little') & 7

def single_step(arg1):
    pc = arg1[6]
    instructions = arg1[10]

    if pc >= len(instructions):
        return arg1

    rax = instructions[pc]  # rax = (value, opcode)
    value, opcode = rax

    var_11 = 1
    if opcode == 0:
        arg1[7] = ashr(arg1, value)
    elif opcode == 1:
        arg1[8] = operand_value(arg1, value) & 7
    elif opcode == 2:
        arg1[9] = operand_value(arg1, value) & 7
    elif opcode == 3:
        arg1[8] = arg1[8] ^ operand_value(arg1, value)
    elif opcode == 4:
        arg1[8] = f1(arg1, operand_value(arg1, value))
    elif opcode == 5:
        arg1[9] = f2(arg1, operand_value(arg1, value))
    elif opcode == 6:
        if arg1[7] != 0:
            arg1[6] = value
            var_11 = 0
    elif opcode == 7:
        arg1[3].append(operand_value(arg1, value))
    else:
        raise Exception(f"Unknown opcode {opcode}")

    if var_11 & 1:
        rax_22 = arg1[6]
        # Check panic condition: rax_22 >= -1 is always true for int64, so original panic triggers always
        # In Rust code, likely meant to be rax_22 > some limit? We will fix to `rax_22 + 1` overflow detection:
        if rax_22 == (2**63 - 1):  # max int64
            raise Exception("panic const_add_overflow")
        arg1[6] = rax_22 + 1

    return arg1

def interpreter(program):
    # program: list of (value, opcode) tuples
    arg1 = [0]*10
    arg1[3] = []  # vector of outputs
    arg1[6] = 0   # program counter
    arg1.append(program)  # store program at arg1[10]

    while arg1[6] < len(program):
        arg1 = single_step(arg1)

    return arg1[3]

# Input data as list of (value, opcode)
input_data = [
    (2,5), (4,2), (3,7), (0,3), (5,3), (3,7), (2,5), (3,7),
    (7,6), (6,6), (0,0)
]

result = interpreter(input_data)
print(result)
