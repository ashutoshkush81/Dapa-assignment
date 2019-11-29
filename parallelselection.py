import multiprocessing as mp
import math
N = mp.cpu_count()
kth_element = -1

def sequential_select(arr):
    temp = arr.copy()
    temp.sort()
    return temp[int(math.ceil(len(temp)/2))-1]


def parallel_select(arr, k, x):

    size_of_arr = len(arr)
    global kth_element

    # Step1 :
    if size_of_arr <= 4:
        temp = arr.copy()
        temp.sort()
        kth_element = temp[k-1]
        return
    else:
        # s is subdivided into s^(1-x) subsequences
        # of length s^x
        no_of_subseq = int(math.floor(size_of_arr**(1-x)))
        max_length = int(math.ceil(size_of_arr/no_of_subseq))

        M = []
        m = 0

        for i in range(no_of_subseq):
            # Find the median of this subsequence
            upto = min(size_of_arr-i*max_length,max_length)
            m = sequential_select(arr[i*max_length:upto+i*max_length])
            # print(m)
            M.append(m)

        # print(M)

        m = sequential_select(M)

        # Sequence S is divied into 3 subsequences:

        L = []
        E = []
        G = []

        for i in range(size_of_arr):
            if arr[i] < m:
                L.append(arr[i])
            elif arr[i] == m:
                E.append(arr[i])
            else:
                G.append(arr[i])


        # Step5

        if len(L) >= k:
            parallel_select(L, k, x)
        elif len(L)+len(E) >= k:
            # print("elif conditions : ", m)
            kth_element = m
            return 
        else:
            parallel_select(G, k-len(L)-len(E), x)
        # print("m ka value h" , m)

if __name__=="__main__":

    arr = [5,9,12,16,18,2,10,13,17,4,7,18,18,11,3,17,20,19,14,8,5,17,1,11,15, 10, 6]
    # print(sorted(arr))
    
    # arr = [1,2,4]
    parallel_select(arr, 21, 0.52204000)
    # print(parallel_select(arr, 21, 0.52204000))
    print(kth_element)