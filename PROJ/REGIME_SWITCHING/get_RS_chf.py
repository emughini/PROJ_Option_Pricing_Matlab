# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# get_RS_chf.m

    
@function
def get_RS_chf(Q=None,dt=None,xi=None,drifts=None,vols=None,initial_state=None,*args,**kwargs):
    varargin = get_RS_chf.varargin
    nargin = get_RS_chf.nargin

    # Risk-Neutral Chf of Regime Switching model with given initial_state
    N=length(xi)
# get_RS_chf.m:3
    Qt=dot(dt,Q)
# get_RS_chf.m:5
    chf=zeros(size(xi))
# get_RS_chf.m:6
    vols=dot(0.5,vols ** 2)
# get_RS_chf.m:8
    drifts=dot(dot(dt,(drifts - vols)),1j)
# get_RS_chf.m:9
    # TODO: vectorize
    for j in arange(1,N).reshape(-1):
        temp=expm(Qt + diag(dot(drifts,xi(j)) - dot(vols,xi(j) ** 2)))
# get_RS_chf.m:13
        chf[j]=sum(temp(arange(),initial_state))
# get_RS_chf.m:14
    
    return chf
    
if __name__ == '__main__':
    pass
    