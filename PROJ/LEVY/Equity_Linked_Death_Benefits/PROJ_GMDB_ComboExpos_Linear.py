# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# PROJ_GMDB_ComboExpos_Linear.m

    
@function
def PROJ_GMDB_ComboExpos_Linear(P=None,Pbar=None,S_0=None,W=None,call=None,r=None,params_levy=None,params_mort=None,T=None,*args,**kwargs):
    varargin = PROJ_GMDB_ComboExpos_Linear.varargin
    nargin = PROJ_GMDB_ComboExpos_Linear.nargin

    #########################################################
# About: Pricing Function for Gauranteed Minimum Death Benefit Options using PROJ method
#        This version assumes a comination of exponentials model of mortality (see first reference below)
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
# T   = time remaining until maturity (in years, e.g. T=10)
#       NOTE: set T=-1 to price a perpetual contract (no expiry)
# call  = 1 for call (else put)
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
# PROJ_GMDB_ComboExpos_Linear.m:38
    a=2 ** P
# PROJ_GMDB_ComboExpos_Linear.m:40
    hat_a=2 ** Pbar
# PROJ_GMDB_ComboExpos_Linear.m:41
    N=dot(hat_a,a)
# PROJ_GMDB_ComboExpos_Linear.m:43
    Delta=1 / a
# PROJ_GMDB_ComboExpos_Linear.m:44
    Delta_s=dot(2,pi) / hat_a
# PROJ_GMDB_ComboExpos_Linear.m:44
    # Deterime if there is a Time to expiry in contract, else it's perpetual
    if nargin < 8:
        T=- 1
# PROJ_GMDB_ComboExpos_Linear.m:48
    
    ##########################################
# Parse Death Model Params
##########################################
    lambda_=params_mort.lambda
# PROJ_GMDB_ComboExpos_Linear.m:54
    
    A=params_mort.A
# PROJ_GMDB_ComboExpos_Linear.m:55
    
    ##########################################
# Levy Parse Model Params, set model inputs
##########################################
    model=params_levy.model
# PROJ_GMDB_ComboExpos_Linear.m:60
    if model == 1:
        sigma=params_levy.sigmaBSM
# PROJ_GMDB_ComboExpos_Linear.m:63
        Psi=lambda x=None: dot(dot(- 1 / 2,sigma ** 2),x ** 2)
# PROJ_GMDB_ComboExpos_Linear.m:65
        mu=r - Psi(- 1j)
# PROJ_GMDB_ComboExpos_Linear.m:66
        phi=lambda s=None: dot(dot(mu,1j),s) - dot(dot(1 / 2,sigma ** 2),s ** 2)
# PROJ_GMDB_ComboExpos_Linear.m:68
        if T > 0:
            diffFgc=lambda c=None: sum(dot(dot(multiply(A,lambda_),(mu + dot(sigma ** 2,c))) / (r + lambda_ - phi(dot(- 1j,c))) ** 2.0,(1 - exp(dot(- (r + lambda_ - phi(dot(- 1j,c))),T)) - multiply(dot(T,exp(dot(- (r + lambda_ - phi(dot(- 1j,c))),T))),(r + lambda_ - phi(dot(- 1j,c)))))))
# PROJ_GMDB_ComboExpos_Linear.m:71
        else:
            diffFgc=lambda c=None: sum(dot(multiply(A,lambda_),(mu + dot(sigma ** 2,c))) / (r + lambda_ - phi(dot(- 1j,c))) ** 2)
# PROJ_GMDB_ComboExpos_Linear.m:73
    else:
        if model == 3:
            alpha=params_levy.alpha
# PROJ_GMDB_ComboExpos_Linear.m:77
            beta=params_levy.beta
# PROJ_GMDB_ComboExpos_Linear.m:78
            NIG_delta=params_levy.delta
# PROJ_GMDB_ComboExpos_Linear.m:79
            sigma=params_levy.sigma
# PROJ_GMDB_ComboExpos_Linear.m:80
            gamma=sqrt(alpha ** 2 - beta ** 2)
# PROJ_GMDB_ComboExpos_Linear.m:82
            Psi=lambda x=None: dot(dot(- 1 / 2,sigma ** 2),x ** 2) - dot(NIG_delta,(sqrt(alpha ** 2 - (beta + dot(1j,x)) ** 2) - gamma))
# PROJ_GMDB_ComboExpos_Linear.m:84
            mu=r - Psi(- 1j)
# PROJ_GMDB_ComboExpos_Linear.m:85
            phi=lambda s=None: dot(dot(mu,1j),s) - dot(dot(1 / 2,sigma ** 2),s ** 2) - dot(NIG_delta,(sqrt(alpha ** 2 - (beta + dot(1j,s)) ** 2) - gamma))
# PROJ_GMDB_ComboExpos_Linear.m:87
            if T > 0:
                diffFgc=lambda c=None: sum(dot(dot(multiply(A,lambda_),(mu + multiply(dot(NIG_delta,sqrt(alpha ** 2 - (beta + c) ** 2)),(beta + c)))) / (r + lambda_ - phi(dot(- 1j,c))) ** 2.0,(1 - exp(dot(- (r + lambda_ - phi(dot(- 1j,c))),T)) - multiply(dot(T,exp(dot(- (r + lambda_ - phi(dot(- 1j,c))),T))),(r + lambda_ - phi(dot(- 1j,c)))))))
# PROJ_GMDB_ComboExpos_Linear.m:90
            else:
                diffFgc=lambda c=None: sum(dot(multiply(A,lambda_),(mu + multiply(dot(NIG_delta,sqrt(alpha ** 2 - (beta + c) ** 2)),(beta + c)))) / (r + lambda_ - phi(dot(- 1j,c))) ** 2)
# PROJ_GMDB_ComboExpos_Linear.m:92
        else:
            if model == 4:
                sigma=params_levy.sigma
# PROJ_GMDB_ComboExpos_Linear.m:96
                lambda_J=params_levy.lam
# PROJ_GMDB_ComboExpos_Linear.m:97
                mu_J=params_levy.muj
# PROJ_GMDB_ComboExpos_Linear.m:98
                sigma_J=params_levy.sigmaj
# PROJ_GMDB_ComboExpos_Linear.m:99
                Psi=lambda x=None: dot(- sigma ** 2 / 2,x ** 2) + dot(lambda_J,(exp(dot(dot(1j,x),mu_J) - dot(sigma_J ** 2 / 2,x ** 2)) - 1))
# PROJ_GMDB_ComboExpos_Linear.m:101
                mu=r - Psi(- 1j)
# PROJ_GMDB_ComboExpos_Linear.m:102
                phi=lambda s=None: dot(dot(1j,s),mu) - dot(sigma ** 2 / 2,s ** 2) + dot(lambda_J,(exp(dot(dot(1j,s),mu_J) - dot(sigma_J ** 2 / 2,s ** 2)) - 1))
# PROJ_GMDB_ComboExpos_Linear.m:104
                if T > 0:
                    diffFgc=lambda c=None: sum(dot(dot(multiply(A,lambda_),(mu + dot(sigma ** 2,c) + multiply(dot(lambda_J,exp(dot(mu_J,c) + dot(dot(1 / 2,sigma_J ** 2),c))),(mu_J + dot(sigma_J ** 2,c))))) / (r + lambda_ - phi(dot(- 1j,c))) ** 2.0,(1 - exp(dot(- (r + lambda_ - phi(dot(- 1j,c))),T)) - multiply(dot(T,exp(dot(- (r + lambda_ - phi(dot(- 1j,c))),T))),(r + lambda_ - phi(dot(- 1j,c)))))))
# PROJ_GMDB_ComboExpos_Linear.m:107
                else:
                    diffFgc=lambda c=None: sum(dot(multiply(A,lambda_),(mu + dot(sigma ** 2,c) + multiply(dot(lambda_J,exp(dot(mu_J,c) + dot(dot(1 / 2,sigma_J ** 2),c))),(mu_J + dot(sigma_J ** 2,c))))) / (r + lambda_ - phi(dot(- 1j,c))) ** 2)
# PROJ_GMDB_ComboExpos_Linear.m:109
            else:
                if model == 5:
                    sigma=params_levy.sigma
# PROJ_GMDB_ComboExpos_Linear.m:114
                    lam_pois=params_levy.lam
# PROJ_GMDB_ComboExpos_Linear.m:115
                    p=params_levy.p_up
# PROJ_GMDB_ComboExpos_Linear.m:116
                    omega=dot(p,lam_pois)
# PROJ_GMDB_ComboExpos_Linear.m:116
                    nv=dot((1 - p),lam_pois)
# PROJ_GMDB_ComboExpos_Linear.m:116
                    v=params_levy.eta1
# PROJ_GMDB_ComboExpos_Linear.m:117
                    w=params_levy.eta2
# PROJ_GMDB_ComboExpos_Linear.m:118
                    D=dot(1 / 2,sigma ** 2)
# PROJ_GMDB_ComboExpos_Linear.m:120
                    Psi=lambda x=None: dot(- D,x ** 2) - multiply(multiply(nv,1j),x) / (v + multiply(1j,x)) + multiply(multiply(omega,1j),x) / (w - multiply(1j,x))
# PROJ_GMDB_ComboExpos_Linear.m:123
                    mu=r - Psi(- 1j)
# PROJ_GMDB_ComboExpos_Linear.m:124
                    phi=lambda s=None: multiply(multiply(mu,1j),s) - multiply(D,s ** 2) - multiply(multiply(nv,1j),s) / (v + multiply(1j,s)) + multiply(multiply(omega,1j),s) / (w - multiply(1j,s))
# PROJ_GMDB_ComboExpos_Linear.m:126
                    if T > 0:
                        diffFgc=lambda c=None: sum(dot(dot(multiply(A,lambda_),(mu + dot(sigma ** 2,c) - dot(nv,v) / (v + c) ** 2 + dot(omega,w) / (w - c) ** 2)) / (r + lambda_ - phi(dot(- 1j,c))) ** 2.0,(1 - exp(dot(- (r + lambda_ - phi(dot(- 1j,c))),T)) - multiply(dot(T,exp(dot(- (r + lambda_ - phi(dot(- 1j,c))),T))),(r + lambda_ - phi(dot(- 1j,c)))))))
# PROJ_GMDB_ComboExpos_Linear.m:129
                    else:
                        diffFgc=lambda c=None: sum(dot(multiply(A,lambda_),(mu + dot(sigma ** 2,c) - dot(nv,v) / (v + c) ** 2 + dot(omega,w) / (w - c) ** 2)) / (r + lambda_ - phi(dot(- 1j,c))) ** 2)
# PROJ_GMDB_ComboExpos_Linear.m:131
                else:
                    if model == 8:
                        sigma=params_levy.sigmaGBM
# PROJ_GMDB_ComboExpos_Linear.m:135
                        VG_mu=params_levy.theta
# PROJ_GMDB_ComboExpos_Linear.m:136
                        VG_sigma=params_levy.sigma
# PROJ_GMDB_ComboExpos_Linear.m:137
                        nv=params_levy.nu
# PROJ_GMDB_ComboExpos_Linear.m:138
                        Psi=lambda x=None: dot(dot(- 1 / 2,sigma ** 2),x ** 2) - dot(1 / nv,log(1 - dot(dot(dot(1j,nv),VG_mu),x) + dot(dot(nv,VG_sigma ** 2) / 2,x ** 2)))
# PROJ_GMDB_ComboExpos_Linear.m:140
                        mu=r - Psi(- 1j)
# PROJ_GMDB_ComboExpos_Linear.m:141
                        phi=lambda s=None: dot(dot(mu,1j),s) - dot(dot(1 / 2,sigma ** 2),s ** 2) - dot(1 / nv,log(1 - dot(dot(dot(1j,nv),VG_mu),s) + dot(dot(nv,VG_sigma ** 2) / 2,s ** 2)))
# PROJ_GMDB_ComboExpos_Linear.m:143
                        if T > 0:
                            diffFgc=lambda c=None: sum(dot(dot(multiply(A,lambda_),(mu + dot(sigma ** 2,c) - (dot(dot(VG_mu,1j),c) - dot(VG_sigma ** 2,c)) / (1 - dot(dot(nv,VG_mu),c) - dot(dot(dot(1 / 2,nv),VG_sigma ** 2),c ** 2)))) / (r + lambda_ - phi(dot(- 1j,c))) ** 2.0,(1 - exp(dot(- (r + lambda_ - phi(dot(- 1j,c))),T)) - multiply(dot(T,exp(dot(- (r + lambda_ - phi(dot(- 1j,c))),T))),(r + lambda_ - phi(dot(- 1j,c)))))))
# PROJ_GMDB_ComboExpos_Linear.m:146
                        else:
                            diffFgc=lambda c=None: sum(dot(multiply(A,lambda_),(mu + dot(sigma ** 2,c) - (dot(dot(VG_mu,1j),c) - dot(VG_sigma ** 2,c)) / (1 - dot(dot(nv,VG_mu),c) - dot(dot(dot(1 / 2,nv),VG_sigma ** 2),c ** 2)))) / (r + lambda_ - phi(dot(- 1j,c))) ** 2)
# PROJ_GMDB_ComboExpos_Linear.m:148
    
    ##########################################
    
    delta1=lambda j=None,k=None: (j == k)
# PROJ_GMDB_ComboExpos_Linear.m:155
    S=dot((arange(0,(N - 1))),Delta_s)
# PROJ_GMDB_ComboExpos_Linear.m:157
    v=lambda j=None: 1 - (delta1(j,1) + delta1(j,N)) / 2
# PROJ_GMDB_ComboExpos_Linear.m:158
    Fphi=lambda s=None: dot(12.0,sin(s / 2) ** 2.0) / (dot(s ** 2.0,(2 + cos(s))))
# PROJ_GMDB_ComboExpos_Linear.m:159
    Fphi1=Fphi(S / a)
# PROJ_GMDB_ComboExpos_Linear.m:160
    Fphi1[1]=1
# PROJ_GMDB_ComboExpos_Linear.m:160
    #coefs
    if T > 0:
        Ak=sum(multiply(repmat(multiply(A,lambda_),length(S),1) / (r + repmat(lambda_,length(S),1) - repmat(phi(S).T,1,2)),(1 - exp(dot(- (r + repmat(lambda_,length(S),1) - repmat(phi(S).T,1,2)),T)))),2)
# PROJ_GMDB_ComboExpos_Linear.m:164
        Ck=sum(multiply(repmat(multiply(A,lambda_),length(S),1) / (r + repmat(lambda_,length(S),1) - repmat(phi(S - 1j).T,1,2)),(1 - exp(dot(- (r + repmat(lambda_,length(S),1) - repmat(phi(S - 1j).T,1,2)),T)))),2)
# PROJ_GMDB_ComboExpos_Linear.m:165
        Fgc=lambda c=None: sum(multiply(multiply(A,lambda_) / (r + lambda_ - phi(dot(- 1j,c))),(1 - exp(dot(- (r + lambda_ - phi(dot(- 1j,c))),T)))))
# PROJ_GMDB_ComboExpos_Linear.m:167
    else:
        Ak=sum(repmat(multiply(A,lambda_),length(S),1) / (r + repmat(lambda_,length(S),1) - repmat(phi(S).T,1,2)),2)
# PROJ_GMDB_ComboExpos_Linear.m:169
        Ck=sum(repmat(multiply(A,lambda_),length(S),1) / (r + repmat(lambda_,length(S),1) - repmat(phi(S - 1j).T,1,2)),2)
# PROJ_GMDB_ComboExpos_Linear.m:170
        Fgc=lambda c=None: sum((multiply(A,lambda_)) / (r + lambda_ - phi(dot(- 1j,c))))
# PROJ_GMDB_ComboExpos_Linear.m:172
    
    # Compute Projections
    x10=real(double(diffFgc(0)) / Fgc(0)) - dot(Delta,(N / 2 - 1))
# PROJ_GMDB_ComboExpos_Linear.m:176
    X0=x10 + dot((arange(0,(N - 1))),Delta)
# PROJ_GMDB_ComboExpos_Linear.m:177
    beta0=dot(a ** (- 1 / 2) / pi,real(fft(multiply(multiply(multiply(multiply((Ak.T),Fphi1),v(arange(1,N))),Delta_s),exp(multiply(dot(- 1j,x10),S))))))
# PROJ_GMDB_ComboExpos_Linear.m:178
    x11=real(double(diffFgc(1)) / Fgc(1)) - dot(Delta,(N / 2 - 1))
# PROJ_GMDB_ComboExpos_Linear.m:180
    X1=x11 + dot((arange(0,(N - 1))),Delta)
# PROJ_GMDB_ComboExpos_Linear.m:181
    beta1=dot(a ** (- 1 / 2) / pi,real(fft(multiply(multiply(multiply(multiply((Ck.T),Fphi1),v(arange(1,N))),Delta_s),exp(multiply(dot(- 1j,x11),S))))))
# PROJ_GMDB_ComboExpos_Linear.m:182
    # Compute Final Payoff and Value
    nn=find((kk < X0) == 1)
# PROJ_GMDB_ComboExpos_Linear.m:185
    n=nn(1)
# PROJ_GMDB_ComboExpos_Linear.m:186
    PHi0=zeros(1,length(S))
# PROJ_GMDB_ComboExpos_Linear.m:187
    nn1=find((kk < X1) == 1)
# PROJ_GMDB_ComboExpos_Linear.m:189
    n1=nn1(1)
# PROJ_GMDB_ComboExpos_Linear.m:190
    PHi1=zeros(1,length(S))
# PROJ_GMDB_ComboExpos_Linear.m:191
    if call == 1:
        PHi0[n]=dot(a ** (1 / 2),(X0(n) - kk)) - dot(a ** (3 / 2) / 2,(kk - X0(n)) ** 2) + dot(1 / 2,a ** (- 1 / 2))
# PROJ_GMDB_ComboExpos_Linear.m:194
        PHi0[n - 1]=dot(a ** (1 / 2),(X0(n - 1) + 1 / a - kk)) - dot(a ** (3 / 2) / 2,(1 / (a ** 2) - (kk - X0(n - 1)) ** 2))
# PROJ_GMDB_ComboExpos_Linear.m:195
        PHi0[arange(n + 1,length(S))]=1 / sqrt(a)
# PROJ_GMDB_ComboExpos_Linear.m:196
        PHi1[n1]=dot(a ** (1 / 2),(X1(n1) - kk)) - dot(a ** (3 / 2) / 2,(kk - X1(n1)) ** 2) + dot(1 / 2,a ** (- 1 / 2))
# PROJ_GMDB_ComboExpos_Linear.m:198
        PHi1[n1 - 1]=dot(a ** (1 / 2),(X1(n1 - 1) + 1 / a - kk)) - dot(a ** (3 / 2) / 2,(1 / (a ** 2) - (kk - X1(n1 - 1)) ** 2))
# PROJ_GMDB_ComboExpos_Linear.m:199
        PHi1[arange(n1 + 1,length(S))]=1 / sqrt(a)
# PROJ_GMDB_ComboExpos_Linear.m:200
        price=dot(dot(S_0,beta1),PHi1.T) - dot(dot(W,beta0),PHi0.T)
# PROJ_GMDB_ComboExpos_Linear.m:202
    else:
        PHi0[n]=dot(a ** (1 / 2),(kk - X0(n) + 1 / a)) - dot(a ** (3 / 2) / 2,(1 / (a ** 2) - (kk - X0(n)) ** 2))
# PROJ_GMDB_ComboExpos_Linear.m:204
        PHi0[n - 1]=dot(a ** (1 / 2),(kk - X0(n - 1))) - dot(a ** (3 / 2) / 2,(kk - X0(n - 1)) ** 2) + dot(1 / 2,a ** (- 1 / 2))
# PROJ_GMDB_ComboExpos_Linear.m:205
        PHi0[arange(1,n - 2)]=1 / sqrt(a)
# PROJ_GMDB_ComboExpos_Linear.m:206
        PHi1[n1]=dot(a ** (1 / 2),(kk - X1(n1) + 1 / a)) - dot(a ** (3 / 2) / 2,(1 / (a ** 2) - (kk - X1(n1)) ** 2))
# PROJ_GMDB_ComboExpos_Linear.m:208
        PHi1[n1 - 1]=dot(a ** (1 / 2),(kk - X1(n1 - 1))) - dot(a ** (3 / 2) / 2,(kk - X1(n1 - 1)) ** 2) + dot(1 / 2,a ** (- 1 / 2))
# PROJ_GMDB_ComboExpos_Linear.m:209
        PHi1[arange(1,n1 - 2)]=1 / sqrt(a)
# PROJ_GMDB_ComboExpos_Linear.m:210
        price=dot(dot(W,beta0),PHi0.T) - dot(dot(S_0,beta1),PHi1.T)
# PROJ_GMDB_ComboExpos_Linear.m:212
    
    return price
    
if __name__ == '__main__':
    pass
    