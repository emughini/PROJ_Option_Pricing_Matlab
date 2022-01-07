# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_BlackScholes_BinomialLattice.m

    ##################################################################
### BINOMIAL LATTICE OPTION PRICER
##################################################################
# Descritpion: Script to Price European/American options in Black-Scholes Models
#              using Binomial Lattice
# Author:      Justin Kirkby
##################################################################
    
    K=100
# Script_BlackScholes_BinomialLattice.m:9
    
    S_0=100
# Script_BlackScholes_BinomialLattice.m:10
    
    r=0.05
# Script_BlackScholes_BinomialLattice.m:11
    
    T=1
# Script_BlackScholes_BinomialLattice.m:12
    
    sigma=0.15
# Script_BlackScholes_BinomialLattice.m:13
    
    M=252
# Script_BlackScholes_BinomialLattice.m:14
    
    call=0
# Script_BlackScholes_BinomialLattice.m:15
    
    american=1
# Script_BlackScholes_BinomialLattice.m:16
    
    price_binomial=BinomialLattice_BlackScholes_func(S_0,K,r,T,sigma,M,call,american)
# Script_BlackScholes_BinomialLattice.m:18
    price_trinomial=TrinomialLattice_BlackScholes_func(S_0,K,r,T,sigma,M,call,american)
# Script_BlackScholes_BinomialLattice.m:19
    
    