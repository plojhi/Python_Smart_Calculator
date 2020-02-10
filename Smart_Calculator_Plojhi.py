"""
This Smart calculator calculates simple equations like 1 + 2; 1 --- 2 etc.
You can define your variables like a = 5
And then you can put the variable into the equation: a + 10
Calculator calculates even complex equations: 2 * ((10 - 3) / (5 - 2)) + 1, also with variables
Typing /help you will se short instructions for this program
Typing /exit you will stop the program
"""
# Determination if it is number
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# Determination of the sign - if it is + or -
def sign(operator):

    for i in range(len(operator)):
        if operator[i][0] == "-":
            if len(operator[i]) % 2 != 0:
                operator[i] = "-"
            else:
                operator[i] = "+"
        elif operator[i][0] == "+":
            operator[i] = "+"
        elif operator[i][0] == "*" and len(operator[i]) > 1:
            return "Invalid expression"
        elif operator[i][0] == "/" and len(operator[i]) > 1:
            return "Invalid expression"
    return operator


# From str input, where is =, to list
def make_list(numbers):
    word = ""
    expresions = []
    for i in numbers:
        if i == " " or i == "=":
            if word == "":
                continue
            else:
                expresions.append(word)
                word = ""
                continue
        else:
            word += i
    if word != "":
        expresions.append(word)
    return expresions

# Creation of a dict form the input, firstly list is made and then dict
def make_dict(numbers):
    number_list = make_list(numbers)
    global numbers_dict

    if len(number_list) == 2:
        dict_key = ""
        dict_value = ""
        for i in number_list[0]:
            if is_number(i) == True:
                print("Invalid identifier")
                pass

        dict_key = number_list[0]

        check_int = 0
        check_str = 0
        for i in number_list[1]:
            if is_number(i) == True:
                check_int +=1
            elif is_number(i) == False:
                check_str +=1

        if check_int > 0 and check_str == 0:
            dict_value = number_list[1]
            numbers_dict[dict_key] = int(dict_value)
            return numbers_dict
        elif check_int > 0 and check_str > 0:
            print("Invalid assignment")
            pass
        else:
            if number_list[1] in numbers_dict:
                numbers_dict[number_list[0]] = numbers_dict[number_list[1]]
                return numbers_dict
            else:
                print("Unknown variable123")
                pass
    else:
        print("Invalid assignment")
        pass

# Split the equation to the list
def equation_split(equation):
    splited = []
    number = ""
    over = 0
    for i in range(len(equation)):
        if over > 0:
            over -= 1
            continue
        elif equation[i].isdigit() == True:
            number = equation[i]
            for j in range(i+1,len(equation)):
                if equation[j].isdigit():
                    number += equation[j]
                    over += 1
                else:
                    splited.append(number)
                    number = ""
                    break
        elif equation[i] in operators:
            operator = equation[i]
            for j in range(i+1,len(equation)):
                if equation[j] == equation[i]:
                    operator += equation[j]
                    over +=1
                else:
                    splited.append(operator)
                    operator = ""
                    break
        elif equation[i] == " ":
            continue
        else:
            splited.append(equation[i])
    if number != "":
        splited.append(number)

    return splited

# from infix equation to postfix equation
def equation_list(numbers):

    equation = equation_split(numbers)
    equation = sign(equation)
    if equation == "Invalid expression":
        return "Invalid expression"

    # Control if is there the same amount of "(" and ")"
    left = equation.count("(")
    right = equation.count(")")
    if left != right:
        return "Invalid expression"

    equation_2 = []
    # if in the equation are keys form numbers_dict, replace them by their value
    for i in equation:
        if is_number(i) == False:
            if i in operators or i == "(" or i == ")":
                equation_2.append(i)
            elif i in numbers_dict:
                equation_2.append(numbers_dict[i])
            else:
                return "Unknown variable"
        elif is_number(i) == True:
            equation_2.append(int(i))



    operators_dict = {"+": 2, "-": 2, "*": 3, "/": 3, "(": 1}    # priority of operators
    operators_stack = []
    equation_stack = []

    for i in equation_2:
        if is_number(i):     # if i is digit push it to the equation list
            equation_stack.append(i)
        elif i == "(":      # if i is (, push it to the operators stack
                operators_stack.append(i)
        elif i == ")":      # if i is ), pop all operators until ")" from operators stack to equation list
            top_operator = operators_stack.pop()
            while top_operator != "(":
                equation_stack.append(top_operator)
                top_operator = operators_stack.pop()
        else:               # if operators stack isn't empty and operator i have higher or same value than top operator in equation stack
            while operators_stack != [] and operators_dict[operators_stack[-1]] >= operators_dict[i]:
                equation_stack.append(operators_stack.pop())
            operators_stack.append(i)
    # empty the operators stack
    while operators_stack != []:
        equation_stack.append(operators_stack.pop())

    return equation_stack

def make_result(numbers):

    sign_count = 0
    numbers = equation_list(numbers)

    if numbers == "Invalid expression":
        return "Invalid expression"
    elif numbers == "Unknown variable":
        return "Unknown variable"
    else:
        stack = []
        for i in numbers:
            if is_number(i):
                stack.append(i)
            elif i in operators:
                b = int(stack.pop())
                a = int(stack.pop())
                if i == "+":
                    result = a + b
                elif i == "-":
                    result = a - b
                elif i == "*":
                    result = a * b
                elif i == "/":
                    result = a / b
                stack.append(result)

        return result


# Main part of the program
numbers_dict = {}
operators = ["+", "-", "*", "/"]
while True:
    numbers = input()

    if "=" in numbers:
        make_dict(numbers)


    elif len(numbers.split()) == 1:

        if is_number(numbers) == True:
            print(int(numbers))
        else:
            if numbers[0] == "/":
                if numbers == "/exit":
                    print("Bye!")
                    break
                elif numbers == "/help":
                    print("""
The program calculates writen equation.
You can firstly define variables as a=5
and then use them in equation as a+10
Typing /exit you will stop the program
                        """)
                else:
                    print("Unknown command")
            elif numbers in numbers_dict:
                print(numbers_dict[numbers])
            elif any(operator in numbers for operator in operators):
                print(make_result(numbers))
            else:
                print("Unknown variable")

    elif any(operator in numbers for operator in operators):
        print(make_result(numbers))

    elif len(numbers) == 0:
        continue
    else:
        print("Invalid expression")
