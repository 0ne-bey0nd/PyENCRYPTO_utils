import threading
import timeit

global_var = 0
mutex = threading.Lock()


def f(iterations):
    global global_var
    for _ in range(iterations):
        global_var += 1


def f_with_lock(iterations):
    global global_var
    for _ in range(iterations):
        mutex.acquire()
        global_var += 1
        mutex.release()


def single_thread(iterations):
    f(iterations)
    f(iterations)


def multi_thread(iterations):
    t1 = threading.Thread(target=f, args=(iterations,))
    t2 = threading.Thread(target=f, args=(iterations,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()


def multi_thread_with_lock(iterations):
    t1 = threading.Thread(target=f_with_lock, args=(iterations,))
    t2 = threading.Thread(target=f_with_lock, args=(iterations,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == '__main__':
    iterations = 1000000
    print(timeit.timeit('single_thread(iterations)', globals=globals(), number=1))
    print(global_var)

    global_var = 0
    print(timeit.timeit('multi_thread(iterations)', globals=globals(), number=1))
    print(global_var)

    global_var = 0
    print(timeit.timeit('multi_thread_with_lock(iterations)', globals=globals(), number=1))
    print(global_var)
    
