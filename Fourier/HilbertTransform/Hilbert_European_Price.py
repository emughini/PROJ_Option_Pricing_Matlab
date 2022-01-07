# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Hilbert_European_Price.m

    
@function
def Hilbert_European_Price(h=None,N=None,r=None,q=None,T=None,S_0=None,W=None,call=None,rnCHF=None,*args,**kwargs):
    varargin = Hilbert_European_Price.varargin
    nargin = Hilbert_European_Price.nargin

    # h = step size
# N = budget
    gridL=arange(- N / 2,- 1)
# Hilbert_European_Price.m:4
    gridR=- fliplr(gridL)
# Hilbert_European_Price.m:4
    g=lambda z=None: multiply(exp(dot(dot(- 1j,z),log(W / S_0))),(multiply(S_0,rnCHF(z - 1j)) - dot(W,rnCHF(z))))
# Hilbert_European_Price.m:5
    H=sum(multiply(g(dot(h,gridL)),(cos(dot(pi,gridL)) - 1)) / gridL + multiply(g(dot(h,gridR)),(cos(dot(pi,gridR)) - 1)) / gridR) / pi
# Hilbert_European_Price.m:6
    # Call option price
    price=dot(0.5,real(dot(S_0,exp(dot(- q,T))) - dot(W,exp(dot(- r,T))) + dot(dot(1j,exp(dot(- r,T))),H)))
# Hilbert_European_Price.m:9
    if call != 1:
        price=price - (dot(S_0,exp(dot(- q,T))) - dot(W,exp(dot(- r,T))))
# Hilbert_European_Price.m:13
    
    return price
    
if __name__ == '__main__':
    pass
    