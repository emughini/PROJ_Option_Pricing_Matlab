# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# rnCHF_disc.m

    
@function
def rnCHF_disc(z=None,levyExponentRN=None,H=None,G=None,T=None,n=None,stateGrid=None,RNdrift=None,*args,**kwargs):
    varargin = rnCHF_disc.varargin
    nargin = rnCHF_disc.nargin

    # k_0 is the bracketing index: grid(k_0) <= v0 < grid(k_0+1)
    #Returns the chf with is linear interpolation of the two bracketing chfs
    dt=T / n
# rnCHF_disc.m:4
    
    P=expm(dot(dt,G))
# rnCHF_disc.m:5
    numStates=length(stateGrid)
# rnCHF_disc.m:7
    numZ=length(z)
# rnCHF_disc.m:8
    ones_=ones(numStates,1)
# rnCHF_disc.m:10
    
    chf=zeros(numStates,numZ)
# rnCHF_disc.m:11
    
    for j in arange(1,numZ).reshape(-1):
        E=diag(exp(dot(dot(levyExponentRN(z(j)),H),dt)))
# rnCHF_disc.m:14
        chf[arange(),j]=dot(dot(E,ones_),exp(dot(dot(1j,RNdrift),z(j))))
# rnCHF_disc.m:15
        EP=dot(E,P)
# rnCHF_disc.m:16
        for k in arange(1,n).reshape(-1):
            chf[arange(),j]=dot(EP,chf(arange(),j))
# rnCHF_disc.m:18
    
    
    return chf
    
if __name__ == '__main__':
    pass
    