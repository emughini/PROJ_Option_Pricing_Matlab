# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# gen_func.m

    
@function
def gen_func(b=None,dt=None,death_prob=None,*args,**kwargs):
    varargin = gen_func.varargin
    nargin = gen_func.nargin

    # Calculates the generating function
    if b == 0:
        gf=1
# gen_func.m:4
    else:
        es=exp(dot(dot(b,dt),(arange(1,length(death_prob)))))
# gen_func.m:6
        gf=dot(death_prob,es.T)
# gen_func.m:7
    
    return gf
    
if __name__ == '__main__':
    pass
    