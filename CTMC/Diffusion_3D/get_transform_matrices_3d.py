# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# get_transform_matrices_3d.m

    
@function
def get_transform_matrices_3d(R=None,method=None,*args,**kwargs):
    varargin = get_transform_matrices_3d.varargin
    nargin = get_transform_matrices_3d.nargin

    if method == 1:
        # LDL Without the permutation
        L,D=ldl(R,nargout=2)
# get_transform_matrices_3d.m:5
        C=inv(L)
# get_transform_matrices_3d.m:6
        Cinv=copy(L)
# get_transform_matrices_3d.m:7
    else:
        if method == 2:
            # Eigen Decomp
            V,D=eig(R,nargout=2)
# get_transform_matrices_3d.m:11
            C=V.T
# get_transform_matrices_3d.m:12
            Cinv=copy(V)
# get_transform_matrices_3d.m:13
        else:
            if method == 3:
                # Cholesky Decomp (Special case of LDL, D=I)
                L=chol(R)
# get_transform_matrices_3d.m:17
                L=L.T
# get_transform_matrices_3d.m:18
                C=inv(L)
# get_transform_matrices_3d.m:19
                Cinv=copy(L)
# get_transform_matrices_3d.m:20
                D=eye(2,2)
# get_transform_matrices_3d.m:21
            else:
                if method == 4:
                    rho12=R(1,2)
# get_transform_matrices_3d.m:24
                    rho23=R(2,3)
# get_transform_matrices_3d.m:25
                    rho13=R(1,3)
# get_transform_matrices_3d.m:26
                    gamma=(dot(rho12,rho13) - rho23) / (1 - rho12 ** 2)
# get_transform_matrices_3d.m:28
                    L=concat([[1,0,0],[rho12,1,0],[rho13,- gamma,1]])
# get_transform_matrices_3d.m:29
                    C=concat([[1,0,0],[- rho12,1,0],[(dot(- gamma,rho12) - rho13),gamma,1]])
# get_transform_matrices_3d.m:30
                    D=diag(concat([1,1 - rho12 ** 2,det(R) / (1 - rho12 ** 2)]))
# get_transform_matrices_3d.m:31
                    Cinv=copy(L)
# get_transform_matrices_3d.m:32
    
    return L,D,C,Cinv
    
if __name__ == '__main__':
    pass
    