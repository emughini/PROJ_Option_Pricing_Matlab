# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# PROJ_MultiplicativeCliquet.m

    
@function
def PROJ_MultiplicativeCliquet(N=None,alph=None,M=None,r=None,T=None,rnCHF=None,contract=None,contractParams=None,*args,**kwargs):
    varargin = PROJ_MultiplicativeCliquet.varargin
    nargin = PROJ_MultiplicativeCliquet.nargin

    # About: Pricing Function for Cliquet-style options (Multiplicative Cliquets) using PROJ method
# Returns: price of contract
# Models Supported: Levy Processes, including jump diffusions and Black-Scholes model
# Author: Justin Lars Kirkby
    
    # ----------------------
# Contract/Model Params 
# ----------------------
# M = number of subintervals of [0,T] (total of M+1 monitoring points in time grid, including S_0)
# r = interest rate (e.g. 0.05)
# T = time to maturity (in years, e.g. T=1)
# rnCHF = risk netural characteristic function (function handle with single argument)
# contract: 6 = Multiplicative Style Cliquet (e.g see Hieber)
# contractParams = container with the required params, such as cap and floor
    
    # ----------------------
# Numerical (PROJ) Params 
# ----------------------
# N    = number of grid/basis points (power of 2, e.g. 2^12), resolution = 2*alph/(N-1)
# alph = log-asset grid width param, grid with is 2*alph
#########################################################
    
    dx=dot(2,alph) / (N - 1)
# PROJ_MultiplicativeCliquet.m:24
    a=1 / dx
# PROJ_MultiplicativeCliquet.m:24
    xmin=dot((1 - N / 2),dx)
# PROJ_MultiplicativeCliquet.m:26
    
    ### Contract Parameters (Not all of these apply to every contact type)
    K=contractParams.K
# PROJ_MultiplicativeCliquet.m:29
    
    C=contractParams.C
# PROJ_MultiplicativeCliquet.m:30
    
    F=contractParams.F
# PROJ_MultiplicativeCliquet.m:31
    
    Alpha=contractParams.Alpha
# PROJ_MultiplicativeCliquet.m:32
    ###########################
    
    lc=log(C) / Alpha
# PROJ_MultiplicativeCliquet.m:35
    lf=log(F) / Alpha
# PROJ_MultiplicativeCliquet.m:36
    ### Choose xmin so that CAP lc is a member
    klc=floor(dot(a,(lc - xmin))) + 1
# PROJ_MultiplicativeCliquet.m:39
    
    xklc=xmin + dot((klc - 1),dx)
# PROJ_MultiplicativeCliquet.m:40
    xmin=xmin + (lc - xklc)
# PROJ_MultiplicativeCliquet.m:41
    
    klf=floor(dot(a,(lf - xmin))) + 1
# PROJ_MultiplicativeCliquet.m:43
    if contract == 6:
        #NOTE: we should then possibly stretch the grid so that lf is a member
        if klc != klf:
            dx=(lc - lf) / (klc - klf)
# PROJ_MultiplicativeCliquet.m:48
            a=1 / dx
# PROJ_MultiplicativeCliquet.m:48
            xmin=lf - dot((klf - 1),dx)
# PROJ_MultiplicativeCliquet.m:49
        hlocalCF=lambda x=None: dot(F,(x <= lf)) + multiply(multiply(exp(dot(Alpha,x)),(x < lc)),(x > lf)) + dot(C,(x >= lc))
# PROJ_MultiplicativeCliquet.m:51
    
    A=dot(32,a ** 4)
# PROJ_MultiplicativeCliquet.m:54
    C_aN=A / N
# PROJ_MultiplicativeCliquet.m:55
    dxi=dot(dot(2,pi),a) / N
# PROJ_MultiplicativeCliquet.m:56
    # ###################################################################
# ### PSI Matrix: 5-Point GAUSSIAN
# #################################################################
    if contract == 6:
        leftGridPoint=lf - dx
# PROJ_MultiplicativeCliquet.m:62
        NNM=klc - klf + 3
# PROJ_MultiplicativeCliquet.m:63
    
    #### Sample
    Neta=dot(5,(NNM)) + 15
# PROJ_MultiplicativeCliquet.m:67
    
    Neta5=(NNM) + 3
# PROJ_MultiplicativeCliquet.m:68
    g2=sqrt(5 - dot(2,sqrt(10 / 7))) / 6
# PROJ_MultiplicativeCliquet.m:69
    g3=sqrt(5 + dot(2,sqrt(10 / 7))) / 6
# PROJ_MultiplicativeCliquet.m:70
    v1=dot(0.5,128) / 225
# PROJ_MultiplicativeCliquet.m:71
    v2=dot(0.5,(322 + dot(13,sqrt(70)))) / 900
# PROJ_MultiplicativeCliquet.m:71
    v3=dot(0.5,(322 - dot(13,sqrt(70)))) / 900
# PROJ_MultiplicativeCliquet.m:71
    thet=zeros(1,Neta)
# PROJ_MultiplicativeCliquet.m:73
    
    thet[dot(5,(arange(1,Neta5))) - 2]=leftGridPoint - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1)))
# PROJ_MultiplicativeCliquet.m:74
    thet[dot(5,(arange(1,Neta5))) - 4]=leftGridPoint - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) - dot(dx,g3)
# PROJ_MultiplicativeCliquet.m:75
    thet[dot(5,(arange(1,Neta5))) - 3]=leftGridPoint - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) - dot(dx,g2)
# PROJ_MultiplicativeCliquet.m:76
    thet[dot(5,(arange(1,Neta5))) - 1]=leftGridPoint - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) + dot(dx,g2)
# PROJ_MultiplicativeCliquet.m:77
    thet[dot(5,(arange(1,Neta5)))]=leftGridPoint - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) + dot(dx,g3)
# PROJ_MultiplicativeCliquet.m:78
    #### Weights
    sig=concat([- 1.5 - g3,- 1.5 - g2,- 1.5,- 1.5 + g2,- 1.5 + g3,- 0.5 - g3,- 0.5 - g2,- 0.5,- 0.5 + g2,- 0.5 + g3])
# PROJ_MultiplicativeCliquet.m:81
    sig[arange(1,5)]=(sig(arange(1,5)) + 2) ** 3 / 6
# PROJ_MultiplicativeCliquet.m:82
    sig[arange(6,10)]=2 / 3 - dot(0.5,(sig(arange(6,10))) ** 3) - (sig(arange(6,10))) ** 2
# PROJ_MultiplicativeCliquet.m:83
    sig[concat([1,5,6,10])]=dot(v3,sig(concat([1,5,6,10])))
# PROJ_MultiplicativeCliquet.m:85
    sig[concat([2,4,7,9])]=dot(v2,sig(concat([2,4,7,9])))
# PROJ_MultiplicativeCliquet.m:85
    sig[concat([3,8])]=dot(v1,sig(concat([3,8])))
# PROJ_MultiplicativeCliquet.m:85
    ##################################
#### Fill Matrix
#### NOTE: this can be made MORE EFFICIENT by using symmetery of x^2
    
    thet=hlocalCF(thet)
# PROJ_MultiplicativeCliquet.m:92
    ThetaTilde=dot(sig(1),(thet(arange(1,Neta - 19,5)) + thet(arange(20,Neta,5)))) + dot(sig(2),(thet(arange(2,Neta - 18,5)) + thet(arange(19,Neta - 1,5)))) + dot(sig(3),(thet(arange(3,Neta - 17,5)) + thet(arange(18,Neta - 2,5)))) + dot(sig(4),(thet(arange(4,Neta - 16,5)) + thet(arange(17,Neta - 3,5)))) + dot(sig(5),(thet(arange(5,Neta - 15,5)) + thet(arange(16,Neta - 4,5)))) + dot(sig(6),(thet(arange(6,Neta - 14,5)) + thet(arange(15,Neta - 5,5)))) + dot(sig(7),(thet(arange(7,Neta - 13,5)) + thet(arange(14,Neta - 6,5)))) + dot(sig(8),(thet(arange(8,Neta - 12,5)) + thet(arange(13,Neta - 7,5)))) + dot(sig(9),(thet(arange(9,Neta - 11,5)) + thet(arange(12,Neta - 8,5)))) + dot(sig(10),(thet(arange(10,Neta - 10,5)) + thet(arange(11,Neta - 9,5))))
# PROJ_MultiplicativeCliquet.m:95
    ####################################
    
    xi=dot(dxi,(arange(1,N - 1)).T)
# PROJ_MultiplicativeCliquet.m:108
    
    b0=1208 / 2520
# PROJ_MultiplicativeCliquet.m:110
    b1=1191 / 2520
# PROJ_MultiplicativeCliquet.m:110
    b2=120 / 2520
# PROJ_MultiplicativeCliquet.m:110
    b3=1 / 2520
# PROJ_MultiplicativeCliquet.m:110
    zeta=(sin(xi / (dot(2,a))) / xi) ** 4.0 / (b0 + dot(b1,cos(xi / a)) + dot(b2,cos(dot(2,xi) / a)) + dot(b3,cos(dot(3,xi) / a)))
# PROJ_MultiplicativeCliquet.m:111
    hvec=multiply(exp(dot(dot(- 1j,xmin),xi)),zeta)
# PROJ_MultiplicativeCliquet.m:112
    
    AA=1 / A
# PROJ_MultiplicativeCliquet.m:115
    beta=concat([[AA],[multiply(rnCHF(xi),hvec)]])
# PROJ_MultiplicativeCliquet.m:116
    
    beta=real(fft(beta))
# PROJ_MultiplicativeCliquet.m:117
    if contract == 6:
        theta=zeros(1,N)
# PROJ_MultiplicativeCliquet.m:121
        theta[arange(1,klf - 2)]=F
# PROJ_MultiplicativeCliquet.m:122
        theta[arange(klf - 1,klc + 1)]=ThetaTilde
# PROJ_MultiplicativeCliquet.m:123
        theta[arange(klc + 2,N)]=C
# PROJ_MultiplicativeCliquet.m:124
        price=dot(theta,beta(arange(1,N)))
# PROJ_MultiplicativeCliquet.m:126
        price=dot(dot(K,exp(dot(- r,T))),(dot(C_aN,price)) ** M)
# PROJ_MultiplicativeCliquet.m:127
    
    return price
    
if __name__ == '__main__':
    pass
    