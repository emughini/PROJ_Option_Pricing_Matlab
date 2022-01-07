# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# decorrelate.m

    
@function
def decorrelate(sigmas=None,drifts=None,C=None,D=None,*args,**kwargs):
    varargin = decorrelate.varargin
    nargin = decorrelate.nargin

    # Applies the decorrelation transform
# C = C matrix, D = Diagonal Matrix
    n=length(sigmas)
# decorrelate.m:4
    drift_dc=zeros(n,1)
# decorrelate.m:5
    sigma_dc=zeros(n,1)
# decorrelate.m:6
    for i in arange(1,n).reshape(-1):
        sigma_dc[i]=sqrt(D(i,i))
# decorrelate.m:9
        sum_terms=0
# decorrelate.m:10
        for j in arange(1,n).reshape(-1):
            s=sigmas(j)
# decorrelate.m:12
            sum_terms=sum_terms + dot((drifts(j) - s ** 2 / 2),C(i,j)) / s
# decorrelate.m:13
        drift_dc[i]=sum_terms
# decorrelate.m:15
    
    return drift_dc,sigma_dc
    
if __name__ == '__main__':
    pass
    