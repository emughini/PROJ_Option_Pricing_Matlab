# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# binaryBracketIncreasing.m

    
@function
def binaryBracketIncreasing(A=None,num=None,*args,**kwargs):
    varargin = binaryBracketIncreasing.varargin
    nargin = binaryBracketIncreasing.nargin

    #--------------------------------------------------------------------------
# Syntax:       [index] = binarySearch(A, n, num);
#               
# Inputs:       A: Array (sorted, asc) that you want to search
#               num: Number you want to search in array A
#               
# Output:       index: Return position in A that A(index) <= num < A(index+1)
#                      or -1 if num < A(1)
#               if num > A(end), return size(A)
#               
# Description:  Use binary search to find left bracket for increasing function
#               
# Complexity:   O(1)    best-case performance
#               O(log_2 (n))    worst-case performance
#               O(1)      auxiliary space
#--------------------------------------------------------------------------
    n=length(A)
# binaryBracketIncreasing.m:18
    left=1
# binaryBracketIncreasing.m:19
    right=copy(n)
# binaryBracketIncreasing.m:20
    if num <= A:
        index=1
# binaryBracketIncreasing.m:23
    else:
        if num >= A:
            index=copy(n)
# binaryBracketIncreasing.m:25
        else:
            for i in arange(1,n).reshape(-1):
                mid=ceil((left + right) / 2)
# binaryBracketIncreasing.m:28
                if A(mid) <= num:
                    if A(mid + 1) > num:
                        index=copy(mid)
# binaryBracketIncreasing.m:32
                        break
                    else:
                        left=copy(mid)
# binaryBracketIncreasing.m:35
                else:
                    right=copy(mid)
# binaryBracketIncreasing.m:38
    