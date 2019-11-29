import multiprocessing as mp
from joblib import Parallel, delayed
import seqentializer as sq
import time
import math
import numpy as np
from matplotlib import pyplot as plt

print("No. of Processors : ", mp.cpu_count())
# declare  n and array global ..
n = 10
array = np.random.randint(1, 10**6, n)
ci = np.zeros(n, dtype=int)


# sequential function ..
def sequential():
    c = np.zeros(n, dtype=int)
    sq.sequilizer(0)

    # step 1 start..
    for i in range(n):
        for j in range(n):
            if (array[i] > array[j] or (array[i] == array[j] and i > j)):
                c[i] = c[i] + 1
            else:
                c[i] = c[i] + 0

    print(array)
    print(c)
    # step 1 end ..

    # step 2 start ..
    final_array = np.zeros(n, dtype=int)
    for i in range(n):
        final_array[c[i]] = array[i]

    print(final_array)


# parallel function ..


def fun(i, j):
    if (array[i] > array[j] or (array[i] == array[j] and i > j)):
        ci[i] = ci[i] + 1
    else:
        ci[i] = ci[i] + 0


def givevalue(i, final_array):
    final_array[ci[i]] = array[i]



def parallel(array, n):
    # step 1 start
    Parallel(n_jobs=-1, require='sharedmem')(delayed(fun)(i, j)
                                            for i in range(n)
                                            for j in range(n))
    # step 1 end ..

    # step 2 start ..
    final_array = np.zeros(n, dtype=int)
    Parallel(n_jobs=-1, require='sharedmem')(delayed(givevalue)(i, final_array)
                                            for i in range(n))
    #step 2 finished ..
    print(ci)
    print(final_array)

    


if __name__ == '__main__':

    seq_start = time.time()
    sequential()
    seq_req = time.time() - seq_start
    print(seq_req)

    parallel_start = time.time()
    parallel(array, n)
    parallel_req = time.time() - parallel_start
    print(parallel_req)

    plt.bar([2],[seq_req*10],label="Seqential_CRCW",color='g',width=1)
    plt.bar([4],[parallel_req*10],label="Parallel_CRCW", color='r',width=.5)
    plt.legend()
    plt.xlabel('Diff. Algo.')
    plt.ylabel('Time(in 10*sec)')
    plt.title('Crcw Implementation')
    plt.show()
    
    print("speed_up : ",seq_req / parallel_req)
