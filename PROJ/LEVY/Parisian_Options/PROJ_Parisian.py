# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# PROJ_Parisian.m

    
@function
def PROJ_Parisian(N=None,call=None,down=None,S_0=None,W=None,H=None,M=None,r=None,rnCHF=None,T=None,Gamm=None,resetting=None,alph=None,*args,**kwargs):
    varargin = PROJ_Parisian.varargin
    nargin = PROJ_Parisian.nargin

    #########################################################
# About: Pricing Function for Parisian-style barrier options using PROJ method
# Models Supported: Levy Processes, including jump diffusions and Black-Scholes model
# Returns: price of contract
# Author: Justin Lars Kirkby
    
    # ----------------------
# Contract/Model Params 
# ----------------------
# S_0 = initial stock price (e.g. 100)
# W   = strike  (e.g. 100)
# r   = interest rate (e.g. 0.05)
# T   = time remaining until maturity (in years, e.g. T=1)
# M   = number of subintervals of [0,T] (total of M+1 monitoring points in time grid, including S_0)
# call = 1 for call (else put)
# down = 1 for down and out (otherwise it's up and out)
# H    = barrier
# Gamm = maximum number of discretely monitored excursions into the knockout region allowed (more than this results in knockout)
# resetting = 1 if a reseting type parisian option (otherwise its cumulative, ie never resets)
# rnCHF = risk netural characteristic function (function handle with single argument)
    
    # ----------------------
# Numerical (PROJ) Params 
# ----------------------
# alph  = grid with is 2*alph
# N     = number of grid/basis points (power of 2, e.g. 2^12), resolution = 2*alph/(N-1)
#########################################################
    
    if logical_not((down == 1 and call != 1)) and logical_not((down != 1 and call == 1)):
        fprintf('Sorry, currently only Up and out calls, and down and out puts have been coded \n')
        return price
    
    gamm0=1
# PROJ_Parisian.m:35
    
    dt=T / M
# PROJ_Parisian.m:37
    nrdt=dot(- r,dt)
# PROJ_Parisian.m:38
    h=log(H / S_0)
# PROJ_Parisian.m:39
    lws=log(W / S_0)
# PROJ_Parisian.m:40
    ######  Gaussian Quad Constants
    q_plus=(1 + sqrt(3 / 5)) / 2
# PROJ_Parisian.m:43
    q_minus=(1 - sqrt(3 / 5)) / 2
# PROJ_Parisian.m:43
    b3=sqrt(15)
# PROJ_Parisian.m:44
    b4=b3 / 10
# PROJ_Parisian.m:44
    dx=dot(2,alph) / (N - 1)
# PROJ_Parisian.m:46
    xmin=- alph / 2
# PROJ_Parisian.m:47
    n_h=floor((h - xmin) / dx + 1)
# PROJ_Parisian.m:49
    xmin=h - dot((n_h - 1),dx)
# PROJ_Parisian.m:50
    
    if h != 0:
        nnot=floor(1 - xmin / dx)
# PROJ_Parisian.m:54
        if abs(h) > dx:
            dx=(h - 0) / (n_h - nnot)
# PROJ_Parisian.m:56
            xmin=dot(dx,(1 - nnot))
# PROJ_Parisian.m:57
            #n_h = floor((h-xmin)/dx +1);  #NOT Numerically Stable
            n_h=floor(nnot + h / dx)
# PROJ_Parisian.m:59
    else:
        nnot=copy(n_h)
# PROJ_Parisian.m:62
    
    a=1 / dx
# PROJ_Parisian.m:65
    a2=a ** 2
# PROJ_Parisian.m:66
    zmin=dot((1 - N / 2),dx)
# PROJ_Parisian.m:67
    
    #Cons = 24*a2/N;
    Cons2=dot(dot(24,a2),exp(nrdt)) / N
# PROJ_Parisian.m:70
    dw=dot(dot(2,pi),a) / N
# PROJ_Parisian.m:71
    grand=dot(dw,(arange(1,N - 1)))
# PROJ_Parisian.m:72
    grand=multiply(multiply(exp(dot(dot(- 1j,zmin),grand)),rnCHF(grand)),(sin(grand / (dot(2,a))) / grand) ** 2.0) / (2 + cos(grand / a))
# PROJ_Parisian.m:73
    beta=dot(Cons2,real(fft(concat([1 / (dot(24,a2)),grand]))))
# PROJ_Parisian.m:74
    
    interp_Atend=0
# PROJ_Parisian.m:77
    if 0 < abs(h) and abs(h) < dx:
        interp_Atend=1
# PROJ_Parisian.m:79
    
    ###########################################################################
####   DETERMINE COMMON Params
###########################################################################
    K=N / 2
# PROJ_Parisian.m:85
    nbar=floor(dot(a,(lws - xmin)) + 1)
# PROJ_Parisian.m:86
    rho=lws - (xmin + dot((nbar - 1),dx))
# PROJ_Parisian.m:87
    zeta=dot(a,rho)
# PROJ_Parisian.m:88
    toepM=concat([[beta(arange(K,1,- 1)).T],[0],[beta(arange(dot(2,K) - 1,K,- 1),+ 1).T]])
# PROJ_Parisian.m:90
    toepM=fft(toepM)
# PROJ_Parisian.m:90
    #### PAYOFF CONSTANTS-----------------------------------
    varthet_01=dot(exp(dot(0.5,dx)),(dot(5,cosh(dot(b4,dx))) - dot(b3,sinh(dot(b4,dx))) + 4)) / 18
# PROJ_Parisian.m:93
    varthet_m10=dot(exp(dot(- 0.5,dx)),(dot(5,cosh(dot(b4,dx))) + dot(b3,sinh(dot(b4,dx))) + 4)) / 18
# PROJ_Parisian.m:94
    varthet_star=varthet_01 + varthet_m10
# PROJ_Parisian.m:95
    ###########################################################################
    if down == 1 and call != 1:
        #l = log(H/S_0);
        n_l=copy(n_h)
# PROJ_Parisian.m:102
        zeta_plus=dot(zeta,q_plus)
# PROJ_Parisian.m:104
        zeta_minus=dot(zeta,q_minus)
# PROJ_Parisian.m:104
        rho_plus=dot(rho,q_plus)
# PROJ_Parisian.m:105
        rho_minus=dot(rho,q_minus)
# PROJ_Parisian.m:105
        ed1=exp(rho_minus)
# PROJ_Parisian.m:107
        ed2=exp(rho / 2)
# PROJ_Parisian.m:107
        ed3=exp(rho_plus)
# PROJ_Parisian.m:107
        dbar_1=zeta ** 2 / 2
# PROJ_Parisian.m:109
        dbar_0=zeta - dbar_1
# PROJ_Parisian.m:110
        d_0=dot(zeta,(dot(5,(dot((1 - zeta_minus),ed1) + dot((1 - zeta_plus),ed3))) + dot(dot(4,(2 - zeta)),ed2))) / 18
# PROJ_Parisian.m:111
        d_1=dot(zeta,(dot(5,(dot(zeta_minus,ed1) + dot(zeta_plus,ed3))) + dot(dot(4,zeta),ed2))) / 18
# PROJ_Parisian.m:112
        Thet=zeros(K,1)
# PROJ_Parisian.m:115
        Thet[arange(1,nbar - 1)]=W - dot(dot(exp(xmin + dot(dx,(arange(0,nbar - 2)))),S_0),varthet_star)
# PROJ_Parisian.m:116
        Thet[nbar]=dot(W,(0.5 + dbar_0 - dot(exp(- rho),(varthet_m10 + d_0))))
# PROJ_Parisian.m:117
        Thet[nbar + 1]=dot(W,(dbar_1 - dot(exp(- rho),d_1)))
# PROJ_Parisian.m:118
        Val=zeros(K,Gamm + 1)
# PROJ_Parisian.m:121
        p=ifft(multiply(toepM,fft(concat([[Thet],[zeros(K,1)]]))))
# PROJ_Parisian.m:122
        for j in arange(1,Gamm).reshape(-1):
            Val[arange(),j]=p(arange(1,K))
# PROJ_Parisian.m:124
        Thet[arange(1,n_l - 1)]=0
# PROJ_Parisian.m:126
        Thet[n_l]=W / 2 - dot(H,varthet_01)
# PROJ_Parisian.m:127
        p=ifft(multiply(toepM,fft(concat([[Thet],[zeros(K,1)]]))))
# PROJ_Parisian.m:128
        Val[arange(),Gamm + 1]=p(arange(1,K))
# PROJ_Parisian.m:129
        #### RESETTING PARISIAN
    ##########################################################
        if resetting == 1:
            for m in arange(M - 2,0,- 1).reshape(-1):
                #These Thet must be kept outside of loop, else they will be inadvertently altered
                Thet[arange(n_l + 1,K - 1)]=(Val(arange(n_l,K - 2),1) + dot(10,Val(arange(n_l + 1,K - 1),1)) + Val(arange(n_l + 2,K),1)) / 12
# PROJ_Parisian.m:137
                Thet[K]=(dot(13,Val(K,1)) + dot(15,Val(K - 1,1)) - dot(5,Val(K - 2,1)) + Val(K - 3,1)) / 48
# PROJ_Parisian.m:138
                ThetPartial=(dot(13,Val(n_l,1)) + dot(15,Val(n_l + 1,1)) - dot(5,Val(n_l + 2,1)) + Val(n_l + 3,1)) / 48
# PROJ_Parisian.m:139
                for j in arange(1,Gamm).reshape(-1):
                    Thet[1]=(dot(13,Val(1,j + 1)) + dot(15,Val(2,j + 1)) - dot(5,Val(3,j + 1)) + Val(4,j + 1)) / 48
# PROJ_Parisian.m:142
                    Thet[arange(2,n_l - 1)]=(Val(arange(1,n_l - 2),j + 1) + dot(10,Val(arange(2,n_l - 1),j + 1)) + Val(arange(3,n_l),j + 1)) / 12
# PROJ_Parisian.m:143
                    Thet[n_l]=(dot(13,Val(n_l,j + 1)) + dot(15,Val(n_l - 1,j + 1)) - dot(5,Val(n_l - 2,j + 1)) + Val(n_l - 3,j + 1)) / 48 + ThetPartial
# PROJ_Parisian.m:144
                    p=ifft(multiply(toepM,fft(concat([[Thet(arange(1,K))],[zeros(K,1)]]))))
# PROJ_Parisian.m:147
                    Val[arange(),j]=p(arange(1,K))
# PROJ_Parisian.m:148
                ### Now to Gamm+1
                j=Gamm + 1
# PROJ_Parisian.m:152
                Thet[arange(1,n_l - 1)]=0
# PROJ_Parisian.m:153
                Thet[n_l]=ThetPartial
# PROJ_Parisian.m:154
                p=ifft(multiply(toepM,fft(concat([[Thet],[zeros(K,1)]]))))
# PROJ_Parisian.m:156
                Val[arange(),j]=p(arange(1,K))
# PROJ_Parisian.m:157
            ##########################################################
    #### CUMULATIVE PARISIAN
    ##########################################################
        else:
            for m in arange(M - 2,0,- 1).reshape(-1):
                for j in arange(1,Gamm).reshape(-1):
                    Thet[1]=(dot(13,Val(1,j + 1)) + dot(15,Val(2,j + 1)) - dot(5,Val(3,j + 1)) + Val(4,j + 1)) / 48
# PROJ_Parisian.m:166
                    Thet[arange(2,n_l - 1)]=(Val(arange(1,n_l - 2),j + 1) + dot(10,Val(arange(2,n_l - 1),j + 1)) + Val(arange(3,n_l),j + 1)) / 12
# PROJ_Parisian.m:167
                    Thet[n_l]=(dot(13,Val(n_l,j + 1)) + dot(15,Val(n_l - 1,j + 1)) - dot(5,Val(n_l - 2,j + 1)) + Val(n_l - 3,j + 1)) / 48 + (dot(13,Val(n_l,j)) + dot(15,Val(n_l + 1,j)) - dot(5,Val(n_l + 2,j)) + Val(n_l + 3,j)) / 48
# PROJ_Parisian.m:169
                    Thet[arange(n_l + 1,K - 1)]=(Val(arange(n_l,K - 2),j) + dot(10,Val(arange(n_l + 1,K - 1),j)) + Val(arange(n_l + 2,K),j)) / 12
# PROJ_Parisian.m:172
                    Thet[K]=(dot(13,Val(K,j)) + dot(15,Val(K - 1,j)) - dot(5,Val(K - 2,j)) + Val(K - 3,j)) / 48
# PROJ_Parisian.m:173
                    p=ifft(multiply(toepM,fft(concat([[Thet(arange(1,K))],[zeros(K,1)]]))))
# PROJ_Parisian.m:175
                    Val[arange(),j]=p(arange(1,K))
# PROJ_Parisian.m:176
                ### Now to Gamm+1
                j=Gamm + 1
# PROJ_Parisian.m:180
                Thet[arange(1,n_l - 1)]=0
# PROJ_Parisian.m:181
                Thet[n_l]=(dot(13,Val(n_l,j)) + dot(15,Val(n_l + 1,j)) - dot(5,Val(n_l + 2,j)) + Val(n_l + 3,j)) / 48
# PROJ_Parisian.m:182
                Thet[arange(n_l + 1,K - 1)]=(Val(arange(n_l,K - 2),j) + dot(10,Val(arange(n_l + 1,K - 1),j)) + Val(arange(n_l + 2,K),j)) / 12
# PROJ_Parisian.m:183
                p=ifft(multiply(toepM,fft(concat([[Thet(arange(1,K))],[zeros(K,1)]]))))
# PROJ_Parisian.m:185
                Val[arange(),j]=p(arange(1,K))
# PROJ_Parisian.m:186
        #######################################################
#######################################################
    else:
        if down != 1 and call == 1:
            #u    = log(H/S_0);
            n_u=copy(n_h)
# PROJ_Parisian.m:193
            sigma=1 - zeta
# PROJ_Parisian.m:195
            sigma_plus=dot((q_plus - 0.5),sigma)
# PROJ_Parisian.m:195
            sigma_minus=dot((q_minus - 0.5),sigma)
# PROJ_Parisian.m:195
            es1=exp(dot(dx,sigma_plus))
# PROJ_Parisian.m:197
            es2=exp(dot(dx,sigma_minus))
# PROJ_Parisian.m:197
            dbar_0=0.5 + dot(zeta,(dot(0.5,zeta) - 1))
# PROJ_Parisian.m:199
            dbar_1=dot(sigma,(1 - dot(0.5,sigma)))
# PROJ_Parisian.m:200
            d_0=dot(dot(exp(dot((rho + dx),0.5)),sigma ** 2) / 18,(dot(5,(dot((1 - q_minus),es2) + dot((1 - q_plus),es1))) + 4))
# PROJ_Parisian.m:202
            d_1=dot(dot(exp(dot((rho - dx),0.5)),sigma) / 18,(dot(5,(dot((dot(0.5,(zeta + 1)) + sigma_minus),es2) + dot((dot(0.5,(zeta + 1)) + sigma_plus),es1))) + dot(4,(zeta + 1))))
# PROJ_Parisian.m:203
            Thet=zeros(K,1)
# PROJ_Parisian.m:207
            Thet[nbar]=dot(W,(dot(exp(- rho),d_0) - dbar_0))
# PROJ_Parisian.m:208
            Thet[nbar + 1]=dot(W,(dot(exp(dx - rho),(varthet_01 + d_1)) - (0.5 + dbar_1)))
# PROJ_Parisian.m:209
            Thet[arange(nbar + 2,K)]=dot(dot(exp(xmin + dot(dx,(arange(nbar + 1,K - 1)))),S_0),varthet_star) - W
# PROJ_Parisian.m:210
            Val=zeros(K,Gamm + 1)
# PROJ_Parisian.m:212
            p=ifft(multiply(toepM,fft(concat([[Thet],[zeros(K,1)]]))))
# PROJ_Parisian.m:213
            for j in arange(1,Gamm).reshape(-1):
                Val[arange(),j]=p(arange(1,K))
# PROJ_Parisian.m:215
            Thet[arange(n_u + 1,K)]=0
# PROJ_Parisian.m:218
            Thet[n_u]=dot(H,varthet_m10) - dot(0.5,W)
# PROJ_Parisian.m:219
            p=ifft(multiply(toepM,fft(concat([[Thet],[zeros(K,1)]]))))
# PROJ_Parisian.m:220
            Val[arange(),Gamm + 1]=p(arange(1,K))
# PROJ_Parisian.m:221
            #### RESETTING PARISIAN
    ##########################################################
    ### For the resetting, its more efficient to pull the
    ### Thet(1:n_u-1) ouside of the loop through j = 1:Gamm
            if resetting == 1:
                for m in arange(M - 2,0,- 1).reshape(-1):
                    #NOTE: these must be defined outside of loop, else we change them and then the next function requires the unchanged value!
                    Thet[1]=(dot(13,Val(1,1)) + dot(15,Val(2,1)) - dot(5,Val(3,1)) + Val(4,1)) / 48
# PROJ_Parisian.m:232
                    Thet[arange(2,n_u - 1)]=(Val(arange(1,n_u - 2),1) + dot(10,Val(arange(2,n_u - 1),1)) + Val(arange(3,n_u),1)) / 12
# PROJ_Parisian.m:233
                    ThetPartial=(dot(13,Val(n_u,1)) + dot(15,Val(n_u - 1,1)) - dot(5,Val(n_u - 2,1)) + Val(n_u - 3,1)) / 48
# PROJ_Parisian.m:234
                    for j in arange(1,Gamm).reshape(-1):
                        Thet[n_u]=ThetPartial + (dot(13,Val(n_u,j + 1)) + dot(15,Val(n_u + 1,j + 1)) - dot(5,Val(n_u + 2,j + 1)) + Val(n_u + 3,j + 1)) / 48
# PROJ_Parisian.m:237
                        Thet[arange(n_u + 1,K - 1)]=(Val(arange(n_u,K - 2),j + 1) + dot(10,Val(arange(n_u + 1,K - 1),j + 1)) + Val(arange(n_u + 2,K),j + 1)) / 12
# PROJ_Parisian.m:239
                        Thet[K]=(dot(13,Val(K,j + 1)) + dot(15,Val(K - 1,j + 1)) - dot(5,Val(K - 2,j + 1)) + Val(K - 3,j + 1)) / 48
# PROJ_Parisian.m:240
                        p=ifft(multiply(toepM,fft(concat([[Thet(arange(1,K))],[zeros(K,1)]]))))
# PROJ_Parisian.m:242
                        Val[arange(),j]=p(arange(1,K))
# PROJ_Parisian.m:243
                    ### Now to Gamm+1
                    j=Gamm + 1
# PROJ_Parisian.m:247
                    Thet[n_u]=ThetPartial
# PROJ_Parisian.m:248
                    Thet[arange(n_u + 1,K)]=0
# PROJ_Parisian.m:249
                    p=ifft(multiply(toepM,fft(concat([[Thet(arange(1,K))],[zeros(K,1)]]))))
# PROJ_Parisian.m:251
                    Val[arange(),j]=p(arange(1,K))
# PROJ_Parisian.m:252
                ##########################################################
    #### CUMULATIVE PARISIAN
    ##########################################################
            else:
                for m in arange(M - 2,0,- 1).reshape(-1):
                    for j in arange(1,Gamm).reshape(-1):
                        Thet[1]=(dot(13,Val(1,j)) + dot(15,Val(2,j)) - dot(5,Val(3,j)) + Val(4,j)) / 48
# PROJ_Parisian.m:260
                        Thet[arange(2,n_u - 1)]=(Val(arange(1,n_u - 2),j) + dot(10,Val(arange(2,n_u - 1),j)) + Val(arange(3,n_u),j)) / 12
# PROJ_Parisian.m:261
                        Thet[n_u]=(dot(13,Val(n_u,j)) + dot(15,Val(n_u - 1,j)) - dot(5,Val(n_u - 2,j)) + Val(n_u - 3,j)) / 48 + (dot(13,Val(n_u,j + 1)) + dot(15,Val(n_u + 1,j + 1)) - dot(5,Val(n_u + 2,j + 1)) + Val(n_u + 3,j + 1)) / 48
# PROJ_Parisian.m:263
                        Thet[arange(n_u + 1,K - 1)]=(Val(arange(n_u,K - 2),j + 1) + dot(10,Val(arange(n_u + 1,K - 1),j + 1)) + Val(arange(n_u + 2,K),j + 1)) / 12
# PROJ_Parisian.m:266
                        Thet[K]=(dot(13,Val(K,j + 1)) + dot(15,Val(K - 1,j + 1)) - dot(5,Val(K - 2,j + 1)) + Val(K - 3,j + 1)) / 48
# PROJ_Parisian.m:267
                        p=ifft(multiply(toepM,fft(concat([[Thet(arange(1,K))],[zeros(K,1)]]))))
# PROJ_Parisian.m:269
                        Val[arange(),j]=p(arange(1,K))
# PROJ_Parisian.m:270
                    ### Now to Gamm+1
                    j=Gamm + 1
# PROJ_Parisian.m:274
                    Thet[1]=(dot(13,Val(1,j)) + dot(15,Val(2,j)) - dot(5,Val(3,j)) + Val(4,j)) / 48
# PROJ_Parisian.m:275
                    Thet[arange(2,n_u - 1)]=(Val(arange(1,n_u - 2),j) + dot(10,Val(arange(2,n_u - 1),j)) + Val(arange(3,n_u),j)) / 12
# PROJ_Parisian.m:276
                    Thet[n_u]=(dot(13,Val(n_u,j)) + dot(15,Val(n_u - 1,j)) - dot(5,Val(n_u - 2,j)) + Val(n_u - 3,j)) / 48
# PROJ_Parisian.m:277
                    Thet[arange(n_u + 1,K)]=0
# PROJ_Parisian.m:278
                    p=ifft(multiply(toepM,fft(concat([[Thet(arange(1,K))],[zeros(K,1)]]))))
# PROJ_Parisian.m:280
                    Val[arange(),j]=p(arange(1,K))
# PROJ_Parisian.m:281
    
    if interp_Atend != 1:
        price=Val(nnot,gamm0)
# PROJ_Parisian.m:288
    else:
        #     Use 5 Point Cubic Interpolation
#     xnot = xmin +(nnot-1)*dx;
#     xs = [xnot-2*dx,xnot-dx,xnot,xnot+dx,xnot+2*dx];
#     ys = [Val(nnot-2,1),Val(nnot-1,1),Val(nnot,1),Val(nnot+1,1),Val(nnot+2,1)];
#     price = spline(xs,ys,0);
        dd=0 - (xmin + dot((nnot - 1),dx))
# PROJ_Parisian.m:297
        price=Val(nnot,gamm0) + dot((Val(nnot + 1,gamm0) - Val(nnot,gamm0)),dd) / dx
# PROJ_Parisian.m:298
    
    return price
    
if __name__ == '__main__':
    pass
    