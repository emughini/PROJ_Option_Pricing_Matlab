# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# getModelInput.m

    
@function
def getModelInput(model=None,dt=None,r=None,q=None,modelParams=None,T=None,*args,**kwargs):
    varargin = getModelInput.varargin
    nargin = getModelInput.nargin

    # model: Levy models (BSM, CGMY, NIG, MJD, Kou)
#        Affine models (Heston)
# r: interest rate
# q: dividend yield
# dt: time increment (this could be time to maturity, or time between monitoring dates)
# modelParams: dictionary of params for specific model
# NOTE: r,q can also be chosen to model forward or FX
# NOTE: the returned cumulants, c1, c2, c4, contain only contain dt in the
# case of Heston, but not the Levy models (this is so we can use this
# function in Exotic contexts)
    
    if nargin < 6:
        T=copy(dt)
# getModelInput.m:14
    
    modelInputs=cellarray([])
# getModelInput.m:17
    modelInputs.dt = copy(dt)
# getModelInput.m:18
    modelInputs.T = copy(T)
# getModelInput.m:19
    modelInputs.r = copy(r)
# getModelInput.m:20
    modelInputs.q = copy(q)
# getModelInput.m:21
    modelInputs.model = copy(model)
# getModelInput.m:22
    if model == 1:
        #----------------------------------------------
    # Unpack the model parameters
        sigmaBSM=modelParams.sigmaBSM
# getModelInput.m:27
        # Set the return object
        w=dot(- 0.5,sigmaBSM ** 2)
# getModelInput.m:30
        modelInputs.RNmu = copy(r - q + w)
# getModelInput.m:31
        # Cumulants (useful for setting trunction range for density support / grids)
        modelInputs.c1 = copy(modelInputs.RNmu)
# getModelInput.m:34
        modelInputs.c2 = copy(sigmaBSM ** 2)
# getModelInput.m:35
        modelInputs.c4 = copy(0)
# getModelInput.m:36
        # Charachteristic Functions / Levy Symbol
        modelInputs.rnCHF = copy(lambda u=None: cf_RN_BSM(u,r - q,dt,sigmaBSM))
# getModelInput.m:39
        modelInputs.rnCHF_T = copy(lambda u=None: cf_RN_BSM(u,r - q,T,sigmaBSM))
# getModelInput.m:40
        modelInputs.rnSYMB = copy(lambda u=None: SYMB_RN_BSM(u,r - q,sigmaBSM))
# getModelInput.m:41
    else:
        if model == 2:
            #----------------------------------------------
    # Unpack the model parameters
            C=modelParams.C
# getModelInput.m:46
            G=modelParams.G
# getModelInput.m:47
            MM=modelParams.MM
# getModelInput.m:48
            Y=modelParams.Y
# getModelInput.m:49
            # Set the return object
            # Set the Risk-Neutral drift (based on interest/div rate and convexity correction)
            w=dot(dot(- C,gamma(- Y)),((MM - 1) ** Y - MM ** Y + (G + 1) ** Y - G ** Y))
# getModelInput.m:54
            modelInputs.RNmu = copy(r - q + w)
# getModelInput.m:55
            # Cumulants (useful for setting trunction range for density support / grids)
            modelInputs.c1 = copy(modelInputs.RNmu + dot(dot(C,gamma(1 - Y)),(MM ** (Y - 1) - G ** (Y - 1))))
# getModelInput.m:58
            modelInputs.c2 = copy(dot(dot(C,gamma(2 - Y)),(MM ** (Y - 2) + G ** (Y - 2))))
# getModelInput.m:59
            modelInputs.c4 = copy(dot(dot(C,gamma(4 - Y)),(MM ** (Y - 4) + G ** (Y - 4))))
# getModelInput.m:60
            # Charachteristic Functions / Levy Symbol
            modelInputs.rnCHF = copy(lambda u=None: cf_RN_CGMY(u,dt,r - q,C,G,MM,Y))
# getModelInput.m:63
            modelInputs.rnCHF_T = copy(lambda u=None: cf_RN_CGMY(u,T,r - q,C,G,MM,Y))
# getModelInput.m:64
            modelInputs.rnSYMB = copy(lambda u=None: SYMB_RN_CGMY(u,r - q,C,G,MM,Y))
# getModelInput.m:65
        else:
            if model == 3:
                #----------------------------------------------
                alpha=modelParams.alpha
# getModelInput.m:69
                beta=modelParams.beta
# getModelInput.m:70
                delta=modelParams.delta
# getModelInput.m:71
                asq=alpha ** 2
# getModelInput.m:73
                bsq=beta ** 2
# getModelInput.m:74
                temp=sqrt(asq - bsq)
# getModelInput.m:75
                w=dot(delta,(sqrt(asq - (beta + 1) ** 2) - temp))
# getModelInput.m:78
                modelInputs.RNmu = copy(r - q + w)
# getModelInput.m:79
                modelInputs.c1 = copy(modelInputs.RNmu + dot(delta,beta) / temp)
# getModelInput.m:82
                modelInputs.c2 = copy(dot(dot(delta,asq),(asq - bsq) ** (- 1.5)))
# getModelInput.m:83
                modelInputs.c4 = copy(dot(dot(dot(dot(3,delta),asq),(asq + dot(4,bsq))),(asq - bsq) ** (- 3.5)))
# getModelInput.m:84
                modelInputs.rnCHF = copy(lambda u=None: cf_RN_NIG(u,r - q,dt,alpha,beta,delta))
# getModelInput.m:87
                modelInputs.rnCHF_T = copy(lambda u=None: cf_RN_NIG(u,r - q,T,alpha,beta,delta))
# getModelInput.m:88
                modelInputs.rnSYMB = copy(lambda u=None: SYMB_RN_NIG(u,r - q,alpha,beta,delta))
# getModelInput.m:89
            else:
                if model == 4:
                    #----------------------------------------------
                    sigma=modelParams.sigma
# getModelInput.m:93
                    lam=modelParams.lam
# getModelInput.m:94
                    muj=modelParams.muj
# getModelInput.m:95
                    sigmaj=modelParams.sigmaj
# getModelInput.m:96
                    # Set the Risk-Neutral drift (based on interest/div rate and convexity correction)
                    modelInputs.sig2 = copy(dot(0.5,sigma ** 2))
# getModelInput.m:100
                    w=dot(- 0.5,sigma ** 2) - dot(lam,(exp(muj + dot(0.5,sigmaj ** 2)) - 1))
# getModelInput.m:101
                    modelInputs.RNmu = copy(r - q + w)
# getModelInput.m:102
                    modelInputs.c1 = copy(modelInputs.RNmu + dot(lam,muj))
# getModelInput.m:105
                    modelInputs.c2 = copy(dot(lam,(sigma ** 2 / lam + muj ** 2 + sigmaj ** 2)))
# getModelInput.m:106
                    modelInputs.c4 = copy(dot(lam,(muj ** 4 + dot(dot(6,sigmaj ** 2),muj ** 2) + dot(3,sigmaj ** 4))))
# getModelInput.m:107
                    modelInputs.rnCHF = copy(lambda u=None: cf_RN_MJD(u,r - q,dt,sigma,muj,sigmaj,lam))
# getModelInput.m:110
                    modelInputs.rnCHF_T = copy(lambda u=None: cf_RN_MJD(u,r - q,T,sigma,muj,sigmaj,lam))
# getModelInput.m:111
                    modelInputs.rnSYMB = copy(lambda u=None: SYMB_RN_MJD(u,r - q,sigma,muj,sigmaj,lam))
# getModelInput.m:112
                else:
                    if model == 5:
                        #----------------------------------------------
                        sigma=modelParams.sigma
# getModelInput.m:116
                        lam=modelParams.lam
# getModelInput.m:117
                        p_up=modelParams.p_up
# getModelInput.m:118
                        eta1=modelParams.eta1
# getModelInput.m:119
                        eta2=modelParams.eta2
# getModelInput.m:120
                        # Set the Risk-Neutral drift (based on interest/div rate and convexity correction)
                        w=dot(- 0.5,sigma ** 2) - dot(lam,(dot(p_up,eta1) / (eta1 - 1) + dot((1 - p_up),eta2) / (eta2 + 1) - 1))
# getModelInput.m:124
                        modelInputs.RNmu = copy(r - q + w)
# getModelInput.m:125
                        modelInputs.c1 = copy(modelInputs.RNmu + dot(lam,p_up) / eta1 + dot(lam,(1 - p_up)) / eta2)
# getModelInput.m:128
                        modelInputs.c2 = copy(sigma ** 2 + dot(dot(2,lam),p_up) / (eta1 ** 2) + dot(dot(2,lam),(1 - p_up)) / (eta2 ** 2))
# getModelInput.m:129
                        modelInputs.c4 = copy(dot(dot(24,lam),(p_up / eta1 ** 4 + (1 - p_up) / eta2 ** 4)))
# getModelInput.m:130
                        modelInputs.rnCHF = copy(lambda u=None: cf_RN_KOU(u,dt,r - q,sigma,lam,p_up,eta1,eta2))
# getModelInput.m:133
                        modelInputs.rnCHF_T = copy(lambda u=None: cf_RN_KOU(u,T,r - q,sigma,lam,p_up,eta1,eta2))
# getModelInput.m:134
                        modelInputs.rnSYMB = copy(lambda u=None: SYMB_RN_Kou(u,r - q,sigma,lam,p_up,eta1,eta2))
# getModelInput.m:135
                    else:
                        if model == 6:
                            #----------------------------------------------
                            theta=modelParams.theta
# getModelInput.m:139
                            rho=modelParams.rho
# getModelInput.m:140
                            if isfield(modelParams,'kappa'):
                                kappa=modelParams.kappa
# getModelInput.m:143
                            else:
                                kappa=modelParams.eta
# getModelInput.m:145
                            if isfield(modelParams,'v_0'):
                                v_0=modelParams.v_0
# getModelInput.m:149
                            else:
                                v_0=modelParams.v0
# getModelInput.m:151
                            if isfield(modelParams,'sigma_v'):
                                sigma_v=modelParams.sigma_v
# getModelInput.m:155
                            else:
                                sigma_v=modelParams.Sigmav
# getModelInput.m:157
                            #----------------------------------------------
                            # Set the Risk-Neutral drift
                            modelInputs.RNmu = copy(r - q - dot(0.5,theta))
# getModelInput.m:163
                            modelInputs.c1 = copy(dot(modelInputs.RNmu,dt) + dot((1 - exp(dot(- kappa,dt))),(theta - v_0)) / (dot(2,kappa)))
# getModelInput.m:166
                            modelInputs.c2 = copy(dot(1 / (dot(8,kappa ** 3)),(dot(dot(dot(dot(dot(sigma_v,dt),kappa),exp(dot(- kappa,dt))),(v_0 - theta)),(dot(dot(8,kappa),rho) - dot(4,sigma_v))) + dot(dot(dot(dot(kappa,rho),sigma_v),(1 - exp(dot(- kappa,dt)))),(dot(16,theta) - dot(8,v_0))) + dot(dot(dot(dot(2,theta),kappa),dt),(dot(dot(dot(- 4,kappa),rho),sigma_v) + sigma_v ** 2 + dot(4,kappa ** 2))) + dot(sigma_v ** 2,(dot((theta - dot(2,v_0)),exp(dot(dot(- 2,kappa),dt))) + dot(theta,(dot(6,exp(dot(- kappa,dt))) - 7)) + dot(2,v_0))) + dot(dot(dot(8,kappa ** 2),(v_0 - theta)),(1 - exp(dot(- kappa,dt)))))))
# getModelInput.m:167
                            modelInputs.c4 = copy(0)
# getModelInput.m:172
                            modelInputs.rnCHF = copy(lambda u=None: cf_RN_Heston(u,dt,r - q,v_0,theta,kappa,sigma_v,rho))
# getModelInput.m:175
                            modelInputs.rnCHF_T = copy(lambda u=None: cf_RN_Heston(u,T,r - q,v_0,theta,kappa,sigma_v,rho))
# getModelInput.m:176
                        else:
                            if model == 7:
                                #----------------------------------------------
    # Unpack the model parameters
                                c=modelParams.c
# getModelInput.m:182
                                lam_p=modelParams.lam_p
# getModelInput.m:183
                                lam_m=modelParams.lam_m
# getModelInput.m:184
                                nu=modelParams.nu
# getModelInput.m:185
                                # NOTE: params have been
    # written in correspondence with CGMY, which is a subclass of KoBoL
                                C=copy(c)
# getModelInput.m:190
                                MM=copy(lam_p)
# getModelInput.m:190
                                G=- lam_m
# getModelInput.m:190
                                Y=copy(nu)
# getModelInput.m:190
                                w=dot(dot(- C,gamma(- Y)),((MM - 1) ** Y - MM ** Y + (G + 1) ** Y - G ** Y))
# getModelInput.m:193
                                modelInputs.RNmu = copy(r - q + w)
# getModelInput.m:194
                                # Cumulants (useful for setting trunction range for density support / grids)
                                modelInputs.c1 = copy(modelInputs.RNmu + dot(dot(C,gamma(1 - Y)),(MM ** (Y - 1) - G ** (Y - 1))))
# getModelInput.m:197
                                modelInputs.c2 = copy(dot(dot(C,gamma(2 - Y)),(MM ** (Y - 2) + G ** (Y - 2))))
# getModelInput.m:198
                                modelInputs.c4 = copy(dot(dot(C,gamma(4 - Y)),(MM ** (Y - 4) + G ** (Y - 4))))
# getModelInput.m:199
                                # Charachteristic Functions / Levy Symbol
                                modelInputs.rnCHF = copy(lambda u=None: cf_RN_KoBoL(u,dt,r - q,c,lam_p,lam_m,nu))
# getModelInput.m:202
                                modelInputs.rnCHF_T = copy(lambda u=None: cf_RN_KoBoL(u,T,r - q,c,lam_p,lam_m,nu))
# getModelInput.m:203
                                modelInputs.rnSYMB = copy(lambda u=None: SYMB_RN_KoBoL(u,r - q,c,lam_p,lam_m,nu))
# getModelInput.m:204
                            else:
                                if model == 8:
                                    #----------------------------------------------
    # Unpack the model parameters
                                    sigma=modelParams.sigma
# getModelInput.m:209
                                    theta=modelParams.theta
# getModelInput.m:210
                                    nu=modelParams.nu
# getModelInput.m:211
                                    # Set the Risk-Neutral drift (based on interest/div rate and convexity correction)
                                    sig2=dot(0.5,sigma ** 2)
# getModelInput.m:215
                                    w=log(1 - dot(theta,nu) - dot(sig2,nu)) / nu
# getModelInput.m:216
                                    modelInputs.RNmu = copy(r - q + w)
# getModelInput.m:217
                                    modelInputs.c1 = copy(modelInputs.RNmu + theta)
# getModelInput.m:220
                                    modelInputs.c2 = copy((dot(sigma,sigma) + dot(dot(nu,theta),theta)))
# getModelInput.m:221
                                    modelInputs.c4 = copy(dot(3,(dot(sigma ** 4,nu) + dot(dot(2,theta ** 4),nu ** 3) + dot(dot(dot(4,sigma ** 2),theta ** 2),nu ** 2))))
# getModelInput.m:222
                                    modelInputs.rnCHF = copy(lambda u=None: cf_RN_VG(u,r - q,dt,sigma,nu,theta))
# getModelInput.m:225
                                    modelInputs.rnCHF_T = copy(lambda u=None: cf_RN_VG(u,r - q,T,sigma,nu,theta))
# getModelInput.m:226
                                    modelInputs.rnSYMB = copy(lambda u=None: SYMB_RN_VG(u,r - q,sigma,nu,theta))
# getModelInput.m:227
                                else:
                                    if model == 9:
                                        #----------------------------------------------
    # Unpack the model parameters
                                        alpha_p=modelParams.alpha_p
# getModelInput.m:232
                                        lam_p=modelParams.lam_p
# getModelInput.m:233
                                        alpha_m=modelParams.alpha_m
# getModelInput.m:234
                                        lam_m=modelParams.lam_m
# getModelInput.m:235
                                        # Set the Risk-Neutral drift (based on interest/div rate and convexity correction)
                                        m1=alpha_p / lam_p - alpha_m / lam_m
# getModelInput.m:239
                                        w=- log(dot((lam_p / (lam_p - 1)) ** alpha_p,(lam_m / (lam_m + 1)) ** alpha_m))
# getModelInput.m:240
                                        modelInputs.RNmu = copy(r - q + w)
# getModelInput.m:242
                                        cumulants=lambda n=None: dot(factorial(n - 1),(alpha_p / lam_p ** n + dot((- 1) ** n,alpha_m) / lam_m ** n))
# getModelInput.m:244
                                        modelInputs.c1 = copy(modelInputs.RNmu + m1)
# getModelInput.m:247
                                        modelInputs.c2 = copy(cumulants(2))
# getModelInput.m:248
                                        modelInputs.c4 = copy(cumulants(4))
# getModelInput.m:249
                                        modelInputs.rnCHF = copy(lambda u=None: cf_RN_BilateralGamma(u,r - q,dt,alpha_p,lam_p,alpha_m,lam_m))
# getModelInput.m:252
                                        modelInputs.rnCHF_T = copy(lambda u=None: cf_RN_BilateralGamma(u,r - q,T,alpha_p,lam_p,alpha_m,lam_m))
# getModelInput.m:253
                                        modelInputs.rnSYMB = copy(lambda u=None: SYMB_RN_BilateralGamma(u,r - q,alpha_p,lam_p,alpha_m,lam_m))
# getModelInput.m:254
    
    return modelInputs
    
if __name__ == '__main__':
    pass
    