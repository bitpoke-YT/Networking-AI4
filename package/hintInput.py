import threading

def input_with_hints(prompt, timeout, hints):
    input_value = None
    is_completed = False

    def target():
        nonlocal input_value, is_completed
        try:
            input_value = input(prompt)
            is_completed = True
        except EOFError:
            # Handle Ctrl+D (Unix) or Ctrl+Z (Windows)
            is_completed = True

    thread = threading.Thread(target=target)
    thread.start()

    for hint in hints:
        thread.join(timeout)
        if is_completed:
            break
        print(hint)

    # Wait indefinitely for the input to complete (after all hints shown)
    thread.join()

    return input_value

def three_input_with_hints(prompt, check, timeout, hints):
    input_value = None
    is_completed = False

    def target():
        nonlocal input_value, is_completed
        try:
            input_value = threeTriesInput(check)
            is_completed = True
        except EOFError:
            # Handle Ctrl+D (Unix) or Ctrl+Z (Windows)
            is_completed = True

    thread = threading.Thread(target=target)
    thread.start()

    for hint in hints:
        thread.join(timeout)
        if is_completed:
            break
        print(hint)

    # Wait indefinitely for the input to complete (after all hints shown)
    thread.join()

    return input_value

def threeTriesInput(requements):
    i = 0
    while i is not 3:
        if type(requements) is list:
            for requement in requements:
                try:
                    requement = str(requement)
                    requement = requement.lower()
                except Exception as x:
                    print("Could Not conver to string \n" + x)
                    return False
                put = input()
                if put.lower == requement.lower():
                    return True
                else:
                    print("Wrong anwer")
                i += 1
        else:
            try:
                requements = str(requements)
                requements = requements.lower()
            except Exception as x:
                print("Could Not conver to string \n" + x)
                return False
            put = input()
            if put.lower == requements.lower():
                return True
            else:
                print("Wrong anwer")
            i += 1
    return False

# Example usage
#hints = [
#     "Hint 1: Please enter your name.",
#     "Hint 2: We're still waiting!",
#     "Hint 3: You can type anything."
# ]

# user_input = input_with_hints("Enter your name: ", 5, hints)
# print("You entered:", user_input)