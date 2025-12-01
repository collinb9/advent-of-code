import sys
import operator
import functools


def read_data(fpath):
    with open(fpath, "r") as fp:
        data = fp.read().splitlines()

    inner = []
    outer = []
    for item in data:
        if not item:
            outer.append(inner)
            inner = []
            continue
        inner.append(item)

    outer.append(inner)
    return outer


def adv(
    registers,
    literal_operand,
    combo_operand,
    instruction_pointer,
    register_value="A",
):
    # Div
    res = registers[register_value] // (2**combo_operand)
    registers[register_value] = res
    return instruction_pointer + 2, None


def bxl(
    registers,
    literal_operand,
    combo_operand,
    instruction_pointer,
    register_value="B",
):
    # Bitwise XOR
    res = registers[register_value] ^ literal_operand
    registers[register_value] = res
    return instruction_pointer + 2, None


def bst(
    registers,
    literal_operand,
    combo_operand,
    instruction_pointer,
    register_value="B",
):
    # Mod
    res = combo_operand % 8
    registers[register_value] = res
    return instruction_pointer + 2, None


def jnz(
    registers,
    literal_operand,
    combo_operand,
    instruction_pointer,
    register_value="A",
):
    # Return value to set instruction pointer to
    if registers[register_value] != 0:
        return literal_operand, None
    return instruction_pointer + 2, None


def bxc(
    registers,
    literal_operand,
    combo_operand,
    instruction_pointer,
    register_value_1="B",
    register_value_2="C",
):
    # Bitwise XOR
    res = registers[register_value_1] ^ registers[register_value_2]
    registers[register_value_1] = res
    return instruction_pointer + 2, None


def out(registers, literal_operand, combo_operand, instruction_pointer):
    # Mod
    res = combo_operand % 8
    return instruction_pointer + 2, res


def bdv(
    registers,
    literal_operand,
    combo_operand,
    instruction_pointer,
    register_value_in="A",
    register_value_out="B",
):
    # Div
    res = registers[register_value_in] // (2**combo_operand)
    registers[register_value_out] = res
    return instruction_pointer + 2, None


def cdv(
    registers,
    literal_operand,
    combo_operand,
    instruction_pointer,
    register_value_in="A",
    register_value_out="C",
):
    # Div
    res = registers[register_value_in] // (2**combo_operand)
    registers[register_value_out] = res
    return instruction_pointer + 2, None


def operands(registers, operand):
    if 0 <= operand <= 3:
        return operand
    if operand == 4:
        return registers["A"]
    if operand == 5:
        return registers["B"]
    if operand == 6:
        return registers["C"]
    return None


def simulate(program, register_a, register_b, register_c):
    registers = {}
    registers["A"] = register_a
    registers["B"] = register_b
    registers["C"] = register_c
    res = []
    instruction_pointer = 0
    instructions = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]
    res = []
    while True:
        # print(registers)
        # print("Instruction pointer before:", instruction_pointer)
        opcode = program[instruction_pointer]
        literal = program[instruction_pointer + 1]
        # if opcode == 5:
        #     print("out funtion at", instruction_pointer, "literal:", literal)
        # print(
        #     "Opcode:",
        #     opcode,
        #     "Literal:",
        #     literal,
        #     "Combo:",
        #     operands(registers, literal),
        # )
        instruction_pointer, output = instructions[opcode](
            registers,
            literal,
            operands(registers, literal),
            instruction_pointer,
        )
        # print("Instruction pointer after:", instruction_pointer)
        if output is not None:
            res.append(output)
        if instruction_pointer >= len(program):
            break
    return res


def main(fpath):
    data = read_data(fpath)
    # print(data)

    (register_a, register_b, register_c), program = data

    register_a = int(register_a.split()[-1])
    register_b = int(register_b.split()[-1])
    register_c = int(register_c.split()[-1])

    program = list(map(int, program[0].split()[-1].split(",")))
    print(program)

    ans1 = simulate(program, register_a, register_b, register_c)
    ans1 = ",".join(map(str, ans1))

    ### Part 2
    # Observations
    # 1. The values that the instruction pointer takes is independent of the values of the registers.
    #    This means that we know ahead of time when each (instruction, operand) pair will be reached.
    # 2. The only instruction which outputs a value is `out` (5). There is only 1 `out` instruction in the program.
    #    `out` has no other affect, apart from incrementing the instruction pointer by 2
    # 3. The value of the instruction pointer is cyclic. It iterates through all instructions and then back to the start.
    # 4. The instructions always end with a `out` (5) followed by a `jnz` (3). The program halts
    #    iff the value in the "A" register is 0. So we can work backwards, starting with A = 0

    """
    Test case (0,3),(5,4),(3,0)

    (0, 3) - A -> A // 8
    (5, 4) - Output A % 8
    (3, 0) - Jump instruction points - causes exit when A = 0, otherwise resets to start

    Work backwards

    * A % 8 = 0 => A = 8n for some n, say A = 8
    * A//8 = 8n, i.e. 8n <= (A / 8) < 8n + 1, so (8^2)n <= A < (8^2)n + 8
    * A % 8 = 3, so set A = (8^2)n + 3
    * A//8 = (8^2)n + 3, i.e. (8^2)n + 3 <= (A / 8) < (8^2)n + 4, so (8^3)n + 8 * 3 <= A < (8^3)n + 8 * 4
    * A % 8 = 4
    * A//8 = (8^3)n + 8 * 3 + 4, i.e. (8^4)n + 8^2 * 3 + 8 * 4 <= A < (8^4) + 8^2 * 3 + 8 * 5
    * A % 8 = 5
    * A//8 = (8^4) + 8^2 * 3 + 8 * 4 + 5, i.e. (8^5)n + 8^3 * 3 + 8^2 * 4 + 8 * 5 <= A < (8^5) + 8^3 * 3 + 8^2 * 4 + 8 * 6
    * A % 8 = 3
    * A//8 = (8^5) + 8^3 * 3 + 8^2 * 4 + 8 * 5 + 3, i.e. (8^6)n + 8^4 * 3 + 8^3 * 4 + 8^2 * 5 + 8 * 3 <= A < (8^6) + 8^4 * 3 + 8^3 * 4 + 8^2 * 5 + 8 * 4
    * A % 8 = 0
    * A//8 = (8^6) + 8^4 * 3 + 8^3 * 4 + 8^2 * 5 + 8 * 3, i.e. (8^7)n + 8^5 * 3 + 8^4 * 4 + 8^3 * 5 + 8^2 * 3 <= A < (8^7) + 8^5 * 3 + 8^4 * 4 + 8^3 * 5 + 8^2 * 3 + 8

    Note that in the above calculation, we can set n = 0, which gives us the range (117440, 117447)
    The actual answer is 117440

    Interestingly, adding the 8^7 terms recreates the initial program, plus an extra (0, 1)

    [adv, bxl, bst, jnz, bxc, out, bdv, cdv]
    Ok, now for the actual program
    (2,4),(1,1),(7,5),(4,0),(0,3),(1,6),(5,5),(3,0)
    (3, 0) - Jump instruction points - causes exit when A = 0, otherwise resets to start
    (5, 5) - Output B % 8
    (1, 6) - B -> B ^ 6
    (0, 3) - A -> A // 8
    (4,0) - B -> B ^ C
    (7,5) - C -> A // 2**B
    (1,1) - B -> B ^ 1
    (2, 4) - B -> A % 8

    Now the output depends on the value of B, it is a bit more complex
    * A = 0,  C = 0, B % 8 = 0 => B = 8n for some n, say B = 0 (n = 0 like the example)
    * A = 0, C = 0, B ^ 6 = 0, so set B = 6
    * B = 6, C = 0 A // 8 = 0, so set A = 0
    * A = 0, C = 0, B ^ C = 6, so set B = 6
    * A = 0, B = 6, C = 0, A // 2**B = 0 = C, so set A = 0
    * A = 0, C = 0, B ^ 1 = 6, so B = 7

    """
    value = 0
    for ii, xx in enumerate(program, 1):
        value += xx * (8**ii)

    ans2 = 0
    for attempt in range(value, value + 8):
        print("Attempt:", attempt)
        result = simulate(program, attempt, register_b, register_c)
        print(result)
        if result == program:
            ans2 = attempt
            break

    return ans1, ans2


if __name__ == "__main__":
    fpath = sys.argv[1]
    answer1, answer2 = main(fpath)
    print("Answer 1: ", answer1)
    print("Answer 2: ", answer2)
