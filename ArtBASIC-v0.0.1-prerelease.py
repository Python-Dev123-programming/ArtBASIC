# ArtBASIC Programming Language

variables = {}

def PRINT(basic_line):
    
    print_command = "PRINT"
    if basic_line.startswith(print_command):
        string = basic_line[6:].strip()
        if (string.startswith("'") and string.endswith("'") or string.startswith('"') and string.endswith('"')):
            print(string[1:-1])
        
        elif not string.strip():
            print(f"Syntax Error in '{basic_line}': No string or empty string!")
        
        elif string in variables:
            print(variables[string])

        elif any(op in string for op in ["+", "-", "*", "/", "**", "%"]):
            try:
                result = eval(string, {}, variables)
                print(result)
            except ZeroDivisionError:
                print(f"Math Error in '{basic_line}': Division by zero is undefined!")
            except TypeError:
                print(f"Syntax Error in '{basic_line}': Unable to evaluate string with integer!")
            except SyntaxError:
                print(f"Syntax Error in '{basic_line}': Unknown syntax!")
            except NameError:
                print(f"Syntax Error in '{basic_line}': Unable to evaluate expression.")
                
        else:
            print(f"Syntax Error in '{basic_line}': Please, wrap the letter or word with quotes!")

def INPUT(basic_line):
    input_command = "INPUT"
    if basic_line.startswith(input_command):
        custom_input = basic_line[6:]
        if (custom_input.startswith("'") and custom_input.endswith("'")) or (custom_input.startswith('"') and custom_input.endswith('"')):
            custom_input = custom_input[1:-1]
            input_line = input(custom_input)
            print(f"'{input_line}'")
        elif not custom_input.strip():
            print(f"Syntax Error in '{basic_line}': No string or empty string!")

def LET(basic_line):
    
    try:
        let_command = "LET"
        if basic_line.startswith(let_command):
            variable = basic_line[4:].split(" = ")
            
            var_name = variable[0].strip()
            var_value = variable[1].strip()
            
            if (var_name.startswith("'") and var_name.endswith("'") or var_name.startswith('"') and var_name.endswith('"')):
                print(f"Syntax Error in '{basic_line}': Cannot create variable with quotes!")
            
            elif var_name.isdigit():
                print(f"Name Error in '{basic_line}': Cannot create variable name with integer!")
            
            if not var_name.isidentifier():
                print(f"Name Error: '{var_name}' is not a valid identifier!")
            
            forbidden_chars = set(" !@#$%^&*()-+=[]{}`~;:'\",.<>/?|\\")
            if any(char in forbidden_chars for char in var_name):
                print(f"Name Error in '{basic_line}': Cannot create variable name with these symbols!")

        try:
            if any(op in var_value for op in ["+", "-", "*", "/", "**", "%"]):
                var_value = eval(var_value, {}, variables)
        except ZeroDivisionError:
            print(f"Math Error in '{basic_line}': Division by zero is undefined!")
        except TypeError:
            print(f"Syntax Error in '{basic_line}': Cannot to evaluate string with integer!")
        except SyntaxError:
            print(f"Syntax Error in '{basic_line}': Unknown syntax!")
        except NameError:
            print(f"Syntax Error in '{basic_line}': Unable to evaluate expression.")
    except IndexError:
        print(f"Syntax Error in '{basic_line}': Variable creation not correct!")
    
    try:
        try:
            variables[var_name] = int(var_value)
        except UnboundLocalError:
            print(f"Syntax Error in '{basic_line}': Variable should have a value!")    
    except ValueError:
        try:
            variables[var_name] = var_value
        except UnboundLocalError:
            print(f"Syntax Error in '{basic_line}': Variable should have a value!")

def DRAW(basic_line):
    draw_command = "DRAW "
    end_character = ":"
    
    if basic_line.startswith(draw_command) and basic_line.endswith(end_character):
        shape = basic_line[5:-1]
        import turtle
        
        t = turtle.Turtle()
        
        if shape == "rectangle":
            for _ in range(2):
                t.forward(100)
                t.right(90)
                t.forward(50)
                t.right(90)
                
        elif shape == "circle":
            t.circle(50)

        elif shape == "triangle":
            for _ in range(3):
                t.forward(100)
                t.left(120)
                
        else:
            print("Drawing Error: Unknown shape!")

def COMMENT(basic_line):
    comment_command = "# "
    if basic_line.startswith(comment_command):
        pass

def FOREVER(basic_line):
    forever_command = "FOREVER"
    if basic_line == f"{forever_command}:":
        while True:
            forever_basic_line = input("...    ")
            
            if forever_basic_line == "END":
                return main()
            
            if forever_basic_line.startswith("PRINT"):
                while True:
                    PRINT(forever_basic_line)
            elif forever_basic_line.startswith("LET"):
                LET(forever_basic_line)
            elif forever_basic_line.startswith("INPUT"):
                while True:
                    INPUT(forever_basic_line)
            elif forever_basic_line.startswith("DRAW ") and basic_line.endswith(":"):
                while True:
                    DRAW(forever_basic_line)
            elif forever_basic_line.startswith("# "):
                COMMENT(forever_basic_line)
            else:
                print(f"Command Error in '{forever_basic_line}': Unknown Command!")
                
def FUNCTION(basic_line):
    function_command = "FUNCTION "
    end_character = ":"
    
    if basic_line.startswith(function_command) and basic_line.endswith(end_character):
        function_name = basic_line[9:-1].strip()
        
        forbidden_chars = set(" !@#$%^&*()-+=[]{}`~;:'\",.<>/?|\\")
        if any(char in forbidden_chars for char in function_name):
            print(f"Name Error in '{basic_line}': Cannot create function name with these symbols!")
            return

        while True:
            function_line = input("...    ")
            
            try:
                with open(f"{function_name}.artbasic", "a") as function_file:            
                    function_file.writelines(f"{function_line}\n")
                    if function_line == "END":
                        return main()
            except FileNotFoundError:
                print("File or Function Creation Error: Cannot create a file or function without a name!")
                return main()
                
def RUN(basic_line):
    run_command = "RUN "
    end_character = ":"
    
    if basic_line.startswith(run_command) and basic_line.endswith(end_character):
        file_name = basic_line[4:-1]
        try:
            with open(f"{file_name}.artbasic", "r") as file:
                lines = file.readlines()
                
                for line in lines:
                    if line.startswith("PRINT"):
                        PRINT(line)
                    elif line.startswith("LET"):
                        LET(line)
                    elif line.startswith("INPUT"):
                        INPUT(line)
                    elif line.startswith("DRAW ") and basic_line.endswith(":"):
                        DRAW(line)
                    elif line.startswith("FOREVER:"):
                        FOREVER(line)
                    elif line.startswith("FUNCTION ") and basic_line.endswith(":"):
                        FUNCTION(line)
        except FileNotFoundError:
            print("File or Function Not Found Error: File or function does not exist!")

def main():
    while True:        
        basic_line = input(f"> ")
        
        if basic_line.startswith("PRINT"):
            PRINT(basic_line)
        elif basic_line.startswith("LET"):
            LET(basic_line)
        elif basic_line.startswith("INPUT"):
            INPUT(basic_line)
        elif basic_line.startswith("DRAW ") and basic_line.endswith(":"):
            DRAW(basic_line)
        elif basic_line.startswith("# "):
            COMMENT(basic_line)
        elif basic_line.startswith("FOREVER:"):
            FOREVER(basic_line)
        elif basic_line.startswith("FUNCTION ") and basic_line.endswith(":"):
            FUNCTION(basic_line)
        elif basic_line.startswith("RUN ") and basic_line.endswith(":"):
            RUN(basic_line)
            
        else:
            print(f"Command Error in '{basic_line}': Unknown Command!")

if __name__ == '__main__':
    main()