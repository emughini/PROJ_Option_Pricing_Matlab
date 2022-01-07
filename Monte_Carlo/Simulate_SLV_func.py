# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Simulate_SLV_func.m

    
@function
def Simulate_SLV_func(N_sim=None,M=None,T=None,S_0=None,r=None,q=None,model=None,params=None,*args,**kwargs):
    varargin = Simulate_SLV_func.varargin
    nargin = Simulate_SLV_func.nargin

    # Simulates Paths of Stochastic Local Volatility Models (basic Euler Scheme for most cases) 
# N_sim = # paths
# M = #time steps on [0,T], ie dt =T/M   
# Note: returns paths of dimension (N_sim,M+1), since they include S_0
    
    # SVLModel:                         (parameters)
#        1 = Heston:                alpha, v0, rho, theta, eta
#        2 = SABR:                  alpha, v0, rho, beta
#        3 = Shifted SABR:          alpha, v0, rho, beta, shift
#        4 = Quadratic SLV:         alpha, v0, rho, theta, eta, a, b, c
#        5 = TanHyp-Heston:         alpha, v0, rho, theta, eta, beta
#        6 = Heston-SABR:           alpha, v0, rho, theta, eta, beta
    
    #==============================
# Initialize Common Params/Vectors
#==============================
    alpha=params.alpha
# Simulate_SLV_func.m:18
    
    v0=params.v0
# Simulate_SLV_func.m:19
    
    rho=params.rho
# Simulate_SLV_func.m:20
    
    Sigmav=copy(alpha)
# Simulate_SLV_func.m:22
    
    if model == 1 or model == 4 or model == 5 or model == 6:
        theta=params.theta
# Simulate_SLV_func.m:25
        eta=params.eta
# Simulate_SLV_func.m:26
    
    Spath=zeros(N_sim,M + 1)
# Simulate_SLV_func.m:29
    Spath[arange(),1]=S_0
# Simulate_SLV_func.m:30
    dt=T / M
# Simulate_SLV_func.m:32
    sqdt=sqrt(dt)
# Simulate_SLV_func.m:33
    sqdtrho1=dot(sqdt,rho)
# Simulate_SLV_func.m:34
    sqdtrho2=dot(sqdt,sqrt(1 - rho ** 2))
# Simulate_SLV_func.m:35
    Zeta=r - q
# Simulate_SLV_func.m:37
    #==============================
# Simulate Based on Specific StochVol Model
#==============================
    
    ##################################################################################
    if model == 1:
        expEta=exp(dot(- eta,dt))
# Simulate_SLV_func.m:45
        driftv=dot(theta,(1 - expEta))
# Simulate_SLV_func.m:46
        vOld=dot(v0,ones(N_sim,1))
# Simulate_SLV_func.m:47
        sqvOld=dot(sqrt(v0),ones(N_sim,1))
# Simulate_SLV_func.m:48
        for m in arange(1,M).reshape(-1):
            W1=randn(N_sim,1)
# Simulate_SLV_func.m:51
            W2=randn(N_sim,1)
# Simulate_SLV_func.m:51
            Spath[arange(),m + 1]=multiply(Spath(arange(),m),exp(dot((Zeta - dot(0.5,vOld)),dt) + multiply(dot(sqdt,sqvOld),W1)))
# Simulate_SLV_func.m:52
            #Spath(:,m+1) = Spath(:,m)*( (1+r)*dt + sqrt(vOld)*(sqrho1*W1 + sqrho2*W2));  #level scheme
            vNew=driftv + dot(vOld,expEta) + multiply(dot(Sigmav,sqvOld),(dot(sqdtrho1,W1) + dot(sqdtrho2,W2)))
# Simulate_SLV_func.m:54
            vOld=abs(vNew)
# Simulate_SLV_func.m:56
            #vOld = max(0,vNew); #least biased scheme
            sqvOld=sqrt(vOld)
# Simulate_SLV_func.m:58
        ##################################################################################        
##################################################################################
    else:
        if model == 2:
            beta=params.beta
# Simulate_SLV_func.m:64
            cons1=dot(dot(- 0.5,(alpha) ** 2),dt)
# Simulate_SLV_func.m:65
            vOld=dot(v0,ones(N_sim,1))
# Simulate_SLV_func.m:66
            for m in arange(1,M).reshape(-1):
                W1=randn(N_sim,1)
# Simulate_SLV_func.m:68
                W2=randn(N_sim,1)
# Simulate_SLV_func.m:68
                Spath[arange(),m + 1]=max(0,Spath(arange(),m) + multiply(multiply(multiply(Spath(arange(),m) ** beta,vOld),sqdt),W1))
# Simulate_SLV_func.m:69
                vOld=multiply(vOld,exp(cons1 + dot(alpha,(dot(sqdtrho1,W1) + dot(sqdtrho2,W2)))))
# Simulate_SLV_func.m:70
            #     ### LOG SCHEME 
#     cons2 = 2*(beta - 1);
#     for m = 1:M
#         W1 = randn(N_sim,1); W2 = randn(N_sim,1);  #Generate two Brownian motions
#         Spath(:,m+1) = Spath(:,m).*exp(-.5*vOld.^2.*Spath(:,m).^cons2*dt + Spath(:,m).^(beta-1).* vOld .*sqdt.*W1);  #level scheme
#         vOld = vOld.*exp(cons1 + alpha*(sqdtrho1*W1 + sqdtrho2*W2));
#     end
            ##################################################################################        
##################################################################################
        else:
            if model == 3:
                beta=params.beta
# Simulate_SLV_func.m:85
                shift=params.shift
# Simulate_SLV_func.m:86
                cons1=dot(dot(- 0.5,(alpha) ** 2),dt)
# Simulate_SLV_func.m:87
                vOld=dot(v0,ones(N_sim,1))
# Simulate_SLV_func.m:88
                for m in arange(1,M).reshape(-1):
                    W1=randn(N_sim,1)
# Simulate_SLV_func.m:90
                    W2=randn(N_sim,1)
# Simulate_SLV_func.m:90
                    ### Note: because of shift, -shift <= S_t
                    Spath[arange(),m + 1]=max(- shift,Spath(arange(),m) + multiply(multiply(multiply((Spath(arange(),m) + shift) ** beta,vOld),sqdt),W1))
# Simulate_SLV_func.m:92
                    vOld=multiply(vOld,exp(cons1 + dot(alpha,(dot(sqdtrho1,W1) + dot(sqdtrho2,W2)))))
# Simulate_SLV_func.m:93
                ##################################################################################        
##################################################################################
            else:
                if model == 4:
                    a=params.a
# Simulate_SLV_func.m:98
                    b=params.b
# Simulate_SLV_func.m:98
                    c=params.c
# Simulate_SLV_func.m:98
                    expEta=exp(dot(- eta,dt))
# Simulate_SLV_func.m:100
                    driftv=dot(theta,(1 - expEta))
# Simulate_SLV_func.m:101
                    vOld=dot(v0,ones(N_sim,1))
# Simulate_SLV_func.m:102
                    sqvOld=dot(sqrt(v0),ones(N_sim,1))
# Simulate_SLV_func.m:103
                    drift=1 + dot(Zeta,dt)
# Simulate_SLV_func.m:105
                    for m in arange(1,M).reshape(-1):
                        W1=randn(N_sim,1)
# Simulate_SLV_func.m:107
                        W2=randn(N_sim,1)
# Simulate_SLV_func.m:107
                        Spath[arange(),m + 1]=max(0,dot(Spath(arange(),m),drift) + multiply(multiply(dot(sqdt,sqvOld),W1),(multiply(Spath(arange(),m),(dot(a,Spath(arange(),m)) + b)) + c)))
# Simulate_SLV_func.m:109
                        vNew=driftv + dot(vOld,expEta) + multiply(dot(Sigmav,sqvOld),(dot(sqdtrho1,W1) + dot(sqdtrho2,W2)))
# Simulate_SLV_func.m:112
                        #vOld = abs(vNew); #Always stays positive, the "reflection" scheme
                        vOld=max(0,vNew)
# Simulate_SLV_func.m:115
                        sqvOld=sqrt(vOld)
# Simulate_SLV_func.m:116
                    ##################################################################################        
##################################################################################
                else:
                    if model == 5:
                        beta=params.beta
# Simulate_SLV_func.m:121
                        expEta=exp(dot(- eta,dt))
# Simulate_SLV_func.m:123
                        driftv=dot(theta,(1 - expEta))
# Simulate_SLV_func.m:124
                        vOld=dot(v0,ones(N_sim,1))
# Simulate_SLV_func.m:125
                        sqvOld=dot(sqrt(v0),ones(N_sim,1))
# Simulate_SLV_func.m:126
                        drift=1 + dot(Zeta,dt)
# Simulate_SLV_func.m:128
                        for m in arange(1,M).reshape(-1):
                            W1=randn(N_sim,1)
# Simulate_SLV_func.m:130
                            W2=randn(N_sim,1)
# Simulate_SLV_func.m:130
                            Spath[arange(),m + 1]=max(0,dot(Spath(arange(),m),drift) + multiply(multiply(dot(sqdt,sqvOld),W1),tanh(dot(beta,Spath(arange(),m)))))
# Simulate_SLV_func.m:132
                            vNew=driftv + dot(vOld,expEta) + multiply(dot(Sigmav,sqvOld),(dot(sqdtrho1,W1) + dot(sqdtrho2,W2)))
# Simulate_SLV_func.m:133
                            #vOld = abs(vNew); #Always stays positive, the "reflection" scheme
                            vOld=max(0,vNew)
# Simulate_SLV_func.m:136
                            sqvOld=sqrt(vOld)
# Simulate_SLV_func.m:137
                    else:
                        if model == 6:
                            drift=1 + dot(Zeta,dt)
# Simulate_SLV_func.m:141
                            expEta=exp(dot(- eta,dt))
# Simulate_SLV_func.m:142
                            driftv=dot(theta,(1 - expEta))
# Simulate_SLV_func.m:143
                            vOld=dot(v0,ones(N_sim,1))
# Simulate_SLV_func.m:144
                            sqvOld=dot(sqrt(v0),ones(N_sim,1))
# Simulate_SLV_func.m:145
                            beta=params.beta
# Simulate_SLV_func.m:147
                            for m in arange(1,M).reshape(-1):
                                W1=randn(N_sim,1)
# Simulate_SLV_func.m:150
                                W2=randn(N_sim,1)
# Simulate_SLV_func.m:150
                                #### LEVEL scheme
                                Spath[arange(),m + 1]=max(0,dot(Spath(arange(),m),drift) + multiply(multiply(multiply(Spath(arange(),m) ** beta,sqvOld),sqdt),W1))
# Simulate_SLV_func.m:153
                                #         #### LOG scheme
#         Spath(:,m+1) = Spath(:,m).*exp(-.5*vOld.^2.*Spath(:,m).^cons2*dt + Spath(:,m).^(beta-1).* sqvOld .*sqdt.*W1);
                                vNew=driftv + dot(vOld,expEta) + multiply(dot(Sigmav,sqvOld),(dot(sqdtrho1,W1) + dot(sqdtrho2,W2)))
# Simulate_SLV_func.m:158
                                vOld=abs(vNew)
# Simulate_SLV_func.m:159
                                #vOld = max(0,vNew); #least biased scheme
                                sqvOld=sqrt(vOld)
# Simulate_SLV_func.m:161
                            #     beta  = params.beta;
#     cons1 = -.5*(alpha)^2*dt;
#     vOld  = v0*ones(N_sim,1); #used to store variance process
#     for m = 1:M
#         W1 = randn(N_sim,1); W2 = randn(N_sim,1);  #Generate two Brownian motions
#         Spath(:,m+1) = max(0, Spath(:,m) + Spath(:,m).^beta.* vOld .*sqdt.*W1);  #level scheme
#         vOld = vOld.*exp(cons1 + alpha*(sqdtrho1*W1 + sqdtrho2*W2));
#         #vOld = vOld + alpha*vOld.*(sqdtrho1*W1 + sqdtrho2*W2);
#     end
#     
#     expEta = exp(-eta*dt);
#     driftv = theta*(1 - expEta);  #analytical drift for variance process
#     vOld   = v0*ones(N_sim,1); #used to store variance process
#     sqvOld = sqrt(v0)*ones(N_sim,1);
#     
#     for m = 1:M
#         W1 = randn(N_sim,1); W2 = randn(N_sim,1);  #Generate two Brownian motions
#         Spath(:,m+1) = Spath(:,m).*exp((Zeta - .5*vOld)*dt + sqdt*sqvOld.*W1);  #log scheme
#         #Spath(:,m+1) = Spath(:,m)*( (1+r)*dt + sqrt(vOld)*(sqrho1*W1 + sqrho2*W2));  #level scheme
#         vNew = driftv + vOld*expEta + Sigmav*sqvOld.*(sqdtrho1*W1 + sqdtrho2*W2);
#         #vNew = (sqvOld +.5*Sigmav*(sqdtrho1*W1 + sqdtrho2*W2)).^2 + eta*(theta - vOld)*dt -.25*Sigmav*dt; #Milstein
#         vOld = abs(vNew); #Always stays positive, the "reflection" scheme
#         #vOld = max(0,vNew); #least biased scheme
#         sqvOld = sqrt(vOld);
#     end
    
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