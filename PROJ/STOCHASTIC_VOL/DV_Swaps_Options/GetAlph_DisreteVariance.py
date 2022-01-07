# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# GetAlph_DisreteVariance.m

    
@function
def GetAlph_DisreteVariance(c2Jump=None,c4Jump=None,model=None,modparam=None,T=None,L1=None,*args,**kwargs):
    varargin = GetAlph_DisreteVariance.varargin
    nargin = GetAlph_DisreteVariance.nargin

    # Gets alph parameter (truncated density width param) to apply PROJ method to ChF of realized variance
# c2Jump - second cumulant of jump component
# c4Jump - fourth cumulant of jump component
# model - SV model id number (see below)
# modparm - container with each param needed for given model
# T - contract maturity
# L1 - truncation gridwidth multiplication param
    
    minalph=0.5
# GetAlph_DisreteVariance.m:10
    
    t=T / 2
# GetAlph_DisreteVariance.m:12
    if model == 1:
        eta=modparam.eta
# GetAlph_DisreteVariance.m:15
        theta=modparam.theta
# GetAlph_DisreteVariance.m:15
        Rho=modparam.rho
# GetAlph_DisreteVariance.m:15
        Sigmav=modparam.Sigmav
# GetAlph_DisreteVariance.m:15
        v0=modparam.v0
# GetAlph_DisreteVariance.m:15
        mu_H=dot(exp(dot(- eta,t)),v0) + dot(theta,(1 - exp(dot(- eta,t))))
# GetAlph_DisreteVariance.m:17
        mfunc=lambda v=None: sqrt(v)
# GetAlph_DisreteVariance.m:19
    else:
        if model == 2:
            eta=modparam.eta
# GetAlph_DisreteVariance.m:22
            theta=modparam.theta
# GetAlph_DisreteVariance.m:22
            Rho=modparam.rho
# GetAlph_DisreteVariance.m:22
            Sigmav=modparam.Sigmav
# GetAlph_DisreteVariance.m:22
            v0=modparam.v0
# GetAlph_DisreteVariance.m:22
            mu_H=dot(exp(dot(- eta,t)),v0) + dot(theta,(1 - exp(dot(- eta,t))))
# GetAlph_DisreteVariance.m:24
            mfunc=lambda v=None: v
# GetAlph_DisreteVariance.m:26
        else:
            if model == 6:
                eta=modparam.eta
# GetAlph_DisreteVariance.m:28
                theta=modparam.theta
# GetAlph_DisreteVariance.m:28
                Rho=modparam.rho
# GetAlph_DisreteVariance.m:28
                Sigmav=modparam.Sigmav
# GetAlph_DisreteVariance.m:28
                v0=modparam.v0
# GetAlph_DisreteVariance.m:28
                mu_H=dot(exp(dot(- eta,t)),v0) + dot(theta,(1 - exp(dot(- eta,t))))
# GetAlph_DisreteVariance.m:30
                mfunc=lambda v=None: exp(v)
# GetAlph_DisreteVariance.m:32
            else:
                if model == 3:
                    #Transform to parameters that can be use in 4/2 model
                    eta=dot(modparam.eta,modparam.theta)
# GetAlph_DisreteVariance.m:36
                    theta=(modparam.eta + modparam.Sigmav ** 2) / eta
# GetAlph_DisreteVariance.m:37
                    Sigmav=- modparam.Sigmav
# GetAlph_DisreteVariance.m:38
                    v0=1 / modparam.v0
# GetAlph_DisreteVariance.m:39
                    Rho=modparam.rho
# GetAlph_DisreteVariance.m:40
                    aa=0
# GetAlph_DisreteVariance.m:41
                    bb=1
# GetAlph_DisreteVariance.m:41
                    mu_H=dot(exp(dot(- eta,t)),v0) + dot(theta,(1 - exp(dot(- eta,t))))
# GetAlph_DisreteVariance.m:43
                    mfunc=lambda v=None: 1.0 / sqrt(v)
# GetAlph_DisreteVariance.m:44
                else:
                    if model == 4:
                        eta=modparam.eta
# GetAlph_DisreteVariance.m:47
                        theta=modparam.theta
# GetAlph_DisreteVariance.m:47
                        Rho=modparam.rho
# GetAlph_DisreteVariance.m:47
                        Sigmav=modparam.Sigmav
# GetAlph_DisreteVariance.m:47
                        v0=modparam.v0
# GetAlph_DisreteVariance.m:47
                        aa=modparam.aa
# GetAlph_DisreteVariance.m:48
                        bb=modparam.bb
# GetAlph_DisreteVariance.m:48
                        mu_H=dot(exp(dot(- eta,t)),v0) + dot(theta,(1 - exp(dot(- eta,t))))
# GetAlph_DisreteVariance.m:50
                        mfunc=lambda v=None: dot(aa,sqrt(v)) + bb / sqrt(v)
# GetAlph_DisreteVariance.m:51
                    else:
                        if model == 5:
                            Rho=modparam.rho
# GetAlph_DisreteVariance.m:54
                            Sigmav=modparam.Sigmav
# GetAlph_DisreteVariance.m:54
                            v0=modparam.v0
# GetAlph_DisreteVariance.m:54
                            av=modparam.av
# GetAlph_DisreteVariance.m:54
                            mu_H=dot(v0,exp(dot(av,t)))
# GetAlph_DisreteVariance.m:56
                            mfunc=lambda v=None: sqrt(v)
# GetAlph_DisreteVariance.m:57
                        else:
                            if model == 7:
                                Rho=modparam.rho
# GetAlph_DisreteVariance.m:60
                                Sigmav=modparam.Sigmav
# GetAlph_DisreteVariance.m:60
                                v0=modparam.v0
# GetAlph_DisreteVariance.m:60
                                eta=modparam.eta
# GetAlph_DisreteVariance.m:60
                                av=modparam.av
# GetAlph_DisreteVariance.m:60
                                theta=modparam.theta
# GetAlph_DisreteVariance.m:60
                                EtaBar=dot(dot(theta,av),exp(dot(av,v0)))
# GetAlph_DisreteVariance.m:63
                                ThetaBar=(eta - dot(dot(theta,exp(dot(av,v0))),(1 - dot(av,v0)))) / EtaBar
# GetAlph_DisreteVariance.m:63
                                mu_H=dot(exp(dot(- EtaBar,t)),v0) + dot(ThetaBar,(1 - exp(dot(- EtaBar,t))))
# GetAlph_DisreteVariance.m:64
                                mfunc=lambda v=None: exp(v)
# GetAlph_DisreteVariance.m:65
    
    c2=c2Jump + mfunc(mu_H) ** 2
# GetAlph_DisreteVariance.m:68
    c4=copy(c4Jump)
# GetAlph_DisreteVariance.m:69
    alph=dot(L1,sqrt(dot(c2,t) + sqrt(dot(c4,T))))
# GetAlph_DisreteVariance.m:70
    alph=max(alph,minalph)
# GetAlph_DisreteVariance.m:71
    return alph
    
if __name__ == '__main__':
    pass
    