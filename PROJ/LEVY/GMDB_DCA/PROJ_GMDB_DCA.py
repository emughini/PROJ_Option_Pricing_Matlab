# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# PROJ_GMDB_DCA.m

    
@function
def PROJ_GMDB_DCA(proj_params=None,S_0=None,gmdb_params=None,r=None,q=None,modelInput=None,*args,**kwargs):
    varargin = PROJ_GMDB_DCA.varargin
    nargin = PROJ_GMDB_DCA.nargin

    #########################################################
# About: Pricing Function for DCA-Style Garuanteed Minimum Withdraw Benefit (GMWB) using PROJ method
    
    # Terminal Payoff:  Payoff(tau) = L*exp(g*tau) + (Gam(tau) - L*exp(g*tau))^+
#                      Gam(tau) = S_M * sum_{m=0}^M(alpha*gamma / S_m)
#                          tau  = time of death (discrete periods)
    
    # Models Supported: Levy Processes, including jump diffusions and Black-Scholes model
# Returns: price of contract
    
    # NOTE: this is the SLOW "Direct" version for testing purpose. In general, use PROJ_GMDB_DCA_Fast
    
    # Author: Justin Lars Kirkby
# References: 1) Equity-Linked  Guaranteed Minimum Death Benefits with Dollar Cost Averaging, J.L.Kirkby & D.Nguyen, 2021
    
    # ----------------------
# Contract/Model Params 
# ----------------------
# S_0 = initial stock price (e.g. 100)
# r   = interest rate (e.g. 0.05)
# q   = dividend yield (e.g. 0.05)
# M   = number of subintervals of [0,T] (total of M+1 monitoring points in time grid, including S_0)
# gmdb_params = container of GMDB contract params, see below
# modelInput =  model inputs, see below
    
    # ----------------------
# Numerical (PROJ) Params 
# ----------------------
# proj_params = numerical params
#   proj_params.N = number of basis elements, e.g. N = 2^10
#   proj_params.L1 = gridwidth param, e.g. L1 = 8
    
    #########################################################
    
    # ------------------
# GMDB Contract Params
# ------------------
    L=gmdb_params.L
# PROJ_GMDB_DCA.m:39
    
    alpha=gmdb_params.alpha
# PROJ_GMDB_DCA.m:40
    
    gamma=gmdb_params.gamma
# PROJ_GMDB_DCA.m:41
    
    contract_type=gmdb_params.contract_type
# PROJ_GMDB_DCA.m:42
    
    p=gmdb_params.death_prob
# PROJ_GMDB_DCA.m:43
    
    g=gmdb_params.g
# PROJ_GMDB_DCA.m:44
    # ------------------
# Model Inputs
# ------------------
    dt=modelInput.dt
# PROJ_GMDB_DCA.m:49
    
    phiR=modelInput.rnCHF
# PROJ_GMDB_DCA.m:50
    
    Z=gen_func(- r,dt,p)
# PROJ_GMDB_DCA.m:53
    if g == 0:
        Zrg=copy(Z)
# PROJ_GMDB_DCA.m:55
    else:
        Zrg=gen_func(- (r - g),dt,p)
# PROJ_GMDB_DCA.m:57
    
    if L == - 1:
        MF=gen_func(r - q - g,dt,p)
# PROJ_GMDB_DCA.m:61
        Zg=gen_func(- g,dt,p)
# PROJ_GMDB_DCA.m:62
        L=dot(dot(alpha,gamma),(dot(exp(dot((r - q),dt)),MF) - Zg)) / (exp(dot((r - q),dt)) - 1)
# PROJ_GMDB_DCA.m:63
    
    call=1
# PROJ_GMDB_DCA.m:66
    N=proj_params.N
# PROJ_GMDB_DCA.m:67
    s=0
# PROJ_GMDB_DCA.m:69
    for n in arange(1,length(p)).reshape(-1):
        M=copy(n)
# PROJ_GMDB_DCA.m:73
        T=dot(n,dt)
# PROJ_GMDB_DCA.m:74
        if contract_type == 2:
            W=copy(S_0)
# PROJ_GMDB_DCA.m:76
        else:
            W=dot(dot(S_0,L),exp(dot(g,T))) / (dot(dot(alpha,gamma),(M + 1)))
# PROJ_GMDB_DCA.m:78
        pr_alpha=getTruncationAlpha(T,proj_params.L1,modelInput,proj_params.model)
# PROJ_GMDB_DCA.m:81
        if n == 1:
            W=dot(2,W) - S_0
# PROJ_GMDB_DCA.m:84
            opt_v=dot(0.5,PROJ_European(3,N,dot(2,pr_alpha),r,q,T,S_0,W,call,phiR,modelInput.c1))
# PROJ_GMDB_DCA.m:85
        else:
            if contract_type == 1 or contract_type == 2:
                ER=0
# PROJ_GMDB_DCA.m:88
                opt_v=PROJ_Asian(N,pr_alpha,S_0,M,W,call,T,r,q,phiR,ER)
# PROJ_GMDB_DCA.m:89
            else:
                if contract_type == 3:
                    opt_v=PROJ_European(3,N,dot(2,pr_alpha),r,q,T,S_0,W,call,modelInput.rnCHF_T,modelInput.c1)
# PROJ_GMDB_DCA.m:91
                    if r != 0:
                        opt_v=dot(opt_v,((1 - exp(dot(dot(- r,(n + 1)),dt))) / (1 - exp(dot(- r,dt))))) / (n + 1)
# PROJ_GMDB_DCA.m:93
                else:
                    if contract_type == 4:
                        opt_v=PROJ_Geometric_Asian(N,pr_alpha,S_0,M,W,call,T,r,q,modelInput.rnSYMB)
# PROJ_GMDB_DCA.m:96
        # fprintf('#.12f \n', opt_v);
        s=s + dot(dot(p(n),(n + 1)),opt_v)
# PROJ_GMDB_DCA.m:101
    
    opt=dot(dot(s,alpha),gamma) / S_0
# PROJ_GMDB_DCA.m:105
    price=dot(L,Zrg) - dot(alpha,(exp(dot(r,dt)) - Z)) / (exp(dot(r,dt)) - 1) + opt
# PROJ_GMDB_DCA.m:106
    return price,opt,L
    
if __name__ == '__main__':
    pass
    