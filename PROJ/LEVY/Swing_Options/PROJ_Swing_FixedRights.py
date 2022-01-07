# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# PROJ_Swing_FixedRights.m

    
@function
def PROJ_Swing_FixedRights(M=None,N=None,alpha=None,rnCHF=None,r=None,Dmax=None,T_0=None,T=None,Ns=None,S_0=None,Ks=None,*args,**kwargs):
    varargin = PROJ_Swing_FixedRights.varargin
    nargin = PROJ_Swing_FixedRights.nargin

    #  
#   FOR NOW: T_0 must = 0
    
    K=N / 2
# PROJ_Swing_FixedRights.m:6
    w=log(Ks / S_0)
# PROJ_Swing_FixedRights.m:7
    K1=Ks(1)
# PROJ_Swing_FixedRights.m:8
    K2=Ks(2)
# PROJ_Swing_FixedRights.m:8
    K3=Ks(3)
# PROJ_Swing_FixedRights.m:8
    K4=Ks(4)
# PROJ_Swing_FixedRights.m:8
    Gx=lambda x=None: G_func_swing(x,K1,K2,K3,K4,S_0)
# PROJ_Swing_FixedRights.m:10
    N=dot(2,K)
# PROJ_Swing_FixedRights.m:12
    dt=(T - T_0) / M
# PROJ_Swing_FixedRights.m:13
    nrdt=dot(- r,dt)
# PROJ_Swing_FixedRights.m:14
    xmin=- alpha / 2 + (w(3) + w(2)) / 2
# PROJ_Swing_FixedRights.m:15
    dxtil=dot(2,alpha) / (N - 1)
# PROJ_Swing_FixedRights.m:17
    nbars=floor((w - xmin) / dxtil + 1)
# PROJ_Swing_FixedRights.m:19
    xnbars=xmin + dot(dxtil,(nbars - 1))
# PROJ_Swing_FixedRights.m:20
    diffs=w - xnbars
# PROJ_Swing_FixedRights.m:22
    nbars[diffs < diffs(1)]=nbars(diffs < diffs(1)) - 1
# PROJ_Swing_FixedRights.m:23
    dx=(w(4) - w(1)) / (nbars(4) - nbars(1))
# PROJ_Swing_FixedRights.m:25
    a=1 / dx
# PROJ_Swing_FixedRights.m:25
    xmin=w(1) - dot((nbars(1) - 1),dx)
# PROJ_Swing_FixedRights.m:26
    nbars[arange(2,3)]=floor((w(arange(2,3)) - xmin) / dx + 1)
# PROJ_Swing_FixedRights.m:28
    nnot=floor(1 - dot(xmin,a))
# PROJ_Swing_FixedRights.m:29
    #####################################
#####################################
###########  PHASE I ################
#####################################
#####################################
    
    ###----------------------------------------
    G=dot(Dmax,Gx(xmin + dot(dx,(arange(0,K - 1)))).T)
# PROJ_Swing_FixedRights.m:38
    ###----------------------------------------
    
    ####################################################################
######## Gaussian 3-point
####################################################################
    
    ######  Gaussian Quad Constants
    q_plus=(1 + sqrt(3 / 5)) / 2
# PROJ_Swing_FixedRights.m:46
    q_minus=(1 - sqrt(3 / 5)) / 2
# PROJ_Swing_FixedRights.m:46
    b3=sqrt(15)
# PROJ_Swing_FixedRights.m:47
    b4=b3 / 10
# PROJ_Swing_FixedRights.m:47
    #### PAYOFF CONSTANTS-----------------------------------
    varthet_01=dot(exp(dot(0.5,dx)),(dot(5,cosh(dot(b4,dx))) - dot(b3,sinh(dot(b4,dx))) + 4)) / 18
# PROJ_Swing_FixedRights.m:50
    ThetaDmax=dot(Dmax,GetThetaG_swing(xmin,K,dx,K1,K2,K3,K4,S_0))
# PROJ_Swing_FixedRights.m:52
    THET=repmat(ThetaDmax,1,Ns + 1)
# PROJ_Swing_FixedRights.m:53
    
    E=dot(S_0,exp(xmin + dot(dx,(arange(0,K - 1)))))
# PROJ_Swing_FixedRights.m:54
    ####################################################################
####################################################################
######  T^dt
####################################################################
    a2=a ** 2
# PROJ_Swing_FixedRights.m:60
    zmin=dot((1 - K),dx)
# PROJ_Swing_FixedRights.m:61
    
    dw=dot(dot(2,pi),a) / N
# PROJ_Swing_FixedRights.m:63
    DW=dot(dw,(arange(1,N - 1)))
# PROJ_Swing_FixedRights.m:64
    grand1=multiply(exp(dot(dot(- 1j,zmin),DW)),(sin(DW / (dot(2,a))) / DW) ** 2.0) / (2 + cos(DW / a))
# PROJ_Swing_FixedRights.m:65
    Cons1=dot(24,a2) / N
# PROJ_Swing_FixedRights.m:66
    ###------------------------------------------------------------------
    Cons2=dot(Cons1,exp(nrdt))
# PROJ_Swing_FixedRights.m:68
    grand=multiply(grand1,rnCHF(DW))
# PROJ_Swing_FixedRights.m:69
    beta=dot(Cons2,real(fft(concat([1 / (dot(24,a2)),grand]))))
# PROJ_Swing_FixedRights.m:70
    
    toepM=concat([[beta(arange(K,1,- 1)).T],[0],[beta(arange(dot(2,K) - 1,K,- 1),+ 1).T]])
# PROJ_Swing_FixedRights.m:71
    toepM=fft(toepM)
# PROJ_Swing_FixedRights.m:71
    ###------------------------------------------------------------------
    
    ### initialize for search
    nms=zeros(1,2)
# PROJ_Swing_FixedRights.m:75
    nms[1]=nbars(2) + 1
# PROJ_Swing_FixedRights.m:76
    nms[2]=nbars(3)
# PROJ_Swing_FixedRights.m:77
    ###----------------------------------------
    Cons4=1 / 12
# PROJ_Swing_FixedRights.m:79
    ###----------------------------------------
    xbars=zeros(1,2)
# PROJ_Swing_FixedRights.m:81
    edn=exp(- dx)
# PROJ_Swing_FixedRights.m:82
    nm1vec=dot(ones(Ns + 1,1),nbars(2))
# PROJ_Swing_FixedRights.m:84
    nm2vec=dot(ones(Ns + 1,1),nbars(3))
# PROJ_Swing_FixedRights.m:85
    CONT_nm1=zeros(K,1)
# PROJ_Swing_FixedRights.m:87
    for m in arange(M - 1,1,- 1).reshape(-1):
        for n in arange(2,Ns + 1).reshape(-1):
            pp=ifft(multiply(toepM,fft(concat([[THET(arange(1,K),n)],[zeros(K,1)]]))))
# PROJ_Swing_FixedRights.m:92
            CONT_n=pp(arange(1,K))
# PROJ_Swing_FixedRights.m:93
            PSI=G + CONT_nm1
# PROJ_Swing_FixedRights.m:94
            if n - 1 > M - m:
                THET[arange(),n]=ThetaDmax
# PROJ_Swing_FixedRights.m:98
                THET[arange(2,K - 1),n]=THET(arange(2,K - 1),n) + dot(Cons4,(CONT_nm1(arange(1,K - 2)) + dot(10,CONT_nm1(arange(2,K - 1))) + CONT_nm1(arange(3,K))))
# PROJ_Swing_FixedRights.m:99
                nm1vec[n]=nbars(2)
# PROJ_Swing_FixedRights.m:100
                nm2vec[n]=nbars(3)
# PROJ_Swing_FixedRights.m:100
            else:
                nms[1]=nbars(2)
# PROJ_Swing_FixedRights.m:103
                nms[2]=nbars(3) + 1
# PROJ_Swing_FixedRights.m:103
                #nms(1) = nm1vec(n); nms(2) = nm2vec(n) +1;  ###NOTE: this is slower than reseting based on previous EE point
                while nms(1) > 1 and CONT_n(nms(1)) > PSI(nms(1)):

                    nms[1]=nms(1) - 1
# PROJ_Swing_FixedRights.m:107

                while nms(2) < K - 1 and CONT_n(nms(2)) > PSI(nms(2)):

                    nms[2]=nms(2) + 1
# PROJ_Swing_FixedRights.m:111

                nms[2]=nms(2) - 1
# PROJ_Swing_FixedRights.m:113
                nm1vec[n]=nms(1)
# PROJ_Swing_FixedRights.m:115
                nm2vec[n]=nms(2)
# PROJ_Swing_FixedRights.m:115
                xnbars=xmin + dot(dx,(nms - 1))
# PROJ_Swing_FixedRights.m:117
                tmp1=CONT_n(nms(1)) - PSI(nms(1))
# PROJ_Swing_FixedRights.m:120
                tmp2=CONT_n(nms(1) + 1) - PSI(nms(1) + 1)
# PROJ_Swing_FixedRights.m:120
                xbars[1]=xnbars(1) + max(0,dot(dx,tmp1) / (tmp1 - tmp2))
# PROJ_Swing_FixedRights.m:121
                tmp1=CONT_n(nms(2)) - PSI(nms(2))
# PROJ_Swing_FixedRights.m:125
                tmp2=CONT_n(nms(2) + 1) - PSI(nms(2) + 1)
# PROJ_Swing_FixedRights.m:125
                xbars[2]=xnbars(2) + max(0,dot(dx,tmp1) / (tmp1 - tmp2))
# PROJ_Swing_FixedRights.m:126
                rhos=xbars - xnbars
# PROJ_Swing_FixedRights.m:129
                zetas=dot(a,rhos)
# PROJ_Swing_FixedRights.m:130
                psis=Get_psis_swing(rhos,zetas,q_plus,q_minus,Ks,a,varthet_01,E,nms,nbars,edn)
# PROJ_Swing_FixedRights.m:133
                varths_dt_n=Get_Varths_swing(zetas,nms,CONT_n)
# PROJ_Swing_FixedRights.m:134
                varths_dt_nm1=Get_VarthsDD_swing(zetas,nms,CONT_nm1)
# PROJ_Swing_FixedRights.m:135
                THET[1,n]=PSI(1)
# PROJ_Swing_FixedRights.m:138
                THET[arange(2,nms(1) - 1),n]=ThetaDmax(arange(2,nms(1) - 1)) + dot(Cons4,(CONT_nm1(arange(1,nms(1) - 2)) + dot(10,CONT_nm1(arange(2,nms(1) - 1))) + CONT_nm1(arange(3,nms(1)))))
# PROJ_Swing_FixedRights.m:139
                THET[nms(1),n]=ThetaDmax(nms(1)) - dot(Dmax,psis(1)) + varths_dt_n(1) + varths_dt_nm1(3)
# PROJ_Swing_FixedRights.m:141
                THET[nms(1) + 1,n]=dot(Dmax,psis(2)) + varths_dt_n(2) + varths_dt_nm1(4)
# PROJ_Swing_FixedRights.m:142
                THET[arange(nms(1) + 2,nms(2) - 1),n]=dot(Cons4,(CONT_n(arange(nms(1) + 1,nms(2) - 2)) + dot(10,CONT_n(arange(nms(1) + 2,nms(2) - 1))) + CONT_n(arange(nms(1) + 3,nms(2)))))
# PROJ_Swing_FixedRights.m:144
                THET[nms(2),n]=dot(Dmax,psis(3)) + varths_dt_n(3) + varths_dt_nm1(1)
# PROJ_Swing_FixedRights.m:146
                THET[nms(2) + 1,n]=ThetaDmax(nms(2) + 1) - dot(Dmax,psis(4)) + varths_dt_n(4) + varths_dt_nm1(2)
# PROJ_Swing_FixedRights.m:147
                THET[arange(nms(2) + 2,K - 1),n]=ThetaDmax(arange(nms(2) + 2,K - 1)) + dot(Cons4,(CONT_nm1(arange(nms(2) + 1,K - 2)) + dot(10,CONT_nm1(arange(nms(2) + 2,K - 1))) + CONT_nm1(arange(nms(2) + 3,K))))
# PROJ_Swing_FixedRights.m:149
                THET[K,n]=PSI(K)
# PROJ_Swing_FixedRights.m:150
            CONT_nm1=copy(CONT_n)
# PROJ_Swing_FixedRights.m:154
        CONT_nm1=zeros(K,1)
# PROJ_Swing_FixedRights.m:156
    
    ##########   Time Zero  ############
### Have N_s rights
    pp=ifft(multiply(toepM,fft(concat([[THET(arange(1,K),Ns)],[zeros(K,1)]]))))
# PROJ_Swing_FixedRights.m:161
    CONT_nm1=pp(arange(1,K))
# PROJ_Swing_FixedRights.m:162
    pp=ifft(multiply(toepM,fft(concat([[THET(arange(1,K),Ns + 1)],[zeros(K,1)]]))))
# PROJ_Swing_FixedRights.m:164
    CONT_n=pp(arange(1,K))
# PROJ_Swing_FixedRights.m:165
    PSI=G + CONT_nm1
# PROJ_Swing_FixedRights.m:168
    
    xnot=xmin + dot((nnot - 1),dx)
# PROJ_Swing_FixedRights.m:170
    xs=concat([xnot - dx,xnot,xnot + dx,xnot + dot(2,dx)])
# PROJ_Swing_FixedRights.m:171
    inds=concat([nnot - 1,nnot,nnot + 1,nnot + 2])
# PROJ_Swing_FixedRights.m:172
    ys=max(PSI(inds),CONT_n(inds))
# PROJ_Swing_FixedRights.m:173
    price=spline(xs,ys,0)
# PROJ_Swing_FixedRights.m:175
    return price
    
if __name__ == '__main__':
    pass
    