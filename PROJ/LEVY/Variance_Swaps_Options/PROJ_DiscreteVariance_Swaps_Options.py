# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# PROJ_DiscreteVariance_Swaps_Options.m

    
@function
def PROJ_DiscreteVariance_Swaps_Options(N=None,alph=None,M=None,r=None,T=None,K=None,rnCHF=None,contract=None,*args,**kwargs):
    varargin = PROJ_DiscreteVariance_Swaps_Options.varargin
    nargin = PROJ_DiscreteVariance_Swaps_Options.nargin

    #########################################################
# About: Pricing Function for Variance Swaps and Options using PROJ method
# Models Supported: Levy Processes, including jump diffusions and Black-Scholes model
# Returns: price of contract
# Author: Justin Lars Kirkby
    
    # ----------------------
# Contract/Model Params 
# ----------------------
# K   = strike (only matters for an option, but is always required)
# r   = interest rate (e.g. 0.05)
# T   = time remaining until maturity (in years, e.g. T=1)
# M   = number of subintervals of [0,T] (total of M+1 monitoring points in time grid, including S_0)
# contract =  1 for for variance swap, 3 for variance call  (other contracts not yet coded)
# rnCHF = risk netural characteristic function (function handle with single argument)
    
    # ----------------------
# Numerical (PROJ) Params 
# ----------------------
# alph  = grid with is 2*alph
# N     = number of grid/basis points (power of 2, e.g. 2^12), resolution = 2*alph/(N-1)
#########################################################
    
    dx=dot(2,alph) / (N - 1)
# PROJ_DiscreteVariance_Swaps_Options.m:25
    a=1 / dx
# PROJ_DiscreteVariance_Swaps_Options.m:26
    A=dot(32,a ** 4)
# PROJ_DiscreteVariance_Swaps_Options.m:27
    C_aN=A / N
# PROJ_DiscreteVariance_Swaps_Options.m:28
    xmin=dot((1 - N / 2),dx)
# PROJ_DiscreteVariance_Swaps_Options.m:29
    dxi=dot(dot(2,pi),a) / N
# PROJ_DiscreteVariance_Swaps_Options.m:31
    # ###################################################################
# ### PSI Matrix: 5-Point GAUSSIAN
# #################################################################
    
    NNM=copy(N)
# PROJ_DiscreteVariance_Swaps_Options.m:37
    
    PSI=zeros(N,NNM)
# PROJ_DiscreteVariance_Swaps_Options.m:39
    
    PSI[1,arange()]=ones(1,NNM)
# PROJ_DiscreteVariance_Swaps_Options.m:40
    #### Sample
    Neta=dot(5,(NNM)) + 15
# PROJ_DiscreteVariance_Swaps_Options.m:43
    
    Neta5=(NNM) + 3
# PROJ_DiscreteVariance_Swaps_Options.m:44
    g2=sqrt(5 - dot(2,sqrt(10 / 7))) / 6
# PROJ_DiscreteVariance_Swaps_Options.m:45
    g3=sqrt(5 + dot(2,sqrt(10 / 7))) / 6
# PROJ_DiscreteVariance_Swaps_Options.m:46
    v1=dot(0.5,128) / 225
# PROJ_DiscreteVariance_Swaps_Options.m:47
    v2=dot(0.5,(322 + dot(13,sqrt(70)))) / 900
# PROJ_DiscreteVariance_Swaps_Options.m:47
    v3=dot(0.5,(322 - dot(13,sqrt(70)))) / 900
# PROJ_DiscreteVariance_Swaps_Options.m:47
    thet=zeros(1,Neta)
# PROJ_DiscreteVariance_Swaps_Options.m:49
    
    thet[dot(5,(arange(1,Neta5))) - 2]=xmin - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1)))
# PROJ_DiscreteVariance_Swaps_Options.m:50
    thet[dot(5,(arange(1,Neta5))) - 4]=xmin - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) - dot(dx,g3)
# PROJ_DiscreteVariance_Swaps_Options.m:51
    thet[dot(5,(arange(1,Neta5))) - 3]=xmin - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) - dot(dx,g2)
# PROJ_DiscreteVariance_Swaps_Options.m:52
    thet[dot(5,(arange(1,Neta5))) - 1]=xmin - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) + dot(dx,g2)
# PROJ_DiscreteVariance_Swaps_Options.m:53
    thet[dot(5,(arange(1,Neta5)))]=xmin - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) + dot(dx,g3)
# PROJ_DiscreteVariance_Swaps_Options.m:54
    #### Weights
    sig=concat([- 1.5 - g3,- 1.5 - g2,- 1.5,- 1.5 + g2,- 1.5 + g3,- 0.5 - g3,- 0.5 - g2,- 0.5,- 0.5 + g2,- 0.5 + g3])
# PROJ_DiscreteVariance_Swaps_Options.m:57
    sig[arange(1,5)]=(sig(arange(1,5)) + 2) ** 3 / 6
# PROJ_DiscreteVariance_Swaps_Options.m:58
    sig[arange(6,10)]=2 / 3 - dot(0.5,(sig(arange(6,10))) ** 3) - (sig(arange(6,10))) ** 2
# PROJ_DiscreteVariance_Swaps_Options.m:59
    sig[concat([1,5,6,10])]=dot(v3,sig(concat([1,5,6,10])))
# PROJ_DiscreteVariance_Swaps_Options.m:61
    sig[concat([2,4,7,9])]=dot(v2,sig(concat([2,4,7,9])))
# PROJ_DiscreteVariance_Swaps_Options.m:61
    sig[concat([3,8])]=dot(v1,sig(concat([3,8])))
# PROJ_DiscreteVariance_Swaps_Options.m:61
    ##################################
###NEW STEP: multiple sig by Upsilon_{a,N}
    sig=dot(C_aN,sig)
# PROJ_DiscreteVariance_Swaps_Options.m:65
    ##################################
#### Fill Matrix
#### NOTE: this can be made MORE EFFICIENT by using symmetery of x^2
    
    zz=exp(dot(dot(1j,dxi),thet ** 2))
# PROJ_DiscreteVariance_Swaps_Options.m:71
    
    thet=copy(zz)
# PROJ_DiscreteVariance_Swaps_Options.m:72
    for j in arange(2,N).reshape(-1):
        PSI[j,arange()]=dot(sig(1),(thet(arange(1,Neta - 19,5)) + thet(arange(20,Neta,5)))) + dot(sig(2),(thet(arange(2,Neta - 18,5)) + thet(arange(19,Neta - 1,5)))) + dot(sig(3),(thet(arange(3,Neta - 17,5)) + thet(arange(18,Neta - 2,5)))) + dot(sig(4),(thet(arange(4,Neta - 16,5)) + thet(arange(17,Neta - 3,5)))) + dot(sig(5),(thet(arange(5,Neta - 15,5)) + thet(arange(16,Neta - 4,5)))) + dot(sig(6),(thet(arange(6,Neta - 14,5)) + thet(arange(15,Neta - 5,5)))) + dot(sig(7),(thet(arange(7,Neta - 13,5)) + thet(arange(14,Neta - 6,5)))) + dot(sig(8),(thet(arange(8,Neta - 12,5)) + thet(arange(13,Neta - 7,5)))) + dot(sig(9),(thet(arange(9,Neta - 11,5)) + thet(arange(12,Neta - 8,5)))) + dot(sig(10),(thet(arange(10,Neta - 10,5)) + thet(arange(11,Neta - 9,5))))
# PROJ_DiscreteVariance_Swaps_Options.m:75
        thet=multiply(thet,zz)
# PROJ_DiscreteVariance_Swaps_Options.m:86
    
    # ###################################################################
# ### Find phi_{Y_1}
# #################################################################
    
    xi=dot(dxi,(arange(1,N - 1)).T)
# PROJ_DiscreteVariance_Swaps_Options.m:94
    
    b0=1208 / 2520
# PROJ_DiscreteVariance_Swaps_Options.m:96
    b1=1191 / 2520
# PROJ_DiscreteVariance_Swaps_Options.m:96
    b2=120 / 2520
# PROJ_DiscreteVariance_Swaps_Options.m:96
    b3=1 / 2520
# PROJ_DiscreteVariance_Swaps_Options.m:96
    zeta=(sin(xi / (dot(2,a))) / xi) ** 4.0 / (b0 + dot(b1,cos(xi / a)) + dot(b2,cos(dot(2,xi) / a)) + dot(b3,cos(dot(3,xi) / a)))
# PROJ_DiscreteVariance_Swaps_Options.m:97
    hvec=multiply(exp(dot(dot(- 1j,xmin),xi)),zeta)
# PROJ_DiscreteVariance_Swaps_Options.m:98
    
    AA=1 / A
# PROJ_DiscreteVariance_Swaps_Options.m:101
    beta=concat([[AA],[multiply(rnCHF(xi),hvec)]])
# PROJ_DiscreteVariance_Swaps_Options.m:102
    
    beta=real(fft(beta))
# PROJ_DiscreteVariance_Swaps_Options.m:103
    phi=dot(PSI(arange(),arange(1,N)),beta)
# PROJ_DiscreteVariance_Swaps_Options.m:105
    #### FIND
    phi=phi ** M
# PROJ_DiscreteVariance_Swaps_Options.m:108
    
    ##########################################################################
##########################################################################
### Redfine xmin for the final inversion
    
    if contract == 1 or contract == 3:
        grid=dot(dx,(arange(0,N - 1)))
# PROJ_DiscreteVariance_Swaps_Options.m:115
        grid[1]=dx / 6
# PROJ_DiscreteVariance_Swaps_Options.m:116
    
    if contract == 1:
        xmin=0
# PROJ_DiscreteVariance_Swaps_Options.m:120
    else:
        if contract == 3:
            xmin=dot(K,T)
# PROJ_DiscreteVariance_Swaps_Options.m:122
    
    C_aN=dot(24,a ** 2) / N
# PROJ_DiscreteVariance_Swaps_Options.m:125
    dw=dot(dot(2,pi),a) / N
# PROJ_DiscreteVariance_Swaps_Options.m:126
    grand=dot(dw,(arange(1,N - 1)).T)
# PROJ_DiscreteVariance_Swaps_Options.m:127
    grand=multiply(multiply(exp(dot(dot(- 1j,xmin),grand)),phi(arange(2,N))),(sin(grand / (dot(2,a))) / grand) ** 2.0) / (2 + cos(grand / a))
# PROJ_DiscreteVariance_Swaps_Options.m:128
    ### Test with FILTER
    applyFilter=0
# PROJ_DiscreteVariance_Swaps_Options.m:131
    if applyFilter == 1:
        epsM=1.2204e-16
# PROJ_DiscreteVariance_Swaps_Options.m:133
        alphaeps=- log(epsM)
# PROJ_DiscreteVariance_Swaps_Options.m:134
        pp=8
# PROJ_DiscreteVariance_Swaps_Options.m:135
        filter=exp(dot(- alphaeps,(xi / (dot(dot(2,pi),a))) ** pp))
# PROJ_DiscreteVariance_Swaps_Options.m:136
        grand=multiply(grand,filter)
# PROJ_DiscreteVariance_Swaps_Options.m:137
    
    beta=real(fft(concat([[1 / (dot(24,a ** 2))],[grand]])))
# PROJ_DiscreteVariance_Swaps_Options.m:140
    
    if contract == 1 or contract == 3:
        price=dot(grid(arange(1,N / 2)),beta(arange(1,N / 2)))
# PROJ_DiscreteVariance_Swaps_Options.m:144
        price=dot(C_aN,price)
# PROJ_DiscreteVariance_Swaps_Options.m:145
    
    
    if contract == 1:
        price=price / T
# PROJ_DiscreteVariance_Swaps_Options.m:149
    else:
        if contract == 3:
            price=dot(exp(dot(- r,T)),price) / T
# PROJ_DiscreteVariance_Swaps_Options.m:151
        else:
            fprintf('Only contract types 1 and 3 are currently supported \n')
    
    return price
    
if __name__ == '__main__':
    pass
    