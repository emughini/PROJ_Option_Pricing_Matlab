# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# get_SV_matrix_expo_inputs.m

    
@function
def get_SV_matrix_expo_inputs(model=None,modparam=None,psi_J=None,dt=None,v=None,dxi=None,r=None,*args,**kwargs):
    varargin = get_SV_matrix_expo_inputs.varargin
    nargin = get_SV_matrix_expo_inputs.nargin

    if model == 1:
        eta=modparam.eta
# get_SV_matrix_expo_inputs.m:4
        theta=modparam.theta
# get_SV_matrix_expo_inputs.m:4
        Rho=modparam.rho
# get_SV_matrix_expo_inputs.m:4
        Sigmav=modparam.Sigmav
# get_SV_matrix_expo_inputs.m:4
        c1=(dot(Rho,eta) / Sigmav - 0.5)
# get_SV_matrix_expo_inputs.m:6
        c2=(r - dot(dot(Rho,eta),theta) / Sigmav)
# get_SV_matrix_expo_inputs.m:6
        c3=dot(0.5,(1 - Rho ** 2))
# get_SV_matrix_expo_inputs.m:6
        v1=dot(dot(dt,1j),(dot(c1,v) + c2 - psi_J(- 1j)))
# get_SV_matrix_expo_inputs.m:7
        v2=dot(dot(dt,c3),v)
# get_SV_matrix_expo_inputs.m:8
        fv=dot((dot(dot(1j,dxi),Rho) / Sigmav),v)
# get_SV_matrix_expo_inputs.m:9
    else:
        if model == 2:
            eta=modparam.eta
# get_SV_matrix_expo_inputs.m:12
            theta=modparam.theta
# get_SV_matrix_expo_inputs.m:12
            Rho=modparam.rho
# get_SV_matrix_expo_inputs.m:12
            Sigmav=modparam.Sigmav
# get_SV_matrix_expo_inputs.m:12
            c1=dot(Rho,eta) / Sigmav - 0.5
# get_SV_matrix_expo_inputs.m:14
            c2=dot(dot(Rho,eta),theta) / Sigmav
# get_SV_matrix_expo_inputs.m:14
            c3=r - psi_J(- 1j) - dot(Rho,Sigmav) / 2
# get_SV_matrix_expo_inputs.m:14
            vsq=v ** 2
# get_SV_matrix_expo_inputs.m:15
            v1=dot(dot(dt,1j),(dot(c1,vsq) - dot(c2,v) + c3))
# get_SV_matrix_expo_inputs.m:16
            v2=dot(dot(dot(dt,0.5),vsq),(1 - Rho ** 2))
# get_SV_matrix_expo_inputs.m:17
            fv=dot((dot(dot(dot(1j,dxi),0.5),Rho) / Sigmav),vsq)
# get_SV_matrix_expo_inputs.m:18
        else:
            if model == 3 or model == 4:
                #Transform to parameters that can be use in 4/2 model
                if model == 3:
                    eta=dot(modparam.eta,modparam.theta)
# get_SV_matrix_expo_inputs.m:23
                    theta=(modparam.eta + modparam.Sigmav ** 2) / eta
# get_SV_matrix_expo_inputs.m:24
                    Sigmav=- modparam.Sigmav
# get_SV_matrix_expo_inputs.m:25
                    Rho=modparam.rho
# get_SV_matrix_expo_inputs.m:27
                    aa=0
# get_SV_matrix_expo_inputs.m:28
                    bb=1
# get_SV_matrix_expo_inputs.m:28
                else:
                    eta=modparam.eta
# get_SV_matrix_expo_inputs.m:30
                    theta=modparam.theta
# get_SV_matrix_expo_inputs.m:30
                    Rho=modparam.rho
# get_SV_matrix_expo_inputs.m:30
                    Sigmav=modparam.Sigmav
# get_SV_matrix_expo_inputs.m:30
                    aa=modparam.aa
# get_SV_matrix_expo_inputs.m:31
                    bb=modparam.bb
# get_SV_matrix_expo_inputs.m:31
                c1=dot(dot(aa,Rho),eta) / Sigmav - dot(0.5,aa ** 2)
# get_SV_matrix_expo_inputs.m:34
                c2=dot(0.5,(dot(dot(Rho,bb),Sigmav) - bb ** 2)) - dot(dot(dot(bb,Rho),eta),theta) / Sigmav
# get_SV_matrix_expo_inputs.m:34
                c3=dot(dot(Rho,eta) / Sigmav,(bb - dot(aa,theta))) + r - psi_J(- 1j) - dot(aa,bb)
# get_SV_matrix_expo_inputs.m:35
                sqrtv=sqrt(v)
# get_SV_matrix_expo_inputs.m:36
                v1=dot(dot(dt,1j),(dot(c1,v) + c2 / v + c3))
# get_SV_matrix_expo_inputs.m:37
                v2=dot(dot(dot(dt,0.5),(1 - Rho ** 2)),(dot(aa,sqrtv) + bb / sqrtv) ** 2)
# get_SV_matrix_expo_inputs.m:38
                fv=dot((dot(dot(1j,dxi),Rho) / Sigmav),(dot(aa,v) + dot(bb,log(v))))
# get_SV_matrix_expo_inputs.m:39
            else:
                if model == 5:
                    Rho=modparam.rho
# get_SV_matrix_expo_inputs.m:42
                    Sigmav=modparam.Sigmav
# get_SV_matrix_expo_inputs.m:42
                    av=modparam.av
# get_SV_matrix_expo_inputs.m:42
                    c1=dot(dot(0.25,Rho),Sigmav) - dot(av,Rho) / Sigmav
# get_SV_matrix_expo_inputs.m:44
                    c2=0.5
# get_SV_matrix_expo_inputs.m:44
                    c3=r - psi_J(- 1j)
# get_SV_matrix_expo_inputs.m:44
                    sqrtv=sqrt(v)
# get_SV_matrix_expo_inputs.m:45
                    v1=dot(dot(dt,1j),(dot(c1,sqrtv) - dot(c2,v) + c3))
# get_SV_matrix_expo_inputs.m:46
                    v2=dot(dot(dot(dt,0.5),(1 - Rho ** 2)),v)
# get_SV_matrix_expo_inputs.m:47
                    fv=dot(dot(dot(dot(1j,dxi),2),Rho) / Sigmav,sqrtv)
# get_SV_matrix_expo_inputs.m:48
                else:
                    if model == 6:
                        eta=modparam.eta
# get_SV_matrix_expo_inputs.m:51
                        theta=modparam.theta
# get_SV_matrix_expo_inputs.m:51
                        Rho=modparam.rho
# get_SV_matrix_expo_inputs.m:51
                        Sigmav=modparam.Sigmav
# get_SV_matrix_expo_inputs.m:51
                        c1v=dot(Rho,(dot(eta / Sigmav,(v - theta)) - Sigmav / 2))
# get_SV_matrix_expo_inputs.m:53
                        c2=0.5
# get_SV_matrix_expo_inputs.m:54
                        c3=r - psi_J(- 1j)
# get_SV_matrix_expo_inputs.m:54
                        expv=exp(v)
# get_SV_matrix_expo_inputs.m:55
                        expv2=expv ** 2
# get_SV_matrix_expo_inputs.m:55
                        v1=dot(dot(dt,1j),(multiply(c1v,expv) - dot(c2,expv2) + c3))
# get_SV_matrix_expo_inputs.m:56
                        v2=dot(dot(dot(dt,0.5),(1 - Rho ** 2)),expv2)
# get_SV_matrix_expo_inputs.m:57
                        fv=dot(dot(dot(1j,dxi),Rho) / Sigmav,expv)
# get_SV_matrix_expo_inputs.m:58
                    else:
                        if model == 7:
                            #      ### Commented Version is With the Second Formultion
#     Rho = modparam.rho; Sigmav = modparam.Sigmav; v0 = modparam.v0; alphav = modparam.alphav; av = modparam.av; bv = modparam.bv;
#     
#     mu_func = @(v)2*(a+Sigmav^2)*v - 2*bv*v.^(1+alphav/2);
#     sig_func = @(v)2*Sigmav*v;
                            #     c1 = (Rho*Sigmav*.5 - Rho*(av + Sigmav)/Sigmav);
#     c2 = .5; c3 = Rho*bv/Sigmav; c4 = r - psi_J(-1i);
#     sqrtv = sqrt(v);
#     v1 = dt*1i*(c1*sqrtv  - c2*v + c3*v.^(1+alphav)/2 + c4 );
#     v2 = dt*.5*(1-Rho^2)*v;
#     fv = 1i*dxi*Rho/Sigmav*sqrtv;
                            Rho=modparam.rho
# get_SV_matrix_expo_inputs.m:74
                            Sigmav=modparam.Sigmav
# get_SV_matrix_expo_inputs.m:74
                            eta=modparam.eta
# get_SV_matrix_expo_inputs.m:74
                            av=modparam.av
# get_SV_matrix_expo_inputs.m:74
                            theta=modparam.theta
# get_SV_matrix_expo_inputs.m:74
                            c1=dot(Rho,theta) / Sigmav
# get_SV_matrix_expo_inputs.m:76
                            c2=dot(Rho,(eta / Sigmav + Sigmav / 2))
# get_SV_matrix_expo_inputs.m:77
                            c3=0.5
# get_SV_matrix_expo_inputs.m:77
                            c4=r - psi_J(- 1j)
# get_SV_matrix_expo_inputs.m:77
                            expv=exp(v)
# get_SV_matrix_expo_inputs.m:78
                            expv2=expv ** 2
# get_SV_matrix_expo_inputs.m:78
                            v1=dot(dot(dt,1j),(dot(c1,exp(dot((1 + av),v))) - dot(c2,expv) - dot(c3,expv2) + c4))
# get_SV_matrix_expo_inputs.m:79
                            v2=dot(dot(dot(dt,0.5),(1 - Rho ** 2)),expv2)
# get_SV_matrix_expo_inputs.m:80
                            fv=dot(dot(dot(1j,dxi),Rho) / Sigmav,expv)
# get_SV_matrix_expo_inputs.m:81
                        else:
                            if model == 8:
                                Rho=modparam.rho
# get_SV_matrix_expo_inputs.m:85
                                Sigmav=modparam.Sigmav
# get_SV_matrix_expo_inputs.m:85
                                eta=modparam.eta
# get_SV_matrix_expo_inputs.m:85
                                theta=modparam.theta
# get_SV_matrix_expo_inputs.m:85
                                vmin=modparam.vmin
# get_SV_matrix_expo_inputs.m:85
                                vmax=modparam.vmax
# get_SV_matrix_expo_inputs.m:85
                                #Qsqrt = @(v) sqrt((v - vmin).*(vmax - v)/denomQ);
                                denomQ=(sqrt(vmax) - sqrt(vmin)) ** 2
# get_SV_matrix_expo_inputs.m:88
                                c1=r - dot(dot(Rho,eta),theta) / Sigmav - psi_J(- 1j)
# get_SV_matrix_expo_inputs.m:90
                                c2=dot(Rho,eta) / Sigmav - 0.5
# get_SV_matrix_expo_inputs.m:91
                                v1=dot(dot(dt,1j),(c1 + dot(v,c2)))
# get_SV_matrix_expo_inputs.m:92
                                v2=dot(dot(dt,0.5),(v - multiply(dot(Rho ** 2 / denomQ,(v - vmin)),(vmax - v))))
# get_SV_matrix_expo_inputs.m:93
                                fv=dot((dot(dot(1j,dxi),Rho) / Sigmav),v)
# get_SV_matrix_expo_inputs.m:94
                                #     c1 = (Rho*eta/Sigmav - .5);  c2 = (r - Rho*eta*theta/Sigmav);   c3 = .5*(1-Rho^2);
#     v1 = dt*1i*(c1*v + c2 - psi_J(-1i));  #Note: we now have the compensated jump component
#     v2 = dt*c3*v;
    
    return v1,v2,fv
    
if __name__ == '__main__':
    pass
    