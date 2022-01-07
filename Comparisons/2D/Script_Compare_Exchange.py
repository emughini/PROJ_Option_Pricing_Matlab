# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_Compare_Exchange.m

    ##################################################################
### 2D Exchange OPTION PRICE COMPARISON (RUN SCRIPT)
##################################################################
# Descritpion: Script to compare pricing methods for Exchange options under 2D Black-Schoels
#              This script compares accuracy/CPU of the following methods,
#                   CTMC approximation
#                   Monte Carlo
#                   Magrabe (anlytical/exact)
#                   COS Method
    
    
    # Author:      Justin Kirkby
# References:  (1) A General Continuous Time Markov Chain Approximation for
#                 Multi-Asset option pricing with systems of correlated diffusions,
#                 Applied Math. and Comput., 2020 (JL Kirkby, Duy Nguyen, Dang Nguyen)
#              (2) M. J. Ruijter and C. W. Oosterlee. Two-dimensional Fourier cosine
#                 series expansion method for pricing financial options. SIAM Journal on
#                 Scientific Computing, 34(5):B642–B671, 2012.
#              (3) Margrabe, W. (1978): "The value of an option to exchange one asset for another,"
#                 Journal of Finance, 33 (1978), pp. 177-186.
##################################################################
    
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_Compare_Exchange.m:23
    cd(folder)
    addpath('../../Analytical/BlackScholes/')
    ##############################################
###  Step 1) CHOOSE MODEL PARAMETERS
##############################################
    r=0.05
# Script_Compare_Exchange.m:30
    
    S_0s=concat([97,97])
# Script_Compare_Exchange.m:31
    
    sigmas=concat([0.15,0.15])
# Script_Compare_Exchange.m:32
    
    rho=0.5
# Script_Compare_Exchange.m:33
    
    T=1
# Script_Compare_Exchange.m:34
    
    call=1
# Script_Compare_Exchange.m:35
    
    ##############################################
### Magrabe Analytical in case of Exchange option 
##############################################
    qs=concat([0,0])
# Script_Compare_Exchange.m:41
    
    ref=Price_Exchange_Option_Margrabe_2D(S_0s(1),S_0s(2),T,rho,sigmas(1),sigmas(2),qs(1),qs(2))
# Script_Compare_Exchange.m:43
    fprintf('\n--------------------------------------------------\n')
    fprintf('Method       |    Price    |    Err   |  CPU \n')
    fprintf('--------------------------------------------------\n')
    fprintf('Ref (Magrabe)| %.8f  |          |       \n',ref)
    fprintf('--------------------------------------------------\n')
    ##############################################
### COS (code available for K==0 only, ie exchange option)
##############################################
    
    addpath('../../Fourier/COS')
    tic
    N=22
# Script_Compare_Exchange.m:59
    L=9
# Script_Compare_Exchange.m:59
    price_cos=Price_Exchange_COS2D(S_0s,T,r,sigmas(1),sigmas(2),rho,N,L)
# Script_Compare_Exchange.m:60
    time_cos=copy(toc)
# Script_Compare_Exchange.m:61
    fprintf('COS-2D       | %.8f  | %.2e | %.4f \n',price_cos,abs(ref - price_cos),time_cos)
    ##############################################
### CTMC Approximation Method
##############################################
    addpath('../../CTMC/')
    addpath('../../CTMC/Diffusion_2D')
    contractParams=cellarray([])
# Script_Compare_Exchange.m:70
    contractParams.contract = copy(1)
# Script_Compare_Exchange.m:71
    
    contractParams.payoff_type = copy(4)
# Script_Compare_Exchange.m:72
    
    contractParams.K = copy(0)
# Script_Compare_Exchange.m:73
    contractParams.call = copy(call)
# Script_Compare_Exchange.m:74
    M=10
# Script_Compare_Exchange.m:75
    
    params=cellarray([])
# Script_Compare_Exchange.m:77
    params.num_devs = copy(5)
# Script_Compare_Exchange.m:78
    
    params.GridMultParam = copy(0.1)
# Script_Compare_Exchange.m:79
    
    params.gridMethod = copy(7)
# Script_Compare_Exchange.m:80
    
    params.m_0 = copy(120)
# Script_Compare_Exchange.m:81
    
    tic
    vals,c_index_1,c_index_2,y_1,y_2=price_2d_ctmc(S_0s,T,r,rho,sigmas,qs,params,contractParams,M,nargout=5)
# Script_Compare_Exchange.m:84
    price_ctmc=vals(c_index_1,c_index_2)
# Script_Compare_Exchange.m:85
    time_ctmc=copy(toc)
# Script_Compare_Exchange.m:86
    fprintf('CTMC         | %.8f  | %.2e | %.4f \n',price_ctmc,abs(ref - price_ctmc),time_ctmc)
    ##############################################
### Monte Carlo
##############################################
    addpath('../../Monte_Carlo')
    tic
    N_sim=10 ** 5
# Script_Compare_Exchange.m:97
    M=200
# Script_Compare_Exchange.m:97
    dt=T / M
# Script_Compare_Exchange.m:98
    drifts=concat([r,r]) - qs
# Script_Compare_Exchange.m:99
    exponential=1
# Script_Compare_Exchange.m:100
    
    paths_1,paths_2=Simulate_Diffusion_2D(S_0s,drifts,sigmas,rho,N_sim,M,dt,exponential,nargout=2)
# Script_Compare_Exchange.m:101
    S_1=paths_1(arange(),M + 1)
# Script_Compare_Exchange.m:102
    S_2=paths_2(arange(),M + 1)
# Script_Compare_Exchange.m:103
    payoffs=max(S_1 - S_2,0)
# Script_Compare_Exchange.m:105
    price_MC=dot(exp(dot(- r,T)),mean(payoffs))
# Script_Compare_Exchange.m:106
    stderr=dot(exp(dot(- r,T)),std(payoffs)) / sqrt(N_sim)
# Script_Compare_Exchange.m:107
    price_MC_L=price_MC - dot(2,stderr)
# Script_Compare_Exchange.m:108
    price_MC_U=price_MC + dot(2,stderr)
# Script_Compare_Exchange.m:108
    time_MC=copy(toc)
# Script_Compare_Exchange.m:109
    fprintf('MC           |[%.3f,%.3f]| %.2e | %.4f \n',price_MC_L,price_MC_U,abs(ref - price_MC),time_MC)
    fprintf('--------------------------------------------------\n')