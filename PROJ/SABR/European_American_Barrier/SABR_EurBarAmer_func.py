# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# SABR_EurBarAmer_func.m

    
@function
def SABR_EurBarAmer_func(call=None,M=None,T=None,S0=None,Kvec=None,r=None,CTMCParams=None,ModParams=None,contract_type=None,L=None,*args,**kwargs):
    varargin = SABR_EurBarAmer_func.varargin
    nargin = SABR_EurBarAmer_func.nargin

    #########################################################
# About: Pricing Function for European, American, and Barrier Options using
# double Layer CTMC approximation for SABR
    
    # Models Supported: SABR
# Returns: price of contract (for vector of strikes)
# Author: Justin Lars Kirkby
    
    # References:  (1) General Valuation Framework for SABR and Stochastic Local Volatility
#                   Models. SIAM J. Financial Mathematics, 2018. (w/ Z. Cui
#                   and D. Nguyen)
    
    # ----------------------
# Contract/Model Params 
# ----------------------
# call = 1 for call option, else Put
# contract_type = type of contact: # 1 = European, 2 = American, 3 = Down and Out Barrier
# Kvec  = strike vector
# S0 = initinal underlying value
# r   = interest rate (e.g. 0.05)
# T   = time remaining until maturity (in years, e.g. T=1)
# ModParams = model parameters: .v0, .alpha, .beta, .rho
# L =  For barrier contract, this is the barrier
    
    # ----------------------
# Numerical (CTMC) Params 
# ----------------------
# CTMCParams: .m_0 = grid/state size for variance process
#             .N = grid/state stize for underlying
#             .gridMult_v = grid non-uniformity multiplier (for variance)
#             .gridMult_s = grid non-uniformity multiplier (for underlying)
#             .gamma = Grid width param for variance grid
#########################################################
    
    m_0=CTMCParams.m_0
# SABR_EurBarAmer_func.m:36
    N=CTMCParams.N
# SABR_EurBarAmer_func.m:37
    gridMult_v=CTMCParams.gridMult_v
# SABR_EurBarAmer_func.m:38
    gridMult_s=CTMCParams.gridMult_s
# SABR_EurBarAmer_func.m:39
    
    gamma=CTMCParams.gamma
# SABR_EurBarAmer_func.m:40
    
    gridMethod_v=5
# SABR_EurBarAmer_func.m:42
    
    gridMethod_s=4
# SABR_EurBarAmer_func.m:43
    
    v0=ModParams.v0
# SABR_EurBarAmer_func.m:45
    alpha=ModParams.alpha
# SABR_EurBarAmer_func.m:46
    beta=ModParams.beta
# SABR_EurBarAmer_func.m:47
    rho=ModParams.rho
# SABR_EurBarAmer_func.m:48
    ######################
###   Set Asset Grid bounds
######################
    if S0 < 0.5:
        ls=dot(0.01,S0)
# SABR_EurBarAmer_func.m:54
    else:
        ls=dot(0.001,S0)
# SABR_EurBarAmer_func.m:56
    
    us=max(dot(4.5,S0),S0 + dot(dot(10,(dot(v0,(S0) ** beta))),sqrt(T)))
# SABR_EurBarAmer_func.m:59
    
    #################################
####   Step 1: Variance Grid / Generators
#################################
    dt=T / M
# SABR_EurBarAmer_func.m:64
    t=sqrt(T) / 2
# SABR_EurBarAmer_func.m:65
    
    mu_func=lambda u=None: dot(0,u)
# SABR_EurBarAmer_func.m:67
    sig_func=lambda u=None: dot(alpha,u)
# SABR_EurBarAmer_func.m:68
    mu_H=copy(v0)
# SABR_EurBarAmer_func.m:69
    sig2_H=dot(v0 ** 2,(exp(dot(alpha ** 2,t)) - 1))
# SABR_EurBarAmer_func.m:70
    lx=max(0.0001,mu_H - dot(gamma,sqrt(sig2_H)))
# SABR_EurBarAmer_func.m:72
    ux=mu_H + dot(gamma,sqrt(sig2_H))
# SABR_EurBarAmer_func.m:73
    #################################
####   Step 1: Variance Grid / Generators
#################################
    center_v=copy(v0)
# SABR_EurBarAmer_func.m:79
    Q,v=General_Q_Matrix_Newest(m_0,mu_func,sig_func,lx,ux,gridMethod_v,center_v,gridMult_v,nargout=2)
# SABR_EurBarAmer_func.m:80
    #################################
####   Step 2: Asset Grid / Grid For Xtilde
#################################
    g=lambda s=None: (s) ** (1 - beta) / (1 - beta)
# SABR_EurBarAmer_func.m:85
    invOneBet=1 / (1 - beta)
# SABR_EurBarAmer_func.m:86
    center_s=copy(S0)
# SABR_EurBarAmer_func.m:88
    
    manualPoint_s=copy(center_s)
# SABR_EurBarAmer_func.m:89
    
    Xgrid=g(getNonUniformGrid(N,ls,us,gridMethod_s,center_s,manualPoint_s,gridMult_s)) - dot(rho / alpha,v0)
# SABR_EurBarAmer_func.m:90
    
    #################################
####   Step 3: Generators (for Xtilde process)
#################################
    Nm=dot(N,m_0)
# SABR_EurBarAmer_func.m:95
    G=zeros(Nm,Nm)
# SABR_EurBarAmer_func.m:96
    
    I=eye(N,N)
# SABR_EurBarAmer_func.m:97
    Payoff=zeros(Nm,1)
# SABR_EurBarAmer_func.m:99
    
    sqrtRho=sqrt(1 - rho ** 2)
# SABR_EurBarAmer_func.m:100
    for j in arange(1,m_0).reshape(-1):
        ##########
    # Step(1): Find G_j (generator with v(j) fixed)
    ##########
        nu_j=v(j)
# SABR_EurBarAmer_func.m:106
        muX_func_nu=lambda x=None: dot(dot(dot(- 0.5,beta),(nu_j) ** 2.0),(dot((1 - beta),(x + dot(rho,nu_j) / alpha))) ** (- 1))
# SABR_EurBarAmer_func.m:107
        sigX_func_nu=lambda x=None: dot(dot(sqrtRho,nu_j),concat([x > - 100]))
# SABR_EurBarAmer_func.m:108
        Gnu=getGenerator_Q_MatrixOnly(Xgrid,muX_func_nu,sigX_func_nu,gridMethod_v)
# SABR_EurBarAmer_func.m:110
        ### FORCE absorbing vs reflecting
        Gnu[1,1]=0
# SABR_EurBarAmer_func.m:113
        Gnu[1,2]=0
# SABR_EurBarAmer_func.m:113
        ##################################
        ##########
    # Step(2): Populate the Generator matrix (recall it is block tridiagonal,
    ##########
        for k in arange(max(1,j - 1),min(m_0,j + 1)).reshape(-1):
            lamjk=Q(j,k)
# SABR_EurBarAmer_func.m:121
            if j == k:
                G[arange(dot((j - 1),N) + 1,dot(j,N)),arange(dot((k - 1),N) + 1,dot(k,N))]=Gnu + dot(lamjk,I)
# SABR_EurBarAmer_func.m:123
            else:
                G[arange(dot((j - 1),N) + 1,dot(j,N)),arange(dot((k - 1),N) + 1,dot(k,N))]=dot(lamjk,I)
# SABR_EurBarAmer_func.m:125
    
    #### Find bracketing variance gridpoint
    k_0=2
# SABR_EurBarAmer_func.m:131
    while v0 >= v(k_0) and k_0 < m_0:

        k_0=k_0 + 1
# SABR_EurBarAmer_func.m:133

    
    k_0=k_0 - 1
# SABR_EurBarAmer_func.m:135
    
    #### Find bracketing Xtilde gridpoint
    x0=g(S0) - dot(rho,v0) / alpha
# SABR_EurBarAmer_func.m:138
    
    j_0=2
# SABR_EurBarAmer_func.m:139
    while x0 >= Xgrid(j_0) and j_0 < N:

        j_0=j_0 + 1
# SABR_EurBarAmer_func.m:141

    
    j_0=j_0 - 1
# SABR_EurBarAmer_func.m:143
    
    ###########################################
#### VALUE : using recursive method
###########################################
    
    P=expm(dot(G,dt))
# SABR_EurBarAmer_func.m:149
    
    initialIndex=dot((k_0 - 1),N) + j_0
# SABR_EurBarAmer_func.m:150
    
    prices=zeros(length(Kvec),1)
# SABR_EurBarAmer_func.m:152
    for k in arange(1,length(Kvec)).reshape(-1):
        K=Kvec(k)
# SABR_EurBarAmer_func.m:155
        if call == 1:
            for j in arange(1,m_0).reshape(-1):
                Payoff[arange(dot((j - 1),N) + 1,dot(j,N))]=max(0,(dot((1 - beta),(max(0,Xgrid + dot(rho,v(j)) / alpha)))) ** invOneBet - K)
# SABR_EurBarAmer_func.m:159
        else:
            for j in arange(1,m_0).reshape(-1):
                Payoff[arange(dot((j - 1),N) + 1,dot(j,N))]=max(0,K - (dot((1 - beta),(max(0,Xgrid + dot(rho,v(j)) / alpha)))) ** invOneBet)
# SABR_EurBarAmer_func.m:163
        ### Now Price
        if contract_type == 3:
            #determine which states remain alive
            alive=zeros(Nm,1)
# SABR_EurBarAmer_func.m:169
            for j in arange(1,m_0).reshape(-1):
                cons=g(L) - dot(v(j),rho) / alpha
# SABR_EurBarAmer_func.m:171
                alive[arange(dot((j - 1),N) + 1,dot(j,N))]=(Xgrid > cons)
# SABR_EurBarAmer_func.m:172
            pVec=multiply(alive,Payoff)
# SABR_EurBarAmer_func.m:174
            for m in arange(M - 1,0,- 1).reshape(-1):
                pVec=multiply(dot(exp(dot(- r,dt)),alive),(dot(P,pVec)))
# SABR_EurBarAmer_func.m:176
        else:
            pVec=dot(exp(dot(- r,dt)),(dot(P,Payoff)))
# SABR_EurBarAmer_func.m:179
            if contract_type == 2:
                for m in arange(M - 2,0,- 1).reshape(-1):
                    pVec=dot(exp(dot(- r,dt)),(dot(P,pVec)))
# SABR_EurBarAmer_func.m:182
                    pVec=max(pVec,Payoff)
# SABR_EurBarAmer_func.m:183
            else:
                if contract_type == 1:
                    for m in arange(M - 2,0,- 1).reshape(-1):
                        pVec=dot(exp(dot(- r,dt)),(dot(P,pVec)))
# SABR_EurBarAmer_func.m:187
        if gridMethod_s == 5:
            prices[k]=pVec(initialIndex)
# SABR_EurBarAmer_func.m:193
        else:
            if gridMethod_s == 4:
                price1=pVec(initialIndex)
# SABR_EurBarAmer_func.m:195
                price2=pVec(initialIndex + 1)
# SABR_EurBarAmer_func.m:196
                prices[k]=price1 + dot((price2 - price1),(x0 - Xgrid(j_0))) / (Xgrid(j_0 + 1) - Xgrid(j_0))
# SABR_EurBarAmer_func.m:197
    
    
    return prices
    
if __name__ == '__main__':
    pass
    