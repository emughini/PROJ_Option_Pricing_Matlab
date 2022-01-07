# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# PROJ_Swing_ConstantRecovery_Aug.m

    
@function
def PROJ_Swing_ConstantRecovery_Aug(r=None,S_0=None,Dmax=None,T_0=None,T=None,tau1=None,Mtau=None,N=None,alpha=None,rnSYMB=None,Ks=None,*args,**kwargs):
    varargin = PROJ_Swing_ConstantRecovery_Aug.varargin
    nargin = PROJ_Swing_ConstantRecovery_Aug.nargin

    #  rnSYMB is risk-neutral Levy symbol
#  Ks = [K1,K2,K3,K4]
    
    K1=Ks(1)
# PROJ_Swing_ConstantRecovery_Aug.m:5
    K2=Ks(2)
# PROJ_Swing_ConstantRecovery_Aug.m:5
    K3=Ks(3)
# PROJ_Swing_ConstantRecovery_Aug.m:5
    K4=Ks(4)
# PROJ_Swing_ConstantRecovery_Aug.m:5
    w=log(Ks / S_0)
# PROJ_Swing_ConstantRecovery_Aug.m:6
    xmin=- alpha / 2 + (w(3) + w(2)) / 2
# PROJ_Swing_ConstantRecovery_Aug.m:7
    Gx=lambda x=None: G_func_swing(x,K1,K2,K3,K4,S_0)
# PROJ_Swing_ConstantRecovery_Aug.m:9
    K=N / 2
# PROJ_Swing_ConstantRecovery_Aug.m:11
    dt=tau1 / Mtau
# PROJ_Swing_ConstantRecovery_Aug.m:12
    nrdt=dot(- r,dt)
# PROJ_Swing_ConstantRecovery_Aug.m:13
    p=floor((T - T_0) / tau1)
# PROJ_Swing_ConstantRecovery_Aug.m:15
    Ttil_p=T - dot(p,tau1)
# PROJ_Swing_ConstantRecovery_Aug.m:16
    Mtau_pr=floor((Ttil_p - T_0) / dt)
# PROJ_Swing_ConstantRecovery_Aug.m:17
    #Ttil_pp1 = Ttil_p -Mtau_pr*dt;  #If a final European step is needed
    M=dot(p,Mtau) + Mtau_pr
# PROJ_Swing_ConstantRecovery_Aug.m:20
    dxtil=dot(2,alpha) / (N - 1)
# PROJ_Swing_ConstantRecovery_Aug.m:22
    #================  Determine xGrid ========================================
    nbars=floor((w - xmin) / dxtil + 1)
# PROJ_Swing_ConstantRecovery_Aug.m:25
    xnbars=xmin + dot(dxtil,(nbars - 1))
# PROJ_Swing_ConstantRecovery_Aug.m:26
    diffs=w - xnbars
# PROJ_Swing_ConstantRecovery_Aug.m:28
    nbars[diffs < diffs(1)]=nbars(diffs < diffs(1)) - 1
# PROJ_Swing_ConstantRecovery_Aug.m:29
    dx=(w(4) - w(1)) / (nbars(4) - nbars(1))
# PROJ_Swing_ConstantRecovery_Aug.m:31
    a=1 / dx
# PROJ_Swing_ConstantRecovery_Aug.m:31
    xmin=w(1) - dot((nbars(1) - 1),dx)
# PROJ_Swing_ConstantRecovery_Aug.m:32
    nbars[arange(2,3)]=floor((w(arange(2,3)) - xmin) / dx + 1)
# PROJ_Swing_ConstantRecovery_Aug.m:34
    rhos=w - xnbars
# PROJ_Swing_ConstantRecovery_Aug.m:36
    zetastar=dot(a,rhos)
# PROJ_Swing_ConstantRecovery_Aug.m:37
    nnot=floor(1 - dot(xmin,a))
# PROJ_Swing_ConstantRecovery_Aug.m:38
    #==========================================================================
    
    ####################################################################
######## Gaussian 3-point
####################################################################
    
    ######  Gaussian Quad Constants
    q_plus=(1 + sqrt(3 / 5)) / 2
# PROJ_Swing_ConstantRecovery_Aug.m:46
    q_minus=(1 - sqrt(3 / 5)) / 2
# PROJ_Swing_ConstantRecovery_Aug.m:46
    b3=sqrt(15)
# PROJ_Swing_ConstantRecovery_Aug.m:47
    b4=b3 / 10
# PROJ_Swing_ConstantRecovery_Aug.m:47
    #### PAYOFF CONSTANTS-----------------------------------
    varthet_01=dot(exp(dot(0.5,dx)),(dot(5,cosh(dot(b4,dx))) - dot(b3,sinh(dot(b4,dx))) + 4)) / 18
# PROJ_Swing_ConstantRecovery_Aug.m:50
    zetas2=zetastar ** 2
# PROJ_Swing_ConstantRecovery_Aug.m:51
    edn=exp(- dx)
# PROJ_Swing_ConstantRecovery_Aug.m:52
    ###----------------------------------------
### Initialize the dstars used in psis function
    rhos_plus=dot(rhos,q_plus)
# PROJ_Swing_ConstantRecovery_Aug.m:56
    rhos_minus=dot(rhos,q_minus)
# PROJ_Swing_ConstantRecovery_Aug.m:56
    zetas_plus=dot(a,rhos_plus)
# PROJ_Swing_ConstantRecovery_Aug.m:57
    zetas_minus=dot(a,rhos_minus)
# PROJ_Swing_ConstantRecovery_Aug.m:57
    eds1=exp(rhos_minus)
# PROJ_Swing_ConstantRecovery_Aug.m:58
    eds2=exp(rhos / 2)
# PROJ_Swing_ConstantRecovery_Aug.m:58
    eds3=exp(rhos_plus)
# PROJ_Swing_ConstantRecovery_Aug.m:58
    dbars_1=zetas2 / 2
# PROJ_Swing_ConstantRecovery_Aug.m:60
    dbars_0=zetastar - dbars_1
# PROJ_Swing_ConstantRecovery_Aug.m:61
    ds_0=multiply(zetastar,(dot(5,(multiply((1 - zetas_minus),eds1) + multiply((1 - zetas_plus),eds3))) + multiply(dot(4,(2 - zetastar)),eds2))) / 18
# PROJ_Swing_ConstantRecovery_Aug.m:62
    ds_1=multiply(dot(edn,zetastar),(dot(5,(multiply(zetas_minus,eds1) + multiply(zetas_plus,eds3))) + multiply(dot(4,zetastar),eds2))) / 18
# PROJ_Swing_ConstantRecovery_Aug.m:63
    dstars=zeros(1,4)
# PROJ_Swing_ConstantRecovery_Aug.m:65
    dstars[1]=dbars_0(2)
# PROJ_Swing_ConstantRecovery_Aug.m:66
    dstars[2]=ds_0(2)
# PROJ_Swing_ConstantRecovery_Aug.m:66
    dstars[3]=ds_1(3)
# PROJ_Swing_ConstantRecovery_Aug.m:67
    dstars[4]=dbars_1(3)
# PROJ_Swing_ConstantRecovery_Aug.m:67
    #==========================================================================
    ThetaG=GetThetaG_swing(xmin,K,dx,K1,K2,K3,K4,S_0)
# PROJ_Swing_ConstantRecovery_Aug.m:70
    THET=zeros(K,M)
# PROJ_Swing_ConstantRecovery_Aug.m:72
    THET[arange(),M]=dot(Dmax,ThetaG)
# PROJ_Swing_ConstantRecovery_Aug.m:73
    E=dot(S_0,exp(xmin + dot(dx,(arange(0,K - 1)))))
# PROJ_Swing_ConstantRecovery_Aug.m:74
    #####################################
###########  PHASE I ################
#####################################
    
    ####################################################################
######  T^dt
####################################################################
    a2=a ** 2
# PROJ_Swing_ConstantRecovery_Aug.m:83
    zmin=dot((1 - K),dx)
# PROJ_Swing_ConstantRecovery_Aug.m:84
    
    dw=dot(dot(2,pi),a) / N
# PROJ_Swing_ConstantRecovery_Aug.m:86
    DW=dot(dw,(arange(1,N - 1)))
# PROJ_Swing_ConstantRecovery_Aug.m:87
    grand1=multiply(exp(dot(dot(- 1j,zmin),DW)),(sin(DW / (dot(2,a))) / DW) ** 2.0) / (2 + cos(DW / a))
# PROJ_Swing_ConstantRecovery_Aug.m:88
    Cons1=dot(24,a2) / N
# PROJ_Swing_ConstantRecovery_Aug.m:89
    ###------------------------------------------------------------------
    chfpoints=rnSYMB(DW)
# PROJ_Swing_ConstantRecovery_Aug.m:91
    Cons2=dot(Cons1,exp(nrdt))
# PROJ_Swing_ConstantRecovery_Aug.m:93
    grand=multiply(grand1,exp(dot(dt,chfpoints)))
# PROJ_Swing_ConstantRecovery_Aug.m:94
    beta=dot(Cons2,real(fft(concat([1 / (dot(24,a2)),grand]))))
# PROJ_Swing_ConstantRecovery_Aug.m:95
    
    toepM=concat([[beta(arange(K,1,- 1)).T],[0],[beta(arange(dot(2,K) - 1,K,- 1),+ 1).T]])
# PROJ_Swing_ConstantRecovery_Aug.m:97
    toepM=fft(toepM)
# PROJ_Swing_ConstantRecovery_Aug.m:97
    ###------------------------------------------------------------------
    
    ### initialize for search
    nms=zeros(1,2)
# PROJ_Swing_ConstantRecovery_Aug.m:101
    nms[1]=nbars(2) + 1
# PROJ_Swing_ConstantRecovery_Aug.m:102
    nms[2]=nbars(3) - 1
# PROJ_Swing_ConstantRecovery_Aug.m:103
    ###----------------------------------------
    Cons4=1 / 12
# PROJ_Swing_ConstantRecovery_Aug.m:105
    ###----------------------------------------
    
    xbars=zeros(1,2)
# PROJ_Swing_ConstantRecovery_Aug.m:108
    ###----------------------------------------
    G=dot(Dmax,Gx(xmin + dot(dx,(arange(0,K - 1)))).T)
# PROJ_Swing_ConstantRecovery_Aug.m:111
    ###----------------------------------------
    
    edn=exp(- dx)
# PROJ_Swing_ConstantRecovery_Aug.m:114
    dK21=(K2 - K1)
# PROJ_Swing_ConstantRecovery_Aug.m:115
    dK43=(K4 - K3)
# PROJ_Swing_ConstantRecovery_Aug.m:116
    Thetbar_dt=dot(dK43,cumsum(beta(arange(dot(2,K),K + 1,- 1))).T) + dot(dK21,concat([[fliplr(cumsum(beta(arange(1,K - 1,1)))).T],[0]]))
# PROJ_Swing_ConstantRecovery_Aug.m:118
    for m in arange(M - 1,M - (Mtau - 1),- 1).reshape(-1):
        pp=ifft(multiply(toepM,fft(concat([[THET(arange(1,K),m + 1)],[zeros(K,1)]]))))
# PROJ_Swing_ConstantRecovery_Aug.m:121
        Cont_dt=pp(arange(1,K)) + Thetbar_dt
# PROJ_Swing_ConstantRecovery_Aug.m:122
        while (nms(1) > 2) and (Cont_dt(nms(1)) > G(nms(1))):

            nms[1]=nms(1) - 1
# PROJ_Swing_ConstantRecovery_Aug.m:126

        nms[2]=nms(2) + 1
# PROJ_Swing_ConstantRecovery_Aug.m:129
        while nms(2) < K - 2 and Cont_dt(nms(2)) > G(nms(2)):

            nms[2]=nms(2) + 1
# PROJ_Swing_ConstantRecovery_Aug.m:131

        nms[2]=nms(2) - 1
# PROJ_Swing_ConstantRecovery_Aug.m:133
        xnbars=xmin + dot(dx,(nms - 1))
# PROJ_Swing_ConstantRecovery_Aug.m:135
        tmp1=Cont_dt(nms(1)) - G(nms(1))
# PROJ_Swing_ConstantRecovery_Aug.m:138
        tmp2=Cont_dt(nms(1) + 1) - G(nms(1) + 1)
# PROJ_Swing_ConstantRecovery_Aug.m:138
        xbars[1]=(dot((xnbars(1) + dx),tmp1) - dot(xnbars(1),tmp2)) / (tmp1 - tmp2)
# PROJ_Swing_ConstantRecovery_Aug.m:139
        tmp1=Cont_dt(nms(2)) - G(nms(2))
# PROJ_Swing_ConstantRecovery_Aug.m:142
        tmp2=Cont_dt(nms(2) + 1) - G(nms(2) + 1)
# PROJ_Swing_ConstantRecovery_Aug.m:142
        xbars[2]=(dot((xnbars(2) + dx),tmp1) - dot(xnbars(2),tmp2)) / (tmp1 - tmp2)
# PROJ_Swing_ConstantRecovery_Aug.m:143
        rhos=xbars - xnbars
# PROJ_Swing_ConstantRecovery_Aug.m:145
        zetas=dot(a,rhos)
# PROJ_Swing_ConstantRecovery_Aug.m:146
        psis=Get_psis_swing_VER2(rhos,zetas,q_plus,q_minus,Ks,a,varthet_01,E,nms,nbars,edn,zetastar,dstars)
# PROJ_Swing_ConstantRecovery_Aug.m:148
        varths_dt=Get_Varths_swing(zetas,nms,Cont_dt)
# PROJ_Swing_ConstantRecovery_Aug.m:149
        THET[arange(1,nms(1) - 1),m]=THET(arange(1,nms(1) - 1),M)
# PROJ_Swing_ConstantRecovery_Aug.m:152
        THET[nms(1),m]=THET(nms(1),M) - dot(Dmax,psis(1)) + varths_dt(1)
# PROJ_Swing_ConstantRecovery_Aug.m:153
        THET[nms(1) + 1,m]=dot(Dmax,psis(2)) + varths_dt(2)
# PROJ_Swing_ConstantRecovery_Aug.m:154
        THET[arange(nms(1) + 2,nms(2) - 1),m]=dot(Cons4,(Cont_dt(arange(nms(1) + 1,nms(2) - 2)) + dot(10,Cont_dt(arange(nms(1) + 2,nms(2) - 1))) + Cont_dt(arange(nms(1) + 3,nms(2)))))
# PROJ_Swing_ConstantRecovery_Aug.m:156
        THET[nms(2),m]=dot(Dmax,psis(3)) + varths_dt(3)
# PROJ_Swing_ConstantRecovery_Aug.m:158
        THET[nms(2) + 1,m]=THET(nms(2) + 1,M) - dot(Dmax,psis(4)) + varths_dt(4)
# PROJ_Swing_ConstantRecovery_Aug.m:159
        THET[arange(nms(2) + 2,K),m]=THET(arange(nms(2) + 2,K),M)
# PROJ_Swing_ConstantRecovery_Aug.m:160
    
    #####################################
#####################################
###########  PHASE II ###############
#####################################
#####################################
    
    Cons3=dot(Cons1,exp(dot(- r,tau1)))
# PROJ_Swing_ConstantRecovery_Aug.m:171
    grand=multiply(grand1,exp(dot(tau1,chfpoints)))
# PROJ_Swing_ConstantRecovery_Aug.m:172
    beta=dot(Cons3,real(fft(concat([1 / (dot(24,a2)),grand]))))
# PROJ_Swing_ConstantRecovery_Aug.m:173
    toepMD=concat([[beta(arange(K,1,- 1)).T],[0],[beta(arange(dot(2,K) - 1,K,- 1),+ 1).T]])
# PROJ_Swing_ConstantRecovery_Aug.m:174
    toepMD=fft(toepMD)
# PROJ_Swing_ConstantRecovery_Aug.m:174
    evec_D1=cumsum(beta(arange(dot(2,K),K + 1,- 1))).T
# PROJ_Swing_ConstantRecovery_Aug.m:176
    evec_D2=concat([[fliplr(cumsum(beta(arange(1,K - 1,1)))).T],[0]])
# PROJ_Swing_ConstantRecovery_Aug.m:177
    count=copy(Mtau)
# PROJ_Swing_ConstantRecovery_Aug.m:179
    
    for m in arange(M - Mtau,1,- 1).reshape(-1):
        pp=ifft(multiply(toepM,fft(concat([[THET(arange(1,K),m + 1)],[zeros(K,1)]]))))
# PROJ_Swing_ConstantRecovery_Aug.m:182
        Cont_dt=pp(arange(1,K))
# PROJ_Swing_ConstantRecovery_Aug.m:183
        pp=ifft(multiply(toepMD,fft(concat([[THET(arange(1,K),m + Mtau)],[zeros(K,1)]]))))
# PROJ_Swing_ConstantRecovery_Aug.m:185
        Cont_D=pp(arange(1,K)) + dot(evec_D2,THET(1,m + Mtau)) + dot(evec_D1,THET(K,m + Mtau))
# PROJ_Swing_ConstantRecovery_Aug.m:186
        PSI=G + Cont_D
# PROJ_Swing_ConstantRecovery_Aug.m:187
        if rem(count,Mtau) == 0:
            nms[1]=nbars(2)
# PROJ_Swing_ConstantRecovery_Aug.m:191
            nms[2]=nbars(3) + 1
# PROJ_Swing_ConstantRecovery_Aug.m:191
        count=count + 1
# PROJ_Swing_ConstantRecovery_Aug.m:193
        while nms(1) > 2 and Cont_dt(nms(1)) > PSI(nms(1)):

            nms[1]=nms(1) - 1
# PROJ_Swing_ConstantRecovery_Aug.m:196

        while nms(2) < K - 2 and Cont_dt(nms(2)) > PSI(nms(2)):

            nms[2]=nms(2) + 1
# PROJ_Swing_ConstantRecovery_Aug.m:200

        nms[2]=nms(2) - 1
# PROJ_Swing_ConstantRecovery_Aug.m:204
        xnbars=xmin + dot(dx,(nms - 1))
# PROJ_Swing_ConstantRecovery_Aug.m:206
        tmp1=Cont_dt(nms(1)) - PSI(nms(1))
# PROJ_Swing_ConstantRecovery_Aug.m:209
        tmp2=Cont_dt(nms(1) + 1) - PSI(nms(1) + 1)
# PROJ_Swing_ConstantRecovery_Aug.m:209
        xbars[1]=xnbars(1) + max(0,dot(dx,tmp1) / (tmp1 - tmp2))
# PROJ_Swing_ConstantRecovery_Aug.m:210
        tmp1=Cont_dt(nms(2)) - PSI(nms(2))
# PROJ_Swing_ConstantRecovery_Aug.m:213
        tmp2=Cont_dt(nms(2) + 1) - PSI(nms(2) + 1)
# PROJ_Swing_ConstantRecovery_Aug.m:213
        xbars[2]=xnbars(2) + max(0,dot(dx,tmp1) / (tmp1 - tmp2))
# PROJ_Swing_ConstantRecovery_Aug.m:214
        rhos=xbars - xnbars
# PROJ_Swing_ConstantRecovery_Aug.m:217
        zetas=dot(a,rhos)
# PROJ_Swing_ConstantRecovery_Aug.m:218
        psis=Get_psis_swing_VER2(rhos,zetas,q_plus,q_minus,Ks,a,varthet_01,E,nms,nbars,edn,zetastar,dstars)
# PROJ_Swing_ConstantRecovery_Aug.m:220
        varths_dt=Get_Varths_swing(zetas,nms,Cont_dt)
# PROJ_Swing_ConstantRecovery_Aug.m:222
        varths_D=Get_VarthsDD_swing(zetas,nms,Cont_D)
# PROJ_Swing_ConstantRecovery_Aug.m:223
        THET[arange(2,nms(1) - 1),m]=THET(arange(2,nms(1) - 1),M) + dot(Cons4,(Cont_D(arange(1,nms(1) - 2)) + dot(10,Cont_D(arange(2,nms(1) - 1))) + Cont_D(arange(3,nms(1)))))
# PROJ_Swing_ConstantRecovery_Aug.m:227
        THET[1,m]=THET(2,m)
# PROJ_Swing_ConstantRecovery_Aug.m:228
        THET[nms(1),m]=THET(nms(1),M) - dot(Dmax,psis(1)) + varths_dt(1) + varths_D(3)
# PROJ_Swing_ConstantRecovery_Aug.m:230
        THET[nms(1) + 1,m]=dot(Dmax,psis(2)) + varths_dt(2) + varths_D(4)
# PROJ_Swing_ConstantRecovery_Aug.m:231
        THET[arange(nms(1) + 2,nms(2) - 1),m]=dot(Cons4,(Cont_dt(arange(nms(1) + 1,nms(2) - 2)) + dot(10,Cont_dt(arange(nms(1) + 2,nms(2) - 1))) + Cont_dt(arange(nms(1) + 3,nms(2)))))
# PROJ_Swing_ConstantRecovery_Aug.m:233
        THET[nms(2),m]=dot(Dmax,psis(3)) + varths_dt(3) + varths_D(1)
# PROJ_Swing_ConstantRecovery_Aug.m:235
        THET[nms(2) + 1,m]=THET(nms(2) + 1,M) - dot(Dmax,psis(4)) + varths_dt(4) + varths_D(2)
# PROJ_Swing_ConstantRecovery_Aug.m:236
        THET[arange(nms(2) + 2,K - 1),m]=THET(arange(nms(2) + 2,K - 1),M) + dot(Cons4,(Cont_D(arange(nms(2) + 1,K - 2)) + dot(10,Cont_D(arange(nms(2) + 2,K - 1))) + Cont_D(arange(nms(2) + 3,K))))
# PROJ_Swing_ConstantRecovery_Aug.m:238
        THET[K,m]=THET(K - 1,m)
# PROJ_Swing_ConstantRecovery_Aug.m:239
        ###----------------------------------------
    
    pp=ifft(multiply(toepM,fft(concat([[THET(arange(1,K),1)],[zeros(K,1)]]))))
# PROJ_Swing_ConstantRecovery_Aug.m:243
    Cont_dt=pp(arange(1,K))
# PROJ_Swing_ConstantRecovery_Aug.m:244
    pp=ifft(multiply(toepMD,fft(concat([[THET(arange(1,K),Mtau)],[zeros(K,1)]]))))
# PROJ_Swing_ConstantRecovery_Aug.m:246
    Cont_D=pp(arange(1,K)) + dot(evec_D2,THET(1,Mtau)) + dot(evec_D1,THET(K,Mtau))
# PROJ_Swing_ConstantRecovery_Aug.m:247
    PSI=G + Cont_D
# PROJ_Swing_ConstantRecovery_Aug.m:248
    xnot=xmin + dot((nnot - 1),dx)
# PROJ_Swing_ConstantRecovery_Aug.m:250
    xs=concat([xnot - dx,xnot,xnot + dx,xnot + dot(2,dx)])
# PROJ_Swing_ConstantRecovery_Aug.m:252
    inds=concat([nnot - 1,nnot,nnot + 1,nnot + 2])
# PROJ_Swing_ConstantRecovery_Aug.m:253
    ys=max(PSI(inds),Cont_dt(inds))
# PROJ_Swing_ConstantRecovery_Aug.m:254
    price=spline(xs,ys,0)
# PROJ_Swing_ConstantRecovery_Aug.m:256
    return price
    
if __name__ == '__main__':
    pass
    