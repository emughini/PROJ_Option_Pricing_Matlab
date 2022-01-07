# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# PROJ_Swing_LinearRec.m

    
@function
def PROJ_Swing_LinearRec(r=None,S_0=None,Dmax=None,rho_tau=None,T_0=None,T=None,Mtau=None,N=None,alpha=None,rnSYMB=None,Ks=None,*args,**kwargs):
    varargin = PROJ_Swing_LinearRec.varargin
    nargin = PROJ_Swing_LinearRec.nargin

    K1=Ks(1)
# PROJ_Swing_LinearRec.m:3
    K2=Ks(2)
# PROJ_Swing_LinearRec.m:3
    K3=Ks(3)
# PROJ_Swing_LinearRec.m:3
    K4=Ks(4)
# PROJ_Swing_LinearRec.m:3
    w=log(Ks / S_0)
# PROJ_Swing_LinearRec.m:4
    Gx=lambda x=None: G_func_swing(x,K1,K2,K3,K4,S_0)
# PROJ_Swing_LinearRec.m:6
    Dset=arange(1,Dmax)
# PROJ_Swing_LinearRec.m:8
    tau_RD=dot(rho_tau,Dset)
# PROJ_Swing_LinearRec.m:9
    tau1=copy(rho_tau)
# PROJ_Swing_LinearRec.m:10
    ##########
    K=N / 2
# PROJ_Swing_LinearRec.m:13
    dt=tau1 / Mtau
# PROJ_Swing_LinearRec.m:14
    nrdt=dot(- r,dt)
# PROJ_Swing_LinearRec.m:15
    p=floor((T - T_0) / tau1)
# PROJ_Swing_LinearRec.m:17
    Ttil_p=T - dot(p,tau1)
# PROJ_Swing_LinearRec.m:18
    Mtau_pr=floor((Ttil_p - T_0) / dt)
# PROJ_Swing_LinearRec.m:19
    M=dot(p,Mtau) + Mtau_pr
# PROJ_Swing_LinearRec.m:20
    xmin=- alpha / 2 + (w(3) + w(2)) / 2
# PROJ_Swing_LinearRec.m:22
    ###########################################################################
    w=log(concat([K1,K2,K3,K4]) / S_0)
# PROJ_Swing_LinearRec.m:26
    dxtil=dot(2,alpha) / (N - 1)
# PROJ_Swing_LinearRec.m:27
    nbars=floor((w - xmin) / dxtil + 1)
# PROJ_Swing_LinearRec.m:29
    xnbars=xmin + dot(dxtil,(nbars - 1))
# PROJ_Swing_LinearRec.m:30
    diffs=w - xnbars
# PROJ_Swing_LinearRec.m:32
    nbars[diffs < diffs(1)]=nbars(diffs < diffs(1)) - 1
# PROJ_Swing_LinearRec.m:33
    dx=(w(4) - w(1)) / (nbars(4) - nbars(1))
# PROJ_Swing_LinearRec.m:35
    a=1 / dx
# PROJ_Swing_LinearRec.m:35
    xmin=w(1) - dot((nbars(1) - 1),dx)
# PROJ_Swing_LinearRec.m:36
    nbars[arange(2,3)]=floor((w(arange(2,3)) - xmin) / dx + 1)
# PROJ_Swing_LinearRec.m:38
    xnbars=xmin + dot(dx,(nbars - 1))
# PROJ_Swing_LinearRec.m:39
    xnbars[1]=w(1)
# PROJ_Swing_LinearRec.m:40
    xnbars[4]=w(4)
# PROJ_Swing_LinearRec.m:40
    rhos=w - xnbars
# PROJ_Swing_LinearRec.m:42
    zetastar=dot(a,rhos)
# PROJ_Swing_LinearRec.m:43
    nnot=floor(1 - dot(xmin,a))
# PROJ_Swing_LinearRec.m:44
    xnot=xmin + dot((nnot - 1),dx)
# PROJ_Swing_LinearRec.m:46
    xs=concat([xnot - dx,xnot,xnot + dx,xnot + dot(2,dx)])
# PROJ_Swing_LinearRec.m:47
    inds=concat([nnot - 1,nnot,nnot + 1,nnot + 2])
# PROJ_Swing_LinearRec.m:48
    #####################################
#####################################
###########  PHASE I ################
#####################################
#####################################
    
    ####################################################################
######## Gaussian 3-point
####################################################################
    
    ######  Gaussian Quad Constants
    q_plus=(1 + sqrt(3 / 5)) / 2
# PROJ_Swing_LinearRec.m:62
    q_minus=(1 - sqrt(3 / 5)) / 2
# PROJ_Swing_LinearRec.m:62
    b3=sqrt(15)
# PROJ_Swing_LinearRec.m:63
    b4=b3 / 10
# PROJ_Swing_LinearRec.m:63
    #### PAYOFF CONSTANTS-----------------------------------
    varthet_01=dot(exp(dot(0.5,dx)),(dot(5,cosh(dot(b4,dx))) - dot(b3,sinh(dot(b4,dx))) + 4)) / 18
# PROJ_Swing_LinearRec.m:66
    zetas2=zetastar ** 2
# PROJ_Swing_LinearRec.m:67
    edn=exp(- dx)
# PROJ_Swing_LinearRec.m:68
    ###----------------------------------------
### Initialize the dstars used in psis function
    rhos_plus=dot(rhos,q_plus)
# PROJ_Swing_LinearRec.m:72
    rhos_minus=dot(rhos,q_minus)
# PROJ_Swing_LinearRec.m:72
    zetas_plus=dot(a,rhos_plus)
# PROJ_Swing_LinearRec.m:73
    zetas_minus=dot(a,rhos_minus)
# PROJ_Swing_LinearRec.m:73
    eds1=exp(rhos_minus)
# PROJ_Swing_LinearRec.m:74
    eds2=exp(rhos / 2)
# PROJ_Swing_LinearRec.m:74
    eds3=exp(rhos_plus)
# PROJ_Swing_LinearRec.m:74
    dbars_1=zetas2 / 2
# PROJ_Swing_LinearRec.m:76
    dbars_0=zetastar - dbars_1
# PROJ_Swing_LinearRec.m:77
    ds_0=multiply(zetastar,(dot(5,(multiply((1 - zetas_minus),eds1) + multiply((1 - zetas_plus),eds3))) + multiply(dot(4,(2 - zetastar)),eds2))) / 18
# PROJ_Swing_LinearRec.m:78
    ds_1=multiply(dot(edn,zetastar),(dot(5,(multiply(zetas_minus,eds1) + multiply(zetas_plus,eds3))) + multiply(dot(4,zetastar),eds2))) / 18
# PROJ_Swing_LinearRec.m:79
    dstars=zeros(1,4)
# PROJ_Swing_LinearRec.m:81
    dstars[1]=dbars_0(2)
# PROJ_Swing_LinearRec.m:82
    dstars[2]=ds_0(2)
# PROJ_Swing_LinearRec.m:82
    dstars[3]=ds_1(3)
# PROJ_Swing_LinearRec.m:83
    dstars[4]=dbars_1(3)
# PROJ_Swing_LinearRec.m:83
    #==========================================================================
    
    ThetaG=GetThetaG_swing(xmin,K,dx,K1,K2,K3,K4,S_0)
# PROJ_Swing_LinearRec.m:86
    THET=zeros(K,M)
# PROJ_Swing_LinearRec.m:88
    THET[arange(),M]=dot(Dmax,ThetaG)
# PROJ_Swing_LinearRec.m:89
    E=dot(S_0,exp(xmin + dot(dx,(arange(0,K - 1)))))
# PROJ_Swing_LinearRec.m:91
    ####################################################################
####################################################################
######  T^dt
####################################################################
    a2=a ** 2
# PROJ_Swing_LinearRec.m:97
    zmin=dot((1 - K),dx)
# PROJ_Swing_LinearRec.m:97
    
    dw=dot(dot(2,pi),a) / N
# PROJ_Swing_LinearRec.m:98
    DW=dot(dw,(arange(1,N - 1)))
# PROJ_Swing_LinearRec.m:98
    grand1=multiply(exp(dot(dot(- 1j,zmin),DW)),(sin(DW / (dot(2,a))) / DW) ** 2.0) / (2 + cos(DW / a))
# PROJ_Swing_LinearRec.m:99
    Cons1=dot(24,a2) / N
# PROJ_Swing_LinearRec.m:100
    ###------------------------------------------------------------------
    chfpoints=rnSYMB(DW)
# PROJ_Swing_LinearRec.m:102
    Cons2=dot(Cons1,exp(nrdt))
# PROJ_Swing_LinearRec.m:104
    grand=multiply(grand1,exp(dot(dt,chfpoints)))
# PROJ_Swing_LinearRec.m:105
    beta=dot(Cons2,real(fft(concat([1 / (dot(24,a2)),grand]))))
# PROJ_Swing_LinearRec.m:106
    
    toepM=concat([[beta(arange(K,1,- 1)).T],[0],[beta(arange(dot(2,K) - 1,K,- 1),+ 1).T]])
# PROJ_Swing_LinearRec.m:107
    toepM=fft(toepM)
# PROJ_Swing_LinearRec.m:107
    ###------------------------------------------------------------------
    
    ### initialize for search
    nms=zeros(1,2)
# PROJ_Swing_LinearRec.m:112
    nms[1]=nbars(2) + 1
# PROJ_Swing_LinearRec.m:113
    nms[2]=nbars(3) - 1
# PROJ_Swing_LinearRec.m:114
    Cons4=1 / 12
# PROJ_Swing_LinearRec.m:116
    xbars=zeros(1,2)
# PROJ_Swing_LinearRec.m:117
    Gs=repmat(Gx(xmin + dot(dx,(arange(0,K - 1)))).T,1,Dmax)
# PROJ_Swing_LinearRec.m:119
    THETG=repmat(ThetaG,1,Dmax)
# PROJ_Swing_LinearRec.m:120
    for d in arange(2,Dmax).reshape(-1):
        Gs[arange(),d]=dot(d,Gs(arange(),d))
# PROJ_Swing_LinearRec.m:123
        THETG[arange(),d]=dot(d,THETG(arange(),d))
# PROJ_Swing_LinearRec.m:124
    
    G=Gs(arange(),end())
# PROJ_Swing_LinearRec.m:126
    
    ###----------------------------------------
    
    edn=exp(- dx)
# PROJ_Swing_LinearRec.m:129
    dK21=(K2 - K1)
# PROJ_Swing_LinearRec.m:130
    dK43=(K4 - K3)
# PROJ_Swing_LinearRec.m:131
    Thetbar_dt=dot(dK43,cumsum(beta(arange(dot(2,K),K + 1,- 1))).T) + dot(dK21,concat([[fliplr(cumsum(beta(arange(1,K - 1,1)))).T],[0]]))
# PROJ_Swing_LinearRec.m:133
    for m in arange(M - 1,M - (Mtau - 1),- 1).reshape(-1):
        pp=ifft(multiply(toepM,fft(concat([[THET(arange(),m + 1)],[zeros(K,1)]]))))
# PROJ_Swing_LinearRec.m:136
        Cont_dt=pp(arange(1,K)) + Thetbar_dt
# PROJ_Swing_LinearRec.m:137
        while Cont_dt(nms(1)) > G(nms(1)):

            nms[1]=nms(1) - 1
# PROJ_Swing_LinearRec.m:141

        while Cont_dt(nms(2)) > G(nms(2)):

            nms[2]=nms(2) + 1
# PROJ_Swing_LinearRec.m:145

        nms[2]=nms(2) - 1
# PROJ_Swing_LinearRec.m:147
        xnbars=xmin + dot(dx,(nms - 1))
# PROJ_Swing_LinearRec.m:149
        tmp1=Cont_dt(nms(1)) - G(nms(1))
# PROJ_Swing_LinearRec.m:152
        tmp2=Cont_dt(nms(1) + 1) - G(nms(1) + 1)
# PROJ_Swing_LinearRec.m:152
        xbars[1]=(dot((xnbars(1) + dx),tmp1) - dot(xnbars(1),tmp2)) / (tmp1 - tmp2)
# PROJ_Swing_LinearRec.m:153
        tmp1=Cont_dt(nms(2)) - G(nms(2))
# PROJ_Swing_LinearRec.m:156
        tmp2=Cont_dt(nms(2) + 1) - G(nms(2) + 1)
# PROJ_Swing_LinearRec.m:156
        xbars[2]=(dot((xnbars(2) + dx),tmp1) - dot(xnbars(2),tmp2)) / (tmp1 - tmp2)
# PROJ_Swing_LinearRec.m:157
        rhos=xbars - xnbars
# PROJ_Swing_LinearRec.m:159
        zetas=dot(a,rhos)
# PROJ_Swing_LinearRec.m:160
        psis=Get_psis_swing_VER2(rhos,zetas,q_plus,q_minus,Ks,a,varthet_01,E,nms,nbars,edn,zetastar,dstars)
# PROJ_Swing_LinearRec.m:162
        varths_dt=Get_Varths_swing(zetas,nms,Cont_dt)
# PROJ_Swing_LinearRec.m:163
        THET[arange(1,nms(1) - 1),m]=THET(arange(1,nms(1) - 1),M)
# PROJ_Swing_LinearRec.m:166
        THET[nms(1),m]=THET(nms(1),M) - dot(Dmax,psis(1)) + varths_dt(1)
# PROJ_Swing_LinearRec.m:167
        THET[nms(1) + 1,m]=dot(Dmax,psis(2)) + varths_dt(2)
# PROJ_Swing_LinearRec.m:168
        THET[arange(nms(1) + 2,nms(2) - 1),m]=dot(Cons4,(Cont_dt(arange(nms(1) + 1,nms(2) - 2)) + dot(10,Cont_dt(arange(nms(1) + 2,nms(2) - 1))) + Cont_dt(arange(nms(1) + 3,nms(2)))))
# PROJ_Swing_LinearRec.m:170
        THET[nms(2),m]=dot(Dmax,psis(3)) + varths_dt(3)
# PROJ_Swing_LinearRec.m:172
        THET[nms(2) + 1,m]=THET(nms(2) + 1,M) - dot(Dmax,psis(4)) + varths_dt(4)
# PROJ_Swing_LinearRec.m:173
        THET[arange(nms(2) + 2,K),m]=THET(arange(nms(2) + 2,K),M)
# PROJ_Swing_LinearRec.m:174
    
    #####################################
#####################################
###########  PHASE II ###############
#####################################
#####################################
    
    toepMDs=zeros(N,Dmax)
# PROJ_Swing_LinearRec.m:186
    for d in arange(1,Dmax).reshape(-1):
        Cons3=dot(Cons1,exp(dot(- r,tau_RD(d))))
# PROJ_Swing_LinearRec.m:190
        grand=multiply(grand1,exp(dot(tau_RD(d),chfpoints)))
# PROJ_Swing_LinearRec.m:191
        beta=dot(Cons3,real(fft(concat([1 / (dot(24,a2)),grand]))))
# PROJ_Swing_LinearRec.m:192
        toepMDs[arange(),d]=fft(concat([[beta(arange(K,1,- 1)).T],[0],[beta(arange(dot(2,K) - 1,K,- 1),+ 1).T]]))
# PROJ_Swing_LinearRec.m:193
    
    Cont_Ds=zeros(K,Dmax)
# PROJ_Swing_LinearRec.m:197
    PSIs=zeros(K,Dmax + 1)
# PROJ_Swing_LinearRec.m:198
    
    ntil=zeros(1,10)
# PROJ_Swing_LinearRec.m:200
    
    dds=zeros(1,10)
# PROJ_Swing_LinearRec.m:201
    for m in arange(M - Mtau,1,- 1).reshape(-1):
        dstr=copy(Dmax)
# PROJ_Swing_LinearRec.m:206
        while (m + dot(dstr,Mtau)) > M:

            dstr=dstr - 1
# PROJ_Swing_LinearRec.m:208

        for d in arange(1,dstr).reshape(-1):
            pp=ifft(multiply(toepMDs(arange(),d),fft(concat([[THET(arange(),m + dot(d,Mtau))],[zeros(K,1)]]))))
# PROJ_Swing_LinearRec.m:212
            Cont_Ds[arange(),d]=pp(arange(1,K))
# PROJ_Swing_LinearRec.m:213
            PSIs[arange(),d]=Gs(arange(),d) + Cont_Ds(arange(),d)
# PROJ_Swing_LinearRec.m:214
        ######################################################
    ### Now need to store Cont_dt in Dmax +1 spot
        pp=ifft(multiply(toepM,fft(concat([[THET(arange(),m + 1)],[zeros(K,1)]]))))
# PROJ_Swing_LinearRec.m:219
        PSIs[arange(),Dmax + 1]=pp(arange(1,K))
# PROJ_Swing_LinearRec.m:220
        ### we only calculate PSIs up to dstr+1, but we still need to allow for exercise even when
	### the continuation value will be zero (also need to fix at end of algorithm)
        for d in arange(dstr + 1,Dmax).reshape(-1):
            PSIs[arange(),d]=Gs(arange(),d)
# PROJ_Swing_LinearRec.m:226
        ###PSIstr is PSI_Star
        PSIstr,I=max(PSIs(arange(),arange(1,Dmax + 1)),[],2,nargout=2)
# PROJ_Swing_LinearRec.m:230
        I[arange(nbars(2),nbars(3))]=Dmax + 1
# PROJ_Swing_LinearRec.m:232
        MstrL,ntil_L=max(PSIstr(arange(1,nbars(1))),nargout=2)
# PROJ_Swing_LinearRec.m:234
        I[arange(1,ntil_L)]=I(ntil_L)
# PROJ_Swing_LinearRec.m:235
        MstrR,ntil_R=max(PSIstr(arange(nbars(4),K)),nargout=2)
# PROJ_Swing_LinearRec.m:237
        ntil_R=nbars(4) - 1 + ntil_R
# PROJ_Swing_LinearRec.m:238
        ntil_R=min(ntil_R,K - 2)
# PROJ_Swing_LinearRec.m:240
        I[arange(ntil_R,K)]=I(ntil_R)
# PROJ_Swing_LinearRec.m:242
        ######################################################
        ##########################
    ##### Find ntilJ
        ntil[1]=ntil_L
# PROJ_Swing_LinearRec.m:249
        dds[1]=I(ntil(1) + 1)
# PROJ_Swing_LinearRec.m:249
        THET[arange(1,ntil(1) + 1),m]=MstrL
# PROJ_Swing_LinearRec.m:250
        j=2
# PROJ_Swing_LinearRec.m:251
        while ntil(j - 1) < ntil_R:

            temp=find(I(arange(ntil(j - 1) + 1,ntil_R)) != dds(j - 1),1)
# PROJ_Swing_LinearRec.m:254
            if isempty(temp):
                ntil[j]=ntil_R
# PROJ_Swing_LinearRec.m:256
            else:
                ntil[j]=min(ntil_R,temp + ntil(j - 1) - 1)
# PROJ_Swing_LinearRec.m:258
            dds[j]=I(ntil(j) + 1)
# PROJ_Swing_LinearRec.m:260
            x_n_til=xmin + dot(dx,(ntil(j) - 1))
# PROJ_Swing_LinearRec.m:262
            tmp1=PSIs(ntil(j),dds(j - 1)) - PSIs(ntil(j),dds(j))
# PROJ_Swing_LinearRec.m:264
            tmp2=PSIs(ntil(j) + 1,dds(j - 1)) - PSIs(ntil(j) + 1,dds(j))
# PROJ_Swing_LinearRec.m:265
            if tmp1 != tmp2:
                xtil=(dot((x_n_til + dx),tmp1) - dot(x_n_til,tmp2)) / (tmp1 - tmp2)
# PROJ_Swing_LinearRec.m:268
            else:
                xtil=copy(x_n_til)
# PROJ_Swing_LinearRec.m:270
            rho=xtil - x_n_til
# PROJ_Swing_LinearRec.m:272
            zeta=dot(a,rho)
# PROJ_Swing_LinearRec.m:273
            if dds(j - 1) <= dstr:
                THET[arange(ntil(j - 1) + 2,ntil(j) - 1),m]=THETG(arange(ntil(j - 1) + 2,ntil(j) - 1),dds(j - 1)) + dot(Cons4,(Cont_Ds(arange(ntil(j - 1) + 1,ntil(j) - 2),dds(j - 1)) + dot(10,Cont_Ds(arange(ntil(j - 1) + 2,ntil(j) - 1),dds(j - 1))) + Cont_Ds(arange(ntil(j - 1) + 3,ntil(j)),dds(j - 1))))
# PROJ_Swing_LinearRec.m:277
            else:
                if dds(j - 1) < Dmax + 1:
                    THET[arange(ntil(j - 1) + 2,ntil(j) - 1),m]=THETG(arange(ntil(j - 1) + 2,ntil(j) - 1),Dmax)
# PROJ_Swing_LinearRec.m:280
                else:
                    if dds(j - 1) == Dmax + 1:
                        THET[arange(ntil(j - 1) + 2,ntil(j) - 1),m]=dot(Cons4,(PSIs(arange(ntil(j - 1) + 1,ntil(j) - 2),dds(j - 1)) + dot(10,PSIs(arange(ntil(j - 1) + 2,ntil(j) - 1),dds(j - 1))) + PSIs(arange(ntil(j - 1) + 3,ntil(j)),dds(j - 1))))
# PROJ_Swing_LinearRec.m:282
            varths_dj=Get_VarthsPSI_swing(zeta,ntil(j),PSIs(arange(),dds(j)),PSIs(arange(),dds(j - 1)))
# PROJ_Swing_LinearRec.m:285
            THET[ntil(j),m]=varths_dj(3) + varths_dj(1)
# PROJ_Swing_LinearRec.m:286
            THET[ntil(j) + 1,m]=varths_dj(4) + varths_dj(2)
# PROJ_Swing_LinearRec.m:287
            j=j + 1
# PROJ_Swing_LinearRec.m:289

        J=j - 1
# PROJ_Swing_LinearRec.m:291
        THET[arange(ntil_R + 2,K),m]=MstrR
# PROJ_Swing_LinearRec.m:293
    
    #########################################
### NEED TO VALUE AT END OF ALGORITHM (couldn't save THET(:,0))
    
    dstr=copy(Dmax)
# PROJ_Swing_LinearRec.m:300
    while (dot(dstr,Mtau)) > M:

        dstr=dstr - 1
# PROJ_Swing_LinearRec.m:302

    
    for d in arange(1,dstr).reshape(-1):
        pp=ifft(multiply(toepMDs(arange(),d),fft(concat([[THET(arange(),dot(d,Mtau))],[zeros(K,1)]]))))
# PROJ_Swing_LinearRec.m:306
        Cont_Ds[arange(),d]=pp(arange(1,K))
# PROJ_Swing_LinearRec.m:307
        PSIs[arange(),d]=Gs(arange(),d) + Cont_Ds(arange(),d)
# PROJ_Swing_LinearRec.m:308
    
    pp=ifft(multiply(toepM,fft(concat([[THET(arange(),1)],[zeros(K,1)]]))))
# PROJ_Swing_LinearRec.m:312
    PSIs[arange(),Dmax + 1]=pp(arange(1,K))
# PROJ_Swing_LinearRec.m:313
    
    for d in arange(dstr + 1,Dmax).reshape(-1):
        PSIs[arange(),d]=Gs(arange(),d)
# PROJ_Swing_LinearRec.m:316
    
    PSIstr,I=max(PSIs(arange(),arange(1,Dmax + 1)),[],2,nargout=2)
# PROJ_Swing_LinearRec.m:319
    
    ys=PSIstr(inds)
# PROJ_Swing_LinearRec.m:321
    price=spline(xs,ys,0)
# PROJ_Swing_LinearRec.m:322
    return price
    
if __name__ == '__main__':
    pass
    