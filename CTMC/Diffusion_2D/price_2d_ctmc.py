# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# price_2d_ctmc.m

    
@function
def price_2d_ctmc(S_0s=None,T=None,r=None,rho=None,sigmas=None,qs=None,params=None,contractParams=None,M=None,*args,**kwargs):
    varargin = price_2d_ctmc.varargin
    nargin = price_2d_ctmc.nargin

    #########################################################
# About: Pricing Function for European/Bermudan/Barrier Options using CTMC approximation method
# Models Supported: 2D Diffusions
# Returns: price of contract
# Author: Justin Lars Kirkby
    
    # References:  (1) A General Continuous Time Markov Chain Approximation for
#               Multi-Asset option pricing with systems of correlated diffusions,
#               Applied Math. and Comput., 2020 (JL Kirkby, Duy Nguyen, Dang Nguyen)
    
    # ----------------------
# Model Params 
# ----------------------
# S_0s   = initial asset prices
# T      = time remaining until maturity (in years, e.g. T=1)
# r      = interest rate (e.g. 0.05)
# rho    = correlation between brownian motions 
# sigmas = volatilities per asset
# qs     = div yeilds per asset
# M      = num monitoring points for Barrier/Bermudan (also controls num steps for multi-step European pricing)
    
    # ----------------------
# Contract Params  (contractParams)
# ----------------------
    
    # contractParams.payoff_type:
# 
# 1: Linear, G = S_1  (linear payoff in first underlying)
# 2: Linear, G = S_2  (linear payoff in second underlying)
# 3: Exchange, G = (S_1 - S_2)^+
# 4: Spread,  G = (S_1 - S_2 - K)^+   (NOTE: must set strike, K)
# 5: Geometric Basket Call / Put,  G = (sqrt(S_1) * sqrt(S_2) - K)^+  (for the call)
# 6: Arithmetic Basket Call / Put,  G = (sqrt(S_1) * sqrt(S_2) - K)^+  (for the call)
# 7: Call-on-Max and Put-on-Min, Gcall = (max(S_1,S_2) - K)^+ , Gput = (K - min(S_1,S_2))^+
# 8: Call/put on just S_2, G = (S_2 - K)^+  (for the call)
# 9: Best-of / Worst-of,  G = max(S_1,S_2), G = min(S_1,S_2)
# 
# contractParams.contract:
    
    # 1: European, Single Step Pricing
# 2: European, Multi Step Pricing (M above controls number of steps)
# 3: Bermudan (M above controls number of monitoring points)
# 4: Barrier (M above controls number of monitoring points)
    
    # Note: for barrier option, set:
#       contractParams.barriers_1 = lower/upper barriers on first asset  (e.g. [0 50])
#       contractParams.barriers_2 = lower/upper barriers on second asset  (e.g. [0 50000000000] to disable barrier on S_2)
    
    # ----------------------
# Numerical (CTMC) Params 
# ----------------------
# params = CTMC parameters
# params.m_0 = num CTCM states
# params.num_devs = num std devs used in the grid
# params.gridMethod = choose the grid method (several RnD versions)
# params.GridMultParam = non-uniformity param, in (0,1)
    
    #########################################################
    
    if nargin < 9:
        M=1
# price_2d_ctmc.m:62
    
    dt=T / M
# price_2d_ctmc.m:64
    contract=contractParams.contract
# price_2d_ctmc.m:66
    if contract == 1:
        dt=1
# price_2d_ctmc.m:69
        M=1
# price_2d_ctmc.m:69
    
    method=4
# price_2d_ctmc.m:72
    num_devs=params.num_devs
# price_2d_ctmc.m:73
    m_0=params.m_0
# price_2d_ctmc.m:74
    GridMultParam=params.GridMultParam
# price_2d_ctmc.m:75
    gridMethod=params.gridMethod
# price_2d_ctmc.m:76
    ##################################
    
    drifts=r - qs
# price_2d_ctmc.m:79
    R=concat([[1,rho],[rho,1]])
# price_2d_ctmc.m:81
    
    L,D,C,Cinv=get_transform_matrices_2d(R,method,nargout=4)
# price_2d_ctmc.m:82
    # Now Define New Uncorrelated System  (the dc underscore)
    drift_dc,sigma_dc=decorrelate(sigmas,drifts,C,D,nargout=2)
# price_2d_ctmc.m:85
    Ls_dc,Rs_dc=get_CTMC_decorr_boundaries(sigmas,C,T,0,sigma_dc,num_devs,nargout=2)
# price_2d_ctmc.m:87
    Y_0s=concat([0,0])
# price_2d_ctmc.m:88
    # Form CTMC 1
    center=Y_0s(1)
# price_2d_ctmc.m:91
    mu_func=lambda s=None: dot(drift_dc(1),concat([s > - 100000]))
# price_2d_ctmc.m:92
    sig_func=lambda s=None: dot(sigma_dc(1),concat([s > - 100000]))
# price_2d_ctmc.m:93
    Q,y_1,c_index_1=Q_Matrix(m_0,mu_func,sig_func,Ls_dc(1),Rs_dc(1),gridMethod,center,GridMultParam,nargout=3)
# price_2d_ctmc.m:94
    P1=expm(dot(Q,dt))
# price_2d_ctmc.m:95
    # Form CTMC 2
    center=Y_0s(2)
# price_2d_ctmc.m:98
    mu_func=lambda s=None: dot(drift_dc(2),concat([s > - 100000]))
# price_2d_ctmc.m:99
    sig_func=lambda s=None: dot(sigma_dc(2),concat([s > - 100000]))
# price_2d_ctmc.m:100
    Q,y_2,c_index_2=Q_Matrix(m_0,mu_func,sig_func,Ls_dc(2),Rs_dc(2),gridMethod,center,GridMultParam,nargout=3)
# price_2d_ctmc.m:101
    P2=expm(dot(Q,dt))
# price_2d_ctmc.m:102
    G=get_payoff_G_matrix_from_ygrid_2d(y_1,y_2,S_0s,sigmas,rho,contractParams)
# price_2d_ctmc.m:104
    if contract == 1:
        vals=dot(dot(dot(exp(dot(- r,T)),P1),G),P2.T)
# price_2d_ctmc.m:107
    else:
        if contract == 2:
            vals=copy(G)
# price_2d_ctmc.m:110
            for m in arange(M - 1,0,- 1).reshape(-1):
                vals=dot(dot(dot(exp(dot(- r,dt)),P1),vals),P2.T)
# price_2d_ctmc.m:112
        else:
            if contract == 3:
                vals=copy(G)
# price_2d_ctmc.m:116
                for m in arange(M - 1,0,- 1).reshape(-1):
                    vals=max(dot(dot(dot(exp(dot(- r,dt)),P1),vals),P2.T),G)
# price_2d_ctmc.m:118
            else:
                if contract == 4:
                    b1=contractParams.barriers_1
# price_2d_ctmc.m:122
                    L1=b1(1)
# price_2d_ctmc.m:122
                    U1=b1(2)
# price_2d_ctmc.m:122
                    b2=contractParams.barriers_2
# price_2d_ctmc.m:123
                    L2=b2(1)
# price_2d_ctmc.m:123
                    U2=b2(2)
# price_2d_ctmc.m:123
                    B=ones(m_0,m_0)
# price_2d_ctmc.m:124
                    for i in arange(1,m_0).reshape(-1):
                        y1=y_1(i)
# price_2d_ctmc.m:126
                        S1=dot(S_0s(1),exp(dot(sigmas(1),y1)))
# price_2d_ctmc.m:127
                        if S1 < L1 or S1 > U1:
                            B[i,arange()]=0
# price_2d_ctmc.m:129
                        else:
                            for j in arange(1,m_0).reshape(-1):
                                y2=y_2(j)
# price_2d_ctmc.m:132
                                S2=dot(S_0s(2),exp(dot(sigmas(2),(y2 + dot(rho,y1)))))
# price_2d_ctmc.m:133
                                if S2 < L2 or S2 > U2:
                                    B[i,j]=0
# price_2d_ctmc.m:135
                    vals=multiply(G,B)
# price_2d_ctmc.m:140
                    for m in arange(M - 1,0,- 1).reshape(-1):
                        vals=dot(exp(dot(- r,dt)),(dot(dot(multiply(B,P1),vals),P2.T)))
# price_2d_ctmc.m:142
    
    return vals,c_index_1,c_index_2,y_1,y_2
    
if __name__ == '__main__':
    pass
    