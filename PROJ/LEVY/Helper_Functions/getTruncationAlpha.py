# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# getTruncationAlpha.m

    
@function
def getTruncationAlpha(T=None,L1=None,modelInput=None,model=None,*args,**kwargs):
    varargin = getTruncationAlpha.varargin
    nargin = getTruncationAlpha.nargin

    # model: Levy models (BSM, CGMY, NIG, MJD, Kou)
#        Affine models (Heston)
    
    if model == 6:
        alpha=dot(L1,sqrt(abs(modelInput.c2) + sqrt(abs(modelInput.c4))))
# getTruncationAlpha.m:6
    else:
        alpha=dot(L1,sqrt(abs(dot(modelInput.c2,T)) + sqrt(abs(dot(modelInput.c4,T)))))
# getTruncationAlpha.m:8
    
    return alpha
    
if __name__ == '__main__':
    pass
    