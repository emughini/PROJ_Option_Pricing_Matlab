# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Simulate_StochVol_Jumps_func.m

    
@function
def Simulate_StochVol_Jumps_func(N_sim=None,M=None,T=None,S_0=None,r=None,q=None,SVModel=None,SVModelParams=None,jumpModel=None,jumpParams=None,*args,**kwargs):
    varargin = Simulate_StochVol_Jumps_func.varargin
    nargin = Simulate_StochVol_Jumps_func.nargin

    # Simulates Paths of Stochastic Volatility Models (basic Euler Scheme for most cases) with jumps
# By default, if no jumpModel or jumpParams are passed, it defaults to stochastic vol without jumps
    
    # N_sim = # paths
# M = #time steps on [0,T], ie dt =T/M   
# T = final time
# S_0 = initial underlying (spot) value
# r = interest rate
# q = dividend / convenience yield
    
    # Note: returns paths of dimension (N_sim,M+1), since they include S_0
    
    #===================================
# jumpModel: 0 = NoJumps, 1 = NormalJumps, 2 = DEJumps, 3 = MixedNormalJumps
#===================================
# SVModel:    (with parameters)
#        1 = HESTON:       Sigmav, v0, rho, eta, theta
#        2 = STEIN-STEIN:  Sigmav, v0, rho, eta, theta
#        3 = 3/2 MODEL:    Sigmav, v0, rho, eta, theta
#        4 = 4/2 MODEL:    Sigmav, v0, rho, eta, theta, aa, bb
#        5 = HULL-WHITE:   Sigmav, v0, rho, av
#        6 = SCOTT:        Sigmav, v0, rho, eta, theta
#        7 = ALPHA-HYPER:  Sigmav, v0, rho, eta, theta
#        8 = "VAR" MODEL:  Sigmav, v0, rho, eta, theta
#        9 = Jacobi Model: vmin, vmax, Sigmav, v0, rho, eta, theta
    
    #==============================
# Initialize Common Params/Vectors
#==============================
    Sigmav=SVModelParams.Sigmav
# Simulate_StochVol_Jumps_func.m:31
    v0=SVModelParams.v0
# Simulate_StochVol_Jumps_func.m:32
    rho=SVModelParams.rho
# Simulate_StochVol_Jumps_func.m:33
    if nargin < 10:
        jumpModel=0
# Simulate_StochVol_Jumps_func.m:36
        jumpParams=cellarray([])
# Simulate_StochVol_Jumps_func.m:36
    
    if SVModel == 1 or SVModel == 2 or SVModel == 3 or SVModel == 4 or SVModel == 6 or SVModel == 7 or SVModel == 8 or SVModel == 9:
        theta=SVModelParams.theta
# Simulate_StochVol_Jumps_func.m:40
        eta=SVModelParams.eta
# Simulate_StochVol_Jumps_func.m:41
    
    if SVModel == 4:
        aa=SVModelParams.aa
# Simulate_StochVol_Jumps_func.m:44
        bb=SVModelParams.bb
# Simulate_StochVol_Jumps_func.m:45
    
    if SVModel == 5 or SVModel == 7:
        av=SVModelParams.av
# Simulate_StochVol_Jumps_func.m:48
    
    Spath=zeros(N_sim,M + 1)
# Simulate_StochVol_Jumps_func.m:51
    Spath[arange(),1]=S_0
# Simulate_StochVol_Jumps_func.m:52
    dt=T / M
# Simulate_StochVol_Jumps_func.m:54
    sqdt=sqrt(dt)
# Simulate_StochVol_Jumps_func.m:55
    sqdtrho1=dot(sqdt,rho)
# Simulate_StochVol_Jumps_func.m:56
    sqdtrho2=dot(sqdt,sqrt(1 - rho ** 2))
# Simulate_StochVol_Jumps_func.m:57
    #==============================
# Initialize Jump Model Params and JumpFunc (function handle)
#==============================
### NOTE:  Jump Model is of the form in LOG space
### X(m+1) = X(m) + drift + Brownian Component + sum(Jumps on [m,m+1])
### By Jump we mean log(Y), e.g. in Merton Model, Jump ~ Normal (since we are in log space )
    
    if jumpModel > 0:
        lambda_=jumpParams.lambda
# Simulate_StochVol_Jumps_func.m:67
        kappa=jumpParams.kappa
# Simulate_StochVol_Jumps_func.m:68
        Zeta=r - q - dot(lambda_,kappa)
# Simulate_StochVol_Jumps_func.m:70
        lamdt=dot(lambda_,dt)
# Simulate_StochVol_Jumps_func.m:71
        if jumpModel == 1:
            muJ=jumpParams.muJ
# Simulate_StochVol_Jumps_func.m:74
            sigJ=jumpParams.sigJ
# Simulate_StochVol_Jumps_func.m:75
            JumpFunc=lambda n=None: sum(muJ + dot(sigJ,randn(n,1)))
# Simulate_StochVol_Jumps_func.m:76
        else:
            if jumpModel == 2:
                p_up=jumpParams.p_up
# Simulate_StochVol_Jumps_func.m:79
                eta1=jumpParams.eta1
# Simulate_StochVol_Jumps_func.m:80
                eta2=jumpParams.eta2
# Simulate_StochVol_Jumps_func.m:81
                JumpFunc=lambda n=None: sum(DoubleExpoRnd(n,p_up,eta1,eta2))
# Simulate_StochVol_Jumps_func.m:82
            else:
                if jumpModel == 3:
                    p_up=jumpParams.p_up
# Simulate_StochVol_Jumps_func.m:85
                    a1=jumpParams.a1
# Simulate_StochVol_Jumps_func.m:86
                    b1=jumpParams.b1
# Simulate_StochVol_Jumps_func.m:86
                    a2=jumpParams.a2
# Simulate_StochVol_Jumps_func.m:87
                    b2=jumpParams.b2
# Simulate_StochVol_Jumps_func.m:87
                    JumpFunc=lambda n=None: sum(MixedNormalRnd(n,p_up,a1,b1,a2,b2))
# Simulate_StochVol_Jumps_func.m:88
    else:
        Zeta=r - q
# Simulate_StochVol_Jumps_func.m:91
    
    #==============================
# Simulate Based on Specific StochVol Model
#==============================
    
    ##################################################################################
    if SVModel == 1:
        # NOTE: Uses Full Truncation Scheme studied in Lord et. al. (2010)
        vOld=dot(v0,ones(N_sim,1))
# Simulate_StochVol_Jumps_func.m:101
        sqvOld=dot(sqrt(v0),ones(N_sim,1))
# Simulate_StochVol_Jumps_func.m:102
        edt=dot(eta,dt)
# Simulate_StochVol_Jumps_func.m:103
        if jumpModel == 0:
            for m in arange(1,M).reshape(-1):
                W1=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:107
                W2=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:107
                Spath[arange(),m + 1]=multiply(Spath(arange(),m),exp(dot((Zeta - dot(0.5,sqvOld ** 2)),dt) + multiply(dot(sqdt,sqvOld),W1)))
# Simulate_StochVol_Jumps_func.m:108
                vNew=vOld - dot(edt,(max(0,vOld) - theta)) + multiply(dot(Sigmav,sqvOld),(dot(sqdtrho1,W1) + dot(sqdtrho2,W2)))
# Simulate_StochVol_Jumps_func.m:110
                vOld=copy(vNew)
# Simulate_StochVol_Jumps_func.m:111
                sqvOld=sqrt(max(0,vOld))
# Simulate_StochVol_Jumps_func.m:112
        else:
            for m in arange(1,M).reshape(-1):
                Poi=PoissonRnd(N_sim,lamdt)
# Simulate_StochVol_Jumps_func.m:117
                sumJumpsVec=zeros(N_sim,1)
# Simulate_StochVol_Jumps_func.m:118
                for n in arange(1,N_sim).reshape(-1):
                    if Poi(n) > 0:
                        sumJumpsVec[n]=JumpFunc(Poi(n))
# Simulate_StochVol_Jumps_func.m:121
                W1=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:125
                W2=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:125
                Spath[arange(),m + 1]=multiply(Spath(arange(),m),exp(dot((Zeta - dot(0.5,sqvOld ** 2)),dt) + sumJumpsVec + multiply(dot(sqdt,sqvOld),W1)))
# Simulate_StochVol_Jumps_func.m:126
                vNew=vOld - dot(edt,(max(0,vOld) - theta)) + multiply(dot(Sigmav,sqvOld),(dot(sqdtrho1,W1) + dot(sqdtrho2,W2)))
# Simulate_StochVol_Jumps_func.m:128
                vOld=copy(vNew)
# Simulate_StochVol_Jumps_func.m:129
                sqvOld=sqrt(max(0,vOld))
# Simulate_StochVol_Jumps_func.m:130
        ##################################################################################        
##################################################################################
    else:
        if SVModel == 2:
            driftv=dot(dot(eta,theta),dt)
# Simulate_StochVol_Jumps_func.m:137
            consv=1 - dot(eta,dt)
# Simulate_StochVol_Jumps_func.m:138
            vOld=dot(v0,ones(N_sim,1))
# Simulate_StochVol_Jumps_func.m:140
            if jumpModel == 0:
                for m in arange(1,M).reshape(-1):
                    W1=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:144
                    W2=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:144
                    Spath[arange(),m + 1]=multiply(Spath(arange(),m),exp(dot((Zeta - dot(0.5,vOld ** 2)),dt) + multiply(dot(sqdt,vOld),W1)))
# Simulate_StochVol_Jumps_func.m:145
                    #Spath(:,m+1) = Spath(:,m).*(conss + vOld.*(sqrho1*W1 + sqrho2*W2));  #level scheme
                    vNew=driftv + dot(vOld,consv) + dot(Sigmav,(dot(sqdtrho1,W1) + dot(sqdtrho2,W2)))
# Simulate_StochVol_Jumps_func.m:147
                    vOld=max(0,vNew)
# Simulate_StochVol_Jumps_func.m:149
            else:
                for m in arange(1,M).reshape(-1):
                    Poi=PoissonRnd(N_sim,lamdt)
# Simulate_StochVol_Jumps_func.m:153
                    #Poi = poissrnd(lamdt, N_sim,1);  #Generate Poisson Column Vector of size N_Sim
                    sumJumpsVec=zeros(N_sim,1)
# Simulate_StochVol_Jumps_func.m:155
                    for n in arange(1,N_sim).reshape(-1):
                        if Poi(n) > 0:
                            sumJumpsVec[n]=JumpFunc(Poi(n))
# Simulate_StochVol_Jumps_func.m:158
                    W1=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:161
                    W2=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:161
                    Spath[arange(),m + 1]=multiply(Spath(arange(),m),exp(dot((Zeta - dot(0.5,vOld ** 2)),dt) + sumJumpsVec + multiply(dot(sqdt,vOld),W1)))
# Simulate_StochVol_Jumps_func.m:162
                    vNew=driftv + dot(vOld,consv) + dot(Sigmav,(dot(sqdtrho1,W1) + dot(sqdtrho2,W2)))
# Simulate_StochVol_Jumps_func.m:163
                    vOld=max(0,vNew)
# Simulate_StochVol_Jumps_func.m:165
            ##################################################################################       
##################################################################################
        else:
            if SVModel == 3:
                vOld=dot(v0,ones(N_sim,1))
# Simulate_StochVol_Jumps_func.m:173
                sqvOld=dot(sqrt(v0),ones(N_sim,1))
# Simulate_StochVol_Jumps_func.m:174
                if jumpModel == 0:
                    for m in arange(1,M).reshape(-1):
                        W1=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:178
                        W2=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:178
                        Spath[arange(),m + 1]=multiply(Spath(arange(),m),exp(dot((Zeta - dot(0.5,vOld)),dt) + multiply(dot(sqdt,sqvOld),W1)))
# Simulate_StochVol_Jumps_func.m:179
                        #Spath(:,m+1) = Spath(:,m)*( (1+r)*dt + sqrt(vOld)*(sqrho1*W1 + sqrho2*W2));  #level scheme
                        vNew=multiply(vOld,(1 + dot(dot(eta,(theta - vOld)),dt) + multiply(dot(Sigmav,sqvOld),(dot(sqdtrho1,W1) + dot(sqdtrho2,W2)))))
# Simulate_StochVol_Jumps_func.m:181
                        vOld=max(0,vNew)
# Simulate_StochVol_Jumps_func.m:183
                        sqvOld=sqrt(vOld)
# Simulate_StochVol_Jumps_func.m:184
                else:
                    for m in arange(1,M).reshape(-1):
                        Poi=PoissonRnd(N_sim,lamdt)
# Simulate_StochVol_Jumps_func.m:188
                        #Poi = poissrnd(lamdt, N_sim,1);  #Generate Poisson Column Vector of size N_Sim
                        sumJumpsVec=zeros(N_sim,1)
# Simulate_StochVol_Jumps_func.m:190
                        for n in arange(1,N_sim).reshape(-1):
                            if Poi(n) > 0:
                                sumJumpsVec[n]=JumpFunc(Poi(n))
# Simulate_StochVol_Jumps_func.m:193
                        W1=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:197
                        W2=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:197
                        Spath[arange(),m + 1]=multiply(Spath(arange(),m),exp(dot((Zeta - dot(0.5,vOld)),dt) + sumJumpsVec + multiply(dot(sqdt,sqvOld),W1)))
# Simulate_StochVol_Jumps_func.m:198
                        vNew=multiply(vOld,(1 + dot(dot(eta,(theta - vOld)),dt) + multiply(dot(Sigmav,sqvOld),(dot(sqdtrho1,W1) + dot(sqdtrho2,W2)))))
# Simulate_StochVol_Jumps_func.m:199
                        vOld=max(0,vNew)
# Simulate_StochVol_Jumps_func.m:201
                        sqvOld=sqrt(vOld)
# Simulate_StochVol_Jumps_func.m:202
                ##################################################################################        
##################################################################################
            else:
                if SVModel == 4:
                    expEta=exp(dot(- eta,dt))
# Simulate_StochVol_Jumps_func.m:209
                    driftv=dot(theta,(1 - expEta))
# Simulate_StochVol_Jumps_func.m:210
                    vOld=dot(v0,ones(N_sim,1))
# Simulate_StochVol_Jumps_func.m:212
                    sqvOld=dot(sqrt(v0),ones(N_sim,1))
# Simulate_StochVol_Jumps_func.m:213
                    if jumpModel == 0:
                        for m in arange(1,M).reshape(-1):
                            W1=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:216
                            W2=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:216
                            Spath[arange(),m + 1]=multiply(Spath(arange(),m),exp(dot((Zeta - dot(0.5,vOld)),dt) + multiply(dot(sqdt,(dot(aa,sqvOld) + bb / sqvOld)),W1)))
# Simulate_StochVol_Jumps_func.m:217
                            #Spath(:,m+1) = Spath(:,m)*( (1+r)*dt + sqrt(vOld)*(sqrho1*W1 + sqrho2*W2));  #level scheme
                            vNew=driftv + dot(vOld,expEta) + multiply(dot(Sigmav,sqvOld),(dot(sqdtrho1,W1) + dot(sqdtrho2,W2)))
# Simulate_StochVol_Jumps_func.m:219
                            vOld=abs(vNew)
# Simulate_StochVol_Jumps_func.m:221
                            #vOld = max(0,vNew);
                            sqvOld=sqrt(vOld)
# Simulate_StochVol_Jumps_func.m:223
                    else:
                        for m in arange(1,M).reshape(-1):
                            Poi=PoissonRnd(N_sim,lamdt)
# Simulate_StochVol_Jumps_func.m:227
                            sumJumpsVec=zeros(N_sim,1)
# Simulate_StochVol_Jumps_func.m:228
                            for n in arange(1,N_sim).reshape(-1):
                                if Poi(n) > 0:
                                    sumJumpsVec[n]=JumpFunc(Poi(n))
# Simulate_StochVol_Jumps_func.m:231
                            W1=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:234
                            W2=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:234
                            Spath[arange(),m + 1]=multiply(Spath(arange(),m),exp(dot((Zeta - dot(0.5,vOld)),dt) + sumJumpsVec + multiply(dot(sqdt,(dot(aa,sqvOld) + bb / sqvOld)),W1)))
# Simulate_StochVol_Jumps_func.m:235
                            vNew=driftv + dot(vOld,expEta) + multiply(dot(Sigmav,sqvOld),(dot(sqdtrho1,W1) + dot(sqdtrho2,W2)))
# Simulate_StochVol_Jumps_func.m:236
                            vOld=abs(vNew)
# Simulate_StochVol_Jumps_func.m:237
                            #vOld = max(0,vNew); #least biased scheme
                            sqvOld=sqrt(vOld)
# Simulate_StochVol_Jumps_func.m:239
                    ##################################################################################    
##################################################################################
                else:
                    if SVModel == 5:
                        driftv=dot((av - Sigmav ** 2 / 2),dt)
# Simulate_StochVol_Jumps_func.m:248
                        vOld=dot(v0,ones(N_sim,1))
# Simulate_StochVol_Jumps_func.m:249
                        if jumpModel == 0:
                            for m in arange(1,M).reshape(-1):
                                W1=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:253
                                W2=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:253
                                Spath[arange(),m + 1]=multiply(Spath(arange(),m),exp(dot((Zeta - dot(0.5,vOld)),dt) + multiply(dot(sqdt,sqrt(vOld)),W1)))
# Simulate_StochVol_Jumps_func.m:254
                                #Spath(:,m+1) = Spath(:,m)*( (1+r)*dt + sqrt(vOld)*(sqrho1*W1 + sqrho2*W2));  #level scheme
                                vNew=multiply(vOld,exp(driftv + dot(Sigmav,(dot(sqdtrho1,W1) + dot(sqdtrho2,W2)))))
# Simulate_StochVol_Jumps_func.m:256
                                vOld=max(0,vNew)
# Simulate_StochVol_Jumps_func.m:257
                        else:
                            for m in arange(1,M).reshape(-1):
                                Poi=PoissonRnd(N_sim,lamdt)
# Simulate_StochVol_Jumps_func.m:261
                                sumJumpsVec=zeros(N_sim,1)
# Simulate_StochVol_Jumps_func.m:262
                                for n in arange(1,N_sim).reshape(-1):
                                    if Poi(n) > 0:
                                        sumJumpsVec[n]=JumpFunc(Poi(n))
# Simulate_StochVol_Jumps_func.m:265
                                W1=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:268
                                W2=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:268
                                Spath[arange(),m + 1]=multiply(Spath(arange(),m),exp(dot((Zeta - dot(0.5,vOld)),dt) + sumJumpsVec + multiply(dot(sqdt,sqrt(vOld)),W1)))
# Simulate_StochVol_Jumps_func.m:269
                                vNew=multiply(vOld,exp(driftv + dot(Sigmav,(dot(sqdtrho1,W1) + dot(sqdtrho2,W2)))))
# Simulate_StochVol_Jumps_func.m:270
                                vOld=max(0,vNew)
# Simulate_StochVol_Jumps_func.m:271
                        ##################################################################################    
##################################################################################
                    else:
                        if SVModel == 6:
                            driftv=dot(dot(eta,theta),dt)
# Simulate_StochVol_Jumps_func.m:278
                            consv=1 - dot(eta,dt)
# Simulate_StochVol_Jumps_func.m:279
                            vOld=dot(v0,ones(N_sim,1))
# Simulate_StochVol_Jumps_func.m:280
                            if jumpModel == 0:
                                for m in arange(1,M).reshape(-1):
                                    W1=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:284
                                    W2=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:284
                                    Spath[arange(),m + 1]=multiply(Spath(arange(),m),exp(dot((Zeta - dot(0.5,exp(dot(2,vOld)))),dt) + multiply(dot(sqdt,exp(vOld)),W1)))
# Simulate_StochVol_Jumps_func.m:285
                                    vNew=driftv + dot(vOld,consv) + dot(Sigmav,(dot(sqdtrho1,W1) + dot(sqdtrho2,W2)))
# Simulate_StochVol_Jumps_func.m:286
                                    vOld=copy(vNew)
# Simulate_StochVol_Jumps_func.m:287
                            else:
                                for m in arange(1,M).reshape(-1):
                                    Poi=PoissonRnd(N_sim,lamdt)
# Simulate_StochVol_Jumps_func.m:291
                                    sumJumpsVec=zeros(N_sim,1)
# Simulate_StochVol_Jumps_func.m:292
                                    for n in arange(1,N_sim).reshape(-1):
                                        if Poi(n) > 0:
                                            sumJumpsVec[n]=JumpFunc(Poi(n))
# Simulate_StochVol_Jumps_func.m:295
                                    W1=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:298
                                    W2=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:298
                                    Spath[arange(),m + 1]=multiply(Spath(arange(),m),exp(dot((Zeta - dot(0.5,exp(dot(2,vOld)))),dt) + sumJumpsVec + multiply(dot(sqdt,exp(vOld)),W1)))
# Simulate_StochVol_Jumps_func.m:299
                                    vNew=driftv + dot(vOld,consv) + dot(Sigmav,(dot(sqdtrho1,W1) + dot(sqdtrho2,W2)))
# Simulate_StochVol_Jumps_func.m:300
                                    vOld=copy(vNew)
# Simulate_StochVol_Jumps_func.m:301
                            ##################################################################################    
##################################################################################
                        else:
                            if SVModel == 7:
                                vOld=dot(v0,ones(N_sim,1))
# Simulate_StochVol_Jumps_func.m:310
                                expvOld=exp(vOld)
# Simulate_StochVol_Jumps_func.m:311
                                if jumpModel == 0:
                                    for m in arange(1,M).reshape(-1):
                                        W1=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:314
                                        W2=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:314
                                        Spath[arange(),m + 1]=multiply(Spath(arange(),m),exp(dot((Zeta - dot(0.5,expvOld ** 2)),dt) + multiply(dot(sqdt,expvOld),W1)))
# Simulate_StochVol_Jumps_func.m:315
                                        vNew=vOld + dot((eta - dot(theta,expvOld ** av)),dt) + dot(Sigmav,(dot(sqdtrho1,W1) + dot(sqdtrho2,W2)))
# Simulate_StochVol_Jumps_func.m:316
                                        vOld=copy(vNew)
# Simulate_StochVol_Jumps_func.m:317
                                        expvOld=exp(vOld)
# Simulate_StochVol_Jumps_func.m:318
                                else:
                                    for m in arange(1,M).reshape(-1):
                                        Poi=PoissonRnd(N_sim,lamdt)
# Simulate_StochVol_Jumps_func.m:322
                                        sumJumpsVec=zeros(N_sim,1)
# Simulate_StochVol_Jumps_func.m:323
                                        for n in arange(1,N_sim).reshape(-1):
                                            if Poi(n) > 0:
                                                sumJumpsVec[n]=JumpFunc(Poi(n))
# Simulate_StochVol_Jumps_func.m:326
                                        W1=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:329
                                        W2=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:329
                                        Spath[arange(),m + 1]=multiply(Spath(arange(),m),exp(dot((Zeta - dot(0.5,expvOld ** 2)),dt) + sumJumpsVec + multiply(dot(sqdt,expvOld),W1)))
# Simulate_StochVol_Jumps_func.m:330
                                        vNew=vOld + dot((eta - dot(theta,expvOld ** av)),dt) + dot(Sigmav,(dot(sqdtrho1,W1) + dot(sqdtrho2,W2)))
# Simulate_StochVol_Jumps_func.m:331
                                        vOld=copy(vNew)
# Simulate_StochVol_Jumps_func.m:332
                                        expvOld=exp(vOld)
# Simulate_StochVol_Jumps_func.m:333
                                ##################################################################################    
##################################################################################
                            else:
                                if SVModel == 8:
                                    if jumpModel == 0:
                                        pass
                                    else:
                                        #### ADD CODE FOR JUMP MODELS!!!!!!!!!!!!!!!!!!!
                                        pass
                                    ##################################################################################    
##################################################################################
                                else:
                                    if SVModel == 9:
                                        vmin=SVModelParams.vmin
# Simulate_StochVol_Jumps_func.m:349
                                        vmax=SVModelParams.vmax
# Simulate_StochVol_Jumps_func.m:350
                                        denom=(sqrt(vmax) - sqrt(vmin)) ** 2
# Simulate_StochVol_Jumps_func.m:351
                                        driftv=dot(dot(eta,theta),dt)
# Simulate_StochVol_Jumps_func.m:352
                                        cons5=(1 - dot(eta,dt))
# Simulate_StochVol_Jumps_func.m:353
                                        rhoSq=rho ** 2
# Simulate_StochVol_Jumps_func.m:354
                                        vOld=dot(v0,ones(N_sim,1))
# Simulate_StochVol_Jumps_func.m:355
                                        QvOld=multiply((vOld - vmin),(vmax - vOld)) / denom
# Simulate_StochVol_Jumps_func.m:356
                                        if jumpModel == 0:
                                            for m in arange(1,M).reshape(-1):
                                                W1=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:359
                                                W2=randn(N_sim,1)
# Simulate_StochVol_Jumps_func.m:359
                                                Spath[arange(),m + 1]=multiply(Spath(arange(),m),exp(dot((Zeta - dot(0.5,vOld)),dt) + multiply(dot(sqdt,sqrt(vOld - dot(rhoSq,QvOld))),W1) + multiply(dot(sqdtrho1,sqrt(QvOld)),W2)))
# Simulate_StochVol_Jumps_func.m:360
                                                vNew=driftv + dot(cons5,vOld) + multiply(dot(dot(Sigmav,sqdt),sqrt(QvOld)),W2)
# Simulate_StochVol_Jumps_func.m:362
                                                ### Variance process must lie between [vmin, vmax]
                                                vOld=min(vmax,max(vmin,vNew))
# Simulate_StochVol_Jumps_func.m:366
                                                QvOld=multiply((vOld - vmin),(vmax - vOld)) / denom
# Simulate_StochVol_Jumps_func.m:367
                                        else:
                                            #### ADD CODE FOR JUMP MODELS!!!!!!!!!!!!!!!!!!!
                                            pass
    
    return Spath
    
if __name__ == '__main__':
    pass
    
    # #### REFORMULATED VERSION
# etahat = eta*theta; thetahat = (eta + Sigmav^2)/etahat; Sigmavhat = -Sigmav; v0hat = 1/v0;
# vOld = v0hat*ones(N_sim,1); #used to store variance process
# sqvOld = sqrt(v0hat)*ones(N_sim,1);
# 
# expkt = exp(-etahat*dt);
# driftv = thetahat*(1 - expkt);  #analytical drift for variance process
# sqtSv = sqdt*Sigmavhat;  #analytical drift for variance process
# 
# for m = 1:M
#     W1 = randn(N_sim,1); W2 = randn(N_sim,1);  #Generate two Brownian motions
# 
#     Spath(:,m+1) = Spath(:,m).*exp((r - .5*vOld)*dt + (sqrho1*W1 + sqrho2*W2)./sqvOld);  #log scheme
#     #Spath(:,m+1) = Spath(:,m)*( (1+r)*dt + sqrt(vOld)*(sqrho1*W1 + sqrho2*W2));  #level scheme
# 
#     vNew = driftv + vOld*expkt + sqtSv*sqvOld.*W1;
# 
#     vOld = abs(vNew); #Always stays positive, the "reflection" scheme
#     sqvOld = sqrt(vOld);
# end