# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# rnCHF_cont.m

    
@function
def rnCHF_cont(z=None,levyExponentRN=None,H=None,G=None,T=None,stateGrid=None,RNdrift=None,*args,**kwargs):
    varargin = rnCHF_cont.varargin
    nargin = rnCHF_cont.nargin

    numStates=length(stateGrid)
# rnCHF_cont.m:2
    numZ=length(z)
# rnCHF_cont.m:3
    ones_=ones(numStates,1)
# rnCHF_cont.m:5
    
    chf=zeros(numStates,numZ)
# rnCHF_cont.m:6
    
    
    for j in arange(1,numZ).reshape(-1):
        chf[arange(),j]=dot(dot(expm(dot(T,(G + diag(dot(levyExponentRN(z(j)),H))))),ones_),exp(dot(dot(1j,RNdrift),z(j))))
# rnCHF_cont.m:9
    
    
    return chf
    
if __name__ == '__main__':
    pass
    