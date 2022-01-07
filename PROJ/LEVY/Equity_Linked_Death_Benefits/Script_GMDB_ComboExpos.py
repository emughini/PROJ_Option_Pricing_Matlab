# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Script_GMDB_ComboExpos.m

    ##################################################################
### GMWB PRICER (RUN SCRIPT)
##################################################################
# Descritpion: Script to Price Guaranteed Minimum Death Benefits (GMDB)
#              using the PROJ method, under combination of exponential mortaily model
    
    # Author:      Zhimin Zhang  (Original Code)
#              Justin Lars Kirkby (Convert into common framework)
    
    # References:  (1) Valuing Equity-Linked Death Benefits in General Exponential
#               Levy Models, J. Comput. and Appl. Math. 2019 (Z. Zhang, Y. Yong, W. Yu)
#              (2) Efficient Option Pricing By Frame Duality with The Fast
#               Fourier Transform, SIAM J. Financial Math., 2015 (J.L. Kirkby)
##################################################################
    folder,name,ext=fileparts(which(mfilename('fullpath')),nargout=3)
# Script_GMDB_ComboExpos.m:15
    cd(folder)
    addpath('../RN_CHF')
    addpath('../Helper_Functions')
    ##############################################
###  Step 1) CHOOSE CONTRACT/GENERAL PARAMETERS
##############################################
    call=0
# Script_GMDB_ComboExpos.m:23
    
    S_0=100
# Script_GMDB_ComboExpos.m:24
    
    W=120
# Script_GMDB_ComboExpos.m:25
    
    r=0.05
# Script_GMDB_ComboExpos.m:26
    
    T=20
# Script_GMDB_ComboExpos.m:27
    
    ##############################################
###  Step 2) CHOOSE MODEL PARAMETERS  (Levy Models)
##############################################
    model=1
# Script_GMDB_ComboExpos.m:32
    
    params=cellarray([])
# Script_GMDB_ComboExpos.m:34
    params.model = copy(model)
# Script_GMDB_ComboExpos.m:35
    if model == 1:
        params.sigmaBSM = copy(0.25)
# Script_GMDB_ComboExpos.m:38
    else:
        if model == 3:
            params.sigma = copy(0.25)
# Script_GMDB_ComboExpos.m:41
            params.alpha = copy(2)
# Script_GMDB_ComboExpos.m:42
            params.beta = copy(0.5)
# Script_GMDB_ComboExpos.m:43
            params.delta = copy(0.05)
# Script_GMDB_ComboExpos.m:44
        else:
            if model == 4:
                params.sigma = copy(0.25)
# Script_GMDB_ComboExpos.m:47
                params.lam = copy(0.6)
# Script_GMDB_ComboExpos.m:48
                params.muj = copy(0.01)
# Script_GMDB_ComboExpos.m:49
                params.sigmaj = copy(0.13)
# Script_GMDB_ComboExpos.m:50
            else:
                if model == 5:
                    params.sigma = copy(0.25)
# Script_GMDB_ComboExpos.m:53
                    params.lam = copy(0.6)
# Script_GMDB_ComboExpos.m:54
                    params.p_up = copy(0.5)
# Script_GMDB_ComboExpos.m:55
                    params.eta1 = copy(1)
# Script_GMDB_ComboExpos.m:56
                    params.eta2 = copy(4)
# Script_GMDB_ComboExpos.m:57
                else:
                    if model == 8:
                        params.sigmaGBM = copy(0.25)
# Script_GMDB_ComboExpos.m:60
                        params.theta = copy(0.01)
# Script_GMDB_ComboExpos.m:61
                        params.sigma = copy(0.05)
# Script_GMDB_ComboExpos.m:62
                        params.nu = copy(2)
# Script_GMDB_ComboExpos.m:63
    
    ##############################################
###  Step 3) CHOOSE Time-Until-Death PARAMETERS (Combination of expos)
##############################################
    params_death=cellarray([])
# Script_GMDB_ComboExpos.m:69
    params_death.A = copy(concat([3,- 2]))
# Script_GMDB_ComboExpos.m:70
    
    params_death.lambda = copy(concat([0.08,0.12]))
# Script_GMDB_ComboExpos.m:71
    
    ##############################################
###  Step 4) CHOOSE PROJ PARAMETERS
##############################################
    order=1
# Script_GMDB_ComboExpos.m:76
    
    P=8
# Script_GMDB_ComboExpos.m:77
    Pbar=P + 2
# Script_GMDB_ComboExpos.m:78
    ##############################################
### PRICE
##############################################
    if order == 1:
        tic
        price=PROJ_GMDB_ComboExpos_Linear(P,Pbar,S_0,W,call,r,params,params_death,T)
# Script_GMDB_ComboExpos.m:85
        toc
        fprintf('%.8f \n',price)
    else:
        fprintf('Only orders 1 (linear) and 2 (quadratic) are supported')
    