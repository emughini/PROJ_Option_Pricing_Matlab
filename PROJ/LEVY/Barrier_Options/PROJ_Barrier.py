# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# PROJ_Barrier.m

    
@function
def PROJ_Barrier(N=None,alph=None,call=None,down=None,S_0=None,W=None,H=None,M=None,r=None,q=None,rnCHF=None,T=None,rebate=None,*args,**kwargs):
    varargin = PROJ_Barrier.varargin
    nargin = PROJ_Barrier.nargin

    #########################################################
# About: Pricing Function for Discrete Barrier Options using PROJ method
# Models Supported: Levy Processes, including jump diffusions and Black-Scholes model
# Returns: price of contract
# Author: Justin Lars Kirkby
    
    # ----------------------
# Contract/Model Params 
# ----------------------
# S_0 = initial stock price (e.g. 100)
# W   = strike  (e.g. 100)
# r   = interest rate (e.g. 0.05)
# q   = dividend yield (e.g. 0.05)
# T   = time remaining until maturity (in years, e.g. T=1)
# M   = number of subintervals of [0,T] (total of M+1 monitoring points in time grid, including S_0)
# call = 1 for call (else put)
# down = 1 for down and out (otherwise it's up and out)
# H    = barrier
# rebate = rebate paid immediately upon passing the barrier (knocking-out)
# rnCHF = risk netural characteristic function (function handle with single argument)
    
    # ----------------------
# Numerical (PROJ) Params 
# ----------------------
# alph  = grid with is 2*alph
# N     = number of grid/basis points (power of 2, e.g. 2^12), resolution = 2*alph/(N-1)
#########################################################
    
    #*****************************
#TODO: Refactor similar to parisian code to simplify
#*****************************
    
    if nargin < 13:
        rebate=0
# PROJ_Barrier.m:35
    
    mult=1
# PROJ_Barrier.m:38
    
    interp_Atend=0
# PROJ_Barrier.m:39
    
    K=N / 2
# PROJ_Barrier.m:42
    dx=dot(2,alph) / (N - 1)
# PROJ_Barrier.m:44
    a=1 / dx
# PROJ_Barrier.m:44
    dt=T / M
# PROJ_Barrier.m:46
    nrdt=dot(- r,dt)
# PROJ_Barrier.m:47
    nqdt=dot(- q,dt)
# PROJ_Barrier.m:47
    Thet=zeros(K,1)
# PROJ_Barrier.m:49
    ######  Gaussian Quad Constants
    q_plus=(1 + sqrt(3 / 5)) / 2
# PROJ_Barrier.m:52
    q_minus=(1 - sqrt(3 / 5)) / 2
# PROJ_Barrier.m:52
    b3=sqrt(15)
# PROJ_Barrier.m:53
    b4=b3 / 10
# PROJ_Barrier.m:53
    if down == 1:
        ##################################     
####  DOWN & OUT 
##################################
        l=log(H / S_0)
# PROJ_Barrier.m:59
        xmin=copy(l)
# PROJ_Barrier.m:60
        nnot=floor(1 - dot(xmin,a))
# PROJ_Barrier.m:61
        if nnot >= K:
            fprintf('nnot is %.0f while K is %.0f, need to increase alpha \n',nnot,K)
        if call == 1 and nnot == 1:
            interp_Atend=1
# PROJ_Barrier.m:68
            #no change is made to dx
        else:
            nnot=max(2,floor(1 - dot(xmin,a)))
# PROJ_Barrier.m:71
            dx=l / (1 - nnot)
# PROJ_Barrier.m:71
        a=1 / dx
# PROJ_Barrier.m:73
        lws=log(W / S_0)
# PROJ_Barrier.m:75
        nbar=floor(dot(a,(lws - xmin)) + 1)
# PROJ_Barrier.m:76
        rho=lws - (xmin + dot((nbar - 1),dx))
# PROJ_Barrier.m:77
        zeta=dot(a,rho)
# PROJ_Barrier.m:78
        a2=a ** 2
# PROJ_Barrier.m:80
        zmin=dot((1 - K),dx)
# PROJ_Barrier.m:81
        ### Extend Pbar, only to invert (aliasing)
        Nmult=dot(mult,N)
# PROJ_Barrier.m:84
        Cons=dot(dot(24,a2),exp(nrdt)) / Nmult
# PROJ_Barrier.m:85
        dw=dot(dot(2,pi),a) / Nmult
# PROJ_Barrier.m:86
        grand=dot(dw,(arange(1,Nmult - 1)))
# PROJ_Barrier.m:87
        grand=multiply(multiply(exp(dot(dot(- 1j,zmin),grand)),rnCHF(grand)),(sin(grand / (dot(2,a))) / grand) ** 2.0) / (2 + cos(grand / a))
# PROJ_Barrier.m:88
        beta=dot(Cons,real(fft(concat([1 / (dot(24,a2)),grand]))))
# PROJ_Barrier.m:89
        toepM=concat([[beta(arange(K,1,- 1)).T],[0],[beta(arange(dot(2,K) - 1,K,- 1),+ 1).T]])
# PROJ_Barrier.m:91
        toepM=fft(toepM)
# PROJ_Barrier.m:91
        varthet_01=dot(exp(dot(0.5,dx)),(dot(5,cosh(dot(b4,dx))) - dot(b3,sinh(dot(b4,dx))) + 4)) / 18
# PROJ_Barrier.m:94
        varthet_m10=dot(exp(dot(- 0.5,dx)),(dot(5,cosh(dot(b4,dx))) + dot(b3,sinh(dot(b4,dx))) + 4)) / 18
# PROJ_Barrier.m:95
        varthet_star=varthet_01 + varthet_m10
# PROJ_Barrier.m:96
        ####---------------------------------------------------
        if rebate != 0:
            val_rebate=dot(rebate,concat([[fliplr(cumsum(beta(arange(1,K - 1,1)))).T],[0]]))
# PROJ_Barrier.m:101
        ##################################     
    #### DOC
    ##################################
        if call == 1:
            sigma=1 - zeta
# PROJ_Barrier.m:108
            sigma_plus=dot((q_plus - 0.5),sigma)
# PROJ_Barrier.m:108
            sigma_minus=dot((q_minus - 0.5),sigma)
# PROJ_Barrier.m:108
            es1=exp(dot(dx,sigma_plus))
# PROJ_Barrier.m:110
            es2=exp(dot(dx,sigma_minus))
# PROJ_Barrier.m:110
            dbar_0=0.5 + dot(zeta,(dot(0.5,zeta) - 1))
# PROJ_Barrier.m:112
            dbar_1=dot(sigma,(1 - dot(0.5,sigma)))
# PROJ_Barrier.m:113
            d_0=dot(dot(exp(dot((rho + dx),0.5)),sigma ** 2) / 18,(dot(5,(dot((1 - q_minus),es2) + dot((1 - q_plus),es1))) + 4))
# PROJ_Barrier.m:115
            d_1=dot(dot(exp(dot((rho - dx),0.5)),sigma) / 18,(dot(5,(dot((dot(0.5,(zeta + 1)) + sigma_minus),es2) + dot((dot(0.5,(zeta + 1)) + sigma_plus),es1))) + dot(4,(zeta + 1))))
# PROJ_Barrier.m:116
            Thet[nbar]=dot(W,(dot(exp(- rho),d_0) - dbar_0))
# PROJ_Barrier.m:119
            Thet[nbar + 1]=dot(W,(dot(exp(dx - rho),(varthet_01 + d_1)) - (0.5 + dbar_1)))
# PROJ_Barrier.m:120
            Thet[arange(nbar + 2,K)]=dot(dot(exp(xmin + dot(dx,(arange(nbar + 1,K - 1)))),S_0),varthet_star) - W
# PROJ_Barrier.m:121
            Thet[1]=Thet(1) + dot(0.5,rebate)
# PROJ_Barrier.m:123
            toepR=concat([[beta(arange(dot(2,K),K,- 1),+ 1).T],[0],[zeros(K - 1,1)]])
# PROJ_Barrier.m:125
            toepR=fft(toepR)
# PROJ_Barrier.m:125
            ### multiplication by Cons2 in each of the toep matrices
            Thetbar1=dot(dot(exp(dot(r,dt)),W),cumsum(beta(arange(dot(2,K),K + 1,- 1))).T)
# PROJ_Barrier.m:129
            Thetbar2=dot(dot(dot(exp(dot(r,dt)),S_0),varthet_star),exp(xmin + dot(dx,(arange(K,dot(2,K) - 1)))).T)
# PROJ_Barrier.m:130
            p=ifft(multiply(toepR,fft(concat([[Thetbar2],[zeros(K,1)]]))))
# PROJ_Barrier.m:131
            Thetbar2=p(arange(1,K))
# PROJ_Barrier.m:132
            p=ifft(multiply(toepM,fft(concat([[Thet(arange(1,K))],[zeros(K,1)]]))))
# PROJ_Barrier.m:135
            if rebate != 0:
                Val=p(arange(1,K)) + dot(exp(nrdt),(Thetbar2 - Thetbar1)) + val_rebate
# PROJ_Barrier.m:138
            else:
                Val=p(arange(1,K)) + dot(exp(nrdt),(Thetbar2 - Thetbar1))
# PROJ_Barrier.m:140
            #######
            for m in arange(M - 2,0,- 1).reshape(-1):
                Thet[arange(2,K - 1)]=(Val(arange(1,K - 2)) + dot(10,Val(arange(2,K - 1))) + Val(arange(3,K))) / 12
# PROJ_Barrier.m:145
                Thet[1]=(dot(13,Val(1)) + dot(15,Val(2)) - dot(5,Val(3)) + Val(4)) / 48
# PROJ_Barrier.m:146
                Thet[K]=dot(2,(dot(13,Val(K)) + dot(15,Val(K - 1)) - dot(5,Val(K - 2)) + Val(K - 3))) / 48
# PROJ_Barrier.m:147
                Thet[1]=Thet(1) + dot(0.5,rebate)
# PROJ_Barrier.m:149
                #######
                p=ifft(multiply(toepM,fft(concat([[Thet(arange(1,K))],[zeros(K,1)]]))))
# PROJ_Barrier.m:151
                Val[arange(1,K)]=p(arange(1,K)) + dot(exp(dot(nqdt,(M - m - 1))),Thetbar2) - dot(exp(dot(nrdt,(M - m - 1))),Thetbar1)
# PROJ_Barrier.m:152
                if rebate != 0:
                    Val=Val + val_rebate
# PROJ_Barrier.m:155
            ##################################     
    #### DOP
    ##################################
        else:
            zeta_plus=dot(zeta,q_plus)
# PROJ_Barrier.m:163
            zeta_minus=dot(zeta,q_minus)
# PROJ_Barrier.m:163
            rho_plus=dot(rho,q_plus)
# PROJ_Barrier.m:164
            rho_minus=dot(rho,q_minus)
# PROJ_Barrier.m:164
            ed1=exp(rho_minus)
# PROJ_Barrier.m:166
            ed2=exp(rho / 2)
# PROJ_Barrier.m:166
            ed3=exp(rho_plus)
# PROJ_Barrier.m:166
            dbar_1=zeta ** 2 / 2
# PROJ_Barrier.m:168
            dbar_0=zeta - dbar_1
# PROJ_Barrier.m:169
            d_0=dot(zeta,(dot(5,(dot((1 - zeta_minus),ed1) + dot((1 - zeta_plus),ed3))) + dot(dot(4,(2 - zeta)),ed2))) / 18
# PROJ_Barrier.m:170
            d_1=dot(zeta,(dot(5,(dot(zeta_minus,ed1) + dot(zeta_plus,ed3))) + dot(dot(4,zeta),ed2))) / 18
# PROJ_Barrier.m:171
            Thet[1]=W / 2 - dot(H,varthet_01)
# PROJ_Barrier.m:173
            Thet[arange(2,nbar - 1)]=W - dot(dot(exp(xmin + dot(dx,(arange(1,nbar - 2)))),S_0),varthet_star)
# PROJ_Barrier.m:174
            Thet[nbar]=dot(W,(0.5 + dbar_0 - dot(exp(- rho),(varthet_m10 + d_0))))
# PROJ_Barrier.m:175
            Thet[nbar + 1]=dot(W,(dbar_1 - dot(exp(- rho),d_1)))
# PROJ_Barrier.m:176
            Thet[1]=Thet(1) + dot(0.5,rebate)
# PROJ_Barrier.m:178
            p=ifft(multiply(toepM,fft(concat([[Thet(arange(1,K))],[zeros(K,1)]]))))
# PROJ_Barrier.m:180
            if rebate != 0:
                Val=p(arange(1,K)) + val_rebate
# PROJ_Barrier.m:182
            else:
                Val=p(arange(1,K))
# PROJ_Barrier.m:184
            #######
            for m in arange(M - 2,0,- 1).reshape(-1):
                Thet[1]=(dot(13,Val(1)) + dot(15,Val(2)) - dot(5,Val(3)) + Val(4)) / 48
# PROJ_Barrier.m:189
                Thet[K]=(dot(13,Val(K)) + dot(15,Val(K - 1)) - dot(5,Val(K - 2)) + Val(K - 3)) / 48
# PROJ_Barrier.m:190
                Thet[arange(2,K - 1)]=(Val(arange(1,K - 2)) + dot(10,Val(arange(2,K - 1))) + Val(arange(3,K))) / 12
# PROJ_Barrier.m:191
                Thet[1]=Thet(1) + dot(0.5,rebate)
# PROJ_Barrier.m:193
                #######
                p=ifft(multiply(toepM,fft(concat([[Thet(arange(1,K))],[zeros(K,1)]]))))
# PROJ_Barrier.m:195
                Val=p(arange(1,K))
# PROJ_Barrier.m:196
                if rebate != 0:
                    Val=Val + val_rebate
# PROJ_Barrier.m:199
        ##################################     
####  UP & OUT 
##################################
    else:
        lws=log(W / S_0)
# PROJ_Barrier.m:208
        u=log(H / S_0)
# PROJ_Barrier.m:209
        nnot=floor(K - dot(a,u))
# PROJ_Barrier.m:211
        if call != 1 and nnot == K - 1:
            interp_Atend=1
# PROJ_Barrier.m:213
        else:
            dx=u / (K - nnot)
# PROJ_Barrier.m:215
            a=1 / dx
# PROJ_Barrier.m:215
        xmin=u - dot((K - 1),dx)
# PROJ_Barrier.m:218
        nbar=floor(dot(a,(lws - xmin)) + 1)
# PROJ_Barrier.m:219
        rho=lws - (xmin + dot((nbar - 1),dx))
# PROJ_Barrier.m:221
        zeta=dot(a,rho)
# PROJ_Barrier.m:222
        a2=a ** 2
# PROJ_Barrier.m:224
        zmin=dot((1 - K),dx)
# PROJ_Barrier.m:225
        ### Extend Pbar, only to invert (aliasing)
        Nmult=dot(mult,N)
# PROJ_Barrier.m:228
        Cons=dot(dot(24,a2),exp(nrdt)) / Nmult
# PROJ_Barrier.m:229
        dw=dot(dot(2,pi),a) / Nmult
# PROJ_Barrier.m:230
        grand=dot(dw,(arange(1,Nmult - 1)))
# PROJ_Barrier.m:231
        grand=multiply(multiply(exp(dot(dot(- 1j,zmin),grand)),rnCHF(grand)),(sin(grand / (dot(2,a))) / grand) ** 2.0) / (2 + cos(grand / a))
# PROJ_Barrier.m:232
        beta=dot(Cons,real(fft(concat([1 / (dot(24,a2)),grand]))))
# PROJ_Barrier.m:233
        toepM=concat([[beta(arange(K,1,- 1)).T],[0],[beta(arange(dot(2,K) - 1,K,- 1),+ 1).T]])
# PROJ_Barrier.m:235
        toepM=fft(toepM)
# PROJ_Barrier.m:236
        varthet_01=dot(exp(dot(0.5,dx)),(dot(5,cosh(dot(b4,dx))) - dot(b3,sinh(dot(b4,dx))) + 4)) / 18
# PROJ_Barrier.m:239
        varthet_m10=dot(exp(dot(- 0.5,dx)),(dot(5,cosh(dot(b4,dx))) + dot(b3,sinh(dot(b4,dx))) + 4)) / 18
# PROJ_Barrier.m:240
        varthet_star=varthet_01 + varthet_m10
# PROJ_Barrier.m:241
        if rebate != 0:
            val_rebate=dot(rebate,cumsum(beta(arange(dot(2,K),K + 1,- 1))).T)
# PROJ_Barrier.m:245
        ##################################     
    #### UOC
    ##################################
        if call == 1:
            sigma=1 - zeta
# PROJ_Barrier.m:253
            sigma_plus=dot((q_plus - 0.5),sigma)
# PROJ_Barrier.m:253
            sigma_minus=dot((q_minus - 0.5),sigma)
# PROJ_Barrier.m:253
            es1=exp(dot(dx,sigma_plus))
# PROJ_Barrier.m:254
            es2=exp(dot(dx,sigma_minus))
# PROJ_Barrier.m:254
            dbar_0=0.5 + dot(zeta,(dot(0.5,zeta) - 1))
# PROJ_Barrier.m:256
            dbar_1=dot(sigma,(1 - dot(0.5,sigma)))
# PROJ_Barrier.m:257
            d_0=dot(dot(exp(dot((rho + dx),0.5)),sigma ** 2) / 18,(dot(5,(dot((1 - q_minus),es2) + dot((1 - q_plus),es1))) + 4))
# PROJ_Barrier.m:259
            d_1=dot(dot(exp(dot((rho - dx),0.5)),sigma) / 18,(dot(5,(dot((dot(0.5,(zeta + 1)) + sigma_minus),es2) + dot((dot(0.5,(zeta + 1)) + sigma_plus),es1))) + dot(4,(zeta + 1))))
# PROJ_Barrier.m:260
            Thet[nbar]=dot(W,(dot(exp(- rho),d_0) - dbar_0))
# PROJ_Barrier.m:263
            Thet[nbar + 1]=dot(W,(dot(exp(dx - rho),(varthet_01 + d_1)) - (0.5 + dbar_1)))
# PROJ_Barrier.m:264
            Thet[arange(nbar + 2,K - 1)]=dot(dot(exp(xmin + dot(dx,(arange(nbar + 1,K - 2)))),S_0),varthet_star) - W
# PROJ_Barrier.m:265
            Thet[K]=dot(H,varthet_m10) - dot(0.5,W)
# PROJ_Barrier.m:266
            Thet[K]=Thet(K) + dot(0.5,rebate)
# PROJ_Barrier.m:268
            #######
            p=ifft(multiply(toepM,fft(concat([[Thet(arange(1,K))],[zeros(K,1)]]))))
# PROJ_Barrier.m:271
            if rebate != 0:
                Val=p(arange(1,K)) + val_rebate
# PROJ_Barrier.m:273
            else:
                Val=p(arange(1,K))
# PROJ_Barrier.m:275
            #######
            for m in arange(M - 2,0,- 1).reshape(-1):
                Thet[1]=(dot(13,Val(1)) + dot(15,Val(2)) - dot(5,Val(3)) + Val(4)) / 48
# PROJ_Barrier.m:281
                Thet[K]=(dot(13,Val(K)) + dot(15,Val(K - 1)) - dot(5,Val(K - 2)) + Val(K - 3)) / 48
# PROJ_Barrier.m:282
                Thet[arange(2,K - 1)]=(Val(arange(1,K - 2)) + dot(10,Val(arange(2,K - 1))) + Val(arange(3,K))) / 12
# PROJ_Barrier.m:283
                Thet[K]=Thet(K) + dot(0.5,rebate)
# PROJ_Barrier.m:285
                p=ifft(multiply(toepM,fft(concat([[Thet(arange(1,K))],[zeros(K,1)]]))))
# PROJ_Barrier.m:287
                Val=p(arange(1,K))
# PROJ_Barrier.m:288
                if rebate != 0:
                    Val=Val + val_rebate
# PROJ_Barrier.m:290
            ##################################     
    #### UOP
    ##################################
        else:
            zeta_plus=dot(zeta,q_plus)
# PROJ_Barrier.m:297
            zeta_minus=dot(zeta,q_minus)
# PROJ_Barrier.m:297
            rho_plus=dot(rho,q_plus)
# PROJ_Barrier.m:298
            rho_minus=dot(rho,q_minus)
# PROJ_Barrier.m:298
            ed1=exp(rho_minus)
# PROJ_Barrier.m:299
            ed2=exp(rho / 2)
# PROJ_Barrier.m:299
            ed3=exp(rho_plus)
# PROJ_Barrier.m:299
            dbar_1=zeta ** 2 / 2
# PROJ_Barrier.m:301
            dbar_0=zeta - dbar_1
# PROJ_Barrier.m:302
            d_0=dot(zeta,(dot(5,(dot((1 - zeta_minus),ed1) + dot((1 - zeta_plus),ed3))) + dot(dot(4,(2 - zeta)),ed2))) / 18
# PROJ_Barrier.m:303
            d_1=dot(zeta,(dot(5,(dot(zeta_minus,ed1) + dot(zeta_plus,ed3))) + dot(dot(4,zeta),ed2))) / 18
# PROJ_Barrier.m:304
            Thet[arange(1,nbar - 1)]=W - dot(dot(exp(xmin + dot(dx,(arange(0,nbar - 2)))),S_0),varthet_star)
# PROJ_Barrier.m:306
            Thet[nbar]=dot(W,(0.5 + dbar_0 - dot(exp(- rho),(varthet_m10 + d_0))))
# PROJ_Barrier.m:307
            Thet[nbar + 1]=dot(W,(dbar_1 - dot(exp(- rho),d_1)))
# PROJ_Barrier.m:308
            Thet[K]=dot(0.5,rebate)
# PROJ_Barrier.m:310
            toepL=concat([[zeros(K,1)],[0],[beta(arange(K - 1,1,- 1)).T]])
# PROJ_Barrier.m:312
            toepL=fft(toepL)
# PROJ_Barrier.m:313
            Thetbar1=dot(dot(exp(dot(r,dt)),W),concat([[fliplr(cumsum(beta(arange(1,K - 1,1)))).T],[0]]))
# PROJ_Barrier.m:315
            Thetbar2=dot(dot(dot(exp(dot(r,dt)),S_0),varthet_star),exp(xmin - dot(dx,(arange(K,1,- 1)))).T)
# PROJ_Barrier.m:316
            p=ifft(multiply(toepL,fft(concat([[Thetbar2],[zeros(K,1)]]))))
# PROJ_Barrier.m:317
            Thetbar2=p(arange(1,K))
# PROJ_Barrier.m:318
            p=ifft(multiply(toepM,fft(concat([[Thet(arange(1,K))],[zeros(K,1)]]))))
# PROJ_Barrier.m:320
            if rebate != 0:
                Val=p(arange(1,K)) + dot(exp(dot(- r,dt)),(Thetbar1 - Thetbar2)) + val_rebate
# PROJ_Barrier.m:323
            else:
                Val=p(arange(1,K)) + dot(exp(dot(- r,dt)),(Thetbar1 - Thetbar2))
# PROJ_Barrier.m:325
            #######
            #######
            for m in arange(M - 2,0,- 1).reshape(-1):
                Thet[1]=dot(2,(dot(13,Val(1)) + dot(15,Val(2)) - dot(5,Val(3)) + Val(4))) / 48
# PROJ_Barrier.m:332
                Thet[K]=(dot(13,Val(K)) + dot(15,Val(K - 1)) - dot(5,Val(K - 2)) + Val(K - 3)) / 48
# PROJ_Barrier.m:333
                Thet[arange(2,K - 1)]=(Val(arange(1,K - 2)) + dot(10,Val(arange(2,K - 1))) + Val(arange(3,K))) / 12
# PROJ_Barrier.m:334
                Thet[K]=Thet(K) + dot(0.5,rebate)
# PROJ_Barrier.m:336
                #######
                p=ifft(multiply(toepM,fft(concat([[Thet(arange(1,K))],[zeros(K,1)]]))))
# PROJ_Barrier.m:338
                Val=p(arange(1,K)) + dot(exp(dot(nrdt,(M - m - 1))),Thetbar1) - dot(exp(dot(nqdt,(M - m - 1))),Thetbar2)
# PROJ_Barrier.m:339
                if rebate != 0:
                    Val=Val + val_rebate
# PROJ_Barrier.m:342
    
    if interp_Atend == 1:
        dd=0 - (xmin + dot((nnot - 1),dx))
# PROJ_Barrier.m:350
        price=Val(nnot) + dot((Val(nnot + 1) - Val(nnot)),dd) / dx
# PROJ_Barrier.m:351
    else:
        price=Val(nnot)
# PROJ_Barrier.m:353
    
    return price
    
if __name__ == '__main__':
    pass
    