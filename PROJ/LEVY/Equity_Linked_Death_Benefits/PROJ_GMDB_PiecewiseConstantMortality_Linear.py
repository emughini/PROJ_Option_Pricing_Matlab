# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m

    
@function
def PROJ_GMDB_PiecewiseConstantMortality_Linear(P=None,Pbar=None,S_0=None,W=None,call=None,r=None,params_levy=None,params_mort=None,*args,**kwargs):
    varargin = PROJ_GMDB_PiecewiseConstantMortality_Linear.varargin
    nargin = PROJ_GMDB_PiecewiseConstantMortality_Linear.nargin

    #########################################################
# About: Pricing Function for Gauranteed Minimum Death Benefit Options using PROJ method
#        This version assumes a piecewise constant model of mortality (see first reference below)
# Models Supported: Levy Processes, including jump diffusions and Black-Scholes model
# Returns: price of contract
    
    # Author: Zhimin Zhang  (Original Code)
#         Justin Lars Kirkby (Convert into common framework)
    
    # References:  (1) Valuing Equity-Linked Death Benefits in General Exponential
#               Levy Models, J. Comput. and Appl. Math. 2019 (Z. Zhang, Y. Yong, W. Yu)
#              (2) Efficient Option Pricing By Frame Duality with The Fast
#               Fourier Transform, SIAM J. Financial Math., 2015 (J.L. Kirkby)
    
    # ----------------------
# Contract/Model Params 
# ----------------------
# S_0 = initial stock price (e.g. 100)
# W   = strike  (e.g. 100)
# r   = interest rate (e.g. 0.05)
# call  = 1 for call (else put)  ... NOTE: currently only a PUT contract is supported
# params_levy = parameters of Levy Model
# params_mort = mortality params
    
    # ----------------------
# Numerical (PROJ) Params 
# ----------------------
# P  = resolution parameter (increase P to use more basis elements)
# Pbar = gridwidth parameter (increase Pbar to increase the truncated density support)
#########################################################
    
    ##########################################
# Set Contract / Numerical Params
##########################################
    kk=log(W / S_0)
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:36
    a=2 ** P
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:38
    hat_a=2 ** Pbar
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:39
    N=dot(hat_a,a)
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:41
    Delta=1 / a
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:42
    Delta_s=dot(2,pi) / hat_a
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:42
    ##########################################
# Parse Death Model Params (Piceweise constant forces of mortality)
##########################################
    qx=params_mort.qx
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:48
    
    x=params_mort.x
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:49
    
    max_age=params_mort.max_age
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:50
    n_years=max_age - x
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:52
    
    px=1 - qx
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:53
    mux=- log(px(arange(1,end() - 1)))
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:54
    ##########################################
# Levy Parse Model Params, set model inputs
##########################################
    model=params_levy.model
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:59
    if model == 1:
        sigma=params_levy.sigmaBSM
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:62
        Psi=lambda x=None: dot(dot(- 1 / 2,sigma ** 2),x ** 2)
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:64
        mu=r - Psi(- 1j)
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:65
        phi=lambda s=None: dot(dot(mu,1j),s) - dot(dot(1 / 2,sigma ** 2),s ** 2)
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:67
    else:
        if model == 3:
            alpha=params_levy.alpha
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:71
            beta=params_levy.beta
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:72
            NIG_delta=params_levy.delta
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:73
            sigma=params_levy.sigma
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:74
            gamma=sqrt(alpha ** 2 - beta ** 2)
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:76
            Psi=lambda x=None: dot(dot(- 1 / 2,sigma ** 2),x ** 2) - dot(NIG_delta,(sqrt(alpha ** 2 - (beta + dot(1j,x)) ** 2) - gamma))
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:78
            mu=r - Psi(- 1j)
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:79
            phi=lambda s=None: dot(dot(mu,1j),s) - dot(dot(1 / 2,sigma ** 2),s ** 2) - dot(NIG_delta,(sqrt(alpha ** 2 - (beta + dot(1j,s)) ** 2) - gamma))
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:81
        else:
            if model == 4:
                sigma=params_levy.sigma
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:85
                lambda_J=params_levy.lam
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:86
                mu_J=params_levy.muj
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:87
                sigma_J=params_levy.sigmaj
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:88
                Psi=lambda x=None: dot(- sigma ** 2 / 2,x ** 2) + dot(lambda_J,(exp(dot(dot(1j,x),mu_J) - dot(sigma_J ** 2 / 2,x ** 2)) - 1))
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:90
                mu=r - Psi(- 1j)
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:91
                phi=lambda s=None: dot(dot(1j,s),mu) - dot(sigma ** 2 / 2,s ** 2) + dot(lambda_J,(exp(dot(dot(1j,s),mu_J) - dot(sigma_J ** 2 / 2,s ** 2)) - 1))
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:93
            else:
                if model == 5:
                    sigma=params_levy.sigma
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:98
                    lam_pois=params_levy.lam
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:99
                    p=params_levy.p_up
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:100
                    omega=dot(p,lam_pois)
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:100
                    nv=dot((1 - p),lam_pois)
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:100
                    v=params_levy.eta1
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:101
                    w=params_levy.eta2
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:102
                    D=dot(1 / 2,sigma ** 2)
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:104
                    Psi=lambda x=None: dot(- D,x ** 2) - multiply(multiply(nv,1j),x) / (v + multiply(1j,x)) + multiply(multiply(omega,1j),x) / (w - multiply(1j,x))
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:107
                    mu=r - Psi(- 1j)
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:108
                    phi=lambda s=None: multiply(multiply(mu,1j),s) - multiply(D,s ** 2) - multiply(multiply(nv,1j),s) / (v + multiply(1j,s)) + multiply(multiply(omega,1j),s) / (w - multiply(1j,s))
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:110
                else:
                    if model == 8:
                        sigma=params_levy.sigmaGBM
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:114
                        VG_mu=params_levy.theta
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:115
                        VG_sigma=params_levy.sigma
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:116
                        nv=params_levy.nu
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:117
                        Psi=lambda x=None: dot(dot(- 1 / 2,sigma ** 2),x ** 2) - dot(1 / nv,log(1 - dot(dot(dot(1j,nv),VG_mu),x) + dot(dot(nv,VG_sigma ** 2) / 2,x ** 2)))
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:119
                        mu=r - Psi(- 1j)
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:120
                        phi=lambda s=None: dot(dot(mu,1j),s) - dot(dot(1 / 2,sigma ** 2),s ** 2) - dot(1 / nv,log(1 - dot(dot(dot(1j,nv),VG_mu),s) + dot(dot(nv,VG_sigma ** 2) / 2,s ** 2)))
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:122
    
    ##########################################
    
    x1=mu - dot(Delta,(N / 2 - 1))
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:128
    X=x1 + dot((arange(0,(N - 1))),Delta)
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:129
    delta1=lambda j=None,k=None: (j == k)
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:130
    S=dot((arange(0,(N - 1))),Delta_s)
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:132
    v=lambda j=None: 1 - (delta1(j,1) + delta1(j,N)) / 2
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:133
    Fphi=lambda s=None: dot(12.0,sin(s / 2) ** 2.0) / (dot(s ** 2.0,(2 + cos(s))))
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:134
    Fphi1=Fphi(S / a)
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:135
    Fphi1[1]=1
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:135
    #coefs
    Ak=zeros(1,N)
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:138
    for k in arange(0,N - 1).reshape(-1):
        Ak[k + 1]=0
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:140
        for j in arange(0,n_years - 1).reshape(-1):
            Ak[k + 1]=Ak(k + 1) + dot(dot(dot(prod(px(arange(x + 1,x + j))),exp(dot(j,mux(x + j + 1)))),mux(x + j + 1)),(exp(dot(- (r + mux(x + j + 1) - phi(S(k + 1))),j)) - exp(dot(- (r + mux(x + j + 1) - phi(S(k + 1))),(j + 1))))) / (r + mux(x + j + 1) - phi(S(k + 1)))
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:142
    
    Bk=zeros(1,N)
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:146
    for k in arange(0,N - 1).reshape(-1):
        Bk[k + 1]=0
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:148
        for j in arange(0,n_years - 1).reshape(-1):
            Bk[k + 1]=Bk(k + 1) + dot(dot(dot(prod(px(arange(x + 1,x + j))),exp(dot(j,mux(x + j + 1)))),mux(x + j + 1)),(exp(dot(- (r + mux(x + j + 1) - phi(S(k + 1) - 1j)),j)) - exp(dot(- (r + mux(x + j + 1) - phi(S(k + 1) - 1j)),(j + 1))))) / (r + mux(x + j + 1) - phi(S(k + 1) - 1j))
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:150
    
    beta0=dot(a ** (- 1 / 2) / pi,real(fft(multiply(multiply(multiply(multiply((Ak),Fphi1),v(arange(1,N))),Delta_s),exp(multiply(dot(- 1j,x1),S))))))
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:154
    beta1=dot(a ** (- 1 / 2) / pi,real(fft(multiply(multiply(multiply(multiply((Bk),Fphi1),v(arange(1,N))),Delta_s),exp(multiply(dot(- 1j,x1),S))))))
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:155
    nn=find((kk < X) == 1)
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:157
    n=nn(1)
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:158
    PHi=zeros(1,length(S))
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:159
    if call == 1:
        fprintf('NOT IMPLEMENTED for call option yet')
        price=- 123456789
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:163
    else:
        PHi[n]=dot(a ** (1 / 2),(kk - X(n) + 1 / a)) - dot(a ** (3 / 2) / 2,(1 / (a ** 2) - (kk - X(n)) ** 2))
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:166
        PHi[n - 1]=dot(a ** (1 / 2),(kk - X(n - 1))) - dot(a ** (3 / 2) / 2,(kk - X(n - 1)) ** 2) + dot(1 / 2,a ** (- 1 / 2))
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:167
        PHi[arange(1,n - 2)]=1 / sqrt(a)
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:168
        price=dot(dot(W,beta0),PHi.T) - dot(dot(S_0,beta1),PHi.T)
# PROJ_GMDB_PiecewiseConstantMortality_Linear.m:170
    
    return price
    
if __name__ == '__main__':
    pass
    