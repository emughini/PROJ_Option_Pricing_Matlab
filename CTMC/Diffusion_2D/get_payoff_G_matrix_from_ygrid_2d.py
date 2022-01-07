# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# get_payoff_G_matrix_from_ygrid_2d.m

    
@function
def get_payoff_G_matrix_from_ygrid_2d(y_1=None,y_2=None,S_0s=None,sigmas=None,rho=None,contractParams=None,*args,**kwargs):
    varargin = get_payoff_G_matrix_from_ygrid_2d.varargin
    nargin = get_payoff_G_matrix_from_ygrid_2d.nargin

    #UNTITLED5 Summary of this function goes here
#   Detailed explanation goes here
    
    payoff_type=contractParams.payoff_type
# get_payoff_G_matrix_from_ygrid_2d.m:5
    if payoff_type == 1:
        payoff=lambda y1=None,y2=None: dot(S_0s(1),exp(dot(sigmas(1),y1)))
# get_payoff_G_matrix_from_ygrid_2d.m:8
    else:
        if payoff_type == 2:
            payoff=lambda y1=None,y2=None: dot(S_0s(2),exp(dot(sigmas(2),(y2 + dot(rho,y1)))))
# get_payoff_G_matrix_from_ygrid_2d.m:11
        else:
            if payoff_type == 3:
                payoff=lambda y1=None,y2=None: max(0,dot(S_0s(1),exp(dot(sigmas(1),y1))) - dot(S_0s(2),exp(dot(sigmas(2),(y2 + dot(rho,y1))))))
# get_payoff_G_matrix_from_ygrid_2d.m:14
            else:
                if payoff_type == 4:
                    K=contractParams.K
# get_payoff_G_matrix_from_ygrid_2d.m:17
                    payoff=lambda y1=None,y2=None: max(0,dot(S_0s(1),exp(dot(sigmas(1),y1))) - dot(S_0s(2),exp(dot(sigmas(2),(y2 + dot(rho,y1))))) - K)
# get_payoff_G_matrix_from_ygrid_2d.m:18
                else:
                    if payoff_type == 5:
                        K=contractParams.K
# get_payoff_G_matrix_from_ygrid_2d.m:21
                        if contractParams.call == 1:
                            payoff=lambda y1=None,y2=None: max(0,dot(sqrt(dot(S_0s(1),exp(dot(sigmas(1),y1)))),sqrt(dot(S_0s(2),exp(dot(sigmas(2),(y2 + dot(rho,y1))))))) - K)
# get_payoff_G_matrix_from_ygrid_2d.m:23
                        else:
                            payoff=lambda y1=None,y2=None: max(0,K - dot(sqrt(dot(S_0s(1),exp(dot(sigmas(1),y1)))),sqrt(dot(S_0s(2),exp(dot(sigmas(2),(y2 + dot(rho,y1))))))))
# get_payoff_G_matrix_from_ygrid_2d.m:25
                    else:
                        if payoff_type == 6:
                            K=contractParams.K
# get_payoff_G_matrix_from_ygrid_2d.m:29
                            if contractParams.call == 1:
                                payoff=lambda y1=None,y2=None: max(0,dot(dot(0.5,S_0s(1)),exp(dot(sigmas(1),y1))) + dot(dot(0.5,S_0s(2)),exp(dot(sigmas(2),(y2 + dot(rho,y1))))) - K)
# get_payoff_G_matrix_from_ygrid_2d.m:31
                            else:
                                payoff=lambda y1=None,y2=None: max(0,K - dot(dot(0.5,S_0s(1)),exp(dot(sigmas(1),y1))) - dot(dot(0.5,S_0s(2)),exp(dot(sigmas(2),(y2 + dot(rho,y1))))))
# get_payoff_G_matrix_from_ygrid_2d.m:33
                        else:
                            if payoff_type == 7:
                                K=contractParams.K
# get_payoff_G_matrix_from_ygrid_2d.m:37
                                if contractParams.call == 1:
                                    payoff=lambda y1=None,y2=None: max(0,max(dot(S_0s(1),exp(dot(sigmas(1),y1))),dot(S_0s(2),exp(dot(sigmas(2),(y2 + dot(rho,y1)))))) - K)
# get_payoff_G_matrix_from_ygrid_2d.m:39
                                else:
                                    payoff=lambda y1=None,y2=None: max(0,K - min(dot(S_0s(1),exp(dot(sigmas(1),y1))),dot(S_0s(2),exp(dot(sigmas(2),(y2 + dot(rho,y1)))))))
# get_payoff_G_matrix_from_ygrid_2d.m:41
                            else:
                                if payoff_type == 8:
                                    K=contractParams.K
# get_payoff_G_matrix_from_ygrid_2d.m:44
                                    if contractParams.call == 1:
                                        payoff=lambda y1=None,y2=None: max(0,dot(S_0s(2),exp(dot(sigmas(2),(y2 + dot(rho,y1))))) - K)
# get_payoff_G_matrix_from_ygrid_2d.m:46
                                    else:
                                        payoff=lambda y1=None,y2=None: max(0,K - dot(S_0s(2),exp(dot(sigmas(2),(y2 + dot(rho,y1))))))
# get_payoff_G_matrix_from_ygrid_2d.m:48
                                else:
                                    if payoff_type == 9:
                                        if contractParams.best == 1:
                                            payoff=lambda y1=None,y2=None: max(dot(S_0s(1),exp(dot(sigmas(1),y1))),dot(S_0s(2),exp(dot(sigmas(2),(y2 + dot(rho,y1))))))
# get_payoff_G_matrix_from_ygrid_2d.m:52
                                        else:
                                            payoff=lambda y1=None,y2=None: min(dot(S_0s(1),exp(dot(sigmas(1),y1))),dot(S_0s(2),exp(dot(sigmas(2),(y2 + dot(rho,y1))))))
# get_payoff_G_matrix_from_ygrid_2d.m:54
    
    
    m_0=length(y_1)
# get_payoff_G_matrix_from_ygrid_2d.m:58
    G=zeros(m_0,m_0)
# get_payoff_G_matrix_from_ygrid_2d.m:59
    for i in arange(1,m_0).reshape(-1):
        for j in arange(1,m_0).reshape(-1):
            G[i,j]=payoff(y_1(i),y_2(j))
# get_payoff_G_matrix_from_ygrid_2d.m:63
    
    return G
    
if __name__ == '__main__':
    pass
    