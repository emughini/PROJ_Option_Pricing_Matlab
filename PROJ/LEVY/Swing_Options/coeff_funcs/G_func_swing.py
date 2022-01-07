# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# G_func_swing.m

    
@function
def G_func_swing(x=None,K1=None,K2=None,K3=None,K4=None,S_0=None,*args,**kwargs):
    varargin = G_func_swing.varargin
    nargin = G_func_swing.nargin

    # K1,..,K4 are the kink points
# G(x) is a function of x = ln(S/S_0)
    w1=log(K1 / S_0)
# G_func_swing.m:4
    w2=log(K2 / S_0)
# G_func_swing.m:4
    w3=log(K3 / S_0)
# G_func_swing.m:4
    w4=log(K4 / S_0)
# G_func_swing.m:4
    y=zeros(size(x))
# G_func_swing.m:6
    y[x <= w1]=K2 - K1
# G_func_swing.m:8
    y[w1 < logical_and(x,x) <= w2]=K2 - dot(S_0,exp(x(w1 < logical_and(x,x) <= w2)))
# G_func_swing.m:9
    y[x < logical_and(w4,x) > w3]=dot(S_0,exp(x(x < logical_and(w4,x) > w3))) - K3
# G_func_swing.m:10
    y[x >= w4]=K4 - K3
# G_func_swing.m:11
    return y
    
if __name__ == '__main__':
    pass
    