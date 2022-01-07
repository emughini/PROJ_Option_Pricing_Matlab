# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# get_RS_matrix_exponential.m

    
@function
def get_RS_matrix_exponential(Q=None,dt=None,xi=None,drifts=None,vols=None,psi_J=None,*args,**kwargs):
    varargin = get_RS_matrix_exponential.varargin
    nargin = get_RS_matrix_exponential.nargin

    N=length(xi)
# get_RS_matrix_exponential.m:2
    m_0=length(drifts)
# get_RS_matrix_exponential.m:3
    Qt=dot(dt,Q.T)
# get_RS_matrix_exponential.m:5
    EXP_A=ones(m_0,m_0,N)
# get_RS_matrix_exponential.m:6
    drifts=dot(dt,drifts)
# get_RS_matrix_exponential.m:8
    vols=dot((dot(0.5,dt)),vols ** 2)
# get_RS_matrix_exponential.m:9
    if nargin < 8:
        for j in arange(1,N).reshape(-1):
            EXP_A[arange(),arange(),j]=expm(Qt + diag(dot(drifts,xi(j)) - dot(vols,xi(j) ** 2)))
# get_RS_matrix_exponential.m:13
    else:
        for j in arange(1,N).reshape(-1):
            EXP_A[arange(),arange(),j]=expm(Qt + diag(dot(drifts,xi(j)) - dot(vols,xi(j) ** 2) + dot(dt,psi_J(xi(j)))))
# get_RS_matrix_exponential.m:17
    
    return EXP_A
    
if __name__ == '__main__':
    pass
    