import multiprocessing as mp
from joblib import Parallel, delayed
import seqentializer as sq
import time
import math
import numpy as np
from parallelselection import make_selection_parallel

N = mp.cpu_count()
n = 16
x = math.log(n / N, n)
k = int(pow(2, math.ceil(1 / x)))
print("No. of cpu :",N)
print("No of element in arr : ",n)
print("Value of x : ",x)
print("Value of k :",k)

# Quick sort code .........................................................
def partition(arr, low, high):
    i = (low - 1)  # index of smaller element
    pivot = arr[high]  # pivot

    for j in range(low, high):

        if arr[j] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return (i + 1)

def quickSort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quickSort(arr, low, pi - 1)
        quickSort(arr, pi + 1, high)

# Quick sort code finished .......................................................

def sequential_select(arr,pos):
    temp = arr.copy()
    temp.sort() 
    return temp[pos]

def erewseqential(array):
    if len(array)<=k:
        quickSort(array,0,len(array)-1)
    else :
        # step - 1 start
        m = list() 
        for i in range(1,k):
            m.append(sequential_select(array,i*int((math.ceil(len(array)/k)))-1))
        print(m)

        # Step 2 start ..

        new_array = list()
        for i in range(k):
            new_array.append(0)
        another_array = list()
        for i in array :
            if i <=m[0]:
                another_array.append(i)
        new_array[0] = another_array

        # Step - 3 start
        for i in range(1,k-1):
            another_array = []
            for j in array :
                if j > m[i-1] and j<=m[i] :
                    another_array.append(j)
            new_array[i] = another_array

        # Step  - 4 start
        another_array = [] 
        for i in array :
            if i > m[k-2] :
                another_array.append(i)
        new_array[k-1] = another_array

        print(new_array)

        # Step - 5 start 

        for i in range(int(k/2)):
            erewseqential(new_array[i])

        for i in range(int(k/2),k):
            erewseqential(new_array[i])

        temp = 0
        for i in range(len(new_array)):
            for j in range(len(new_array[i])):
                array[temp] = new_array[i][j]
                temp+=1


def erewparallel(array):
    if len(array)<=k:
        quickSort(array,0,len(array)-1)
    else :
        # Step 1 start ..
        m = list()
        for i in range (1 , k):
            m.append(make_selection_parallel(array,i*(math.ceil(len(array)/k))- 1, x))
        print(m)

        # Step 2 start ..

        new_array = list()
        for i in range(k):
            new_array.append(0)
        another_array = list()
        for i in array :
            if i <=m[0]:
                another_array.append(i)
        new_array[0] = another_array

        # Step - 3 start
        for i in range(1,k-1):
            another_array = []
            for j in array :
                if j > m[i-1] and j<=m[i] :
                    another_array.append(j)
            new_array[i] = another_array

        # Step  - 4 start
        another_array = [] 
        for i in array :
            if i > m[k-2] :
                another_array.append(i)
        new_array[k-1] = another_array

        print(new_array)

        # Step - 5 start 

        Parallel(n_jobs= -1 , require='sharedmem')(delayed(erewparallel)(new_array[i]) for i in range(int(k/2)))

        # for i in range(int(k/2)):
        #     erewseqential(new_array[i])

        Parallel(n_jobs= -1 , require='sharedmem')(delayed(erewparallel)(new_array[i]) for i in range(int(k/2),k))

        # for i in range(int(k/2),k):
        #     erewseqential(new_array[i])
        temp = 0
        for i in range(len(new_array)):
            for j in range(len(new_array[i])):
                array[temp] = new_array[i][j]
                temp+=1




if __name__=='__main__':
    arr = np.random.randint(1, 10**6, n)
    array = arr.copy()
    print("Initial Array : ",array)
    
    sequential_start = time.time()
    sq.sequilizer(1)
    erewseqential(array)
    sequential_end = time.time() - sequential_start
    print(sequential_end)
    print(array)

    array = arr.copy()
    parallel_start = time.time()
    erewparallel(array)
    parallel_end = time.time() - parallel_start
    print(parallel_end)
    print(array)

    speed_up = sequential_end / parallel_end 
    print("speed_up : ", speed_up)





