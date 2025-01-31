## Functions can have inputs/functionality/output
def add(n1, n2):
    return n1 + n2

def subtract(n1, n2):
    return n1 - n2

def multiply(n1, n2):
    return n1 * n2

def divide(n1, n2):
    return n1 / n2

##Functions are first-class objects, can be passed around as arguments e.g. int/string/float etc.

def calculate(calc_function, n1, n2):
    return calc_function(n1, n2)

result = calculate(add, 2, 3)
print(result)

##Functions can be nested in other functions

def outer_function():
    print("I'm outer")

    def nested_function():
        print("I'm inner")

    nested_function()

outer_function()

## Functions can be returned from other functions
def outer_function():
    print("I'm outer")

    def nested_function():
        print("I'm inner")

    return nested_function

inner_function = outer_function()
inner_function


## Simple Python Decorator Functions
import time

def delay_decorator(function):
    def wrapper_function():
        time.sleep(2)
        #Do something before
        function()
        function()
        #Do something after
    return wrapper_function

@delay_decorator
def say_hello():
    print("Hello")

#With the @ syntactic sugar
@delay_decorator
def say_bye():
    print("Bye")

#Without the @ syntactic sugar
def say_greeting():
    print("How are you?")
decorated_function = delay_decorator(say_greeting)
decorated_function()


# --------------------------------------- Function Composition (Combining Functions) -----------------------------------
def combine_functions(func1, func2):
    def composed_function(*args, **kwargs):  # Handle arguments generically
        func1(*args, **kwargs)
        func2(*args, **kwargs)
    return composed_function

composed_func = combine_functions(func1, func2)  # Combine func1 and func2

@my_decorator  # Apply the decorator to the composed function
def my_combined_function():
    composed_func() # Call the combined function

my_combined_function()


# --------------------------------------------- Passing Arguments to Decorators ----------------------------------------
def my_decorator(message):  # Decorator takes an argument
    def decorator(func):  # Inner decorator function
        def wrapper():
            print(message)  # Use the argument
            func()
        return wrapper
    return decorator

@my_decorator("Applying to func1")
def func1():
    print("Function 1")

@my_decorator("Applying to func2")
def func2():
    print("Function 2")

func1()
func2()


class User:
    def __init__(self, name):
        self.name = name
        self.is_logged_in = False

def is_authenticated_decorator(function):
    def wrapper(*args, **kwargs):
        if args[0].is_logged_in:
            function(args[0])
    return wrapper

@is_authenticated_decorator
def create_blog_post(user):
    print(f"This is {user.name}'s new blog post.")

new_user = User("angela")
new_user.is_logged_in = True
create_blog_post(new_user)