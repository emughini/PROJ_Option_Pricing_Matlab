# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# get_payoff_G_matrix_from_ygrid_3d.m

    
@function
def get_payoff_G_matrix_from_ygrid_3d(y_1=None,y_2=None,y_3=None,S_0s=None,sigmas=None,R=None,contractParams=None,*args,**kwargs):
    varargin = get_payoff_G_matrix_from_ygrid_3d.varargin
    nargin = get_payoff_G_matrix_from_ygrid_3d.nargin

    #UNTITLED5 Summary of this function goes here
#   Detailed explanation goes here
    
    payoff_type=contractParams.payoff_type
# get_payoff_G_matrix_from_ygrid_3d.m:5
    rho12=R(1,2)
# get_payoff_G_matrix_from_ygrid_3d.m:7
    rho23=R(2,3)
# get_payoff_G_matrix_from_ygrid_3d.m:8
    rho13=R(1,3)
# get_payoff_G_matrix_from_ygrid_3d.m:9
    gamma=(dot(rho12,rho13) - rho23) / (1 - rho12 ** 2)
# get_payoff_G_matrix_from_ygrid_3d.m:11
    if payoff_type == 1 or payoff_type == 2:
        dim=contractParams.dim
# get_payoff_G_matrix_from_ygrid_3d.m:14
        if dim == 1:
            payoff=lambda y1=None,y2=None,y3=None: dot(S_0s(1),exp(dot(sigmas(1),y1)))
# get_payoff_G_matrix_from_ygrid_3d.m:16
        else:
            if dim == 2:
                payoff=lambda y1=None,y2=None,y3=None: dot(S_0s(2),exp(dot(sigmas(2),(y2 + dot(rho12,y1)))))
# get_payoff_G_matrix_from_ygrid_3d.m:18
            else:
                payoff=lambda y1=None,y2=None,y3=None: dot(S_0s(3),exp(dot(sigmas(3),(dot(rho13,y1) - dot(gamma,y2) + y3))))
# get_payoff_G_matrix_from_ygrid_3d.m:20
    else:
        if payoff_type == 5:
            K=contractParams.K
# get_payoff_G_matrix_from_ygrid_3d.m:25
            if contractParams.call == 1:
                payoff=lambda y1=None,y2=None,y3=None: max(0,(dot(dot(dot(dot(dot(S_0s(1),exp(dot(sigmas(1),y1))),S_0s(2)),exp(dot(sigmas(2),(y2 + dot(rho12,y1))))),S_0s(3)),exp(dot(sigmas(3),(dot(rho13,y1) - dot(gamma,y2) + y3))))) ** (1 / 3) - K)
# get_payoff_G_matrix_from_ygrid_3d.m:27
            else:
                payoff=lambda y1=None,y2=None,y3=None: max(0,K - (dot(dot(dot(dot(dot(S_0s(1),exp(dot(sigmas(1),y1))),S_0s(2)),exp(dot(sigmas(2),(y2 + dot(rho12,y1))))),S_0s(3)),exp(dot(sigmas(3),(dot(rho13,y1) - dot(gamma,y2) + y3))))) ** (1 / 3))
# get_payoff_G_matrix_from_ygrid_3d.m:29
        else:
            if payoff_type == 6:
                K=contractParams.K
# get_payoff_G_matrix_from_ygrid_3d.m:33
                if contractParams.call == 1:
                    payoff=lambda y1=None,y2=None,y3=None: max(0,dot((1 / 3),(dot(S_0s(1),exp(dot(sigmas(1),y1))) + dot(S_0s(2),exp(dot(sigmas(2),(y2 + dot(rho12,y1))))) + dot(S_0s(3),exp(dot(sigmas(3),(dot(rho13,y1) - dot(gamma,y2) + y3)))))) - K)
# get_payoff_G_matrix_from_ygrid_3d.m:35
                else:
                    payoff=lambda y1=None,y2=None,y3=None: max(0,K - dot((1 / 3),(dot(S_0s(1),exp(dot(sigmas(1),y1))) + dot(S_0s(2),exp(dot(sigmas(2),(y2 + dot(rho12,y1))))) + dot(S_0s(3),exp(dot(sigmas(3),(dot(rho13,y1) - dot(gamma,y2) + y3)))))))
# get_payoff_G_matrix_from_ygrid_3d.m:37
    
    
    m_0=length(y_1)
# get_payoff_G_matrix_from_ygrid_3d.m:44
    G=zeros(m_0,m_0,m_0)
# get_payoff_G_matrix_from_ygrid_3d.m:45
    for i in arange(1,m_0).reshape(-1):
        for j in arange(1,m_0).reshape(-1):
            for k in arange(1,m_0).reshape(-1):
                G[i,j,k]=payoff(y_1(i),y_2(j),y_3(k))
# get_payoff_G_matrix_from_ygrid_3d.m:50
    
    return G
    
if __name__ == '__main__':
    pass
    