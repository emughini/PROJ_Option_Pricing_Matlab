# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# PROJ_Bermudan_Put.m

    
@function
def PROJ_Bermudan_Put(M=None,S_0=None,W=None,r=None,T=None,rnCHF=None,N=None,alph=None,*args,**kwargs):
    varargin = PROJ_Bermudan_Put.varargin
    nargin = PROJ_Bermudan_Put.nargin

    #########################################################
# About: Pricing Function for Bermudan Put Options using PROJ method
# Models Supported: Levy Processes, including jump diffusions and Black-Scholes model
# Returns: price of contract
# Author: Justin Lars Kirkby
    
    # ----------------------
# Contract/Model Params 
# ----------------------
# S_0 = initial stock price, 
# W   = strike, 
# r   = interest rate, 
# T   = time remaining until maturity
# M   = number of subintervals of [0,T] (total of M+1 monitoring points in time grid, including S_0)
# rnCHF = risk netural characteristic function (function handle with single argument)
    
    # ----------------------
# Numerical (PROJ) Params 
# ----------------------
# alph =  grid with is 2*alph
# N  = number of grid points (power of 2, e.g. 2^12), resolution = 2*alph/(N-1)
#########################################################
    
    dt=T / M
# PROJ_Bermudan_Put.m:25
    K=N / 2
# PROJ_Bermudan_Put.m:26
    dx=dot(2,alph) / (N - 1)
# PROJ_Bermudan_Put.m:28
    a=1 / dx
# PROJ_Bermudan_Put.m:28
    ThetM=zeros(K,1)
# PROJ_Bermudan_Put.m:30
    Cons3=1 / 48
# PROJ_Bermudan_Put.m:31
    Cons4=1 / 12
# PROJ_Bermudan_Put.m:32
    lws=log(W / S_0)
# PROJ_Bermudan_Put.m:34
    
    # Will perturb so that log(S_0/S_0)=0 is a member ... note: xnbar = lws
    
    nnot=K / 2
# PROJ_Bermudan_Put.m:38
    dxtil=1 / a
# PROJ_Bermudan_Put.m:39
    
    nbar=floor(dot(lws,a) + K / 2)
# PROJ_Bermudan_Put.m:40
    if abs(lws) < dxtil:
        dx=copy(dxtil)
# PROJ_Bermudan_Put.m:42
    else:
        if lws < 0:
            dx=lws / (1 + nbar - K / 2)
# PROJ_Bermudan_Put.m:44
            nbar=nbar + 1
# PROJ_Bermudan_Put.m:45
        else:
            if lws > 0:
                dx=lws / (nbar - K / 2)
# PROJ_Bermudan_Put.m:47
    
    #### Populate Beta coefficients for orthogonal projection
    a=1 / dx
# PROJ_Bermudan_Put.m:52
    xmin=dot((1 - K / 2),dx)
# PROJ_Bermudan_Put.m:53
    a2=a ** 2
# PROJ_Bermudan_Put.m:56
    Cons2=dot(dot(24,a2),exp(dot(- r,dt))) / N
# PROJ_Bermudan_Put.m:57
    zmin=dot((1 - K),dx)
# PROJ_Bermudan_Put.m:58
    
    dw=dot(dot(2,pi),a) / N
# PROJ_Bermudan_Put.m:60
    grand=(arange(dw,dot((N - 1),dw),dw))
# PROJ_Bermudan_Put.m:61
    grand=multiply(multiply(exp(dot(dot(- 1j,zmin),grand)),rnCHF(grand)),(sin(grand / (dot(2,a))) / grand) ** 2.0) / (2 + cos(grand / a))
# PROJ_Bermudan_Put.m:62
    beta=dot(Cons2,real(fft(concat([1 / (dot(24,a2)),grand]))))
# PROJ_Bermudan_Put.m:63
    
    toepM=concat([[beta(arange(K,1,- 1)).T],[0],[beta(arange(dot(2,K) - 1,K,- 1),+ 1).T]])
# PROJ_Bermudan_Put.m:65
    toepM=fft(toepM)
# PROJ_Bermudan_Put.m:66
    #### Initial terminal payoff coefficients (recursion proceeds backwards in time)
    Gs=zeros(K,1)
# PROJ_Bermudan_Put.m:69
    Gs[arange(1,nbar)]=dot(exp(xmin + dot(dx,(arange(0,nbar - 1)))),S_0)
# PROJ_Bermudan_Put.m:70
    ######  Gaussian Quadudrature Constants
    q_plus=(1 + sqrt(3 / 5)) / 2
# PROJ_Bermudan_Put.m:74
    q_minus=(1 - sqrt(3 / 5)) / 2
# PROJ_Bermudan_Put.m:74
    b3=sqrt(15)
# PROJ_Bermudan_Put.m:75
    b4=b3 / 10
# PROJ_Bermudan_Put.m:75
    #### PAYOFF CONSTANTS-----------------------------------
    varthet_01=dot(exp(dot(0.5,dx)),(dot(5,cosh(dot(b4,dx))) - dot(b3,sinh(dot(b4,dx))) + 4)) / 18
# PROJ_Bermudan_Put.m:78
    varthet_m10=dot(exp(dot(- 0.5,dx)),(dot(5,cosh(dot(b4,dx))) + dot(b3,sinh(dot(b4,dx))) + 4)) / 18
# PROJ_Bermudan_Put.m:79
    varthet_star=varthet_01 + varthet_m10
# PROJ_Bermudan_Put.m:80
    ThetM[nbar]=dot(W,(0.5 - varthet_m10))
# PROJ_Bermudan_Put.m:82
    ThetM[arange(1,nbar - 1)]=W - dot(varthet_star,Gs(arange(1,nbar - 1)))
# PROJ_Bermudan_Put.m:83
    Gs[arange(1,nbar)]=W - Gs(arange(1,nbar))
# PROJ_Bermudan_Put.m:84
    # #### Compute Augmentation (Not used in this version, but left here for reference, see below where it would be used)
# toepL = [zeros(K,1); 0 ; beta(K-1:-1:1)'];
# toepL = fft(toepL);
# Thetbar2 = W - S_0*varthet_star*exp(xmin - dx*(K:-1:1))';
# p = ifft(toepL.*fft([Thetbar2; zeros(K,1)]));
# theta_aug  = p(1:K);  #already includes the exp(-r*dt) through Beta
    
    #######
    p=ifft(multiply(toepM,fft(concat([[ThetM(arange(1,K))],[zeros(K,1)]]))))
# PROJ_Bermudan_Put.m:94
    Cont=p(arange(1,K))
# PROJ_Bermudan_Put.m:95
    
    #######
    
    Thet=zeros(K,1)
# PROJ_Bermudan_Put.m:98
    kstr=nbar + 1
# PROJ_Bermudan_Put.m:100
    for m in arange(M - 2,0,- 1).reshape(-1):
        while kstr > 1 and Cont(kstr) > Gs(kstr):

            kstr=kstr - 1
# PROJ_Bermudan_Put.m:105

        if kstr >= 2:
            xkstr=xmin + dot((kstr - 1),dx)
# PROJ_Bermudan_Put.m:108
            Ck1=Cont(kstr - 1)
# PROJ_Bermudan_Put.m:110
            Ck2=Cont(kstr)
# PROJ_Bermudan_Put.m:110
            Ck3=Cont(kstr + 1)
# PROJ_Bermudan_Put.m:110
            Gk2=Gs(kstr)
# PROJ_Bermudan_Put.m:112
            Gk3=Gs(kstr + 1)
# PROJ_Bermudan_Put.m:112
            tmp1=Ck2 - Gk2
# PROJ_Bermudan_Put.m:114
            tmp2=Ck3 - Gk3
# PROJ_Bermudan_Put.m:114
            xstrs=(dot((xkstr + dx),tmp1) - dot(xkstr,tmp2)) / (tmp1 - tmp2)
# PROJ_Bermudan_Put.m:115
        else:
            xkstr=copy(xmin)
# PROJ_Bermudan_Put.m:117
            kstr=1
# PROJ_Bermudan_Put.m:118
            xstrs=copy(xmin)
# PROJ_Bermudan_Put.m:118
            Ck2=Cont(kstr)
# PROJ_Bermudan_Put.m:119
            Ck1=copy(Ck2)
# PROJ_Bermudan_Put.m:119
            Ck3=Cont(kstr + 1)
# PROJ_Bermudan_Put.m:119
        rho=xstrs - xkstr
# PROJ_Bermudan_Put.m:122
        zeta=dot(a,rho)
# PROJ_Bermudan_Put.m:123
        zeta2=zeta ** 2
# PROJ_Bermudan_Put.m:125
        zeta3=dot(zeta,zeta2)
# PROJ_Bermudan_Put.m:125
        zeta4=dot(zeta,zeta3)
# PROJ_Bermudan_Put.m:125
        zeta_plus=dot(zeta,q_plus)
# PROJ_Bermudan_Put.m:127
        zeta_minus=dot(zeta,q_minus)
# PROJ_Bermudan_Put.m:127
        rho_plus=dot(rho,q_plus)
# PROJ_Bermudan_Put.m:128
        rho_minus=dot(rho,q_minus)
# PROJ_Bermudan_Put.m:128
        ed1=exp(rho_minus)
# PROJ_Bermudan_Put.m:130
        ed2=exp(rho / 2)
# PROJ_Bermudan_Put.m:130
        ed3=exp(rho_plus)
# PROJ_Bermudan_Put.m:130
        dbar_1=zeta2 / 2
# PROJ_Bermudan_Put.m:132
        dbar_0=zeta - dbar_1
# PROJ_Bermudan_Put.m:133
        d_0=dot(zeta,(dot(5,(dot((1 - zeta_minus),ed1) + dot((1 - zeta_plus),ed3))) + dot(dot(4,(2 - zeta)),ed2))) / 18
# PROJ_Bermudan_Put.m:134
        d_1=dot(dot(exp(- dx),zeta),(dot(5,(dot(zeta_minus,ed1) + dot(zeta_plus,ed3))) + dot(dot(4,zeta),ed2))) / 18
# PROJ_Bermudan_Put.m:135
        Thet[arange(1,kstr - 1)]=ThetM(arange(1,kstr - 1))
# PROJ_Bermudan_Put.m:138
        Ck4=Cont(kstr + 2)
# PROJ_Bermudan_Put.m:140
        Thet[kstr]=dot(W,(0.5 + dbar_0)) - dot(dot(S_0,exp(xkstr)),(varthet_m10 + d_0)) + dot(zeta4 / 8,(Ck1 - dot(2,Ck2) + Ck3)) + dot(zeta3 / 3,(Ck2 - Ck1)) + dot(zeta2 / 4,(Ck1 + dot(2,Ck2) - Ck3)) - dot(zeta,Ck2) - Ck1 / 24 + dot(5 / 12,Ck2) + Ck3 / 8
# PROJ_Bermudan_Put.m:141
        Thet[kstr + 1]=dot(W,dbar_1) - dot(dot(S_0,exp(xkstr + dx)),d_1) + dot(zeta4 / 8,(- Ck2 + dot(2,Ck3) - Ck4)) + dot(zeta3 / 6,(dot(3,Ck2) - dot(4,Ck3) + Ck4)) - dot(dot(0.5,zeta2),Ck2) + dot(Cons4,(Ck2 + dot(10,Ck3) + Ck4))
# PROJ_Bermudan_Put.m:146
        Thet[arange(kstr + 2,K - 1)]=dot(Cons4,(Cont(arange(kstr + 1,K - 2)) + dot(10,Cont(arange(kstr + 2,K - 1))) + Cont(arange(kstr + 3,K))))
# PROJ_Bermudan_Put.m:149
        Thet[K]=dot(Cons3,(dot(13,Cont(K)) + dot(15,Cont(K - 1)) - dot(5,Cont(K - 2)) + Cont(K - 3)))
# PROJ_Bermudan_Put.m:150
        p=ifft(multiply(toepM,fft(concat([[Thet(arange(1,K))],[zeros(K,1)]]))))
# PROJ_Bermudan_Put.m:152
        Cont[arange(1,K)]=p(arange(1,K))
# PROJ_Bermudan_Put.m:154
    
    price=Cont(nnot)
# PROJ_Bermudan_Put.m:157
    return price
    
if __name__ == '__main__':
    pass
    