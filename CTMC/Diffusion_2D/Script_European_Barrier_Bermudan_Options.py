# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_European_Barrier_Bermudan_Options.m

    ##################################################################
### 2D EUROPEAN/Barrier/Bermudan OPTION PRICER (RUN SCRIPT)
##################################################################
# Descritpion: Script to Price European options in 2D Diffusion Models
#              using the CTMC Approximation
    
    #              This script is configured initially to compare against analytical exchange option price,
#              but it can be used to price numerous payoffs with European/Barrier/Bermudan style
    
    # Author:      Justin Kirkby
# References:  (1) A General Continuous Time Markov Chain Approximation for
#               Multi-Asset option pricing with systems of correlated diffusions,
#               Applied Math. and Comput., 2020 (with Duy Nguyen and Dang Nguyen)
##################################################################
    
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_European_Barrier_Bermudan_Options.m:16
    cd(folder)
    addpath('../')
    addpath('../../Analytical/BlackScholes/')
    ##############################################
###  Step 1) CHOOSE MODEL PARAMETERS
##############################################
    r=0.0
# Script_European_Barrier_Bermudan_Options.m:24
    
    S_0s=concat([97,97])
# Script_European_Barrier_Bermudan_Options.m:25
    
    sigmas=concat([0.15,0.15])
# Script_European_Barrier_Bermudan_Options.m:26
    
    qs=concat([0,0])
# Script_European_Barrier_Bermudan_Options.m:27
    
    rho=0.5
# Script_European_Barrier_Bermudan_Options.m:28
    
    T=1
# Script_European_Barrier_Bermudan_Options.m:29
    
    M=10
# Script_European_Barrier_Bermudan_Options.m:30
    
    ##############################################
### Step 3) Choose Contract Params
##############################################
    contractParams=cellarray([])
# Script_European_Barrier_Bermudan_Options.m:36
    # ---------------
# Contract Types:
# ---------------  
# 1: European, Single Step Pricing
# 2: European, Multi Step Pricing (M above controls number of steps)
# 3: Bermudan (M above controls number of monitoring points)
# 4: Barrier (M above controls number of monitoring points)
    contractParams.contract = copy(1)
# Script_European_Barrier_Bermudan_Options.m:45
    if contractParams.contract == 4:
        # Set Barrier For Barrier Option (initially configured to price with only a barrier on the first underlying)
        contractParams.barriers_1 = copy(concat([0,50]))
# Script_European_Barrier_Bermudan_Options.m:49
        contractParams.barriers_2 = copy(concat([0,50000000000]))
# Script_European_Barrier_Bermudan_Options.m:50
    
    # ---------------
# Payoff Types:
# ---------------  
# 1: Linear, G = S_1  (linear payoff in first underlying)
# 2: Linear, G = S_2  (linear payoff in second underlying)
# 3: Exchange, G = (S_1 - S_2)^+
# 4: Spread,  G = (S_1 - S_2 - K)^+   (NOTE: must set strike, K)
# 5: Geometric Basket Call / Put,  G = (sqrt(S_1) * sqrt(S_2) - K)^+  (for the call)
# 6: Arithmetic Basket Call / Put,  G = (sqrt(S_1) * sqrt(S_2) - K)^+  (for the call)
# 7: Call-on-Max and Put-on-Min, Gcall = (max(S_1,S_2) - K)^+ , Gput = (K - min(S_1,S_2))^+
# 8: Call/put on just S_2, G = (S_2 - K)^+  (for the call)
# 9: Best-of / Worst-of,  G = max(S_1,S_2), G = min(S_1,S_2)
    contractParams.payoff_type = copy(4)
# Script_European_Barrier_Bermudan_Options.m:65
    # Payoff Dependent Contract parameters (ignored for certain payoffs)
    contractParams.K = copy(0)
# Script_European_Barrier_Bermudan_Options.m:68
    
    contractParams.call = copy(1)
# Script_European_Barrier_Bermudan_Options.m:69
    
    ##############################################
###  Step 4) CHOOSE CTMC PARAMETERS
##############################################
    params=cellarray([])
# Script_European_Barrier_Bermudan_Options.m:74
    params.num_devs = copy(5)
# Script_European_Barrier_Bermudan_Options.m:75
    
    params.GridMultParam = copy(0.1)
# Script_European_Barrier_Bermudan_Options.m:76
    
    params.gridMethod = copy(7)
# Script_European_Barrier_Bermudan_Options.m:77
    
    params.m_0 = copy(120)
# Script_European_Barrier_Bermudan_Options.m:78
    
    ##############################################
### Step 5) PRICE
##############################################
    tic
    vals,c_index_1,c_index_2,y_1,y_2=price_2d_ctmc(S_0s,T,r,rho,sigmas,qs,params,contractParams,M,nargout=5)
# Script_European_Barrier_Bermudan_Options.m:86
    price_ctmc=vals(c_index_1,c_index_2)
# Script_European_Barrier_Bermudan_Options.m:87
    time_ctmc=copy(toc)
# Script_European_Barrier_Bermudan_Options.m:88
    fprintf('CTMC Price: %.8f   (time: %.3f)\n',price_ctmc,time_ctmc)
    # Analytical price in case of Spread
    if contractParams.payoff_type == 4 and (contractParams.contract <= 2) and contractParams.K == 0:
        price_exchange=Price_Exchange_Option_Margrabe_2D(S_0s(1),S_0s(2),T,rho,sigmas(1),sigmas(2),qs(1),qs(2))
# Script_European_Barrier_Bermudan_Options.m:94
        fprintf('Exact Exchange Price: %.8f\n',price_exchange)
        fprintf('Error: %.2e\n',price_ctmc - price_exchange)
    