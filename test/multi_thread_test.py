import threading
import timeit

global_var = 0
mutex = threading.Lock()

def f(tid):

    global global_var
    input(f"{tid} before add global_var: {global_var} before input")
    print(f"{tid} before add global_var: {global_var} after input")
    mutex.acquire()
    global_var += 1
    print(f"{tid} global_var: {global_var}")
    input("after add")
    mutex.release()


t1 = threading.Thread(target=f, args=(1,))
t2 = threading.Thread(target=f, args=(2,))

t1.start()
t2.start()

t1.join()
t2.join()

print(global_var)
