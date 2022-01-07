# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_BlackScholes_Plot_Greeks_For_Strike.m

    ##################################################################
# Descritpion: Script to plot Delta/Gamma of European option under Black Scholes Merton Model
# Author:      Justin Kirkby
##################################################################
    
    # ---------------------
#  Contract/Market Params
# ---------------------
    call=1
# Script_BlackScholes_Plot_Greeks_For_Strike.m:9
    
    K=100
# Script_BlackScholes_Plot_Greeks_For_Strike.m:10
    
    r=0.1
# Script_BlackScholes_Plot_Greeks_For_Strike.m:11
    
    q=0.0
# Script_BlackScholes_Plot_Greeks_For_Strike.m:12
    
    T=1
# Script_BlackScholes_Plot_Greeks_For_Strike.m:13
    
    moneyness=concat([arange(0.2,1.8,0.01)])
# Script_BlackScholes_Plot_Greeks_For_Strike.m:15
    Svec=dot(K,moneyness)
# Script_BlackScholes_Plot_Greeks_For_Strike.m:16
    
    sigma=0.15
# Script_BlackScholes_Plot_Greeks_For_Strike.m:18
    
    ########################
# Plots
########################
    
    # Plot Prices (as function of moneyness)
    h=figure()
# Script_BlackScholes_Plot_Greeks_For_Strike.m:25
    subplot(5,1,1)
    values=BSM_Greeks(0,S_0,sigma,r,q,T,Kvec,call)
# Script_BlackScholes_Plot_Greeks_For_Strike.m:27
    plot(moneyness,values)
    grid('on')
    ylabel('price')
    
    # Plot Deltas (as function of moneyness)
    subplot(5,1,2)
    values=BSM_Greeks(1,S_0,sigma,r,q,T,Kvec,call)
# Script_BlackScholes_Plot_Greeks_For_Strike.m:34
    plot(moneyness,values)
    grid('on')
    ylabel('delta')
    
    # Plot Gammas (as function of moneyness)
    subplot(5,1,3)
    values=BSM_Greeks(2,S_0,sigma,r,q,T,Kvec,call)
# Script_BlackScholes_Plot_Greeks_For_Strike.m:40
    plot(moneyness,values)
    grid('on')
    ylabel('gamma')
    
    # Plot Thetas (as function of moneyness)
    subplot(5,1,4)
    values=BSM_Greeks(3,S_0,sigma,r,q,T,Kvec,call)
# Script_BlackScholes_Plot_Greeks_For_Strike.m:47
    plot(moneyness,values)
    grid('on')
    ylabel('theta')
    
    # Plot Vegas (as function of moneyness)
    subplot(5,1,5)
    values=BSM_Greeks(4,S_0,sigma,r,q,T,Kvec,call)
# Script_BlackScholes_Plot_Greeks_For_Strike.m:54
    plot(moneyness,values)
    grid('on')
    ylabel('vegas')
    xlabel('$K/S_0$','interpreter','latex')