# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# cf_RN_Heston.m

    
@function
def cf_RN_Heston(u=None,T=None,r=None,v_0=None,theta=None,kappa=None,sigma_v=None,rho=None,*args,**kwargs):
    varargin = cf_RN_Heston.varargin
    nargin = cf_RN_Heston.nargin

    # HESTON Risk Neutral CHF  
# r = risk netural rate of interest (or pass r-q, interest minus div yield)
# T = time
# v_0 = spot variance
# theta = long term variance level
# kappa = rate of variance mean reversion
# sigma_v = volatility of variance
# rho = correlation between Brownian motions
    
    alpha=dot(- 0.5,(u ** 2 + dot(u,1j)))
# cf_RN_Heston.m:11
    beta=kappa - dot(dot(dot(rho,sigma_v),u),1j)
# cf_RN_Heston.m:12
    omega2=sigma_v ** 2
# cf_RN_Heston.m:13
    gamma=dot(0.5,omega2)
# cf_RN_Heston.m:14
    D=sqrt(beta ** 2 - multiply(dot(4.0,alpha),gamma))
# cf_RN_Heston.m:16
    bD=beta - D
# cf_RN_Heston.m:18
    eDt=exp(dot(- D,T))
# cf_RN_Heston.m:19
    G=bD / (beta + D)
# cf_RN_Heston.m:21
    B=multiply((bD / omega2),((1.0 - eDt) / (1.0 - multiply(G,eDt))))
# cf_RN_Heston.m:22
    psi=(1.0 - multiply(G,eDt)) / (1.0 - G)
# cf_RN_Heston.m:23
    A=dot(((dot(kappa,theta)) / (omega2)),(dot(bD,T) - dot(2.0,log(psi))))
# cf_RN_Heston.m:24
    y=exp(A + dot(B,v_0) + dot(dot(dot(1j,u),r),T))
# cf_RN_Heston.m:26
    return y
    
if __name__ == '__main__':
    pass
    