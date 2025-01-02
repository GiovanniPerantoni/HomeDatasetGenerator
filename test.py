import time


N = 10000
TOTAL_TIME = 5
TIMESTEP = 0.1


def time0():
    start_time = time.time()
    l = [i**2 for i in range(N)]
    end_time = time.time()
    # while (end_time-start_time < 1):
    #    end_time = time.time()
    print(end_time - start_time)


def time1():
    current_time = 0
    start_time = time.time()
    while (abs(TOTAL_TIME-current_time) > 0.00001):
        l = [i**2 for i in range(N)]
        current_time += TIMESTEP
        #print("  ", current_time)
        time.sleep(TIMESTEP)
    end_time = time.time()
    print("Execution time:", end_time-start_time)


def time2():
    current_time = 0
    start_time = time.time()
    while (abs(TOTAL_TIME-current_time) > 0.00001):
        l = [i**2 for i in range(N)]
        current_time += TIMESTEP
        #print("  ", current_time)
        while (time.time()-start_time < current_time):
           pass
    end_time = time.time()
    print("Execution time:", end_time-start_time)


def time3():
    current_time = 0
    start_time = time.time()
    while (abs(TOTAL_TIME-current_time) > 0.00001):
        exec_start = time.time()
        l = [i**2 for i in range(N)]
        current_time += TIMESTEP
        #print("  ", current_time)
        elapsed_time = time.time() - exec_start
        sleep_time = max(0, TIMESTEP-elapsed_time)
        time.sleep(sleep_time)
    end_time = time.time()
    print("Execution time:", end_time-start_time)


def main():
    time0()
    print("Time 1")
    time1()
    print("Time 2")
    time2()
    print("Time 3")
    time3()


if __name__ == "__main__":
    main()
