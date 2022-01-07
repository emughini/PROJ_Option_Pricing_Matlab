# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# PROJ_Cliquet.m

    
@function
def PROJ_Cliquet(N=None,alph=None,M=None,r=None,q=None,T=None,rnCHF=None,contract=None,contractParams=None,*args,**kwargs):
    varargin = PROJ_Cliquet.varargin
    nargin = PROJ_Cliquet.nargin

    #########################################################
# About: Pricing Function for Cliquet-style options (Additive Cliquets) using PROJ method
# Models Supported: Levy Processes, including jump diffusions and Black-Scholes model
# Returns: price of contract
# Author: Justin Lars Kirkby
    
    # ----------------------
# Contract/Model Params 
# ----------------------
# M = number of subintervals of [0,T] (total of M+1 monitoring points in time grid, including S_0)
# r = interest rate (e.g. 0.05)
# q = dividend yield (e.g. 0.05)
# T = time to maturity (in years, e.g. T=1)
# rnCHF = risk netural characteristic function (function handle with single argument)
# contract: 1 = sum of local caps
#           2 = sum of local caps & floors
#           3 = cliquet: local & global caps & floors
#           4 = cliquet: local floor & cap, global floor, NO GLOBAL CAP (e.g. like Wilmott)  
#           5 = MPP: ie monthly point-to-point  or Monthly Cap Sum (Bernard, Li)
# contractParams - container with the required params, such as cap and floor
    
    # ----------------------
# Numerical (PROJ) Params 
# ----------------------
# N = number of grid/basis points (power of 2, e.g. 2^12), resolution = 2*alph/(N-1)
# alph = log-asset grid width param, grid with is 2*alph
#########################################################
    
    dx=dot(2,alph) / (N - 1)
# PROJ_Cliquet.m:30
    a=1 / dx
# PROJ_Cliquet.m:30
    dt=T / M
# PROJ_Cliquet.m:31
    xmin=dot((1 - N / 2),dx)
# PROJ_Cliquet.m:33
    
    ### Contract Parameters (Not all of these apply to every contact type)
    K=contractParams.K
# PROJ_Cliquet.m:36
    
    C=contractParams.C
# PROJ_Cliquet.m:38
    
    F=contractParams.F
# PROJ_Cliquet.m:39
    
    CG=contractParams.CG
# PROJ_Cliquet.m:40
    
    FG=contractParams.FG
# PROJ_Cliquet.m:41
    
    lc=log(1 + C)
# PROJ_Cliquet.m:44
    lf=log(1 + F)
# PROJ_Cliquet.m:45
    ### Choose xmin so that CAP lc is a member
    klc=floor(dot(a,(lc - xmin))) + 1
# PROJ_Cliquet.m:48
    
    xklc=xmin + dot((klc - 1),dx)
# PROJ_Cliquet.m:49
    xmin=xmin + (lc - xklc)
# PROJ_Cliquet.m:50
    
    klf=floor(dot(a,(lf - xmin))) + 1
# PROJ_Cliquet.m:52
    if contract == 1 or contract == 5:
        hlocalCF=lambda x=None: multiply((exp(x) - 1),(x < lc)) + dot(C,(x >= lc))
# PROJ_Cliquet.m:55
    else:
        if contract == 2 or contract == 3 or contract == 4:
            #NOTE: we should then possibly stretch the grid so that lf is a member
            if klc != klf:
                dx=(lc - lf) / (klc - klf)
# PROJ_Cliquet.m:59
                a=1 / dx
# PROJ_Cliquet.m:59
                xmin=lf - dot((klf - 1),dx)
# PROJ_Cliquet.m:60
            hlocalCF=lambda x=None: dot(F,(x <= lf)) + multiply(multiply((exp(x) - 1),(x < lc)),(x > lf)) + dot(C,(x >= lc))
# PROJ_Cliquet.m:62
    
    A=dot(32,a ** 4)
# PROJ_Cliquet.m:65
    C_aN=A / N
# PROJ_Cliquet.m:66
    dxi=dot(dot(2,pi),a) / N
# PROJ_Cliquet.m:67
    # ###################################################################
# ### PSI Matrix: 5-Point GAUSSIAN
# #################################################################
    if contract == 2 or contract == 3 or contract == 4:
        leftGridPoint=lf - dx
# PROJ_Cliquet.m:74
        NNM=klc - klf + 3
# PROJ_Cliquet.m:75
    else:
        if contract == 1 or contract == 5:
            leftGridPoint=copy(xmin)
# PROJ_Cliquet.m:77
            NNM=klc + 1
# PROJ_Cliquet.m:78
        else:
            #NOTE: this can be made more efficient by putting an upper bound, to reflect lc
            leftGridPoint=copy(xmin)
# PROJ_Cliquet.m:81
            NNM=copy(N)
# PROJ_Cliquet.m:82
    
    
    PSI=zeros(N - 1,NNM)
# PROJ_Cliquet.m:86
    
    #### Sample
    Neta=dot(5,(NNM)) + 15
# PROJ_Cliquet.m:89
    
    Neta5=(NNM) + 3
# PROJ_Cliquet.m:90
    g2=sqrt(5 - dot(2,sqrt(10 / 7))) / 6
# PROJ_Cliquet.m:91
    g3=sqrt(5 + dot(2,sqrt(10 / 7))) / 6
# PROJ_Cliquet.m:92
    v1=dot(0.5,128) / 225
# PROJ_Cliquet.m:93
    v2=dot(0.5,(322 + dot(13,sqrt(70)))) / 900
# PROJ_Cliquet.m:93
    v3=dot(0.5,(322 - dot(13,sqrt(70)))) / 900
# PROJ_Cliquet.m:93
    thet=zeros(1,Neta)
# PROJ_Cliquet.m:95
    
    thet[dot(5,(arange(1,Neta5))) - 2]=leftGridPoint - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1)))
# PROJ_Cliquet.m:96
    thet[dot(5,(arange(1,Neta5))) - 4]=leftGridPoint - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) - dot(dx,g3)
# PROJ_Cliquet.m:97
    thet[dot(5,(arange(1,Neta5))) - 3]=leftGridPoint - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) - dot(dx,g2)
# PROJ_Cliquet.m:98
    thet[dot(5,(arange(1,Neta5))) - 1]=leftGridPoint - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) + dot(dx,g2)
# PROJ_Cliquet.m:99
    thet[dot(5,(arange(1,Neta5)))]=leftGridPoint - dot(1.5,dx) + dot(dx,(arange(0,Neta5 - 1))) + dot(dx,g3)
# PROJ_Cliquet.m:100
    #### Weights
    sig=concat([- 1.5 - g3,- 1.5 - g2,- 1.5,- 1.5 + g2,- 1.5 + g3,- 0.5 - g3,- 0.5 - g2,- 0.5,- 0.5 + g2,- 0.5 + g3])
# PROJ_Cliquet.m:103
    sig[arange(1,5)]=(sig(arange(1,5)) + 2) ** 3 / 6
# PROJ_Cliquet.m:104
    sig[arange(6,10)]=2 / 3 - dot(0.5,(sig(arange(6,10))) ** 3) - (sig(arange(6,10))) ** 2
# PROJ_Cliquet.m:105
    sig[concat([1,5,6,10])]=dot(v3,sig(concat([1,5,6,10])))
# PROJ_Cliquet.m:107
    sig[concat([2,4,7,9])]=dot(v2,sig(concat([2,4,7,9])))
# PROJ_Cliquet.m:107
    sig[concat([3,8])]=dot(v1,sig(concat([3,8])))
# PROJ_Cliquet.m:107
    ##################################
###NEW STEP: multiple sig by Upsilon_{a,N}
    sig=dot(C_aN,sig)
# PROJ_Cliquet.m:111
    ##################################
#### Fill Matrix
#### NOTE: this can be made MORE EFFICIENT by using symmetery of x^2
    
    zz=exp(dot(dot(1j,dxi),hlocalCF(thet)))
# PROJ_Cliquet.m:117
    thet=copy(zz)
# PROJ_Cliquet.m:118
    for j in arange(1,N - 1).reshape(-1):
        PSI[j,arange()]=dot(sig(1),(thet(arange(1,Neta - 19,5)) + thet(arange(20,Neta,5)))) + dot(sig(2),(thet(arange(2,Neta - 18,5)) + thet(arange(19,Neta - 1,5)))) + dot(sig(3),(thet(arange(3,Neta - 17,5)) + thet(arange(18,Neta - 2,5)))) + dot(sig(4),(thet(arange(4,Neta - 16,5)) + thet(arange(17,Neta - 3,5)))) + dot(sig(5),(thet(arange(5,Neta - 15,5)) + thet(arange(16,Neta - 4,5)))) + dot(sig(6),(thet(arange(6,Neta - 14,5)) + thet(arange(15,Neta - 5,5)))) + dot(sig(7),(thet(arange(7,Neta - 13,5)) + thet(arange(14,Neta - 6,5)))) + dot(sig(8),(thet(arange(8,Neta - 12,5)) + thet(arange(13,Neta - 7,5)))) + dot(sig(9),(thet(arange(9,Neta - 11,5)) + thet(arange(12,Neta - 8,5)))) + dot(sig(10),(thet(arange(10,Neta - 10,5)) + thet(arange(11,Neta - 9,5))))
# PROJ_Cliquet.m:121
        thet=multiply(thet,zz)
# PROJ_Cliquet.m:132
    
    # ###################################################################
# ### Find phi_{Y_1}
# #################################################################
    
    xi=dot(dxi,(arange(1,N - 1)).T)
# PROJ_Cliquet.m:140
    
    b0=1208 / 2520
# PROJ_Cliquet.m:142
    b1=1191 / 2520
# PROJ_Cliquet.m:142
    b2=120 / 2520
# PROJ_Cliquet.m:142
    b3=1 / 2520
# PROJ_Cliquet.m:142
    zeta=(sin(xi / (dot(2,a))) / xi) ** 4.0 / (b0 + dot(b1,cos(xi / a)) + dot(b2,cos(dot(2,xi) / a)) + dot(b3,cos(dot(3,xi) / a)))
# PROJ_Cliquet.m:143
    hvec=multiply(exp(dot(dot(- 1j,xmin),xi)),zeta)
# PROJ_Cliquet.m:144
    
    AA=1 / A
# PROJ_Cliquet.m:147
    beta=concat([[AA],[multiply(rnCHF(xi),hvec)]])
# PROJ_Cliquet.m:148
    
    beta=real(fft(beta))
# PROJ_Cliquet.m:149
    if contract == 2 or contract == 3 or contract == 4:
        phi=dot(PSI,beta(arange(klf - 1,klc + 1)))
# PROJ_Cliquet.m:152
        sumBetaLeft=dot(C_aN,sum(beta(arange(1,klf - 2))))
# PROJ_Cliquet.m:153
        sumBetaRight=1 - sumBetaLeft - dot(C_aN,sum(beta(arange(klf - 1,klc + 1))))
# PROJ_Cliquet.m:154
        phi=phi + dot(exp(dot(dot(1j,F),xi)),sumBetaLeft) + dot(exp(dot(dot(1j,C),xi)),sumBetaRight)
# PROJ_Cliquet.m:155
    else:
        if contract == 1 or contract == 5:
            phi=dot(PSI,beta(arange(1,klc + 1)))
# PROJ_Cliquet.m:157
            sumBetaRight=dot(C_aN,sum(beta(arange(klc + 2,N))))
# PROJ_Cliquet.m:158
            phi=phi + dot(exp(dot(dot(1j,C),xi)),sumBetaRight)
# PROJ_Cliquet.m:159
        else:
            phi=dot(PSI,beta)
# PROJ_Cliquet.m:161
    
    phi=phi ** M
# PROJ_Cliquet.m:165
    
    ##########################################################################
##########################################################################
### Redfine xmin for the final inversion
    
    #REDO FOR contract == 2 or ==3
    if contract == 1 or contract == 2:
        ymin=dot(M,(exp(dot((r - q),dt)) - 1)) + dot((1 - N / 2),dx)
# PROJ_Cliquet.m:174
        #grid = ymin + dx*(0:N-1);
    else:
        if contract == 3:
            CminusF=CG - FG
# PROJ_Cliquet.m:177
            ymin=FG - dx
# PROJ_Cliquet.m:178
            kc=floor(dot(a,(CG - ymin))) + 1
# PROJ_Cliquet.m:179
            z=dot(a,(CG - (ymin + dot((kc - 1),dx))))
# PROJ_Cliquet.m:180
            z2=z ** 2
# PROJ_Cliquet.m:181
            z3=dot(z,z2)
# PROJ_Cliquet.m:181
            z4=dot(z,z3)
# PROJ_Cliquet.m:181
            z5=dot(z,z4)
# PROJ_Cliquet.m:181
            theta=zeros(1,N / 2)
# PROJ_Cliquet.m:183
            theta[1]=dx / 120
# PROJ_Cliquet.m:184
            theta[2]=dot(dx,7) / 30
# PROJ_Cliquet.m:185
            theta[3]=dot(dx,121) / 120
# PROJ_Cliquet.m:186
            theta[arange(4,kc - 2)]=dot(dx,(arange(2,kc - 4)))
# PROJ_Cliquet.m:187
            k=kc - 1
# PROJ_Cliquet.m:188
            theta[k]=dot(dx,(dot(k,(- z4 / 24 + z3 / 6 - z2 / 4 + z / 6 + 23 / 24)) - z5 / 30 + z4 / 6 - z3 / 3 + z2 / 3 - z / 6 - 59 / 30)) + dot(CminusF,(z - 1) ** 4) / 24
# PROJ_Cliquet.m:189
            k=copy(kc)
# PROJ_Cliquet.m:191
            theta[k]=dot(dx,(dot(k,(z4 / 8 - z3 / 3 + dot(2,z) / 3 + 0.5)) + z5 / 10 - z4 / 2 + dot(2,z3) / 3 + z2 / 3 - dot(4,z) / 3 - 37 / 30)) + dot(CminusF,(- z4 / 8 + z3 / 3 - dot(2,z) / 3 + 1 / 2))
# PROJ_Cliquet.m:192
            k=kc + 1
# PROJ_Cliquet.m:194
            theta[k]=dot(dx,(dot(k,(- z4 / 8 + z3 / 6 + z2 / 4 + z / 6 + 1 / 24)) - z5 / 10 + z4 / 2 - z3 / 3 - dot(2,z2) / 3 - z / 2 - 2 / 15)) + dot(CminusF,(0.5 + dot(1 / 24,(dot(3,z4) - dot(4,z3) - dot(6,z2) - dot(4,z) + 11))))
# PROJ_Cliquet.m:195
            k=kc + 2
# PROJ_Cliquet.m:197
            theta[k]=dot(dx,(z5 / 30 + dot((k - 4),z4) / 24)) + dot(CminusF,(1 - z4 / 24))
# PROJ_Cliquet.m:198
            theta[arange(kc + 3,N / 2)]=CminusF
# PROJ_Cliquet.m:199
        else:
            if contract == 4 or contract == 5:
                ymin=FG - dx
# PROJ_Cliquet.m:201
                theta=zeros(1,N / 2)
# PROJ_Cliquet.m:202
                theta[1]=dx / 120
# PROJ_Cliquet.m:203
                theta[2]=dot(dx,7) / 30
# PROJ_Cliquet.m:204
                theta[3]=dot(dx,121) / 120
# PROJ_Cliquet.m:205
                theta[arange(4,N / 2)]=dot(dx,(arange(2,N / 2 - 2)))
# PROJ_Cliquet.m:206
    
    ### Filtering (optional)
    applyFilter=0
# PROJ_Cliquet.m:211
    
    if applyFilter == 1:
        epsM=1.2204e-16
# PROJ_Cliquet.m:213
        alphaeps=- log(epsM)
# PROJ_Cliquet.m:214
        pp=4
# PROJ_Cliquet.m:215
        filter=exp(dot(- alphaeps,(xi / (dot(dot(2,pi),a))) ** pp))
# PROJ_Cliquet.m:216
        hvec=multiply(multiply(filter,exp(dot(dot(- 1j,ymin),xi))),zeta)
# PROJ_Cliquet.m:217
    else:
        hvec=multiply(exp(dot(dot(- 1j,ymin),xi)),zeta)
# PROJ_Cliquet.m:219
    
    beta=real(fft(concat([[1 / A],[multiply(hvec,phi)]])))
# PROJ_Cliquet.m:223
    # Final pricing step, depends on contract type
    if contract == 1 or contract == 2:
        grid=ymin + dot(dx,(arange(0,N - 1)))
# PROJ_Cliquet.m:227
        price=dot(grid(arange(1,N)),beta(arange(1,N)))
# PROJ_Cliquet.m:228
        price=dot(dot(dot(K,exp(dot(- r,T))),C_aN),price)
# PROJ_Cliquet.m:229
    else:
        if contract == 3 or contract == 4 or contract == 5:
            price=dot(theta,beta(arange(1,N / 2)))
# PROJ_Cliquet.m:231
            price=dot(dot(K,exp(dot(- r,T))),(FG + dot(C_aN,price)))
# PROJ_Cliquet.m:232
    
    return price
    
if __name__ == '__main__':
    pass
    