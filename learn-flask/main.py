import time

current_time = time.time()
print(current_time)


def speed_calc_decorator(function):
    def timer_function():
        global current_time
        function()
        run_time = time.time()
        print(run_time - current_time)

    return timer_function



@speed_calc_decorator
def fast_function():
    for i in range(1000000):
        i * i
fast_function()

@speed_calc_decorator
def slow_function():
    for i in range(10000000):
        i * i
slow_function()

