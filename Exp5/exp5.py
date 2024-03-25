def precedence(op):
    if op in ["+", "-"]:
        return 1
    if op in ["*", "/"]:
        return 2
    if op == "^":
        return 3
    return 0

def infic_to_postfix(exp):
    stack = []
    postfix = ""
    for char in exp:
        if char.isalnum():
            postfix += char
        elif char == "(":
            stack.append(char)
        elif char == ")":
            while stack and stack[-1] != "(":
                postfix += stack.pop()
            stack.pop()
        else:
            while stack and stack[-1] != "(" and precedence(stack[-1]) >= precedence(char):
                postfix += stack.pop()
            stack.append(char)
    while stack:
        postfix += stack.pop()
    return postfix

def is_op(char):
    return char in ["+", "-", "*", "/", "^", "="]

def display_quadruple(quadruples):
    print("Quadruple Representation:")
    print("{:<10} {:<10} {:<10} {:<10}".format("Operator", "Arg1", "Arg2", "Result"))
    for quadruple in quadruples:
        print("{:<10} {:<10} {:<10} {:<10}".format(*quadruple))

def postfix_to_quadruple(exp):
    stack = []
    quadruples = []
    temp = 1
    for char in exp:
        if char.isalnum():
            stack.append(char)
        elif is_op(char):
            op2 = stack.pop()
            op1 = stack.pop()
            temp_var = "T" + str(temp)
            temp += 1 
            quadruples.append([char, op1, op2, temp_var])
            stack.append(temp_var)
    return quadruples


def main():
    exp = input("Enter the infix expression: ")
    exp = infic_to_postfix(exp)
    print("Postfix expression:", exp)
    quadruples = postfix_to_quadruple(exp)
    display_quadruple(quadruples)


if __name__ == "__main__":
    main()
