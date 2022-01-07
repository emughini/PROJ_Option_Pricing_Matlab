# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_EuropeanOptions.m

    ##################################################################
### EUROPEAN OPTION PRICER (RUN SCRIPT)
##################################################################
# Descritpion: Script to Price European options in Levy/Heston Models
#              using the PROJ method
# Author:      Justin Kirkby
# References:  (1) Efficient Option Pricing By Frame Duality with The Fast
#              Fourier Transform, SIAM J. Financial Math., 2015
#              (2) Robust Option Pricing with Characteristic Functions and
#              the B-Spline Order of density Projection, JCF, 2017
##################################################################
    
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_EuropeanOptions.m:13
    cd(folder)
    addpath('../RN_CHF')
    addpath('../Helper_Functions')
    ##############################################
###  Step 1) CHOOSE CONTRACT/GENERAL PARAMETERS
##############################################
    call=1
# Script_EuropeanOptions.m:22
    
    S_0=100
# Script_EuropeanOptions.m:23
    
    W=100
# Script_EuropeanOptions.m:24
    
    r=0.05
# Script_EuropeanOptions.m:25
    
    q=0.01
# Script_EuropeanOptions.m:26
    
    T=1
# Script_EuropeanOptions.m:27
    
    ##############################################
###  Step 2) CHOOSE MODEL PARAMETERS  (Levy Models)
##############################################
    model=1
# Script_EuropeanOptions.m:32
    
    params=cellarray([])
# Script_EuropeanOptions.m:33
    if model == 1:
        params.sigmaBSM = copy(0.15)
# Script_EuropeanOptions.m:36
    else:
        if model == 2:
            params.C = copy(0.02)
# Script_EuropeanOptions.m:39
            params.G = copy(5)
# Script_EuropeanOptions.m:40
            params.MM = copy(15)
# Script_EuropeanOptions.m:41
            params.Y = copy(1.2)
# Script_EuropeanOptions.m:42
        else:
            if model == 3:
                params.alpha = copy(15)
# Script_EuropeanOptions.m:45
                params.beta = copy(- 5)
# Script_EuropeanOptions.m:46
                params.delta = copy(0.5)
# Script_EuropeanOptions.m:47
            else:
                if model == 4:
                    params.sigma = copy(0.12)
# Script_EuropeanOptions.m:50
                    params.lam = copy(0.4)
# Script_EuropeanOptions.m:51
                    params.muj = copy(- 0.12)
# Script_EuropeanOptions.m:52
                    params.sigmaj = copy(0.18)
# Script_EuropeanOptions.m:53
                else:
                    if model == 5:
                        params.sigma = copy(0.15)
# Script_EuropeanOptions.m:56
                        params.lam = copy(3)
# Script_EuropeanOptions.m:57
                        params.p_up = copy(0.2)
# Script_EuropeanOptions.m:58
                        params.eta1 = copy(25)
# Script_EuropeanOptions.m:59
                        params.eta2 = copy(10)
# Script_EuropeanOptions.m:60
                    else:
                        if model == 6:
                            params.v_0 = copy(0.0175)
# Script_EuropeanOptions.m:63
                            params.theta = copy(0.0398)
# Script_EuropeanOptions.m:64
                            params.kappa = copy(1.5768)
# Script_EuropeanOptions.m:65
                            params.sigma_v = copy(0.5751)
# Script_EuropeanOptions.m:66
                            params.rho = copy(- 0.5711)
# Script_EuropeanOptions.m:67
                        else:
                            if model == 8:
                                params.sigma = copy(0.2)
# Script_EuropeanOptions.m:70
                                params.nu = copy(0.85)
# Script_EuropeanOptions.m:71
                                params.theta = copy(0.1)
# Script_EuropeanOptions.m:72
                            else:
                                if model == 9:
                                    params.alpha_p = copy(1.18)
# Script_EuropeanOptions.m:75
                                    params.lam_p = copy(10.57)
# Script_EuropeanOptions.m:76
                                    params.alpha_m = copy(1.44)
# Script_EuropeanOptions.m:77
                                    params.lam_m = copy(5.57)
# Script_EuropeanOptions.m:78
    
    ##############################################
###  Step 3) CHOOSE PROJ PARAMETERS
##############################################
    order=3
# Script_EuropeanOptions.m:84
    
    UseCumulant=1
# Script_EuropeanOptions.m:85
    
    #---------------------
# APPROACH 1: Cumulant Based approach for grid width
# (see "Robust Option Pricing with Characteritics Functions and the BSpline Order of Density Projection")
#---------------------
    if UseCumulant == 1:
        logN=14
# Script_EuropeanOptions.m:92
        if model == 6:
            L1=18
# Script_EuropeanOptions.m:94
        else:
            L1=12
# Script_EuropeanOptions.m:96
        #---------------------
# APPROACH 2: Manual GridWidth approach 
#---------------------
    else:
        P=7
# Script_EuropeanOptions.m:102
        Pbar=3
# Script_EuropeanOptions.m:103
    
    ##############################################
### PRICE
##############################################
###  Note: rnCHF is the risk netural CHF, c1,c2,c4 are the cumulants
    modelInput=getModelInput(model,T,r,q,params)
# Script_EuropeanOptions.m:110
    if UseCumulant == 1:
        alpha=getTruncationAlpha(T,L1,modelInput,model)
# Script_EuropeanOptions.m:113
    else:
        logN=P + Pbar
# Script_EuropeanOptions.m:115
        alpha=2 ** Pbar / 2
# Script_EuropeanOptions.m:116
    
    N=2 ** logN
# Script_EuropeanOptions.m:118
    
    tic
    price=PROJ_European(order,N,alpha,r,q,T,S_0,W,call,modelInput.rnCHF,dot(modelInput.c1,T))
# Script_EuropeanOptions.m:122
    toc
    fprintf('%.8f \n',price)
    ##############################################
### Plots
##############################################
    plot_convergence=1
# Script_EuropeanOptions.m:130
    plot_smile=1
# Script_EuropeanOptions.m:131
    if plot_convergence:
        figure()
        Nvec=2.0 ** concat([3,4,5,6,7,8,9,10])
# Script_EuropeanOptions.m:135
        errs=zeros(1,length(Nvec))
# Script_EuropeanOptions.m:136
        ref=PROJ_European(order,2 ** 12,alpha,r,q,T,S_0,W,call,modelInput.rnCHF,dot(modelInput.c1,T))
# Script_EuropeanOptions.m:138
        for i in arange(1,length(errs)).reshape(-1):
            val=PROJ_European(order,Nvec(i),alpha,r,q,T,S_0,W,call,modelInput.rnCHF,dot(modelInput.c1,T))
# Script_EuropeanOptions.m:140
            errs[i]=log10(abs(val - ref))
# Script_EuropeanOptions.m:141
        # Plot
        plot(log2(Nvec),errs,'r-+')
        ylabel('$log_{10}(|err|)$','interpreter','latex')
        xlabel('$log_{2}(N)$','interpreter','latex')
        title('Convergence')
        grid('on')
    
    if plot_smile:
        figure()
        Kvec=dot(S_0,concat([arange(0.2,1.8,0.01)]))
# Script_EuropeanOptions.m:154
        # NOTE: there is a much more efficient version of this code for pricing many strikes
    # This script is just to provide and example of the smile
        values=zeros(1,length(Kvec))
# Script_EuropeanOptions.m:158
        for i in arange(1,length(values)).reshape(-1):
            values[i]=PROJ_European(order,N,alpha,r,q,T,S_0,Kvec(i),call,modelInput.rnCHF,dot(modelInput.c1,T))
# Script_EuropeanOptions.m:160
        if call == 1:
            intrinsic=max(S_0 - Kvec,0)
# Script_EuropeanOptions.m:164
        else:
            intrinsic=max(Kvec - S_0,0)
# Script_EuropeanOptions.m:166
        # Plot
        plot(Kvec,values)
        hold('on')
        plot(Kvec,intrinsic,'r--')
        ylabel('price')
        xlabel('strike')
        grid('on')
    