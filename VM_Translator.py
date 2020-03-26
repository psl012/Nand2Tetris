import os

# Global Variables
directory = "C:/Users/Paul/Documents/External IDEs/Nand2tetris/projects/07/MemoryAccess/StaticTest/StaticTest.vm"
fo = open(directory, "r")
result_fo = open(os.path.splitext(directory)[0] + ".asm", "w")
next_counter = 0


def main():
    global fo
    global result_fo
    lines = []
    result = []

    # Initialization
    result_fo.write("// Initialize\n")
    result_fo.write("@256\n")
    result_fo.write("D=A\n")       # D=A
    result_fo.write("@0\n")        # @0
    result_fo.write("M=D\n")       # M = D

    for line in fo:
        if line[0] == "/" and line[1] == "/" or len(line.strip()) == 0:
            nothing = 1
        else:
            translate(line.strip())
    result_fo.write("\n(END)\n")
    result_fo.write("@END\n")
    result_fo.write("0;JEQ\n")


def translate(line):
    global result_fo
    global next_counter

    line_parts = line.split()
    if line_parts[0] == "push":
        if line_parts[1] == "constant" and line_parts[2].isnumeric():
            i = line_parts[2]   # @i
            result_fo.write("\n// Push constant \n")
            result_fo.write("@" + i + "\n")
            result_fo.write("D=A\n")
            result_fo.write("@0\n")
            result_fo.write("A=M\n")
            result_fo.write("M=D\n")
            result_fo.write("@0\n")
            result_fo.write("M=M+1\n")

        elif line_parts[1] == "local" and line_parts[2].isnumeric():
            pusher("@1", line_parts[2])

        elif line_parts[1] == "argument" and line_parts[2].isnumeric():
            pusher("@2", line_parts[2])

        elif line_parts[1] == "this" and line_parts[2].isnumeric():
            pusher("@3", line_parts[2])

        elif line_parts[1] == "that" and line_parts[2].isnumeric():
            pusher("@4", line_parts[2])

        elif line_parts[1] == "temp" and line_parts[2].isnumeric():
            result_fo.write("\n// Push Temp \n")
            mem_location = str(int(line_parts[2]) + 5)
            result_fo.write("@" + mem_location + "\n")
            result_fo.write("D=M\n")
            result_fo.write("@0\n")
            result_fo.write("A=M\n")
            result_fo.write("M=D\n")
            result_fo.write("@0\n")
            result_fo.write("M=M+1\n")

        elif line_parts[1] == "pointer" and line_parts[2].isnumeric():
            result_fo.write("\n// Push Pointer \n")
            mem_location = str(int(line_parts[2]) + 3)
            result_fo.write("@" + mem_location + "\n")
            result_fo.write("D=M\n")
            result_fo.write("@0\n")
            result_fo.write("A=M\n")
            result_fo.write("M=D\n")
            result_fo.write("@0\n")
            result_fo.write("M=M+1\n")

        elif line_parts[1] == "static" and line_parts[2].isnumeric():
            result_fo.write("\n// Push Static \n")
            mem_location = "@Foo." + line_parts[2]
            result_fo.write(mem_location + "\n")
            result_fo.write("D=M\n")
            result_fo.write("@0\n")
            result_fo.write("A=M\n")
            result_fo.write("M=D\n")
            result_fo.write("@0\n")
            result_fo.write("M=M+1\n")

    elif line_parts[0] == "pop":
        if line_parts[1] == "local" and line_parts[2].isnumeric():
            popper("Local", "@1", line_parts[2])
        elif line_parts[1] == "argument" and line_parts[2].isnumeric():
            popper("Argument", "@2", line_parts[2])
        elif line_parts[1] == "this" and line_parts[2].isnumeric():
            popper("this", "@3", line_parts[2])
        elif line_parts[1] == "that" and line_parts[2].isnumeric():
            popper("this", "@4", line_parts[2])
        elif line_parts[1] == "temp" and line_parts[2].isnumeric():
            result_fo.write("\n// Pop Temp\n")
            result_fo.write("@0\n")
            result_fo.write("M=M-1\n")
            result_fo.write("A=M\n")
            result_fo.write("D=M\n")
            temp_location = str(int(line_parts[2]) + 5)
            result_fo.write("@" + temp_location + "\n")
            result_fo.write("M=D\n")

        elif line_parts[1] == "pointer" and line_parts[2].isnumeric():
            result_fo.write("\n// Pop Pointer\n")
            result_fo.write("@0\n")
            result_fo.write("M=M-1\n")
            result_fo.write("A=M\n")
            result_fo.write("D=M\n")
            mem_location = str(int(line_parts[2]) + 3)
            result_fo.write("@" + mem_location + "\n")
            result_fo.write("M=D\n")

        elif line_parts[1] == "static" and line_parts[2].isnumeric():
            result_fo.write("\n// Pop Static\n")
            mem_location = "@Foo." + line_parts[2]
            result_fo.write("@0\n")
            result_fo.write("M=M-1\n")
            result_fo.write("A=M\n")
            result_fo.write("D=M\n")
            result_fo.write(mem_location + "\n")
            result_fo.write("M=D\n")

    elif line_parts[0] == "add":
        result_fo.write("\n// Add \n")
        result_fo.write("@0\n")
        result_fo.write("A=M-1\n")
        result_fo.write("D=M\n")
        result_fo.write("A=A-1\n")
        result_fo.write("M=M+D\n")
        result_fo.write("D=A\n")
        result_fo.write("@0\n")
        result_fo.write("M=D+1\n")

    elif line_parts[0] == "sub":
        result_fo.write("\n// Sub \n")
        result_fo.write("@0\n")
        result_fo.write("A=M-1\n")
        result_fo.write("D=M\n")
        result_fo.write("A=A-1\n")
        result_fo.write("M=M-D\n")
        result_fo.write("D=A\n")
        result_fo.write("@0\n")
        result_fo.write("M=D+1\n")

    elif line_parts[0] == "neg":
        result_fo.write("\n// Neg \n")
        result_fo.write("@0\n")
        result_fo.write("A=M-1\n")
        result_fo.write("D=M\n")
        result_fo.write("M=M-D\n")
        result_fo.write("M=M-D\n")

    elif line_parts[0] == "eq":
        result_fo.write("\n// Eq \n")
        result_fo.write("@0\n")
        result_fo.write("A=M-1\n")
        result_fo.write("D=M\n")
        result_fo.write("A=A-1\n")
        result_fo.write("M=M-D\n")
        result_fo.write("D=M\n")
        result_fo.write("@EQUAL" + str(next_counter) + "\n")
        result_fo.write("D;JEQ\n")
        result_fo.write("\n")

        result_fo.write("@0\n")         # the two constants are not equal
        result_fo.write("M=M-1\n")
        result_fo.write("A=M-1\n")
        result_fo.write("M=0\n")
        result_fo.write("\n")
        result_fo.write("@NEXT" + str(next_counter) + "\n")
        result_fo.write("0;JEQ\n")

        result_fo.write("\n// If two constants are equal")
        result_fo.write("\n(EQUAL" + str(next_counter) + ")\n")    # the two constants are equal
        result_fo.write("@0\n")
        result_fo.write("M=M-1\n")
        result_fo.write("A=M-1\n")
        result_fo.write("M=-1\n")

        result_fo.write("\n(NEXT" + str(next_counter) + ")")
        next_counter = next_counter + 1

    elif line_parts[0] == "gt":
        result_fo.write("\n// Gt \n")
        result_fo.write("@0\n")
        result_fo.write("A=M-1\n")
        result_fo.write("D=M\n")
        result_fo.write("A=A-1\n")
        result_fo.write("M=M-D\n")
        result_fo.write("D=M\n")
        result_fo.write("@GREATER" + str(next_counter) + "\n")
        result_fo.write("D;JGT\n")
        result_fo.write("\n")

        result_fo.write("@0\n")         # the two constants are not equal
        result_fo.write("M=M-1\n")
        result_fo.write("A=M-1\n")
        result_fo.write("M=0\n")
        result_fo.write("\n")
        result_fo.write("@NEXT" + str(next_counter) + "\n")
        result_fo.write("0;JEQ\n")

        result_fo.write("\n// If x > y")
        result_fo.write("\n(GREATER" + str(next_counter) + ")\n")    # the two constants are equal
        result_fo.write("@0\n")
        result_fo.write("M=M-1\n")
        result_fo.write("A=M-1\n")
        result_fo.write("M=-1\n")

        result_fo.write("\n(NEXT" + str(next_counter) + ")")
        next_counter = next_counter + 1

    elif line_parts[0] == "lt":
        result_fo.write("\n// Lt \n")
        result_fo.write("@0\n")
        result_fo.write("A=M-1\n")
        result_fo.write("D=M\n")
        result_fo.write("A=A-1\n")
        result_fo.write("M=M-D\n")
        result_fo.write("D=M\n")
        result_fo.write("@LESSER" + str(next_counter) + "\n")
        result_fo.write("D;JLT\n")
        result_fo.write("\n")

        result_fo.write("@0\n")         # the x is not < than y
        result_fo.write("M=M-1\n")
        result_fo.write("A=M-1\n")
        result_fo.write("M=0\n")
        result_fo.write("\n")
        result_fo.write("@NEXT" + str(next_counter) + "\n")
        result_fo.write("0;JEQ\n")

        result_fo.write("\n// If x > y")
        result_fo.write("\n(LESSER" + str(next_counter) + ")\n")    # the two constants are equal
        result_fo.write("@0\n")
        result_fo.write("M=M-1\n")
        result_fo.write("A=M-1\n")
        result_fo.write("M=-1\n")

        result_fo.write("\n(NEXT" + str(next_counter) + ")")
        next_counter = next_counter + 1

    elif line_parts[0] == "and":
        result_fo.write("\n// AND\n")
        result_fo.write("@0\n")
        result_fo.write("M=M-1\n")
        result_fo.write("A=M\n")
        result_fo.write("D=M\n")
        result_fo.write("A=A-1\n")
        result_fo.write("M=D&M\n")

    elif line_parts[0] == "or":
        result_fo.write("\n// OR\n")
        result_fo.write("@0\n")
        result_fo.write("M=M-1\n")
        result_fo.write("A=M\n")
        result_fo.write("D=M\n")
        result_fo.write("A=A-1\n")
        result_fo.write("M=D|M\n")

    elif line_parts[0] == "not":
        result_fo.write("\n // Not\n")
        result_fo.write("@0\n")
        result_fo.write("A=M-1\n")
        result_fo.write("M=!M\n")


def pusher(mem_number, line):
    result_fo.write("\n// Push Local \n")
    result_fo.write("@" + line + "\n")
    result_fo.write("D=A\n")
    result_fo.write(mem_number + "\n")  # the memorylocation
    result_fo.write("A=M+D\n")
    result_fo.write("D=M\n")
    result_fo.write("@0\n")
    result_fo.write("A=M\n")
    result_fo.write("M=D\n")
    result_fo.write("@0\n")
    result_fo.write("M=M+1\n")


def popper(mem_type_name, mem_number, mem_storage):
    result_fo.write("\n// Pop " + mem_type_name + "\n")
    result_fo.write("@" + mem_storage + "\n")  # local "M"
    result_fo.write("D=A\n")
    result_fo.write(mem_number + "\n")   # @1
    result_fo.write("M=M+D\n")  # RAM[1 + local M]

    result_fo.write("@0\n")
    result_fo.write("M=M-1\n")
    result_fo.write("A=M\n")
    result_fo.write("D=M\n")
    result_fo.write(mem_number + "\n")  # @1
    result_fo.write("A=M\n")
    result_fo.write("M=D\n")

    result_fo.write("@" + mem_storage + "\n")
    result_fo.write("D=A\n")
    result_fo.write(mem_number + "\n")
    result_fo.write("M=M-D\n")


main()
