# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_Compare_Spread.m

    ##################################################################
### 2D Spread OPTION PRICE COMPARISON (RUN SCRIPT)
##################################################################
# Descritpion: Script to compare pricing methods for Spread options under 2D Black-Schoels
#              This script compares accuracy/CPU of the following methods,
#                   CTMC approximation (2020)
#                   Monte Carlo
#                   Kirk Approximation (1995)
#                   Bjerksund & Stensland approx (2006)
#                   COS Method (2015)
    
    
    # Author:      Justin Kirkby
# References:  (1) A General Continuous Time Markov Chain Approximation for
#                 Multi-Asset option pricing with systems of correlated diffusions,
#                 Applied Math. and Comput., 2020 (JL Kirkby, Duy Nguyen, Dang Nguyen)
#              (2) Bjerksund, P. and Stensland, G. (2006): "Closed form spread option valuation"
#              (3) Kirk, E. (1995): "Correlation in the energy markets," In Managing Energy Price
#                 Risk (First Edition). London: Risk Publications and Enron, pp. 71-78.
#              (4) M. J. Ruijter and C. W. Oosterlee. Two-dimensional Fourier cosine
#                series expansion method for pricing financial options. SIAM Journal on
#                Scientific Computing, 34(5):B642–B671, 2012.
##################################################################
    
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_Compare_Spread.m:25
    cd(folder)
    ##############################################
###  Step 1) CHOOSE MODEL PARAMETERS
##############################################
    r=0.0
# Script_Compare_Spread.m:31
    
    S_0s=concat([97,97])
# Script_Compare_Spread.m:32
    
    sigmas=concat([0.15,0.15])
# Script_Compare_Spread.m:33
    
    qs=concat([0,0])
# Script_Compare_Spread.m:34
    
    rho=0.5
# Script_Compare_Spread.m:35
    
    T=1
# Script_Compare_Spread.m:36
    
    K=10
# Script_Compare_Spread.m:37
    
    call=1
# Script_Compare_Spread.m:38
    
    ##############################################
### Analytical Approximations
##############################################
    addpath('../../Analytical/BlackScholes/')
    fprintf('\n--------------------------------------------------\n')
    fprintf('Method          |    Price    |    Err   |  CPU \n')
    fprintf('--------------------------------------------------\n')
    # Use BjerksundStensland: NOTE, this is only approximation
    ref=Price_Spread_Option_BjerksundStensland_2D(K,S_0s(1),S_0s(2),T,r,rho,sigmas(1),sigmas(2),qs(1),qs(2))
# Script_Compare_Spread.m:51
    fprintf('Ref(BS Approx)  | %.8f  |          |       \n',ref)
    fprintf('--------------------------------------------------\n')
    tic
    price_kirk=Price_Spread_Option_Kirk_2D(K,S_0s(1),S_0s(2),T,r,rho,sigmas(1),sigmas(2),qs(1),qs(2))
# Script_Compare_Spread.m:57
    time_kirk=copy(toc)
# Script_Compare_Spread.m:58
    fprintf('Kirk            | %.8f  | %.2e | %.4f \n',price_kirk,abs(ref - price_kirk),time_kirk)
    ##############################################
### CTMC Approximation Method
##############################################
    addpath('../../CTMC/')
    addpath('../../CTMC/Diffusion_2D')
    contractParams=cellarray([])
# Script_Compare_Spread.m:67
    contractParams.contract = copy(1)
# Script_Compare_Spread.m:68
    
    contractParams.payoff_type = copy(4)
# Script_Compare_Spread.m:69
    
    contractParams.K = copy(K)
# Script_Compare_Spread.m:70
    contractParams.call = copy(call)
# Script_Compare_Spread.m:71
    M=10
# Script_Compare_Spread.m:72
    
    params=cellarray([])
# Script_Compare_Spread.m:74
    params.num_devs = copy(5)
# Script_Compare_Spread.m:75
    
    params.GridMultParam = copy(0.1)
# Script_Compare_Spread.m:76
    
    params.gridMethod = copy(7)
# Script_Compare_Spread.m:77
    
    params.m_0 = copy(120)
# Script_Compare_Spread.m:78
    
    tic
    vals,c_index_1,c_index_2,y_1,y_2=price_2d_ctmc(S_0s,T,r,rho,sigmas,qs,params,contractParams,M,nargout=5)
# Script_Compare_Spread.m:81
    price_ctmc=vals(c_index_1,c_index_2)
# Script_Compare_Spread.m:82
    time_ctmc=copy(toc)
# Script_Compare_Spread.m:83
    fprintf('CTMC            | %.8f  | %.2e | %.4f \n',price_ctmc,abs(ref - price_ctmc),time_ctmc)
    ##############################################
### COS (code available for K==0 only, ie exchange option)
##############################################
    if K == 0:
        addpath('../../Fourier/COS')
        tic
        N=19
# Script_Compare_Spread.m:94
        L=8
# Script_Compare_Spread.m:94
        price_cos=Price_Exchange_COS2D(S_0s,T,r,sigmas(1),sigmas(2),rho,N,L)
# Script_Compare_Spread.m:95
        time_cos=copy(toc)
# Script_Compare_Spread.m:96
        fprintf('COS             | %.8f  | %.2e | %.4f \n',price_cos,abs(ref - price_cos),time_cos)
    
    ##############################################
### Monte Carlo
##############################################
    addpath('../../Monte_Carlo')
    tic
    N_sim=10 ** 5
# Script_Compare_Spread.m:106
    M=200
# Script_Compare_Spread.m:106
    dt=T / M
# Script_Compare_Spread.m:107
    drifts=concat([r,r]) - qs
# Script_Compare_Spread.m:108
    exponential=1
# Script_Compare_Spread.m:109
    
    paths_1,paths_2=Simulate_Diffusion_2D(S_0s,drifts,sigmas,rho,N_sim,M,dt,exponential,nargout=2)
# Script_Compare_Spread.m:110
    S_1=paths_1(arange(),M + 1)
# Script_Compare_Spread.m:111
    S_2=paths_2(arange(),M + 1)
# Script_Compare_Spread.m:112
    payoffs=max(S_1 - S_2 - K,0)
# Script_Compare_Spread.m:114
    price_MC=dot(exp(dot(- r,T)),mean(payoffs))
# Script_Compare_Spread.m:115
    stderr=dot(exp(dot(- r,T)),std(payoffs)) / sqrt(N_sim)
# Script_Compare_Spread.m:116
    price_MC_L=price_MC - dot(2,stderr)
# Script_Compare_Spread.m:117
    price_MC_U=price_MC + dot(2,stderr)
# Script_Compare_Spread.m:117
    time_MC=copy(toc)
# Script_Compare_Spread.m:118
    fprintf('MC              |[%.3f,%.3f]| %.2e | %.4f \n',price_MC_L,price_MC_U,abs(ref - price_MC),time_MC)
    fprintf('--------------------------------------------------\n')