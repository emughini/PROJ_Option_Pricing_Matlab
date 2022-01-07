# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# MixedNormalRnd.m

    
@function
def MixedNormalRnd(n=None,p=None,a1=None,b1=None,a2=None,b2=None,*args,**kwargs):
    varargin = MixedNormalRnd.varargin
    nargin = MixedNormalRnd.nargin

    # Returns a column vector of size n of MixedNormal Random Variables
#   Detailed explanation goes here
    
    Bern=rand(n,1) < p
# MixedNormalRnd.m:5
    
    Norm=randn(n,1)
# MixedNormalRnd.m:6
    MNorm=zeros(n,1)
# MixedNormalRnd.m:8
    MNorm[Bern == 1]=a1 + dot(b1,Norm(Bern == 1))
# MixedNormalRnd.m:9
    MNorm[Bern == 0]=a2 + dot(b2,Norm(Bern == 0))
# MixedNormalRnd.m:10
    return MNorm
    
if __name__ == '__main__':
    pass
    