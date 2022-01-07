# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_BlackScholes_Prices_Greeks.m

    ##################################################################
# Descritpion: Script to calc prices and Greeks European options under Black Scholes Merton Model
# Author:      Justin Kirkby
##################################################################
    
    # ---------------------
#  Contract/Market Params
# ---------------------
    call=1
# Script_BlackScholes_Prices_Greeks.m:9
    
    S_0=100
# Script_BlackScholes_Prices_Greeks.m:10
    
    r=0.0
# Script_BlackScholes_Prices_Greeks.m:11
    
    q=0.0
# Script_BlackScholes_Prices_Greeks.m:12
    
    T=1
# Script_BlackScholes_Prices_Greeks.m:13
    
    Kvec=dot(S_0,concat([arange(0.2,1.8,0.01)]))
# Script_BlackScholes_Prices_Greeks.m:14
    
    sigma=0.2
# Script_BlackScholes_Prices_Greeks.m:16
    
    # ---------------------
# Select what to calculate
# G = Greek: 
#         0:Price
#         1:Delta, 2:Gamma, 3:Theta
#         4:Vega,  5:Rho,   6:Vanna
#         7:Vomma
#  
# ---------------------
    G=0
# Script_BlackScholes_Prices_Greeks.m:27
    # ---------------------
    
    values=BSM_Greeks(G,S_0,sigma,r,q,T,Kvec,call)
# Script_BlackScholes_Prices_Greeks.m:30
    # Plot
    plot(Kvec,values)
    ylabel('price (or greek)')
    xlabel('strike')
    grid('on')