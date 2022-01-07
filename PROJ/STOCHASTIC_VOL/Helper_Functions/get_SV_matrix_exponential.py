# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# get_SV_matrix_exponential.m

    
@function
def get_SV_matrix_exponential(Q=None,dt=None,xi=None,v1=None,v2=None,fv=None,psi_J=None,m_0=None,N=None,*args,**kwargs):
    varargin = get_SV_matrix_exponential.varargin
    nargin = get_SV_matrix_exponential.nargin

    Qt=dot(dt,Q.T)
# get_SV_matrix_exponential.m:3
    EXP_A=ones(m_0,m_0,N)
# get_SV_matrix_exponential.m:4
    for j in arange(1,N).reshape(-1):
        EXP_A[arange(),arange(),j]=Qt + diag(dot(v1,xi(j)) - dot(v2,xi(j) ** 2) + dot(dt,psi_J(xi(j))))
# get_SV_matrix_exponential.m:6
    
    ### Define Toeplitz matrix (note the special structure:
### .. Before exponentiation it is: Toeplitz + skew-symmetric + zero diagonal
    Lambda_dxi=zeros(m_0,m_0)
# get_SV_matrix_exponential.m:11
    for k in arange(1,m_0).reshape(-1):
        for j in arange(k + 1,m_0).reshape(-1):
            Lambda_dxi[k,j]=fv(k) - fv(j)
# get_SV_matrix_exponential.m:15
            Lambda_dxi[j,k]=- Lambda_dxi(k,j)
# get_SV_matrix_exponential.m:16
    
    Lambda_dxi=exp(Lambda_dxi)
# get_SV_matrix_exponential.m:20
    
    EXP_A[arange(),arange(),1]=expm(EXP_A(arange(),arange(),1))
# get_SV_matrix_exponential.m:22
    
    ### (note: for n=1, Lambda is matrix of ones, so we start next loop at n=2)
    
    Lambda=copy(Lambda_dxi)
# get_SV_matrix_exponential.m:25
    
    for j in arange(2,N).reshape(-1):
        EXP_A[arange(),arange(),j]=multiply(expm(EXP_A(arange(),arange(),j)),Lambda)
# get_SV_matrix_exponential.m:28
        Lambda=multiply(Lambda,Lambda_dxi)
# get_SV_matrix_exponential.m:29
    
    return EXP_A
    
if __name__ == '__main__':
    pass
    