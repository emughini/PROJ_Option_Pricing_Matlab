# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# price_3d_ctmc.m

    
@function
def price_3d_ctmc(S_0s=None,T=None,r=None,R=None,sigmas=None,qs=None,params=None,contractParams=None,M=None,*args,**kwargs):
    varargin = price_3d_ctmc.varargin
    nargin = price_3d_ctmc.nargin

    if nargin < 9:
        M=1
# price_3d_ctmc.m:4
    
    dt=T / M
# price_3d_ctmc.m:6
    contract=contractParams.contract
# price_3d_ctmc.m:8
    if contract == 1:
        dt=1
# price_3d_ctmc.m:11
        M=1
# price_3d_ctmc.m:11
    
    method=4
# price_3d_ctmc.m:14
    num_devs=params.num_devs
# price_3d_ctmc.m:15
    m_0=params.m_0
# price_3d_ctmc.m:16
    GridMultParam=params.GridMultParam
# price_3d_ctmc.m:17
    gridMethod=params.gridMethod
# price_3d_ctmc.m:18
    ##################################
    
    drifts=r - qs
# price_3d_ctmc.m:21
    L,D,C,Cinv=get_transform_matrices_3d(R,method,nargout=4)
# price_3d_ctmc.m:23
    # Now Define New Uncorrelated System  (the dc underscore)
    drift_dc,sigma_dc=decorrelate(sigmas,drifts,C,D,nargout=2)
# price_3d_ctmc.m:26
    Ls_dc,Rs_dc=get_CTMC_decorr_boundaries(sigmas,C,T,num_devs,sigma_dc,nargout=2)
# price_3d_ctmc.m:28
    Y_0s=concat([0,0,0])
# price_3d_ctmc.m:29
    # Form CTMC 1
    center=Y_0s(1)
# price_3d_ctmc.m:32
    mu_func=lambda s=None: dot(drift_dc(1),concat([s > - 100000]))
# price_3d_ctmc.m:33
    sig_func=lambda s=None: dot(sigma_dc(1),concat([s > - 100000]))
# price_3d_ctmc.m:34
    Q,y_1,c_index_1=Q_Matrix(m_0,mu_func,sig_func,Ls_dc(1),Rs_dc(1),gridMethod,center,GridMultParam,nargout=3)
# price_3d_ctmc.m:35
    P1=expm(dot(Q,dt))
# price_3d_ctmc.m:36
    # Form CTMC 2
    center=Y_0s(2)
# price_3d_ctmc.m:39
    mu_func=lambda s=None: dot(drift_dc(2),concat([s > - 100000]))
# price_3d_ctmc.m:40
    sig_func=lambda s=None: dot(sigma_dc(2),concat([s > - 100000]))
# price_3d_ctmc.m:41
    Q,y_2,c_index_2=Q_Matrix(m_0,mu_func,sig_func,Ls_dc(2),Rs_dc(2),gridMethod,center,GridMultParam,nargout=3)
# price_3d_ctmc.m:42
    P2=expm(dot(Q,dt))
# price_3d_ctmc.m:43
    # Form CTMC 3
    center=Y_0s(3)
# price_3d_ctmc.m:46
    mu_func=lambda s=None: dot(drift_dc(3),concat([s > - 100000]))
# price_3d_ctmc.m:47
    sig_func=lambda s=None: dot(sigma_dc(3),concat([s > - 100000]))
# price_3d_ctmc.m:48
    Q,y_3,c_index_3=Q_Matrix(m_0,mu_func,sig_func,Ls_dc(3),Rs_dc(3),gridMethod,center,GridMultParam,nargout=3)
# price_3d_ctmc.m:49
    P3=expm(dot(Q,dt))
# price_3d_ctmc.m:50
    G=get_payoff_G_matrix_from_ygrid_3d(y_1,y_2,y_3,S_0s,sigmas,R,contractParams)
# price_3d_ctmc.m:53
    if contract == 1:
        # vals = exp(-r*T)*P1*G*P2.';
        vals=0
# price_3d_ctmc.m:57
        for i in arange(1,m_0).reshape(-1):
            for j in arange(1,m_0).reshape(-1):
                for k in arange(1,m_0).reshape(-1):
                    vals=vals + dot(dot(dot(P1(c_index_1,i),P2(c_index_2,j)),P3(c_index_3,k)),G(i,j,k))
# price_3d_ctmc.m:61
        vals=dot(vals,exp(dot(- r,T)))
# price_3d_ctmc.m:65
    
    return vals,c_index_1,c_index_2,c_index_3,y_1,y_2,y_3
    
if __name__ == '__main__':
    pass
    