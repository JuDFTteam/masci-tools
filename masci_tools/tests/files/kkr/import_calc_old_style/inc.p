C ======================================================================
C              parameters file for the host TBKKR package
C                                          last update:   05/06/2004
C ======================================================================
C 
C Description of parameters follows below
C
C a) parameters that have to be set by hand before compilation
C ============================================================
C
C PARAMETER   MEANING (settings)
C ----------------------------------------------------------------------
C KREL         switch for non-relativistic (KREL=0) or relativistic 
C              (KREL=1) program. Attention: several other parameters
C              depend explicitly on KREL, they are set automatically
C              Used for Dirac solver in ASA
C KORBIT       Spin-orbit (KORBIT=1) on non-spin-orbit (KORBIT=0) added
C              to the Schroedinger or SRA equations. Works with FP.
C              KREL and KORBIT cannot be both non-zero.
C KNOCO        (0/1) Collinear/Non-collinear magnetism 
C              (even in non-relativistic non-spin-orbit case)
C KNOSPH       switch for spherical (KNOSPH=0) or non-spherical 
C              (KNOSPH=1) program. Same obs. as for KREL applies.
C KSP          switch for spin-polarised (KSP=1) or paramagnetic 
C              (KSP=0) calculation. It determines the value of NSPIND 
C LMAXD        cut-off for the angular momentum expansion
C IEMXD        dimension for energy-dependent arrays 
C IRMD         number of radial mesh points in (0,...,RWS)
C IRNSD        number of radial mesh points in (RMT,...,RWS)
C NRD          number of real space 
C KPOIBZ       and reciprocal space vectors
C NMAXD,ISHLD  paremeters for the Ewald summations
C NTREFD       parameter in broyden subroutine
C              MUST BE 0 for the host program 
C NATYPD       number of different atomic types in the unit cell 
C NAEZD        number of different atomic sites in the unit cell
C NSHELD       number of blocks of the GF matrix that need to be
C              calculated (NATYPD + off-diagonals in case of impurity)
C NATOMIMPD    size of the cluster for impurity-calculation output of GF
C              should be 1, if you donot do such a calculation
C NREFD        number of reference potentials
C NPRINCD      number of atoms in one principal layer
C NEMBD        number of sites added to the slab in 2D calculations
C              to extend the structure left and right (down and up)
C NCELLD       number of cells (shapes) in non-spherical part
C IPAND        number of panels in non-spherical part
C NFUND,IRID
C NGSHD        shape functions parameters in non-spherical part 
C
C WLENGTH   Word length for direct access files, compiler dependent
C           WLENGTH =1 for ifort but =4 for other compilers
C
C b) parameters derived from the values of the previous ones
C ============================================================
C
C PARAMETER   MEANING (settings)
C ----------------------------------------------------------------------
C NSPIND      number of spin directions, depending on KSP and KREL
C LNC         (Logical) Coupled equations in two spins 
C             (switches true if KREL=1 or KORBIT=1 or KNOCO=1)
C LPOTD       highest expansion in potential 
C NCLEB       number of Clebsch-Gordon coefficients
C NLAYERD     number of principal layers (NAEZD/NPRINCD)
C             used in the inversion routines (independent on NATYPD)
C NSPOTD      number of potentials for storing non-sph. potentials
C NTPERD      parameter in broyden subroutines
C
C =====================================================================
C                           fixed parameters
C =====================================================================
      INTEGER KREL,KNOSPH,KSP,LMAXD,IEMXD,IRMD,IRNSD,
     &        NRD,KPOIBZ,NMAXD,ISHLD,NTREFD,NATYPD,NAEZD,NSHELD,
     &        NATOMIMPD,NREFD,NPRINCD,NEMBD,NCELLD,IPAND,NFUND,IRID,
     &        NGSHD,NCHEBD,NTOTD,KORBIT,WLENGTH,KNOCO
C ---------------------------------------------------------------------
C     general settings
      PARAMETER ( KREL = 0 )
      PARAMETER ( KORBIT = 1 )   ! set to 1 if NEWSOSOL under RUNOPT, otherwise 0
      PARAMETER ( KNOCO= 0 )
      PARAMETER ( KNOSPH = 1 )
      PARAMETER ( KSP = 1 )
      PARAMETER ( LMAXD = 3 )  ! SET ACCORDING TO lmax VALUE OF INPUTCARD
      PARAMETER ( IEMXD = 101 )
      PARAMETER ( IRMD = 900, IRNSD = 890 )
!      PARAMETER ( NRD = 20000, KPOIBZ = 32000 )
      PARAMETER ( NRD = 25000, KPOIBZ = 250000)
      PARAMETER ( NMAXD = 5000000, ISHLD= 200000 )
      PARAMETER ( NTREFD = 0 )             ! must be 0 for host program
C ---------------------------------------------------------------------
C     structure-dependent
      PARAMETER ( NAEZD = 80 ) ! number of atoms in unit cell. Set to NATYP of inputcard
      PARAMETER ( NATYPD = NAEZD )
      PARAMETER ( NSHELD = NATYPD + 155)
!      PARAMETER ( NSHELD = NATYPD + 300)
!      PARAMETER ( NSHELD = NATYPD +1500)
      PARAMETER ( NATOMIMPD = 150)
      PARAMETER ( NREFD = NAEZD )
      PARAMETER ( NPRINCD = 10)
      PARAMETER ( NEMBD = 20)
C ---------------------------------------------------------------------
C     non-spherical potential 
      PARAMETER ( NCELLD = NAEZD, IPAND = 70 )
      PARAMETER ( NTOTD = IPAND+30, NCHEBD = 15 )
      PARAMETER ( NFUND = 900, IRID = 300, NGSHD = 60000)
!      PARAMETER ( NFUND = 289, IRID = 500, NGSHD = 60000)
!      PARAMETER ( NFUND = 289, IRID = 200, NGSHD = 60000) ! 13079
C ---------------------------------------------------------------------
C     I/O
      PARAMETER (WLENGTH = 1)
      
C
C =====================================================================
C                         derived parameters
C =====================================================================
      INTEGER NSPIND,LPOTD,NCLEB,NLAYERD,NSATYPD,NSPOTD,NTPERD
      LOGICAL LNC
C
      PARAMETER ( NSPIND = KREL + (1-KREL)*(KSP+1) )
      PARAMETER ( LPOTD = 2*LMAXD )
      PARAMETER ( NCLEB = (LMAXD*2+1)**2 * (LMAXD+1)**2 )
      PARAMETER ( NLAYERD = (NAEZD/NPRINCD) )
      PARAMETER ( NSATYPD = (NATYPD-1)*KNOSPH+1,
     &            NSPOTD = (2*KREL + (1-KREL)*NSPIND) * NSATYPD )
      PARAMETER ( NTPERD=NATYPD-NTREFD )
      PARAMETER ( LNC = KREL.NE.0.OR.KORBIT.NE.0.OR.KNOCO.NE.0 ) 
C =====================================================================

C ======================================================================
C   parameters file for the host TBKKR package -- TB-clusters settings
C ======================================================================
C
C     Description of parameters follows below (have to be set by hand
C     before compilation)
C ======================================================================
C
C PARAMETER   MEANING (settings)
C ----------------------------------------------------------------------
C NCLSD        maximum number of different TB-clusters
C NACLSD       maximum number of atoms in a TB-cluster
C
C ======================================================================
      INTEGER NCLSD, NACLSD
C
      PARAMETER ( NCLSD = NAEZD + NEMBD )
      PARAMETER ( NACLSD = 500  )
!      PARAMETER ( NACLSD = 1500  )
C ======================================================================

