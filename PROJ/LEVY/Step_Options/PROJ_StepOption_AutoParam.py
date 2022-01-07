# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# PROJ_StepOption_AutoParam.m

    
@function
def PROJ_StepOption_AutoParam(N=None,stepRho=None,call=None,down=None,S_0=None,W=None,H=None,M=None,r=None,q=None,rnCHF=None,T=None,L1=None,c2=None,c4=None,alphMult=None,TOLProb=None,TOLMean=None,rnCHFT=None,*args,**kwargs):
    varargin = PROJ_StepOption_AutoParam.varargin
    nargin = PROJ_StepOption_AutoParam.nargin

    #########################################################
# About: Pricing Function for STEP-style barrier options and FADER options using PROJ method 
#     Step Payoff: exp(-stepRho*R) * (S_T - W)^+  for a call, where R is the proportion of time spent in knock-out region
#     Fader (Fade-in) Payoff: (1 - R) * (S_T - W)^+ for a call, where R is the proportion of time spent in knock-out region
#           (Fade-out) Can be priced by parity (Fade-in + Fade-out = Vanilla), so Price(Fade-out) = Price(Vanilla) - Price(Fade-in)
# Models Supported: Levy Processes, including jump diffusions and Black-Scholes model
# Returns: price of contract
# Author: Justin Lars Kirkby
    
    # For algo/contract details and see section 4.4 of "Robust Barrier Option Pricing by Frame Projection under
#   Exponential Levy Dynamics", App. Math. Finance, 2017
# Contract is based on the paper "Step Options", (Linetsky, V.), Math. Finance 1999.
    
    # ----------------------
# Contract/Model Params 
# ----------------------
# stepRho: if >= 0, then Step-Option: "softener" h(R) = exp(-stepRho * R)
#          if = -1, then Fader-Option: "softener" h(R) = 1 - R 
# S_0 = initial stock price (e.g. 100)
# W   = strike  (e.g. 100)
# r   = interest rate (e.g. 0.05)
# q   = dividend yield
# T   = time remaining until maturity (in years, e.g. T=1)
# M   = number of subintervals of [0,T] (total of M+1 monitoring points in time grid, including S_0)
# call = 1 for call (else put)
# down = 1 for down and out (otherwise it's up and out)
# H    = barrier
# rnCHF, rnCHF_T = risk netural characteristic function (function handle with single argument),
#   at time steps dt=1/M and T, respectively
    
    # ----------------------
# Numerical (PROJ) Params 
# ----------------------
# This version uses automated parameter selection, starting from the initial guess of N basis elements
# L1      = gridwidth param, e.g. L1 = 10 (grid width is iteratively increased if this is found to be insufficient)
# N       = initial choice of number of grid/basis points (power of 2, e.g. 2^12), auto increased if found to be insufficient
#           
# TOLProb = probability estimate accuracy, e.g. 5e-08;
# TOLMean = mean estimate accuracy, e.g. 1e-05;
# alphMult = used to increase grid width during parameter selection, e.g. alphMult = 1.1
#########################################################
    
    Gamm=M + 1
# PROJ_StepOption_AutoParam.m:44
    
    tauM=1 / (M + 1)
# PROJ_StepOption_AutoParam.m:45
    if stepRho >= 0:
        stepSoftener=lambda u=None: exp(dot(dot(- stepRho,tauM),u))
# PROJ_StepOption_AutoParam.m:48
    else:
        if stepRho == - 1:
            stepSoftener=lambda u=None: 1 - u / (M + 1)
# PROJ_StepOption_AutoParam.m:51
        else:
            if stepRho == - 2:
                stepSoftener=lambda u=None: dot(1,(u == 0))
# PROJ_StepOption_AutoParam.m:54
    
    gamm0=1
# PROJ_StepOption_AutoParam.m:57
    
    dt=T / M
# PROJ_StepOption_AutoParam.m:59
    nrdt=dot(- r,dt)
# PROJ_StepOption_AutoParam.m:60
    h=log(H / S_0)
# PROJ_StepOption_AutoParam.m:61
    lws=log(W / S_0)
# PROJ_StepOption_AutoParam.m:62
    ######  Gaussian Quad Constants
    q_plus=(1 + sqrt(3 / 5)) / 2
# PROJ_StepOption_AutoParam.m:65
    q_minus=(1 - sqrt(3 / 5)) / 2
# PROJ_StepOption_AutoParam.m:65
    b3=sqrt(15)
# PROJ_StepOption_AutoParam.m:66
    b4=b3 / 10
# PROJ_StepOption_AutoParam.m:66
    alph=max(dot(dot(2,alphMult),abs(h)),dot(L1,sqrt(abs(dot(c2,T)) + sqrt(abs(dot(c4,T))))))
# PROJ_StepOption_AutoParam.m:68
    #=======================================
#Step 1: Satisfy Probability Tolerance
#=======================================
    Nmax=max(2 ** 8,dot(2,N))
# PROJ_StepOption_AutoParam.m:74
    
    ErrProb=10
# PROJ_StepOption_AutoParam.m:76
    numTimesInLoop=0
# PROJ_StepOption_AutoParam.m:77
    N=N / 2
# PROJ_StepOption_AutoParam.m:78
    alph=alph / alphMult
# PROJ_StepOption_AutoParam.m:78
    
    while abs(ErrProb) > TOLProb and N < Nmax / 2:

        alph=dot(alphMult,alph)
# PROJ_StepOption_AutoParam.m:82
        N=dot(2,N)
# PROJ_StepOption_AutoParam.m:83
        numTimesInLoop=numTimesInLoop + 1
# PROJ_StepOption_AutoParam.m:84
        fprintf('[-alpha,alpha] = [%.4f, %.4f] \n',- alph,alph)
        fprintf('\n')
        dx=dot(2,alph) / (N - 1)
# PROJ_StepOption_AutoParam.m:89
        a=1 / dx
# PROJ_StepOption_AutoParam.m:89
        dw=dot(dot(2,pi),a) / N
# PROJ_StepOption_AutoParam.m:90
        xmin=- alph / 2
# PROJ_StepOption_AutoParam.m:91
        xmax=xmin + dot((N / 2 - 1),dx)
# PROJ_StepOption_AutoParam.m:91
        gam1=(xmax - xmin) / 2
# PROJ_StepOption_AutoParam.m:92
        gam2=(xmax + xmin) / 2
# PROJ_StepOption_AutoParam.m:92
        grand=dot(dw,(arange(1,(N - 1))))
# PROJ_StepOption_AutoParam.m:93
        Prob=sum(multiply(multiply(exp(dot(dot(- 1j,gam2),grand)),sin(dot(gam1,grand))) / grand,rnCHFT(grand)))
# PROJ_StepOption_AutoParam.m:95
        Prob=Prob + sum(multiply(multiply(exp(dot(dot(1j,gam2),grand)),sin(dot(gam1,grand))) / grand,rnCHFT(- grand)))
# PROJ_StepOption_AutoParam.m:96
        Prob=dot(dw / pi,(gam1 + Prob))
# PROJ_StepOption_AutoParam.m:97
        ErrProb=(1 - Prob)
# PROJ_StepOption_AutoParam.m:98
        fprintf('NL = %.0f, ProbError: %.3e\n',numTimesInLoop,ErrProb)

    
    #=======================================
#Step 2: Satisfy Mean Tolerance
#=======================================
    
    numTimesInLoop=0
# PROJ_StepOption_AutoParam.m:108
    ErrMean=10
# PROJ_StepOption_AutoParam.m:109
    while abs(ErrMean) > TOLMean and N <= Nmax:

        if numTimesInLoop > 0:
            N=dot(2,N)
# PROJ_StepOption_AutoParam.m:112
        numTimesInLoop=numTimesInLoop + 1
# PROJ_StepOption_AutoParam.m:114
        dx=dot(2,alph) / (N - 1)
# PROJ_StepOption_AutoParam.m:116
        xmin=- alph / 2
# PROJ_StepOption_AutoParam.m:118
        n_h=floor((h - xmin) / dx + 1)
# PROJ_StepOption_AutoParam.m:119
        xmin=h - dot((n_h - 1),dx)
# PROJ_StepOption_AutoParam.m:120
        if h != 0:
            nnot=floor(1 - xmin / dx)
# PROJ_StepOption_AutoParam.m:124
            if abs(h) > dx:
                dx=(h - 0) / (n_h - nnot)
# PROJ_StepOption_AutoParam.m:126
                xmin=dot(dx,(1 - nnot))
# PROJ_StepOption_AutoParam.m:127
                #n_h = floor((h-xmin)/dx +1);  #NOT Numerically Stable
                n_h=floor(nnot + h / dx)
# PROJ_StepOption_AutoParam.m:129
        else:
            nnot=copy(n_h)
# PROJ_StepOption_AutoParam.m:132
        a=1 / dx
# PROJ_StepOption_AutoParam.m:135
        a2=a ** 2
# PROJ_StepOption_AutoParam.m:136
        zmin=dot((1 - N / 2),dx)
# PROJ_StepOption_AutoParam.m:137
        Cons2=dot(dot(24,a2),exp(nrdt)) / N
# PROJ_StepOption_AutoParam.m:139
        dw=dot(dot(2,pi),a) / N
# PROJ_StepOption_AutoParam.m:140
        grand=dot(dw,(arange(1,N - 1)))
# PROJ_StepOption_AutoParam.m:141
        grand=multiply(multiply(exp(dot(dot(- 1j,zmin),grand)),rnCHF(grand)),(sin(grand / (dot(2,a))) / grand) ** 2.0) / (2 + cos(grand / a))
# PROJ_StepOption_AutoParam.m:142
        beta=dot(Cons2,real(fft(concat([1 / (dot(24,a2)),grand]))))
# PROJ_StepOption_AutoParam.m:143
        varthet_star=(dot(exp(dot(0.5,dx)),(dot(5,cosh(dot(b4,dx))) - dot(b3,sinh(dot(b4,dx))) + 4)) + dot(exp(dot(- 0.5,dx)),(dot(5,cosh(dot(b4,dx))) + dot(b3,sinh(dot(b4,dx))) + 4))) / 18
# PROJ_StepOption_AutoParam.m:146
        ErrMean=dot(dot(exp(dot(r,dt)),varthet_star),(dot(beta,exp(zmin + dot(dx,(arange(0,N - 1)))).T))) - exp(dot((r - q),dt))
# PROJ_StepOption_AutoParam.m:148
        ErrMean=dot(dot(ErrMean,M),S_0)
# PROJ_StepOption_AutoParam.m:149
        fprintf('NLMean = %.0f, ErrMean = %.3e\n',numTimesInLoop,ErrMean)

    
    fprintf('Final log2(N): %.0f \n',log2(N))
    interp_Atend=0
# PROJ_StepOption_AutoParam.m:154
    if 0 < abs(h) and abs(h) < dx:
        interp_Atend=1
# PROJ_StepOption_AutoParam.m:156
    
    ###########################################################################
####   DETERMINE COMMON Params
###########################################################################
    K=N / 2
# PROJ_StepOption_AutoParam.m:163
    nbar=floor(dot(a,(lws - xmin)) + 1)
# PROJ_StepOption_AutoParam.m:164
    rho=lws - (xmin + dot((nbar - 1),dx))
# PROJ_StepOption_AutoParam.m:165
    zeta=dot(a,rho)
# PROJ_StepOption_AutoParam.m:166
    toepM=concat([[beta(arange(K,1,- 1)).T],[0],[beta(arange(dot(2,K) - 1,K,- 1),+ 1).T]])
# PROJ_StepOption_AutoParam.m:168
    toepM=fft(toepM)
# PROJ_StepOption_AutoParam.m:168
    #### PAYOFF CONSTANTS-----------------------------------
    varthet_01=dot(exp(dot(0.5,dx)),(dot(5,cosh(dot(b4,dx))) - dot(b3,sinh(dot(b4,dx))) + 4)) / 18
# PROJ_StepOption_AutoParam.m:171
    varthet_m10=dot(exp(dot(- 0.5,dx)),(dot(5,cosh(dot(b4,dx))) + dot(b3,sinh(dot(b4,dx))) + 4)) / 18
# PROJ_StepOption_AutoParam.m:172
    varthet_star=varthet_01 + varthet_m10
# PROJ_StepOption_AutoParam.m:173
    ###########################################################################
    if down == 1 and call != 1:
        #l = log(H/S_0);
        n_l=copy(n_h)
# PROJ_StepOption_AutoParam.m:179
        zeta_plus=dot(zeta,q_plus)
# PROJ_StepOption_AutoParam.m:181
        zeta_minus=dot(zeta,q_minus)
# PROJ_StepOption_AutoParam.m:181
        rho_plus=dot(rho,q_plus)
# PROJ_StepOption_AutoParam.m:182
        rho_minus=dot(rho,q_minus)
# PROJ_StepOption_AutoParam.m:182
        ed1=exp(rho_minus)
# PROJ_StepOption_AutoParam.m:184
        ed2=exp(rho / 2)
# PROJ_StepOption_AutoParam.m:184
        ed3=exp(rho_plus)
# PROJ_StepOption_AutoParam.m:184
        dbar_1=zeta ** 2 / 2
# PROJ_StepOption_AutoParam.m:186
        dbar_0=zeta - dbar_1
# PROJ_StepOption_AutoParam.m:187
        d_0=dot(zeta,(dot(5,(dot((1 - zeta_minus),ed1) + dot((1 - zeta_plus),ed3))) + dot(dot(4,(2 - zeta)),ed2))) / 18
# PROJ_StepOption_AutoParam.m:188
        d_1=dot(zeta,(dot(5,(dot(zeta_minus,ed1) + dot(zeta_plus,ed3))) + dot(dot(4,zeta),ed2))) / 18
# PROJ_StepOption_AutoParam.m:189
        Thet=zeros(K,1)
# PROJ_StepOption_AutoParam.m:191
        Thet[arange(1,nbar - 1)]=W - dot(dot(exp(xmin + dot(dx,(arange(0,nbar - 2)))),S_0),varthet_star)
# PROJ_StepOption_AutoParam.m:192
        Thet[nbar]=dot(W,(0.5 + dbar_0 - dot(exp(- rho),(varthet_m10 + d_0))))
# PROJ_StepOption_AutoParam.m:193
        Thet[nbar + 1]=dot(W,(dbar_1 - dot(exp(- rho),d_1)))
# PROJ_StepOption_AutoParam.m:194
        Val=zeros(K,Gamm + 1)
# PROJ_StepOption_AutoParam.m:197
        ThetTemp=zeros(K,1)
# PROJ_StepOption_AutoParam.m:199
        for j in arange(1,Gamm).reshape(-1):
            gamm=j - 1
# PROJ_StepOption_AutoParam.m:201
            ThetTemp[arange(1,n_l - 1)]=dot(stepSoftener(gamm + 1),Thet(arange(1,n_l - 1)))
# PROJ_StepOption_AutoParam.m:202
            ThetTemp[n_l]=dot(dot(0.5,(stepSoftener(gamm + 1) + stepSoftener(gamm))),Thet(n_l))
# PROJ_StepOption_AutoParam.m:204
            ThetTemp[arange(n_l + 1,K)]=dot(stepSoftener(gamm),Thet(arange(n_l + 1,K)))
# PROJ_StepOption_AutoParam.m:206
            p=ifft(multiply(toepM,fft(concat([[ThetTemp],[zeros(K,1)]]))))
# PROJ_StepOption_AutoParam.m:208
            Val[arange(),j]=p(arange(1,K))
# PROJ_StepOption_AutoParam.m:209
        #  NOTE: this introduces a kink and we use interpolation in next step
    #  ... this can be improved
        ##########################################################
    #### CUMULATIVE PARISIAN
    ##########################################################
    #NOTE: DIFFERS FROM parisian in the first step ... M-1
        for m in arange(M - 2,0,- 1).reshape(-1):
            for j in arange(1,m + 1).reshape(-1):
                Thet[1]=(dot(13,Val(1,j + 1)) + dot(15,Val(2,j + 1)) - dot(5,Val(3,j + 1)) + Val(4,j + 1)) / 48
# PROJ_StepOption_AutoParam.m:222
                Thet[arange(2,n_l - 1)]=(Val(arange(1,n_l - 2),j + 1) + dot(10,Val(arange(2,n_l - 1),j + 1)) + Val(arange(3,n_l),j + 1)) / 12
# PROJ_StepOption_AutoParam.m:223
                Thet[n_l]=(dot(13,Val(n_l,j + 1)) + dot(15,Val(n_l - 1,j + 1)) - dot(5,Val(n_l - 2,j + 1)) + Val(n_l - 3,j + 1)) / 48 + (dot(13,Val(n_l,j)) + dot(15,Val(n_l + 1,j)) - dot(5,Val(n_l + 2,j)) + Val(n_l + 3,j)) / 48
# PROJ_StepOption_AutoParam.m:225
                Thet[arange(n_l + 1,K - 1)]=(Val(arange(n_l,K - 2),j) + dot(10,Val(arange(n_l + 1,K - 1),j)) + Val(arange(n_l + 2,K),j)) / 12
# PROJ_StepOption_AutoParam.m:228
                Thet[K]=(dot(13,Val(K,j)) + dot(15,Val(K - 1,j)) - dot(5,Val(K - 2,j)) + Val(K - 3,j)) / 48
# PROJ_StepOption_AutoParam.m:229
                p=ifft(multiply(toepM,fft(concat([[Thet(arange(1,K))],[zeros(K,1)]]))))
# PROJ_StepOption_AutoParam.m:231
                Val[arange(),j]=p(arange(1,K))
# PROJ_StepOption_AutoParam.m:232
            ### Now to Gamm+1
            j=Gamm + 1
# PROJ_StepOption_AutoParam.m:236
            Thet[arange(1,n_l - 1)]=0
# PROJ_StepOption_AutoParam.m:237
            Thet[n_l]=(dot(13,Val(n_l,j)) + dot(15,Val(n_l + 1,j)) - dot(5,Val(n_l + 2,j)) + Val(n_l + 3,j)) / 48
# PROJ_StepOption_AutoParam.m:238
            Thet[arange(n_l + 1,K - 1)]=(Val(arange(n_l,K - 2),j) + dot(10,Val(arange(n_l + 1,K - 1),j)) + Val(arange(n_l + 2,K),j)) / 12
# PROJ_StepOption_AutoParam.m:239
            p=ifft(multiply(toepM,fft(concat([[Thet(arange(1,K))],[zeros(K,1)]]))))
# PROJ_StepOption_AutoParam.m:241
            Val[arange(),j]=p(arange(1,K))
# PROJ_StepOption_AutoParam.m:242
        #######################################################
#######################################################
    else:
        if down != 1 and call == 1:
            #u    = log(H/S_0);
            n_u=copy(n_h)
# PROJ_StepOption_AutoParam.m:249
            sigma=1 - zeta
# PROJ_StepOption_AutoParam.m:251
            sigma_plus=dot((q_plus - 0.5),sigma)
# PROJ_StepOption_AutoParam.m:251
            sigma_minus=dot((q_minus - 0.5),sigma)
# PROJ_StepOption_AutoParam.m:251
            es1=exp(dot(dx,sigma_plus))
# PROJ_StepOption_AutoParam.m:253
            es2=exp(dot(dx,sigma_minus))
# PROJ_StepOption_AutoParam.m:253
            dbar_0=0.5 + dot(zeta,(dot(0.5,zeta) - 1))
# PROJ_StepOption_AutoParam.m:255
            dbar_1=dot(sigma,(1 - dot(0.5,sigma)))
# PROJ_StepOption_AutoParam.m:256
            d_0=dot(dot(exp(dot((rho + dx),0.5)),sigma ** 2) / 18,(dot(5,(dot((1 - q_minus),es2) + dot((1 - q_plus),es1))) + 4))
# PROJ_StepOption_AutoParam.m:258
            d_1=dot(dot(exp(dot((rho - dx),0.5)),sigma) / 18,(dot(5,(dot((dot(0.5,(zeta + 1)) + sigma_minus),es2) + dot((dot(0.5,(zeta + 1)) + sigma_plus),es1))) + dot(4,(zeta + 1))))
# PROJ_StepOption_AutoParam.m:259
            Thet=zeros(K,1)
# PROJ_StepOption_AutoParam.m:261
            Thet[nbar]=dot(W,(dot(exp(- rho),d_0) - dbar_0))
# PROJ_StepOption_AutoParam.m:262
            Thet[nbar + 1]=dot(W,(dot(exp(dx - rho),(varthet_01 + d_1)) - (0.5 + dbar_1)))
# PROJ_StepOption_AutoParam.m:263
            Thet[arange(nbar + 2,K)]=dot(dot(exp(xmin + dot(dx,(arange(nbar + 1,K - 1)))),S_0),varthet_star) - W
# PROJ_StepOption_AutoParam.m:264
            Val=zeros(K,Gamm + 1)
# PROJ_StepOption_AutoParam.m:266
            ThetTemp=zeros(K,1)
# PROJ_StepOption_AutoParam.m:268
            for j in arange(1,Gamm).reshape(-1):
                gamm=j - 1
# PROJ_StepOption_AutoParam.m:270
                ThetTemp[arange(1,n_u - 1)]=dot(stepSoftener(gamm),Thet(arange(1,n_u - 1)))
# PROJ_StepOption_AutoParam.m:271
                ThetTemp[n_u]=dot(dot(0.5,(stepSoftener(gamm) + stepSoftener(gamm + 1))),Thet(n_u))
# PROJ_StepOption_AutoParam.m:273
                ThetTemp[arange(n_u + 1,K)]=dot(stepSoftener(gamm + 1),Thet(arange(n_u + 1,K)))
# PROJ_StepOption_AutoParam.m:275
                p=ifft(multiply(toepM,fft(concat([[ThetTemp],[zeros(K,1)]]))))
# PROJ_StepOption_AutoParam.m:277
                Val[arange(),j]=p(arange(1,K))
# PROJ_StepOption_AutoParam.m:278
            ##########################################################
    #### CUMULATIVE PARISIAN
    ##########################################################
            for m in arange(M - 2,0,- 1).reshape(-1):
                for j in arange(1,Gamm).reshape(-1):
                    Thet[1]=(dot(13,Val(1,j)) + dot(15,Val(2,j)) - dot(5,Val(3,j)) + Val(4,j)) / 48
# PROJ_StepOption_AutoParam.m:286
                    Thet[arange(2,n_u - 1)]=(Val(arange(1,n_u - 2),j) + dot(10,Val(arange(2,n_u - 1),j)) + Val(arange(3,n_u),j)) / 12
# PROJ_StepOption_AutoParam.m:287
                    Thet[n_u]=(dot(13,Val(n_u,j)) + dot(15,Val(n_u - 1,j)) - dot(5,Val(n_u - 2,j)) + Val(n_u - 3,j)) / 48 + (dot(13,Val(n_u,j + 1)) + dot(15,Val(n_u + 1,j + 1)) - dot(5,Val(n_u + 2,j + 1)) + Val(n_u + 3,j + 1)) / 48
# PROJ_StepOption_AutoParam.m:289
                    Thet[arange(n_u + 1,K - 1)]=(Val(arange(n_u,K - 2),j + 1) + dot(10,Val(arange(n_u + 1,K - 1),j + 1)) + Val(arange(n_u + 2,K),j + 1)) / 12
# PROJ_StepOption_AutoParam.m:292
                    Thet[K]=(dot(13,Val(K,j + 1)) + dot(15,Val(K - 1,j + 1)) - dot(5,Val(K - 2,j + 1)) + Val(K - 3,j + 1)) / 48
# PROJ_StepOption_AutoParam.m:293
                    p=ifft(multiply(toepM,fft(concat([[Thet(arange(1,K))],[zeros(K,1)]]))))
# PROJ_StepOption_AutoParam.m:295
                    Val[arange(),j]=p(arange(1,K))
# PROJ_StepOption_AutoParam.m:296
                ### Now to Gamm+1
                j=Gamm + 1
# PROJ_StepOption_AutoParam.m:300
                Thet[1]=(dot(13,Val(1,j)) + dot(15,Val(2,j)) - dot(5,Val(3,j)) + Val(4,j)) / 48
# PROJ_StepOption_AutoParam.m:301
                Thet[arange(2,n_u - 1)]=(Val(arange(1,n_u - 2),j) + dot(10,Val(arange(2,n_u - 1),j)) + Val(arange(3,n_u),j)) / 12
# PROJ_StepOption_AutoParam.m:302
                Thet[n_u]=(dot(13,Val(n_u,j)) + dot(15,Val(n_u - 1,j)) - dot(5,Val(n_u - 2,j)) + Val(n_u - 3,j)) / 48
# PROJ_StepOption_AutoParam.m:303
                Thet[arange(n_u + 1,K)]=0
# PROJ_StepOption_AutoParam.m:304
                p=ifft(multiply(toepM,fft(concat([[Thet(arange(1,K))],[zeros(K,1)]]))))
# PROJ_StepOption_AutoParam.m:306
                Val[arange(),j]=p(arange(1,K))
# PROJ_StepOption_AutoParam.m:307
    
    if interp_Atend != 1:
        price=Val(nnot,gamm0)
# PROJ_StepOption_AutoParam.m:313
    else:
        dd=0 - (xmin + dot((nnot - 1),dx))
# PROJ_StepOption_AutoParam.m:316
        price=Val(nnot,gamm0) + dot((Val(nnot + 1,gamm0) - Val(nnot,gamm0)),dd) / dx
# PROJ_StepOption_AutoParam.m:317
    
    return price
    
if __name__ == '__main__':
    pass
    