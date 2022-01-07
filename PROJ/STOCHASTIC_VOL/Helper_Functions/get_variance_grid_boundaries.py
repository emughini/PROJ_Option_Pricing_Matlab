# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# get_variance_grid_boundaries.m

    
@function
def get_variance_grid_boundaries(model=None,modparam=None,t=None,gamma=None,*args,**kwargs):
    varargin = get_variance_grid_boundaries.varargin
    nargin = get_variance_grid_boundaries.nargin

    # Retrive lower and upper boundaries for variance grid, based on first two moments of variance process
# model : see below
# modparam : container with each of the model parameters required
# t: time to maturity used for the vairance grid
# gamma: grid mult param, rougly centered around +/- gamma standard deviations of the variance process
    
    if model == 1:
        eta=modparam.eta
# get_variance_grid_boundaries.m:9
        theta=modparam.theta
# get_variance_grid_boundaries.m:9
        Sigmav=modparam.Sigmav
# get_variance_grid_boundaries.m:9
        v0=modparam.v0
# get_variance_grid_boundaries.m:9
        mu_H=dot(exp(dot(- eta,t)),v0) + dot(theta,(1 - exp(dot(- eta,t))))
# get_variance_grid_boundaries.m:11
        sig2_H=dot(dot(Sigmav ** 2 / eta,v0),(exp(dot(- eta,t)) - exp(dot(dot(- 2,eta),t)))) + dot(dot(theta,Sigmav ** 2) / (dot(2,eta)),(1 - dot(2,exp(dot(- eta,t))) + exp(dot(dot(- 2,eta),t))))
# get_variance_grid_boundaries.m:12
    else:
        if model == 2 or model == 6:
            eta=modparam.eta
# get_variance_grid_boundaries.m:15
            theta=modparam.theta
# get_variance_grid_boundaries.m:15
            Sigmav=modparam.Sigmav
# get_variance_grid_boundaries.m:15
            v0=modparam.v0
# get_variance_grid_boundaries.m:15
            mu_H=dot(exp(dot(- eta,t)),v0) + dot(theta,(1 - exp(dot(- eta,t))))
# get_variance_grid_boundaries.m:17
            sig2_H=dot(Sigmav ** 2 / (dot(2,eta)),(1 - exp(dot(dot(- 2,eta),t))))
# get_variance_grid_boundaries.m:18
        else:
            if model == 3:
                #Transform to parameters that can be use in 4/2 model
                eta=dot(modparam.eta,modparam.theta)
# get_variance_grid_boundaries.m:22
                theta=(modparam.eta + modparam.Sigmav ** 2) / eta
# get_variance_grid_boundaries.m:23
                Sigmav=- modparam.Sigmav
# get_variance_grid_boundaries.m:24
                v0=1 / modparam.v0
# get_variance_grid_boundaries.m:25
                mu_H=dot(exp(dot(- eta,t)),v0) + dot(theta,(1 - exp(dot(- eta,t))))
# get_variance_grid_boundaries.m:27
                sig2_H=dot(dot(Sigmav ** 2 / eta,v0),(exp(dot(- eta,t)) - exp(dot(dot(- 2,eta),t)))) + dot(dot(theta,Sigmav ** 2) / (dot(2,eta)),(1 - exp(dot(- eta,t)) + exp(dot(dot(- 2,eta),t))))
# get_variance_grid_boundaries.m:28
            else:
                if model == 4:
                    eta=modparam.eta
# get_variance_grid_boundaries.m:31
                    theta=modparam.theta
# get_variance_grid_boundaries.m:31
                    Sigmav=modparam.Sigmav
# get_variance_grid_boundaries.m:31
                    v0=modparam.v0
# get_variance_grid_boundaries.m:31
                    mu_H=dot(exp(dot(- eta,t)),v0) + dot(theta,(1 - exp(dot(- eta,t))))
# get_variance_grid_boundaries.m:33
                    sig2_H=dot(dot(Sigmav ** 2 / eta,v0),(exp(dot(- eta,t)) - exp(dot(dot(- 2,eta),t)))) + dot(dot(theta,Sigmav ** 2) / (dot(2,eta)),(1 - exp(dot(- eta,t)) + exp(dot(dot(- 2,eta),t))))
# get_variance_grid_boundaries.m:34
                else:
                    if model == 5:
                        Sigmav=modparam.Sigmav
# get_variance_grid_boundaries.m:37
                        v0=modparam.v0
# get_variance_grid_boundaries.m:37
                        av=modparam.av
# get_variance_grid_boundaries.m:37
                        mu_H=dot(v0,exp(dot(av,t)))
# get_variance_grid_boundaries.m:39
                        sig2_H=dot(dot(v0 ** 2,exp(dot(dot(2,av),t))),(exp(dot(Sigmav ** 2,t)) - 1))
# get_variance_grid_boundaries.m:40
                    else:
                        if model == 7:
                            #      ### Commented Version is With the Second Formultion
#     Rho = modparam.rho; Sigmav = modparam.Sigmav; v0 = modparam.v0; alphav = modparam.alphav; av = modparam.av; bv = modparam.bv;
#     Av     = 2*(av + Sigmav^2 - (v0)^(alphav/2)); 
#     mu_H   = v0*exp(Av*t);
#     sig2_H = v0^2*exp(2*av*t)*(exp((2*Sigmav)^2*t)-1);
                            ### Estimate Mean and Variance Using Stein Stein and First order approx
                            Sigmav=modparam.Sigmav
# get_variance_grid_boundaries.m:49
                            v0=modparam.v0
# get_variance_grid_boundaries.m:49
                            eta=modparam.eta
# get_variance_grid_boundaries.m:49
                            av=modparam.av
# get_variance_grid_boundaries.m:49
                            theta=modparam.theta
# get_variance_grid_boundaries.m:49
                            EtaBar=dot(dot(theta,av),exp(dot(av,v0)))
# get_variance_grid_boundaries.m:50
                            ThetaBar=(eta - dot(dot(theta,exp(dot(av,v0))),(1 - dot(av,v0)))) / EtaBar
# get_variance_grid_boundaries.m:50
                            mu_H=dot(exp(dot(- EtaBar,t)),v0) + dot(ThetaBar,(1 - exp(dot(- EtaBar,t))))
# get_variance_grid_boundaries.m:51
                            sig2_H=dot(Sigmav ** 2 / (dot(2,EtaBar)),(1 - exp(dot(dot(- 2,EtaBar),t))))
# get_variance_grid_boundaries.m:53
    
    if model == 8:
        lx=copy(vmin)
# get_variance_grid_boundaries.m:57
        ux=copy(vmax)
# get_variance_grid_boundaries.m:58
    else:
        if model == 2:
            lx=max(0.01,mu_H - dot(gamma,sqrt(sig2_H)))
# get_variance_grid_boundaries.m:61
        else:
            if model == 6 or model == 7:
                lx=mu_H - dot(gamma,sqrt(sig2_H))
# get_variance_grid_boundaries.m:63
            else:
                lx=max(1e-05,mu_H - dot(gamma,sqrt(sig2_H)))
# get_variance_grid_boundaries.m:65
        ux=mu_H + dot(gamma,sqrt(sig2_H))
# get_variance_grid_boundaries.m:67
    
    return lx,v0,ux
    
if __name__ == '__main__':
    pass
    