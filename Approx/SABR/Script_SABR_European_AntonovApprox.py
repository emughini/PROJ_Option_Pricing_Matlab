# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_SABR_European_AntonovApprox.m

    ################################
# NOTE: This script and pricing function are in progress, and have not been well tested
###############################
    
    #Calculating forward value of the call with Antonov's mapping strategy
    T=1
# Script_SABR_European_AntonovApprox.m:6
    
    r=0.0
# Script_SABR_European_AntonovApprox.m:7
    
    F_0=1.1
# Script_SABR_European_AntonovApprox.m:8
    
    ModParams.v0 = copy(0.2)
# Script_SABR_European_AntonovApprox.m:10
    
    ModParams.beta = copy(0.7)
# Script_SABR_European_AntonovApprox.m:11
    
    ModParams.alpha = copy(0.08)
# Script_SABR_European_AntonovApprox.m:12
    
    ModParams.rho = copy(0)
# Script_SABR_European_AntonovApprox.m:13
    
    # ModParams.v0     = 0.25;  #Inital volatility
# ModParams.beta   = 0.6;  #Exponent
# ModParams.alpha     = 0.3;  #Vol-vol
# ModParams.rho     = -0.5; #Correlation
    
    Kvec=dot(F_0,concat([0.6,0.8,0.9,0.95,0.999,1.05,1.1,1.2,1.4]))
# Script_SABR_European_AntonovApprox.m:21
    call=0
# Script_SABR_European_AntonovApprox.m:22
    ### Price Strikes
    prices=zeros(length(Kvec),1)
# Script_SABR_European_AntonovApprox.m:25
    for k in arange(1,length(Kvec)).reshape(-1):
        K=Kvec(k)
# Script_SABR_European_AntonovApprox.m:27
        prices[k]=SABR_European_AntonovApprox(F_0,K,T,call,r,ModParams)
# Script_SABR_European_AntonovApprox.m:28
        fprintf('%.8f\n',prices(k))
    