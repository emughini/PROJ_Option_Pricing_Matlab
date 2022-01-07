# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# DoubleExpoRnd.m

    
@function
def DoubleExpoRnd(n=None,p_up=None,eta1=None,eta2=None,*args,**kwargs):
    varargin = DoubleExpoRnd.varargin
    nargin = DoubleExpoRnd.nargin

    # Returns a column vector of size n of DoubleExponetial Random Variables
# Note: To Generate an expo(mean=1/lambda), use E = -log(Unif)/lambda
# eta1 is expo param for up jumps, eta2 for down jumps
    
    Bern=rand(n,1) < p_up
# DoubleExpoRnd.m:6
    
    Unif=rand(n,1)
# DoubleExpoRnd.m:8
    DExpo=zeros(n,1)
# DoubleExpoRnd.m:9
    DExpo[Bern == 1]=- log(Unif(Bern == 1)) / eta1
# DoubleExpoRnd.m:10
    DExpo[Bern == 0]=log(Unif(Bern == 0)) / eta2
# DoubleExpoRnd.m:11
    
    return DExpo
    
if __name__ == '__main__':
    pass
    