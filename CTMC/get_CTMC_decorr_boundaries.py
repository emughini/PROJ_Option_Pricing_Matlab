# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# get_CTMC_decorr_boundaries.m

    
@function
def get_CTMC_decorr_boundaries(sigmas=None,C=None,T=None,num_devs=None,sigma_dc=None,num_devs_Y=None,*args,**kwargs):
    varargin = get_CTMC_decorr_boundaries.varargin
    nargin = get_CTMC_decorr_boundaries.nargin

    Ls_dc_0=zeros(1,length(sigmas))
# get_CTMC_decorr_boundaries.m:3
    Rs_dc_0=zeros(1,length(sigmas))
# get_CTMC_decorr_boundaries.m:4
    if nargin < 6:
        num_devs_Y=copy(num_devs)
# get_CTMC_decorr_boundaries.m:7
    
    Ls_dc=zeros(size(sigmas))
# get_CTMC_decorr_boundaries.m:10
    Rs_dc=zeros(size(sigmas))
# get_CTMC_decorr_boundaries.m:11
    for i in arange(1,length(sigmas)).reshape(-1):
        Ls_dc[i]=min(concat([Ls_dc_0(i),Rs_dc_0(i),dot(dot(- num_devs_Y,sigma_dc(i)),sqrt(T))]))
# get_CTMC_decorr_boundaries.m:13
        Rs_dc[i]=max(concat([Ls_dc_0(i),Rs_dc_0(i),dot(dot(num_devs_Y,sigma_dc(i)),sqrt(T))]))
# get_CTMC_decorr_boundaries.m:14
    
    return Ls_dc,Rs_dc
    
if __name__ == '__main__':
    pass
    