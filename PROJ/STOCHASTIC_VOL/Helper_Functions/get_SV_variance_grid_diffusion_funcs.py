# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# get_SV_variance_grid_diffusion_funcs.m

    
@function
def get_SV_variance_grid_diffusion_funcs(model=None,modparam=None,*args,**kwargs):
    varargin = get_SV_variance_grid_diffusion_funcs.varargin
    nargin = get_SV_variance_grid_diffusion_funcs.nargin

    #UNTITLED3 Summary of this function goes here
#   Detailed explanation goes here
    if model == 1:
        eta=modparam.eta
# get_SV_variance_grid_diffusion_funcs.m:5
        theta=modparam.theta
# get_SV_variance_grid_diffusion_funcs.m:5
        Sigmav=modparam.Sigmav
# get_SV_variance_grid_diffusion_funcs.m:5
        mu_func=lambda v=None: dot(eta,(theta - v))
# get_SV_variance_grid_diffusion_funcs.m:6
        sig_func=lambda v=None: dot(Sigmav,sqrt(v))
# get_SV_variance_grid_diffusion_funcs.m:7
    else:
        if model == 2:
            eta=modparam.eta
# get_SV_variance_grid_diffusion_funcs.m:10
            theta=modparam.theta
# get_SV_variance_grid_diffusion_funcs.m:10
            Sigmav=modparam.Sigmav
# get_SV_variance_grid_diffusion_funcs.m:10
            mu_func=lambda v=None: dot(eta,(theta - v))
# get_SV_variance_grid_diffusion_funcs.m:11
            sig_func=lambda v=None: dot(Sigmav,(v > - 100))
# get_SV_variance_grid_diffusion_funcs.m:12
        else:
            if model == 3 or model == 4:
                #Transform to parameters that can be use in 4/2 model
                if model == 3:
                    eta=dot(modparam.eta,modparam.theta)
# get_SV_variance_grid_diffusion_funcs.m:18
                    theta=(modparam.eta + modparam.Sigmav ** 2) / eta
# get_SV_variance_grid_diffusion_funcs.m:19
                    Sigmav=- modparam.Sigmav
# get_SV_variance_grid_diffusion_funcs.m:20
                else:
                    eta=modparam.eta
# get_SV_variance_grid_diffusion_funcs.m:23
                    theta=modparam.theta
# get_SV_variance_grid_diffusion_funcs.m:23
                    Sigmav=modparam.Sigmav
# get_SV_variance_grid_diffusion_funcs.m:23
                mu_func=lambda v=None: dot(eta,(theta - v))
# get_SV_variance_grid_diffusion_funcs.m:26
                sig_func=lambda v=None: dot(Sigmav,sqrt(v))
# get_SV_variance_grid_diffusion_funcs.m:27
            else:
                if model == 5:
                    Sigmav=modparam.Sigmav
# get_SV_variance_grid_diffusion_funcs.m:31
                    av=modparam.av
# get_SV_variance_grid_diffusion_funcs.m:31
                    mu_func=lambda v=None: dot(av,v)
# get_SV_variance_grid_diffusion_funcs.m:33
                    sig_func=lambda v=None: dot(Sigmav,v)
# get_SV_variance_grid_diffusion_funcs.m:34
                else:
                    if model == 6:
                        eta=modparam.eta
# get_SV_variance_grid_diffusion_funcs.m:37
                        theta=modparam.theta
# get_SV_variance_grid_diffusion_funcs.m:37
                        Sigmav=modparam.Sigmav
# get_SV_variance_grid_diffusion_funcs.m:37
                        mu_func=lambda v=None: dot(eta,(theta - v))
# get_SV_variance_grid_diffusion_funcs.m:38
                        sig_func=lambda v=None: dot(Sigmav,(v > - 100))
# get_SV_variance_grid_diffusion_funcs.m:39
                    else:
                        if model == 7:
                            #      ### Commented Version is With the Second Formultion
#     Rho = modparam.rho; Sigmav = modparam.Sigmav; v0 = modparam.v0; alphav = modparam.alphav; av = modparam.av; bv = modparam.bv;
#     
#     mu_func = @(v)2*(a+Sigmav^2)*v - 2*bv*v.^(1+alphav/2);
#     sig_func = @(v)2*Sigmav*v;
                            Sigmav=modparam.Sigmav
# get_SV_variance_grid_diffusion_funcs.m:49
                            eta=modparam.eta
# get_SV_variance_grid_diffusion_funcs.m:49
                            av=modparam.av
# get_SV_variance_grid_diffusion_funcs.m:49
                            theta=modparam.theta
# get_SV_variance_grid_diffusion_funcs.m:49
                            mu_func=lambda v=None: eta - dot(theta,exp(dot(av,v)))
# get_SV_variance_grid_diffusion_funcs.m:50
                            sig_func=lambda v=None: dot(Sigmav,(v > - 100))
# get_SV_variance_grid_diffusion_funcs.m:51
                        else:
                            if model == 8:
                                Sigmav=modparam.Sigmav
# get_SV_variance_grid_diffusion_funcs.m:55
                                eta=modparam.eta
# get_SV_variance_grid_diffusion_funcs.m:55
                                theta=modparam.theta
# get_SV_variance_grid_diffusion_funcs.m:55
                                vmin=modparam.vmin
# get_SV_variance_grid_diffusion_funcs.m:55
                                vmax=modparam.vmax
# get_SV_variance_grid_diffusion_funcs.m:55
                                #Qsqrt = @(v) sqrt((v - vmin).*(vmax - v)/denomQ);
                                denomQ=(sqrt(vmax) - sqrt(vmin)) ** 2
# get_SV_variance_grid_diffusion_funcs.m:58
                                mu_func=lambda u=None: dot(eta,(theta - u))
# get_SV_variance_grid_diffusion_funcs.m:59
                                sig_func=lambda u=None: dot(Sigmav / sqrt(denomQ),sqrt(multiply((u - vmin),(vmax - u))))
# get_SV_variance_grid_diffusion_funcs.m:60
    
    return mu_func,sig_func
    
if __name__ == '__main__':
    pass
    