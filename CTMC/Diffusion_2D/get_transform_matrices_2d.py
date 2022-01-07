# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# get_transform_matrices_2d.m

    
@function
def get_transform_matrices_2d(R=None,method=None,*args,**kwargs):
    varargin = get_transform_matrices_2d.varargin
    nargin = get_transform_matrices_2d.nargin

    #UNTITLED4 Summary of this function goes here
#   Detailed explanation goes here
    if method == 1:
        # LDL Without the permutation
        L,D=ldl(R,nargout=2)
# get_transform_matrices_2d.m:6
        C=inv(L)
# get_transform_matrices_2d.m:7
        Cinv=copy(L)
# get_transform_matrices_2d.m:8
    else:
        if method == 2:
            # Eigen Decomp
            V,D=eig(R,nargout=2)
# get_transform_matrices_2d.m:12
            C=V.T
# get_transform_matrices_2d.m:13
            Cinv=copy(V)
# get_transform_matrices_2d.m:14
        else:
            if method == 3:
                # Cholesky Decomp (Special case of LDL, D=I)
                L=chol(R)
# get_transform_matrices_2d.m:18
                L=L.T
# get_transform_matrices_2d.m:19
                C=inv(L)
# get_transform_matrices_2d.m:20
                Cinv=copy(L)
# get_transform_matrices_2d.m:21
                D=eye(2,2)
# get_transform_matrices_2d.m:22
            else:
                if method == 4:
                    rho=R(1,2)
# get_transform_matrices_2d.m:25
                    L=concat([[1,0],[rho,1]])
# get_transform_matrices_2d.m:26
                    D=diag(concat([1,1 - rho ** 2]))
# get_transform_matrices_2d.m:27
                    C=concat([[1,0],[- rho,1]])
# get_transform_matrices_2d.m:28
                    Cinv=copy(L)
# get_transform_matrices_2d.m:30
    
    return L,D,C,Cinv
    
if __name__ == '__main__':
    pass
    