# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c), Forschungszentrum Jülich GmbH, IAS-1/PGI-1, Germany.         #
#                All rights reserved.                                         #
# This file is part of the Masci-tools package.                               #
# (Material science tools)                                                    #
#                                                                             #
# The code is hosted on GitHub at https://github.com/judftteam/masci-tools.   #
# For further information on the license, see the LICENSE.txt file.           #
# For further information please visit http://judft.de/.                      #
#                                                                             #
###############################################################################
from masci_tools.io.common_functions import open_general
"""
In this module you find the kkrparams class that helps defining the KKR input parameters
Also some defaults for the parameters are defined.
"""

__copyright__ = ('Copyright (c), 2017, Forschungszentrum Jülich GmbH,' 'IAS-1/PGI-1, Germany. All rights reserved.')
__license__ = 'MIT license, see LICENSE.txt file'
__version__ = '1.8.6'
__contributors__ = 'Philipp Rüßmann'

# This defines the default parameters for KKR used in the aiida plugin:
__kkr_default_params__ = {
    'LMAX': 3,  # lmax-cutoff
    'INS': 1,  # use shape corrections (full potential)
    'KSHAPE': 2,  # basically the same information as INS (KSHAPE=2*INS should always hold!)
    'NSPIN': 2,  # spin-polarized calculation (but by default not automatically initialized with external field)
    'RMAX': 10.,  # Madelung sum real-space cutoff
    'GMAX': 100.,  # Madelung sum reciprocal-space cutoff
    'RCLUSTZ': 2.3  # size of screening cluster (in alat units)
}

# prevent kkrparams to add brackets around these keywords automatically
__forbid_brackets__ = ['use_input_alat']


class kkrparams(object):
    """
    Class for creating and handling the parameter input for a KKR calculation
    Optional keyword arguments are passed to init and stored in values dictionary.

    Example usage: params = kkrparams(LMAX=3, BRAVAIS=array([[1,0,0], [0,1,0], [0,0,1]]))

    Alternatively values can be set afterwards either individually with
        params.set_value('LMAX', 3)
    or multiple keys at once with
        params.set_multiple_values(EMIN=-0.5, EMAX=1)

    Other useful functions

    - print the description of a keyword: params.get_description([key]) where [key] is a string for a keyword in params.values
    - print a list of mandatory keywords: params.get_all_mandatory()
    - print a list of keywords that are set including their value: params.get_set_values()

    .. note:
        KKR-units (e.g. atomic units with energy in Ry, length in a_Bohr) are assumed
        except for the keys'<RBLEFT>', '<RBRIGHT>', 'ZPERIODL', and 'ZPERIODR' which should be given in Ang. units!
    """

    def __init__(self, **kwargs):
        """
        Initialize class instance with containing the attribute values that also have
        a format, mandatory flags (defaults for KKRcode, changed for example via params_type='voronoi' keyword) and a description.
        """

        # keywords for KKRhost and voronoi (all allowed keys for inputcard)
        self._DEFAULT_KEYWORDS_KKR = dict([  # complete list of keywords, detault all that are not mandatory to None
            # lattice
            ('ALATBASIS', [
                None, '%f', True,
                'Description of lattice: Length unit in Bohr radii usually conventional lattice parameter'
            ]),
            ('BRAVAIS', [
                None, '%f %f %f\n%f %f %f\n%f %f %f', True,
                'Description of lattice: Bravais vectors in units of [ALATBASIS]'
            ]),
            ('NAEZ', [None, '%i', True, 'Description of lattice: Number of sites in unit cell']),
            ('<RBASIS>', [None, '%f %f %f', True, 'Description of lattice: Positions of sites in unit cell']),
            ('CARTESIAN', [
                None, '%l', False,
                'Description of lattice: Interpret the basis vector coordinates as reduced (w. respect to bravais) or as cartesian (in lattice constant units)'
            ]),
            ('INTERFACE', [None, '%l', False, 'Description of lattice, 2D mode: needs to be TRUE for 2D calculation']),
            ('<NLBASIS>', [
                None, '%i', False,
                'Description of lattice, 2D mode: Number of basis sites forming the half-infinite lattice to the lower (=left) part of the slab.'
            ]),
            ('<RBLEFT>', [
                None, '%f %f %f', False,
                'Description of lattice, 2D mode: Positions of sites forming the basis sites of the half-infinite lattice to the lower (=left) part of the slab.'
            ]),
            ('ZPERIODL', [
                None, '%f %f %f', False,
                'Description of lattice, 2D mode: Lattice vector describing the periodicity perpendicular to the slab-plane for the half-infinite lattice to the lower (=left) part of the slab (plays the role of the 3rd Bravais vector for this half-infinite lattice). The <RBLEFT> vectors are periodically repeated by the ZPERIODL vector.'
            ]),
            ('<NRBASIS>', [
                None, '%i', False,
                'Description of lattice, 2D mode: Number of basis sites forming the half-infinite lattice to the upper (=right) part of the slab.'
            ]),
            ('<RBRIGHT>', [
                None, '%f %f %f', False,
                'Description of lattice, 2D mode: Positions of sites forming the basis sites of the half-infinite lattice to the upper (=right) part of the slab.'
            ]),
            ('ZPERIODR', [
                None, '%f %f %f', False,
                'Description of lattice, 2D mode: Lattice vector describing the periodicity perpendicular to the slab-plane for the half-infinite lattice to the upper (=right) part of the slab (plays the role of the 3rd Bravais vector for this half-infinite lattice). The <RBRIGHT> vectors are periodically repeated by the ZPERIODR vector.'
            ]),
            ('KSHAPE', [
                None, '%i', False,
                'Description of lattice, shape functions: 0 for ASA ([INS]=0), 2 for full potential ([INS]=1)'
            ]),
            ('<SHAPE>', [
                None, '%i', False,
                'Description of lattice, shape functions: Indexes which shape function from the shape-function file to use in which atom. Default is that each atom has its own shape function.'
            ]),
            # chemistry
            ('<ZATOM>', [
                None, '%f', True,
                'Chemistry, Atom types: Nuclear charge per atom. Negative value signals to use value read in from the potential file.'
            ]),
            ('NSPIN',
             [None, '%i', True, 'Chemistry, Atom types: Number of spin directions in potential. Values 1 or 2']),
            ('KVREL', [
                None, '%i', False,
                'Chemistry, Atom types: Relativistic treatment of valence electrons. Takes values 0 (Schroedinger), 1 (Scalar relativistic), 2 (Dirac ; works only in ASA mode)'
            ]),
            ('<SOCSCL>', [
                None, '%f', False,
                'Chemistry, Atom types: Spin-orbit coupling scaling per atom. Takes values between 0. (no spin-orbit) and 1. (full spin-orbit). Works only in combination with the Juelich spin orbit solver (runoption NEWSOSOL)'
            ]),
            ('KEXCOR', [
                None, '%i', False,
                'Chemistry, Exchange-correlation: Type of exchange correlation potential. Takes values 0 (LDA, Moruzzi-Janak-Williams), 1 (LDA, von Barth-Hedin), 2 (LDA, Vosko-Wilk-Nussair), 3 (GGA, Perdew-Wang 91), 4 (GGA, PBE), 5 (GGA, PBEsol)'
            ]),
            ('LAMBDA_XC', [
                None, '%f', False,
                'Chemistry, Exchange-correlation: Scale the magnetic part of the xc-potential and energy. Takes values between 0. (fully suppressed magnetisc potential) and 1. (normal magnetic potential).'
            ]),
            ('NAT_LDAU',
             [None, '%i', False, 'Chemistry, Exchange-correlation: Numer of atoms where LDA+U will be used']),
            ('LDAU_PARA', [
                None, '%i %i %f %f %f', False,
                'Chemistry, Exchange-correlation: For each atom where LDA+U should be used, the entries are: [atom type] [angular mom. to apply LDA+U] [Ueff] [Jeff] [Eref] where [atom type] is between 1...[NATYP].'
            ]),
            ('KREADLDAU', [
                None, '%i', False,
                "Chemistry, Exchange-correlation: Takes values 0 or 1; if [KREADLDAU]=1 then read previously calculated LDA+U matrix elements from file 'ldaupot'."
            ]),
            ('NATYP', [
                None, '%i', False,
                'Chemistry, CPA mode: Number of atom types; CPA is triggered by setting [NATYP]>[NAEZ].'
            ]),
            ('<SITE>', [
                None, '%i', False,
                'Chemistry, CPA mode: Takes values 1 < [<SITE>] < [NAEZ] Assigns the position (given by [<RBASIS>]) where the atom-dependent read-in potential is situated. E.g., if the 3rd-in-the-row potential should be positioned at the 2nd <RBASIS> vector, then the 3rd entry of the <SITE> list should have the value 2.'
            ]),
            ('<CPA-CONC>', [
                None, '%f', False,
                'Chemistry, CPA mode: Takes values 0. < [<CPA-CONC>] < 1. Assigns the alloy-concentration corresponding to the atom-dependent read-in potential. Together with the variable <SITE>, <CPA-CONC> assigns the number and concentration of the atom-dependent potentials residing at each site form 1 to [NAEZ]. The sum of concentrations at each site should equal 1.'
            ]),
            ('<KAOEZL>', [
                None, '%i', False,
                'Chemistry, 2D mode: Controls the type of t-matrix at the lower (=left) half-crystal sites in case of embedding as these are given in the left-decimation file (i.e., changes the order compared to the one in the left-decimation file).'
            ]),
            ('<KAOEZR>', [
                None, '%i', False,
                'Chemistry, 2D mode: Controls the type of t-matrix at the upper (=right) half-crystal sites in case of embedding as these are given in the right-decimation file (i.e., changes the order compared to the one in the right-decimation file).'
            ]),
            # external fields
            ('LINIPOL', [
                None, '%l', False,
                'External fields: If TRUE, triggers an external magn. field per atom in the first iteration.'
            ]),
            ('HFIELD', [
                None, '%f', False,
                'External fields: Value of an external magnetic field in the first iteration. Works only with LINIPOL, XINIPOL'
            ]),
            ('XINIPOL', [None, '%i', False, 'External fields: Integer multiplying the HFIELD per atom']),
            ('VCONST', [None, '%f', False, 'External fields: Constant potential shift in the first iteration.']),
            ('IVSHIFT', [None, '%i', False, 'External fields: Apply VCONST only on selected atom.']),
            # accuracy
            ('LMAX', [None, '%i', True, 'Accuracy: Angular momentum cutoff']),
            ('BZDIVIDE', [
                None, '%i %i %i', False,
                'Accuracy: Maximal Brillouin zone mesh. Should not violate symmetry (e.g cubic symmetry implies i1=i2=i3; terragonal symmetry in xy implies i1=i2; i1=i2=i3 is always safe.)'
            ]),
            ('EMIN',
             [None, '%f', False, 'Accuracy, Valence energy contour: Lower value (in Ryd) for the energy contour']),
            ('EMAX', [
                None, '%f', False,
                'Accuracy, Valence energy contour: Maximum value (in Ryd) for the DOS calculation Controls also [NPT2] in some cases'
            ]),
            ('TEMPR', [None, '%f', False, 'Accuracy, Valence energy contour: Electronic temperature in K.']),
            ('NPT1', [
                None, '%i', False,
                'Accuracy, Valence energy contour: Number of energies in the 1st part of the rectangular contour ("going up").'
            ]),
            ('NPT2', [
                None, '%i', False,
                'Accuracy, Valence energy contour: Number of energies in the 2nd part of the rectangular contour ("going right").'
            ]),
            ('NPT3', [
                None, '%i', False,
                'Accuracy, Valence energy contour: Number of energies in the 3rd part of the rectangular contour (Fermi smearing part).'
            ]),
            ('NPOL', [
                None, '%i', False,
                'Accuracy, Valence energy contour: Number of Matsubara poles For DOS calculations, set [NPOL]=0'
            ]),
            ('EBOTSEMI', [None, '%f', False, 'Accuracy, Semicore energy contour: Bottom of semicore contour in Ryd.']),
            ('EMUSEMI', [None, '%f', False, 'Accuracy, Semicore energy contour: Top of semicore contour in Ryd.']),
            ('TKSEMI', [
                None, '%f', False,
                'Accuracy, Semicore energy contour: "Temperature" in K controlling height of semicore contour.'
            ]),
            ('NPOLSEMI', [
                None, '%i', False,
                'Accuracy, Semicore energy contour: Control of height of semicore contour: Im z = (2 * [NPOLSEMI] * pi * kB * [TKSEMI] ) with kB=0.6333659E-5'
            ]),
            ('N1SEMI', [
                None, '%i', False,
                'Accuracy, Semicore energy contour: Number of energies in first part of semicore contour ("going up").'
            ]),
            ('N2SEMI', [
                None, '%i', False,
                'Accuracy, Semicore energy contour: Number of energies in second part of semicore contour ("going right").'
            ]),
            ('N3SEMI', [
                None, '%i', False,
                'Accuracy, Semicore energy contour: Number of energies in third part of semicore contour ("going down").'
            ]),
            ('FSEMICORE', [
                None, '%f', False,
                'Accuracy, Semicore energy contour: Initial normalization factor for semicore states (approx. 1.).'
            ]),
            ('CPAINFO', [
                None, '%f %i', False,
                'Accuracy, CPA mode: CPA-error max. tolerance and max. number of CPA-cycle iterations.'
            ]),
            ('RCLUSTZ', [
                None, '%f', False,
                'Accuracy, Screening clusters: Radius of screening clusters in units of [ALATBASIS], default is 11 Bohr radii.'
            ]),
            ('RCLUSTXY', [
                None, '%f', False,
                'Accuracy, Screening clusters: If [RCLUSTXY] does not equal [RCLUSTZ] then cylindrical clusters are created with radius [RCLUSTXY] and height [RCLUSTZ].'
            ]),
            ('<RMTREF>', [
                None, '%f', False,
                'Accuracy, Screening clusters: Muffin tin radius in Bohr radii for each site forming screening clusters. Negative value signals automatic calculation by the code.'
            ]),
            ('NLEFTHOS', [
                None, '%i', False,
                'Accuracy, Screening clusters 2D mode: The vectors [<RBLEFT>] are repeated i=1,...,[NLEFTHOS] times, shifted by i*[ZPERIODL], for the later formation of screening clusters.'
            ]),
            ('<RMTREFL>', [
                None, '%f', False,
                'Accuracy, Screening clusters 2D mode: Muffin-tin radius in Bohr radii for each site forming screening clusters in the lower (=left) half-crystal. Negative value signals automatic calculation by the code.'
            ]),
            ('NRIGHTHO', [
                None, '%i', False,
                'Accuracy, Screening clusters 2D mode: The vectors [<RBRIGHT>] are repeated i=1,...,[NRIGHTHO] times, shifted by i*[ZPERIODR], for the later formation of screening clusters.'
            ]),
            ('<RMTREFR>', [
                None, '%f', False,
                'Accuracy, Screening clusters 2D mode: Muffin-tin radius in Bohr radii for each site forming screening clusters in the upper (=right) half-crystal. Negative value signals automatic calculation by the code.'
            ]),
            ('INS', [
                None, '%i', False,
                'Accuracy, Radial solver: Takes values 0 for ASA and 1 for full potential Must be 0 for Munich Dirac solver ([KREL]=2)'
            ]),
            ('ICST', [None, '%i', False, 'Accuracy, Radial solver: Number of iterations in the radial solver']),
            ('R_LOG', [
                None, '%f', False,
                'Accuracy, Radial solver: Radius up to which log-rule is used for interval width. Used in conjunction with runopt NEWSOSOL'
            ]),
            ('NPAN_LOG', [
                None, '%i', False,
                'Accuracy, Radial solver: Number of intervals from nucleus to [R_LOG] Used in conjunction with runopt NEWSOSOL'
            ]),
            ('NPAN_EQ', [
                None, '%i', False,
                'Accuracy, Radial solver: Number of intervals from [R_LOG] to muffin-tin radius Used in conjunction with runopt NEWSOSOL'
            ]),
            ('NCHEB', [
                None, '%i', False,
                'Accuracy, Radial solver: Number of Chebyshev polynomials per interval Used in conjunction with runopt NEWSOSOL'
            ]),
            ('<FPRADIUS>', [
                None, '%f', False,
                'Accuracy, Radial solver: Full potential limit per atom (in Bohr radii); at points closer to the nucleus, the potential is assumed spherical. Negative values indicate to use values from potential file. Values larger than the muffin tin indicate to use the muffin tin radius.'
            ]),
            ('RMAX', [
                None, '%f', True,
                'Accuracy, Ewald summation for Madelung potential: Max. radius in [ALATBASIS] for real space Ewald sum'
            ]),
            ('GMAX', [
                None, '%f', True,
                'Accuracy, Ewald summation for Madelung potential: Max. radius in 2*pi/[ALATBASIS] for reciprocal space Ewald sum'
            ]),
            ('<LLOYD>', [None, '%i', False, "Accuracy, LLoyd's formula: Set to 1 in order to use Lloyd's formula"]),
            ('<DELTAE>', [
                None, '(%f, %f)', False,
                "Accuracy, LLoyd's formula: Energy difference for derivative calculation in Lloyd's formula"
            ]),
            ('<TOLRDIF>', [
                None, '%e', False,
                'Accuracy, Virtual atoms: For distance between scattering-centers smaller than [<TOLRDIF>], free GF is set to zero. Units are Bohr radii.'
            ]),
            ('<RMTCORE>', [
                None, '%f', False,
                'Accuracy: Muffin tin radium in Bohr radii for each atom site. This sets the value of RMT used internally in the KKRcode. Needs to be smaller than the touching RMT of the cells. In particular for structure relaxations this should be kept constant.'
            ]),
            ('NMIN', [
                None, '%i', False,
                'Accuracy: Minimal number of point per shape function panel. Only used by voronoi code in shape function generation.'
            ]),
            ('POT_NS_CUTOFF', [
                None, '%f', False,
                'Accuracy: non-spherical cutoff for potential at the end of the iteration (defaults to 0.1*qbound if not set).'
            ]),
            # scf cycle
            ('NSTEPS', [
                None, '%i', False,
                'Self-consistency control: Max. number of self-consistency iterations. Is reset to 1 in several cases that require only 1 iteration (DOS, Jij, write out GF).'
            ]),
            ('IMIX', [
                None, '%i', False,
                "Self-consistency control: Mixing scheme for potential. 0 means straignt (linear) mixing, 3 means Broyden's 1st method, 4 means Broyden's 2nd method, 5 means Anderson's method"
            ]),
            ('STRMIX', [None, '%f', False, 'Self-consistency control: Linear mixing parameter Set to 0. if [NPOL]=0']),
            ('ITDBRY', [
                None, '%i', False,
                'Self-consistency control: how many iterations to keep in the Broyden/Anderson mixing scheme.'
            ]),
            ('FCM', [
                None, '%f', False,
                'Self-consistency control: Factor for increased linear mixing of magnetic part of potential compared to non-magnetic part.'
            ]),
            ('BRYMIX', [None, '%f', False, 'Self-consistency control: Parameter for Broyden mixing.']),
            ('QBOUND',
             [None, '%e', False,
              'Self-consistency control: Lower limit of rms-error in potential to stop iterations.']),
            ('NSIMPLEMIXFIRST', [
                None, '%i', False,
                'Self-consistency control: Number of simple mixing steps to do before starting more aggressive mixing scheme (only has effect for IMIX>3).'
            ]),
            ('DENEF_MIXSCALE', [
                None, '%f', False,
                'Self-consistency control: Inverse scaling factor for charge neutrality mixing, should nirmally be set to the value the denisty at EF (used only with semi-circle contour integration).'
            ]),
            # mixing of noco angles
            ('SPINMIXQBOUND', [
                None, '%e', False,
                'Self-consistency control: threshold in degrees after which the rms of the nonco angles a assumed to not change anymore (i.e. activate fixing of all angles simultaneously)'
            ]),
            ('SPINMIXALPHA', [None, '%e', False, 'Self-consistency control: Broyden mixing factor for nonco angles']),
            ('SPINMIXNSIMPLE', [
                None, '%i', False,
                'Self-consistency control: number of simple mixing steps before Broyden spinmixing starts ( should be >=1).'
            ]),
            ('SPINMIXMEMLEN', [None, '%i', False,
                               'Self-consistency control: Memory length of the Broyden spin mixing']),
            ('<WRITE_ANGLES_ALLITER>',
             [None, '%l', False, 'Self-consistency control: write out the nonco angles for all iterations']),
            ('<USE_BROYDEN_SPINMIX>',
             [None, '%l', False, 'Self-consistency control: Use Broyden mixing for nonco angles']),
            #code options
            ('RUNOPT', [
                None, '%s%s%s%s%s%s%s%s', False,
                'Running and test options: 8-character keywords in a row without spaces between them'
            ]),
            ('TESTOPT', [
                None, '%s%s%s%s%s%s%s%s\n%s%s%s%s%s%s%s%s', False,
                'Running and test options: optional 8-character keywords in a row without spaces between them plus a secod row of the same.'
            ]),
            ('<MPI_SCHEME>', [
                None, '%i', False,
                'Parallelization scheme (defaults to 0 which means auto parallelization, 1=atom, 2=energy parallelization preferred).'
            ]),
            #file names
            ('FILES', [
                None, '%s', False,
                'Filenames: Name of potential and shapefun file (list of two strings, empty string will set back to default of the one file that is supposed to be changed)'
            ]),
            ('DECIFILES', [
                None, '%s', False,
                'Filenames: Name of left and right decifiles (use "vaccum" name to inducate vacuum continuation)'
            ]),
            # special options
            ('JIJRAD', [
                None, '%f', False,
                'Exchange coupling: Radius in alat which defines the cutoff for calcultion of Jij pairs'
            ]),
            ('JIJRADXY',
             [None, '%f', False, 'Exchange coupling: use a cylindical cluster in which Jij pairs are searched for']),
            ('JIJSITEI', [
                None, '%i', False,
                'Exchange coupling: allow for the selection of specific sites in i in the unit cell, which should be considered in the calculation (default: all sites)'
            ]),
            ('JIJSITEJ', [
                None, '%i', False,
                'Exchange coupling: allow for the selection of specific sites in j in the unit cell, which should be considered in the calculation (default: all sites)'
            ]),
            ('EFSET',
             [None, '%f', False, 'Set Fermi level (in voronoi of the jellium starting potential) to this value.']),
            # Bogoliubov de Gennes mode:
            ('<USE_BDG>', [
                None, '%l', False,
                'Superconductivity: Activate Bogoliubov de Gennes (BdG) mode. Attention: needs Chebychev solver!'
            ]),
            ('<DELTA_BDG>',
             [None, '%f', False,
              'Superconductivity: Starting value of BdG coupling constant in Ry (defaults to 1e-4)']),
            ('<LAMBDA_BDG>',
             [None, '%f', False, 'Superconductivity: Electron-phonon coupling parameter in Ry (defaults to 1.0)']),
            ('<LM_SCALE_BDG>', [
                None, '%f', False,
                'Superconductivity: Scaling factor for lambda_BdG on some L channels (e.g. used to get more structure into BdG matrix. Defaults to 1.0)'
            ]),
            ('<AT_SCALE_BDG>', [
                None, '%f', False,
                'Superconductivity: Scaling factor for lambda_BdG (e.g. used to deactivate BdG coupling in some layers by setting the value to 0)'
            ]),
            ('<MIXFAC_BDG>', [
                None, '%f', False,
                'Superconductivity: Mixing factor used in the mixing of the BdG Delta (defaults to 0.1)'
            ]),
            ('<MIXFAC_BDG_BRY>', [
                None, '%f', False,
                'Superconductivity: Mixing factor used in the Broyden mixing of the BdG Delta (defaults to value of <MIXFAC_BDG>)'
            ]),
            ('<NINIT_BROYDEN_BDG>', [
                None, '%i', False,
                'Superconductivity: Number of simple mixing steps before Broyden for BdG Delta starts (defaults to 1).'
            ]),
            ('<MEMLEN_BROYDEN_BDG>',
             [None, '%i', False, 'Superconductivity: Memory length of Broyden mixing (defaults to 20)']),
            ('<TEMP_BDG>', [
                None, '%f', False,
                'Superconductivity: Smearing temperature for the calculation of the anomalous density (used to calculate Tc, defaults to 0).'
            ]),
            ('<USE_E_SYMM_BDG>', [
                None, '%l', False,
                'Superconductivity: Use only the ee block in the contour integration and mirror the results for the hh block (works only for Temp_BdG=0, defaults to False)'
            ]),
            ('<CUSTOM_TESTSTRING>',
             [None, '%s', False, 'Superconductivity: String input for some test options with BdG']),
            # misc
            ('IM_E_CIRC_MIN', [
                None, '%f', False,
                'Minimal imaginary part (for energy point closest to EF) in semi-circular contour (needs USE_SEMI_CIRCLE_CONTOUR to become active.'
            ]),
            ('MAX_NUM_KMESH', [
                None, '%i', False,
                'Maximal number of differet k-meshes used to coarsen the BZ integration at elevated imaginary parts of the energy.'
            ]),
            ('WFAC_RENORM', [
                None, '%f', False,
                'Renormalization factor for energy integration weights (can be used to shift the Fermi level around).'
            ]),
            # array dimensions
            ('NSHELD', [None, '%i', False, 'Array dimension: number of shells (default: 300)']),
            ('IEMXD', [None, '%i', False, 'Array dimension: number of energy points (default: 101)']),
            ('IRID', [None, '%i', False, 'Array dimension: number of radial points']),
            ('IPAND', [None, '%i', False, 'Array dimension: number of shapefunction panels']),
            ('NPRINCD',
             [None, '%i', False, 'Array dimension: number of layers in each principle layer (decimation technique).']),
            ('KPOIBZ', [None, '%i', False, 'Array dimension: Max number of k-points in IBZ']),
            ('NATOMIMPD', [None, '%i', False, 'Array dimension: needed for Jij']),
            # new style run options
            ('<CALC_GF_EFERMI>',
             [None, '%l', False, "Run option: calculation of cluster Green function at E Fermi (former: 'GF-EF')"]),
            ('<SET_CHEBY_NOSPEEDUP>', [
                None, '%l', False,
                "Run option: always calculate irregular solution in Chebychev solver (even if not needed) (former: 'norllsll')"
            ]),
            ('<SET_CHEBY_NOSOC>',
             [None, '%l', False, "Run option: set SOC strength to 0 for all atoms (former: 'NOSOC')"]),
            ('<DECOUPLE_SPIN_CHEBY>', [
                None, '%l', False,
                'Run option: decouple spin matrices in Chebychev solver neglecting SOC and for collinear calculations only'
            ]),
            ('<CALC_COMPLEX_BANDSTRUCTURE>',
             [None, '%l', False, "Run option: complex band structure (former: 'COMPLEX')"]),
            ('<CALC_EXCHANGE_COUPLINGS>',
             [None, '%l', False, "Run option: calculate magnetic exchange coupling parameters (former: 'XCPL')"]),
            ('<CALC_EXCHANGE_COUPLINGS_ENERGY>',
             [None, '%l', False, "Run option: write energy-resolved Jij-files also if npol/=0 (former: 'Jijenerg')"]),
            ('<CALC_GMAT_LM_FULL>', [
                None, '%l', False,
                "Run option: calculate all lm-lm components of systems greens function and store to file `gflle` (former: 'lmlm-dos')"
            ]),
            ('<DIRAC_SCALE_SPEEFOFLIGHT>',
             [None, '%l', False, "Run option: scale the speed of light for Dirac solver (former: 'CSCALE')"]),
            ('<DISABLE_CHARGE_NEUTRALITY>', [
                None, '%l', False,
                "Run option: no charge neutrailty required: leaving Fermi level unaffected (former: 'no-neutr')"
            ]),
            ('<DISABLE_PRINT_SERIALNUMBER>', [
                None, '%l', False,
                "Run option: deactivate writing of serial number and version information to files (for backwards compatibility) (former: 'noserial')"
            ]),
            ('<DISABLE_REFERENCE_SYSTEM>',
             [None, '%l', False, "Run option: deactivate the tight-binding reference system (former: 'lrefsysf')"]),
            ('<DISABLE_TMAT_SRATRICK>',
             [None, '%l', False, "Run option: deactivate SRATRICK in solver for t-matirx (former: 'nosph')"]),
            ('<FIX_NONCO_ANGLES>', [
                None, '%l', False,
                "Run option: fix direction of non-collinear magnetic moments (Chebychev solver) (former: 'FIXMOM')"
            ]),
            ('<FORMATTED_FILE>', [
                None, '%l', False,
                "Run option: write files ascii-format. only effective with some other write-options (former: 'fileverb')"
            ]),
            ('<FORCE_BZ_SYMM>', [
                None, '%l', False,
                'Run option: force using symmetries of the Brillouin zone (effective only for the Chebychev solver, should not be used with SOC!)'
            ]),
            ('<IMPURITY_OPERATOR_ONLY>', [
                None, '%l', False,
                "Run option: only for `write_pkkr_operators`: disable costly recalculation of host operators (former: 'IMP_ONLY')"
            ]),
            ('<MODIFY_SOC_DIRAC>', [None, '%l', False, "Run option: modify SOC for Dirac solver (former: 'SOC')"]),
            ('<NO_MADELUNG>', [
                None, '%l', False,
                "Run option: do not add some energy terms (coulomb, XC, eff. pot.) to total energy (former: 'NoMadel')"
            ]),
            ('<PRINT_GIJ>',
             [None, '%l', False, "Run option: print cluster G_ij matrices to outfile (former: 'Gmatij')"]),
            ('<PRINT_GMAT>', [None, '%l', False, "Run option: print Gmat to outfile (former: 'Gmat')"]),
            ('<PRINT_ICKECK>',
             [None, '%l', False, "Run option: enable test-output of ICHECK matrix from gfmask (former: 'ICHECK')"]),
            ('<PRINT_KMESH>', [None, '%l', False, "Run option: output of k-mesh (former: 'k-net')"]),
            ('<PRINT_KPOINTS>', [None, '%l', False, "Run option: print k-points to outfile (former: 'BZKP')"]),
            ('<PRINT_PROGRAM_FLOW>',
             [None, '%l', False, "Run option: monitor the program flow in some parts of the code (former: 'flow')"]),
            ('<PRINT_RADIAL_MESH>',
             [None, '%l', False, "Run option: write mesh information to output (former: 'RMESH')"]),
            ('<PRINT_REFPOT>', [None, '%l', False, "Run option: test output of refpot (former: 'REFPOT')"]),
            ('<PRINT_TAU_STRUCTURE>', [
                None, '%l', False,
                "Run option: write extensive information about k-mesh symmetrization and structure of site-diagonal tau matrices to output (former: 'TAUSTRUC')"
            ]),
            ('<PRINT_TMAT>', [None, '%l', False, "Run option: print t-matrix to outfile (former: 'tmat')"]),
            ('<RELAX_SPINANGLE_DIRAC>', [
                None, '%l', False,
                "Run option: relax the spin angle in a SCF calculation [only DIRAC mode] (former: 'ITERMDIR')"
            ]),
            ('<SEARCH_EFERMI>', [
                None, '%l', False,
                "Run option: modify convergence parameters to scan for fermi energy only (to reach charge neutrality). (former: 'SEARCHEF')"
            ]),
            ('<SET_GMAT_TO_ZERO>',
             [None, '%l', False, "Run option: set GMAT=0 in evaluation of density (former: 'GMAT=0')"]),
            ('<SET_EMPTY_SYSTEM>',
             [None, '%l', False, "Run option: set potential and nuclear charge to zero (former: 'zeropot')"]),
            ('<SET_KMESH_LARGE>',
             [None, '%l', False, "Run option: set equal k-mesh (largest) for all energy points (former: 'fix mesh')"]),
            ('<SET_KMESH_SMALL>',
             [None, '%l', False, "Run option: set equal k-mesh (smallest) for all energy points (former: 'fix4mesh')"]),
            ('<SET_TMAT_NOINVERSION>', [
                None, '%l', False,
                "Run option: do not perform inversion to get msst = Delta t^-1, but msst = Delta t. (former: 'testgmat')"
            ]),
            ('<SIMULATE_ASA>', [
                None, '%l', False,
                "Run option: set non-spherical potential to zero in full-potential calculation with Chebychev solver (former: 'simulasa')"
            ]),
            ('<SLOW_MIXING_EFERMI>', [
                None, '%l', False,
                "Run option: renormalize Fermi-energy shift by mixing factor during mixing (former: 'slow-neu')"
            ]),
            ('<STOP_1A>', [None, '%l', False, "Run option: stop after main1a (former: 'STOP1A')"]),
            ('<STOP_1B>', [None, '%l', False, "Run option: stop after main1b (former: 'STOP1B')"]),
            ('<STOP_1C>', [None, '%l', False, "Run option: stop after main1c (former: 'STOP1C')"]),
            ('<SYMMETRIZE_GMAT>',
             [None, '%l', False,
              "Run option: use symmetrization [G(k) + G(-k)]/2 in k-point loop (former: 'symG(k)')"]),
            ('<SYMMETRIZE_POTENTIAL_CUBIC>', [
                None, '%l', False,
                "Run option: keep only symmetric part of potential (L=1,11,21,25,43,47). (former: 'potcubic')"
            ]),
            ('<SYMMETRIZE_POTENTIAL_MADELUNG>', [
                None, '%l', False,
                "Run option: symmetrize potential in consistency to madelung potential (former: 'potsymm')"
            ]),
            ('<TORQUE_OPERATOR_ONLYMT>', [
                None, '%l', False,
                "Run option: for torque operator: include only the part within the muffin tin (former: 'ONLYMT')"
            ]),
            ('<TORQUE_OPERATOR_ONLYSPH>', [
                None, '%l', False,
                "Run option: for torque operator: include only the spherically symmetric part (former: 'ONLYSPH')"
            ]),
            ('<USE_CHEBYCHEV_SOLVER>', [None, '%l', False,
                                        "Run option: use the Chebychev solver (former: 'NEWSOSOL')"]),
            ('<USE_COND_LB>', [
                None, '%l', False,
                "Run option: perform calculation of conductance in Landauer-Büttiker formalism (former: 'CONDUCT')"
            ]),
            ('<USE_CONT>',
             [None, '%l', False, "Run option: no usage of embedding points. NEMB is set to 0. (former: 'CONT')"]),
            ('<USE_DECI_ONEBULK>', [
                None, '%l', False,
                "Run option: in case of decimation: use same bulk on right and left. Speeds up calculations. (former: 'ONEBULK')"
            ]),
            ('<USE_DECIMATION>',
             [None, '%l', False,
              "Run option: use Decimation technique for semi-infinite systems (former: 'DECIMATE')"]),
            ('<USE_EWALD_2D>', [
                None, '%l', False,
                "Run option: use 2D ewald sum instead of 3D sum (Attention: does not work always!) (former: 'ewald2d')"
            ]),
            ('<USE_FULL_BZ>', [
                None, '%l', False,
                "Run option: use full Brillouin zone, i.e. switch off symmetries for k-space integration (former: 'fullBZ')"
            ]),
            ('<USE_LDAU>',
             [None, '%l', False, "Run option: use LDA+U as exchange-correlation potential (former: 'LDA+U')"]),
            ('<USE_LLOYD>', [
                None, '%l', False,
                "Run option: use Lloyds formula to correct finite angular momentum cutoff (former: 'LLOYD')"
            ]),
            ('<USE_QDOS>',
             [None, '%l', False,
              "Run option: writes out qdos files for band structure calculations. (former: 'qdos')"]),
            ('<USE_READCPA>', [None, '%l', False, "Run option: read cpa t-matrix from file (former: 'readcpa')"]),
            ('<USE_RIGID_EFERMI>', [
                None, '%l', False,
                "Run option: keep the Fermi energy fixed during self-consistency (former: 'rigid-ef')"
            ]),
            ('<USE_SEMICORE>', [None, '%l', False, "Run option: use semicore contour (former: 'SEMICORE')"]),
            ('<USE_SEMI_CIRCLE_CONTOUR>',
             [None, '%l', False, 'Run option: use semi-circular energy contour (set number of points with NPT1)']),
            ('<USE_SPHERICAL_POTENTIAL_ONLY>',
             [None, '%l', False, "Run option: keeping only spherical component of potential (former: 'Vspher')"]),
            ('<USE_VIRTUAL_ATOMS>', [None, '%l', False, "Run option: add virtual atoms (former: 'VIRATOMS')"]),
            ('<WRITE_BDG_TESTS>',
             [None, '%l', False, "Run option: test options for Bogouliubov-deGennes (former: 'BdG_dev')"]),
            ('<WRITE_DOS>',
             [None, '%l', False, "Run option: write out DOS files in any case (also if npol!=0) (former: 'DOS')"]),
            ('<WRITE_DOS_LM>', [
                None, '%l', False,
                "Run option: write out DOS files with decomposition into l and m components (former: 'lmdos')"
            ]),
            ('<WRITE_GMAT_PLAIN>',
             [None, '%l', False, "Run option: write out Green function as plain text file (former: 'GPLAIN')"]),
            ('<WRITE_GREEN_HOST>', [
                None, '%l', False,
                "Run option: write green function of the host to file `green_host` (former: 'WRTGREEN')"
            ]),
            ('<WRITE_GREEN_IMP>',
             [None, '%l', False, "Run option: write out impurity Green function to GMATLL_GES (former: 'GREENIMP')"]),
            ('<WRITE_COMPLEX_QDOS>', [None, '%l', False,
                                      "Run option: write complex qdos to file (former: 'compqdos')"]),
            ('<WRITE_CPA_PROJECTION_FILE>',
             [None, '%l', False, "Run option: write CPA projectors to file (former: 'projfile')"]),
            ('<WRITE_DECI_POT>',
             [None, '%l', False, "Run option: write decimation-potential file (former: 'deci-pot')"]),
            ('<WRITE_DECI_TMAT>',
             [None, '%l', False, "Run option: write t-matrix to file 'decifile' (former: 'deci-out')"]),
            ('<WRITE_DENSITY_ASCII>',
             [None, '%l', False, "Run option: write density rho2ns to file densitydn.ascii (former: 'den-asci')"]),
            ('<WRITE_ENERGY_MESH>',
             [None, '%l', False, "Run option: write out the energy mesh to file `emesh.scf` (former: 'EMESH')"]),
            ('<WRITE_GENERALIZED_POTENTIAL>', [
                None, '%l', False,
                "Run option: write potential in general format. Usually prepares for running the VORONOI program. (former: 'GENPOT')"
            ]),
            ('<WRITE_GMAT_FILE>', [None, '%l', False, "Run option: write GMAT to file (former: 'gmatfile')"]),
            ('<WRITE_GREF_FILE>', [None, '%l', False, "Run option: write GREF to file (former: 'greffile')"]),
            ('<WRITE_GMAT_ASCII>',
             [None, '%l', False, "Run option: write GMAT to formatted file `gmat.ascii` (former: 'gmatasci')"]),
            ('<WRITE_KKRIMP_INPUT>',
             [None, '%l', False, "Run option: write out files for KKRimp-code (former: 'KKRFLEX')"]),
            ('<WRITE_KKRSUSC_INPUT>',
             [None, '%l', False, "Run option: write out files for KKRsusc-code (former: 'KKRSUSC')"]),
            ('<WRITE_KPTS_FILE>',
             [None, '%l', False, "Run option: write and read k-mesh to/from file `kpoints` (former: 'kptsfile')"]),
            ('<WRITE_LLOYD_CDOS_FILE>',
             [None, '%l', False, "Run option: write Lloyd array to file  (former: 'wrtcdos')"]),
            ('<WRITE_LLOYD_DGREF_FILE>',
             [None, '%l', False, "Run option: write Lloyd array to file  (former: 'wrtdgref')"]),
            ('<WRITE_LLOYD_DTMAT_FILE>',
             [None, '%l', False, "Run option: write Lloyd array to file  (former: 'wrtdtmat')"]),
            ('<WRITE_LLOYD_FILE>',
             [None, '%l', False, "Run option: write several Lloyd-arrays to files (former: 'llyfiles')"]),
            ('<WRITE_LLOYD_G0TR_FILE>',
             [None, '%l', False, "Run option: write Lloyd array to file  (former: 'wrtgotr')"]),
            ('<WRITE_LLOYD_TRALPHA_FILE>',
             [None, '%l', False, "Run option: write Lloyd array to file  (former: 'wrttral')"]),
            ('<WRITE_MADELUNG_FILE>', [
                None, '%l', False,
                "Run option: write madelung summation to file 'abvmad.unformatted' instead of keeping it in memory (former: 'madelfil')"
            ]),
            ('<WRITE_PKKR_INPUT>',
             [None, '%l', False, "Run option: write out files for Pkkprime-code (former: 'FERMIOUT')"]),
            ('<WRITE_PKKR_OPERATORS>', [
                None, '%l', False,
                "Run option: for Fermi-surface output: calculate various operators in KKR basis. (former: 'OPERATOR')"
            ]),
            ('<WRITE_POTENTIAL_TESTS>', [
                None, '%l', False,
                "Run option: write potential at different steps in main2 to different files (former: 'vintrasp' and 'vpotout')"
            ]),
            ('<WRITE_RHO2NS>', [
                None, '%l', False,
                "Run option: write array rho2ns into file out_rhoval (from main1c) and out_rhotot (from main2) (former: 'RHOVALTW' and 'RHOVALW')"
            ]),
            ('<WRITE_RHOQ_INPUT>', [
                None, '%l', False,
                "Run option: write out files needed for rhoq module (Quasiparticle interference) (former: 'rhoqtest')"
            ]),
            ('<WRITE_TMAT_FILE>', [None, '%l', False, "Run option: write t-matix to file (former: 'tmatfile')"]),
            ('<WRITE_TB_COUPLING>', [
                None, '%l', False,
                "Run option: write couplings in tight-binging reference system to file `couplings.dat` (former: 'godfrin')"
            ]),
            ('<CALC_WRONSKIAN>', [
                None, '%l', False,
                'Run option: calculate the wronskian relations of first and second kind for the wavefunctions (see PhD Bauer pp 48)'
            ]),
            # end new style run options
        ])

        # keywords for KKRimp (all allowed settings for config file)
        self._DEFAULT_KEYS_KKRIMP = dict([  # complete list of keywords, detault all that are not mandatory to None
            # chemistry
            ('NSPIN',
             [None, '%i', False, 'Chemistry, Atom types: Number of spin directions in potential. Values 1 or 2']),
            ('KVREL', [
                None, '%i', False,
                'Chemistry, Atom types: Relativistic treatment of valence electrons. Takes values 0 (Schroedinger), 1 (Scalar relativistic), 2 (Dirac ; works only in ASA mode)'
            ]),
            ('XC', [
                None, '%s', False,
                'Chemistry, Exchange-correlation: Type of exchange correlation potential. Takes values 0 (LDA, Moruzzi-Janak-Williams), 1 (LDA, von Barth-Hedin), 2 (LDA, Vosko-Wilk-Nussair), 3 (GGA, Perdew-Wang 91), 4 (GGA, PBE), 5 (GGA, PBEsol)'
            ]),
            # external fields
            ('HFIELD', [
                None, '%f %i', False,
                'External fields: Value of an external magnetic field in the first iteration. Works only with LINIPOL, XINIPOL'
            ]),
            # accuracy
            ('INS', [
                None, '%i', False,
                'Accuracy, Radial solver: Takes values 0 for ASA and 1 for full potential Must be 0 for Munich Dirac solver ([KREL]=2)'
            ]),
            ('ICST', [None, '%i', False, 'Accuracy, Radial solver: Number of iterations in the radial solver']),
            ('RADIUS_LOGPANELS', [
                None, '%f', False,
                'Accuracy, Radial solver: Radius up to which log-rule is used for interval width. Used in conjunction with runopt NEWSOSOL'
            ]),
            ('NPAN_LOG', [
                None, '%i', False,
                'Accuracy, Radial solver: Number of intervals from nucleus to [R_LOG] Used in conjunction with runopt NEWSOSOL'
            ]),
            ('NPAN_EQ', [
                None, '%i', False,
                'Accuracy, Radial solver: Number of intervals from [R_LOG] to muffin-tin radius Used in conjunction with runopt NEWSOSOL'
            ]),
            ('NCHEB', [
                None, '%i', False,
                'Accuracy, Radial solver: Number of Chebyshev polynomials per interval Used in conjunction with runopt NEWSOSOL'
            ]),
            ('NPAN_LOGPANELFAC', [None, '%i', False, 'Accuracy, Radial solver: division factor logpanel']),
            ('RADIUS_MIN', [None, '%i', False, 'Accuracy, Radial solver: ']),
            ('NCOLL', [None, '%i', False, 'Accuracy, Radial solver: use nonco_angles solver (1/0)']),
            ('SPINORBIT', [None, '%i', False, 'Accuracy, Radial solver: use SOC solver (1/0)']),
            # scf cycle
            ('SCFSTEPS', [
                None, '%i', False,
                'Self-consistency control: Max. number of self-consistency iterations. Is reset to 1 in several cases that require only 1 iteration (DOS, Jij, write out GF).'
            ]),
            ('IMIX', [
                None, '%i', False,
                "Self-consistency control: Mixing scheme for potential. 0 means straignt (linear) mixing, 3 means Broyden's 1st method, 4 means Broyden's 2nd method, 5 means Anderson's method"
            ]),
            ('IMIXSPIN', [
                None, '%i', False,
                'Self-consistency control: Mixing scheme for magnetic moments. 0 means straignt (linear) mixing, >1 means Broyden mixing for spin moment directions.'
            ]),
            ('MIXFAC', [None, '%f', False, 'Self-consistency control: Linear mixing parameter Set to 0. if [NPOL]=0']),
            ('ITDBRY', [
                None, '%i', False,
                'Self-consistency control: how many iterations to keep in the Broyden/Anderson mixing scheme.'
            ]),
            ('BRYMIX', [None, '%f', False, 'Self-consistency control: Parameter for Broyden mixing.']),
            ('QBOUND',
             [None, '%e', False,
              'Self-consistency control: Lower limit of rms-error in potential to stop iterations.']),
            ('QBOUND_LDAU',
             [None, '%e', False, 'Self-consistency control: Lower limit of rms-error for LDA+U potential.']),
            ('NSIMPLEMIXFIRST', [
                None, '%i', False,
                'Self-consistency control: Number of simple mixing steps to do before starting more aggressive mixing scheme (only has effect for IMIX>3).'
            ]),
            #code options
            ('RUNFLAG', [None, '%s', False, 'Running and test options: e.g. lmdos, GBULKtomemory, LDA+U, SIMULASA']),
            ('TESTFLAG', [None, '%s', False, 'Running and test options: e.g. tmatnew, noscatteringmoment']),
            ('CALCFORCE', [None, '%i', False, 'Calculate forces']),
            ('CALCJIJMAT', [None, '%i', False, 'Calculate Jijmatrix']),
            ('CALCORBITALMOMENT', [None, '%i', False, 'Calculate orbital moment (SOC solver only, 0/1)']),
        ])

        if 'params_type' in kwargs:
            self.__params_type = kwargs.pop('params_type')
        else:
            #parameter are set for kkr or voronoi code? (changes mandatory flags)
            self.__params_type = 'kkr'  #default value, also possible: 'voronoi', 'kkrimp'
        valid_types = ['kkr', 'voronoi', 'kkrimp']
        if self.__params_type not in valid_types:
            raise ValueError(f'params_type can only be one of {valid_types} but got {self.__params_type}')

        # initialize keywords dict
        if self.__params_type == 'kkrimp':
            keyw = self._create_keywords_dict_kkrimp(**kwargs)
        else:
            keyw = self._create_keywords_dict(**kwargs)

        #values of keywords:
        self.values = {}
        #formatting info
        self.__format = {}
        #mandatory flag
        self._mandatory = {}
        # description of each key
        self.__description = {}

        for key in keyw:
            self.values[key] = keyw[key][0]
            self.__format[key] = keyw[key][1]
            self._mandatory[key] = keyw[key][2]
            self.__description[key] = keyw[key][3]

        # update mandatory set for voronoi, kkrimp cases
        self._update_mandatory()

    @classmethod
    def get_KKRcalc_parameter_defaults(self, silent=False):
        """
        set defaults (defined in header of this file) and returns dict, kkrparams_version
        """
        p = kkrparams()
        for key, val in list(__kkr_default_params__.items()):
            p.set_value(key, val, silent=silent)
        return dict(p.get_set_values()), __version__

    def get_dict(self, group=None, subgroup=None):
        """
        Returns values dictionary.

        Prints values belonging to a certain group only if the 'group' argument
        is one of the following: 'lattice', 'chemistry', 'accuracy',
        'external fields', 'scf cycle', 'other'

        Additionally the subgroups argument allows to print only a subset of
        all keys in a certain group. The following subgroups are available.

        - in 'lattice' group  '2D mode', 'shape functions'
        - in 'chemistry' group 'Atom types', 'Exchange-correlation', 'CPA mode', '2D mode'
        - in 'accuracy' group  'Valence energy contour', 'Semicore energy contour',
          'CPA mode', 'Screening clusters', 'Radial solver',
          'Ewald summation', 'LLoyd'

        """
        out_dict = self.values

        #check for grouping
        group_searchstrings = {
            'lattice': 'Description of lattice',
            'chemistry': 'Chemistry',
            'external fields': 'External fields:',
            'accuracy': 'Accuracy',
            'scf cycle': 'Self-consistency control:',
            'other': ['Running and test options', 'Name of potential and shapefun file']
        }
        subgroups_all = {
            'lattice': ['2D mode', 'shape functions'],
            'chemistry': ['Atom types', 'Exchange-correlation', 'CPA mode', '2D mode'],
            'accuracy': [
                'Valence energy contour', 'Semicore energy contour', 'CPA mode', 'Screening clusters', 'Radial solver',
                'Ewald summation', 'LLoyd'
            ]
        }
        if group in ['lattice', 'chemistry', 'accuracy', 'external fields', 'scf cycle', 'other']:
            print(f'Returning only values belonging to group {group}')
            tmp_dict = {}
            for key in list(out_dict.keys()):
                desc = self.__description[key]
                key_in_group = False
                if group_searchstrings[group] != 'other':
                    if group_searchstrings[group] in desc:
                        key_in_group = True
                else:
                    if group_searchstrings[group][0] in desc or group_searchstrings[group][1] in desc:
                        key_in_group = True
                if key_in_group:
                    tmp_dict[key] = self.values[key]

            #check for subgrouping and overwrite tmp_dict accordingly
            if group in ['lattice', 'chemistry', 'accuracy']:
                if subgroup in subgroups_all[group]:
                    print(f'Restrict keys additionally to subgroup {subgroup}')
                    tmp_dict2 = {}
                    for key in list(tmp_dict.keys()):
                        desc = self.__description[key]
                        key_in_group = False
                        if subgroup in desc:
                            key_in_group = True
                            if key_in_group:
                                tmp_dict2[key] = self.values[key]
                    tmp_dict = tmp_dict2

            # overwrite out_dict with tmp_dict
            out_dict = tmp_dict

        return out_dict

    def _get_type_from_string(self, fmtstr):
        """Helper function of get_type"""
        if 'f' in fmtstr or 'e' in fmtstr:
            keytype = float
        elif 'i' in fmtstr:
            keytype = int
        elif 'l' in fmtstr:
            keytype = bool
        elif 's' in fmtstr:
            keytype = str
        else:
            print('Error: type of keyvalue not found:', fmtstr)
            raise TypeError(f'Type not found for format string: {fmtstr}')
        return keytype

    def get_type(self, key):
        """Extract expected type of 'key' from format info"""
        try:
            fmtstr = self.__format[key]
        except KeyError:
            fmtstr = None
        if fmtstr is not None:
            # simple format or complex pattern
            simplefmt = True
            if fmtstr.count('%') > 1:
                simplefmt = False
            if simplefmt:
                keytype = self._get_type_from_string(fmtstr)
            else:
                fmtlist = fmtstr.replace('\n', '').replace(' ', '').split('%')[1:]
                keytype = []
                for fmtstr in fmtlist:
                    keytype.append(self._get_type_from_string(fmtstr))
            return keytype
        else:
            return None

    def _check_valuetype(self, key):
        """Consistency check if type of value matches expected type from format info"""

        # this is the type which is expected
        cmptypes = self.get_type(key)

        # check if entry is numpy array and change to list automatically:
        try:
            tmpval = self.values[key].flatten().tolist()
        except:
            tmpval = self.values[key]
        tmptype = type(tmpval)

        # get type of value
        if tmptype == list:
            valtype = []
            for val in range(len(tmpval)):
                if cmptypes == str:
                    tmpval[val] = str(tmpval[val])  # for pytho2/3 compatibility
                valtype.append(type(tmpval[val]))
        else:
            if cmptypes == str:
                tmpval = str(tmpval)  # for pytho2/3 compatibility
                tmptype = type(tmpval)
            valtype = tmptype
        #print(key, valtype, self.get_type(key))

        # check if type matches format info
        success = True
        if cmptypes is not None:
            #print(key, type(valtype), valtype, cmptypes)
            changed_type_automatically = False
            if valtype == int and cmptypes == float:
                changed_type_automatically = True
                self.values[key] = float(self.values[key])
            elif type(valtype) == list:
                for ival in range(len(valtype)):
                    if valtype[ival] == int and cmptypes == float:
                        changed_type_automatically = True
                        self.values[key][ival] = float(self.values[key][ival])
            elif valtype != cmptypes and tmpval is not None:
                success = False
                print('Error: type of value does not match expected type for ', key, self.values[key], cmptypes,
                      type(self.values[key]), valtype)
                raise TypeError(
                    'type of value does not match expected type for key={}; value={}; expected type={}; got type={}'.
                    format(key, self.values[key], cmptypes, type(self.values[key])))

            if changed_type_automatically:
                print(
                    'Warning: filling value of "%s" with integer but expects float. Converting automatically and continue'
                    % key)

        return success

    def get_value(self, key):
        """Gets value of keyword 'key'"""
        if key not in list(self.values.keys()):
            print(f'Error key ({key}) not found in values dict! {self.values}')
            raise KeyError
        else:
            # deal with special cases of runopt and testopt (lists of codewords)
            if key in ['RUNOPT', 'TESTOPT'] and self.values[key] is None:
                return []
            else:
                return self.values[key]

    def set_value(self, key, value, silent=False):
        """Sets value of keyword 'key'"""
        if value is None:
            if not silent:
                print('Warning setting value None is not permitted!')
                print(f'Use remove_value funciton instead! Ignore keyword {key}')
        else:
            key = key.upper()  # make case insensitive
            if self.__params_type == 'kkrimp' and key == 'XC':
                value = self.change_XC_val_kkrimp(value)
            self.values[key] = value
            self._check_valuetype(key)

    def remove_value(self, key):
        """Removes value of keyword 'key', i.e. resets to None"""
        self.values[key] = None

    def set_multiple_values(self, **kwargs):
        """Set multiple values (in example value1 and value2 of keywords 'key1' and 'key2') given as key1=value1, key2=value2"""
        for key in kwargs:
            key2 = self._add_brackets_to_key(key, self.values)
            #print('setting', key2, kwargs[key])
            self.set_value(key2, kwargs[key])

    def get_set_values(self):
        """Return a list of all keys/values that are set (i.e. not None)"""
        set_values = []
        added = 0
        for key in list(self.values.keys()):
            if self.values[key] is not None:
                set_values.append([key, self.values[key]])
                added += 1
        if added == 0:
            print('No values set')
        return set_values

    def get_all_mandatory(self):
        """Return a list of mandatory keys"""
        self._update_mandatory()
        mandatory_list = []
        for key in list(self.values.keys()):
            if self.is_mandatory(key):
                mandatory_list.append(key)
        return mandatory_list

    def is_mandatory(self, key):
        """Returns mandatory flag (True/False) for keyword 'key'"""
        return self._mandatory[key]

    def get_description(self, key=None, search=None):
        """
        Returns description of keyword 'key'
        If 'key' is None, print all descriptions of all available keywords
        If 'search' is not None, print all keys+descriptions where the search string is found
        """
        if key is not None:
            return self.__description[key]
        for key in self.values.keys():
            if search is None or search.lower() in key.lower() or search.lower() in self.__description[key].lower():
                print(f'{key:25}', self.__description[key])

    def _create_keywords_dict(self, **kwargs):
        """
        Creates KKR inputcard keywords dictionary and fills entry if value is given in **kwargs

        entries of keyword dictionary are: 'keyword', [value, format, keyword_mandatory, description]

        where

        - 'value' can be a single entry or a list of entries
        - 'format' contains formatting info
        - 'keyword_mandatory' is a logical stating if keyword needs to be defined to run a calculation
        - 'description' is a string containing human redable info about the keyword
        """

        default_keywords = self._DEFAULT_KEYWORDS_KKR

        for key in kwargs:
            key2 = self._add_brackets_to_key(key, default_keywords)
            val = kwargs[key]
            if self.__params_type == 'kkrimp':
                if key == 'KEXCORE':
                    key2 = 'XC'
                if key == 'R_LOG':
                    key2 = 'RADIUS_LOGPANELS'
                if key == 'STRMIX':
                    key2 = 'MIXFAC'
                if key == 'RUNOPT':
                    key2 = 'RUNFLAG'
                if key == 'TESTOPT':
                    key2 = 'TESTFLAG'
                if key == 'NSTEPS':
                    key2 = 'SCFSTEPS'
            # workaround to fix inconsistency of XC input between host and impurity code
            if self.__params_type == 'kkrimp' and key2 == 'XC':
                val = self.change_XC_val_kkrimp(val)
                kwargs[key] = val
            default_keywords[key2][0] = val

        return default_keywords

    def _update_mandatory(self):
        """Check if mandatory flags need to be updated if certain keywords are set"""
        # initialize all mandatory flags to False and update list afterwards
        for key in list(self.values.keys()):
            self._mandatory[key] = False

        runopts = []
        if self.values.get('RUNOPT', None) is not None:
            for runopt in self.values['RUNOPT']:
                runopts.append(runopt.strip())

        #For a KKR calculation these keywords are always mandatory:
        mandatory_list = ['ALATBASIS', 'BRAVAIS', 'NAEZ', '<RBASIS>', 'NSPIN', 'LMAX', 'RMAX', 'GMAX', '<ZATOM>']

        if self.values.get('NPOL', None) is not None and self.values['NPOL'] != 0:
            mandatory_list += ['EMIN']
        #Mandatory in 2D
        if self.values.get('INTERFACE', None):
            mandatory_list += ['<NLBASIS>', '<RBLEFT>', 'ZPERIODL', '<NRBASIS>', '<RBRIGHT>', 'ZPERIODR']
        #Mandatory in LDA+U
        if 'NAT_LDAU' in list(self.values.keys()) and 'LDAU' in runopts:
            mandatory_list += ['NAT_LDAU', 'LDAU_PARA']
        #Mandatory in CPA
        if self.values.get('NATYP', None) is not None and self.values['NATYP'] > self.values['NAEZ']:
            mandatory_list += ['NATYP', '<SITE>', '<CPA-CONC>']
        #Mandatory in SEMICORE
        if 'EBOTSEMI' in list(self.values.keys()) and 'SEMICORE' in runopts:
            mandatory_list += ['EBOTSEMI', 'EMUSEMI', 'TKSEMI', 'NPOLSEMI', 'N1SEMI', 'N2SEMI', 'N3SEMI', 'FSEMICORE']
        if self.values['INS'] == 1 and 'WRITEALL' not in runopts:
            mandatory_list += ['<SHAPE>']

        for key in mandatory_list:
            self._mandatory[key] = True

        # overwrite if mandatory list needs to be changed (determinded from value of self.__params_type):
        if self.__params_type == 'voronoi':
            self._update_mandatory_voronoi()
        if self.__params_type == 'kkrimp':
            self._update_mandatory_kkrimp()

    def _check_mandatory(self):
        """Check if all mandatory keywords are set"""
        self._update_mandatory()
        for key in list(self.values.keys()):
            if self._mandatory[key] and self.values[key] is None:
                print('Error not all mandatory keys are set!')
                set_of_mandatory = set(self.get_all_mandatory())
                set_of_keys = set([key[0] for key in self.get_set_values()])
                print(set_of_mandatory - set_of_keys, 'missing')
                raise ValueError(f'Missing mandatory key(s): {set_of_mandatory - set_of_keys}')

    def _check_array_consistency(self):
        """Check all keys in __listargs if they match their specification (mostly 1D array, except for special cases e.g. <RBASIS>)"""
        from numpy import array, ndarray

        vec3_entries = ['<RBASIS>', '<RBLEFT>', '<RBRIGHT>', 'ZPERIODL', 'ZPERIODR']

        #success = [True]
        for key in list(self.__listargs.keys()):
            if self.values[key] is not None:
                tmpsuccess = True
                #print('checking', key, self.values[key], self.__listargs[key])
                if type(self.values[key]) not in [list, ndarray]:
                    self.values[key] = array([self.values[key]])
                cmpdims = (self.__listargs[key],)
                if key in vec3_entries:
                    cmpdims = (self.__listargs[key], 3)
                    # automatically convert if naez==1 and only 1D array is given
                    if self.__listargs[key] == 1 and len(array(
                            self.values[key]).shape) == 1 and key not in ['ZPERIODL', 'ZPERIODR']:
                        print(f'Warning: expected 2D array for {key} but got 1D array, converting automatically')
                        self.values[key] = array([self.values[key]])
                tmpdims = array(self.values[key]).shape
                if tmpdims[0] != cmpdims[0]:
                    tmpsuccess = False
                if len(tmpdims) == 2 and tmpdims[1] != cmpdims[1]:
                    tmpsuccess = False
                #success.append(tmpsuccess)

                if not tmpsuccess:
                    print('check consistency:', key, self.values[key], cmpdims, tmpdims, tmpsuccess)
                    raise TypeError(f'Error: array input not consistent for key {key}')

    def _check_input_consistency(self, set_lists_only=False, verbose=False):
        """Check consistency of input, to be done before wrinting to inputcard"""
        from numpy import array

        # first check if all mandatory values are there
        if not set_lists_only:
            self._check_mandatory()

        # lists of array arguments
        if self.__params_type != 'kkrimp':
            keywords = self.values
            naez = keywords['NAEZ']
            if keywords['NATYP'] is not None:
                natyp = keywords['NATYP']
            else:
                natyp = keywords['NAEZ']
            if keywords['<NLBASIS>'] is not None:
                nlbasis = keywords['<NLBASIS>']
            else:
                nlbasis = 1
            if keywords['<NRBASIS>'] is not None:
                nrbasis = keywords['<NRBASIS>']
            else:
                nrbasis = 1
            lmax = keywords['LMAX']

            listargs = dict([['<RBASIS>', naez], ['<RBLEFT>', nlbasis], ['<RBRIGHT>', nrbasis], ['<SHAPE>', natyp],
                             ['<ZATOM>', natyp], ['<SOCSCL>', natyp], ['<SITE>', natyp], ['<CPA-CONC>', natyp],
                             ['<KAOEZL>', nlbasis], ['<KAOEZR>', nrbasis], ['XINIPOL', natyp], ['<RMTREF>', natyp],
                             ['<RMTREFL>', nlbasis], ['<RMTREFR>', nrbasis], ['<FPRADIUS>', natyp], ['BZDIVIDE', 3],
                             ['<RBLEFT>', nrbasis], ['ZPERIODL', 3], ['<RBRIGHT>', nrbasis], ['ZPERIODR', 3],
                             ['LDAU_PARA', 5], ['CPAINFO', 2], ['<DELTAE>', 2], ['FILES', 2], ['DECIFILES', 2],
                             ['<RMTCORE>', naez], ['<AT_SCALE_BDG>', natyp], ['<LM_SCALE_BDG>', (lmax + 1)**2]])
            # deal with special stuff for voronoi:
            if self.__params_type == 'voronoi':
                listargs['<RMTCORE>'] = naez
                self.update_to_voronoi()
            special_formatting = ['BRAVAIS', 'RUNOPT', 'TESTOPT', 'FILES', 'DECIFILES', 'JIJSITEI', 'JIJSITEJ']
        else:
            special_formatting = ['RUNFLAG', 'TESTFLAG']
            listargs = dict([['HFIELD', 2]])

        self.__special_formatting = special_formatting
        self.__listargs = listargs

        # ruturn after setting __special_formatting and __listargs lists
        if set_lists_only:
            return

        # check for consistency of array arguments
        self._check_array_consistency()

        if self.__params_type != 'kkrimp':
            # some special checks
            bulkmode = False
            set_values = [key[0] for key in self.get_set_values()]
            if 'INTERFACE' not in set_values or self.values['INTERFACE']:
                bulkmode = True

            bravais = array(self.values['BRAVAIS'])
            if bulkmode and sum(bravais[2]**2) == 0:
                print("Error: 'BRAVAIS' matches 2D calculation but 'INTERFACE' is not set to True!")
                raise ValueError

            # check if KSHAPE and INS are consistent and add missing values automatically
            # WARNING: KSHAPE should be 2*INS !!!
            if 'INS' not in set_values and 'KSHAPE' in set_values:
                self.set_value('INS', self.get_value('KSHAPE') // 2)
                print(f"setting INS automatically with KSHAPE value ({self.get_value('KSHAPE') // 2})")
            elif 'INS' in set_values and 'KSHAPE' not in set_values:
                self.set_value('KSHAPE', self.get_value('INS') * 2)
                print(f"setting KSHAPE automatically with INS value ({self.get_value('INS') * 2})")
            elif 'INS' in set_values and 'KSHAPE' in set_values:
                ins = self.get_value('INS')
                kshape = self.get_value('KSHAPE')
                if (ins != 0 and kshape == 0) or (ins == 0 and kshape != 0):
                    print(
                        "Error: values of 'INS' and 'KSHAPE' are both found but are inconsistent (should be 0/0 or 1/2)"
                    )
                    raise ValueError('INS,KSHAPE mismatch')

    def fill_keywords_to_inputfile(self, is_voro_calc=False, output='inputcard', no_check=False, verbose=False):
        """
        Fill new inputcard with keywords/values
        automatically check for input consistency (can be disabled by the no_check input)
        if is_voro_calc==True change mandatory list to match voronoi code, default is KKRcode
        """
        from numpy import array

        # first check input consistency
        if is_voro_calc:
            self.__params_type = 'voronoi'

        # check for inconsistencies in input before writing file
        self._check_input_consistency(set_lists_only=no_check)

        #rename for easy reference
        keywords = self.values
        keyfmts = self.__format

        if self.__params_type != 'kkrimp':
            sorted_keylist = [  #run/testopts
                'RUNOPT',
                'TESTOPT',
                #lattice:
                'ALATBASIS',
                'BRAVAIS',
                'NAEZ',
                'CARTESIAN',
                '<RBASIS>',
                'INTERFACE',
                '<NLBASIS>',
                '<RBLEFT>',
                'ZPERIODL',
                '<NRBASIS>',
                '<RBRIGHT>',
                'ZPERIODR',
                'KSHAPE',
                '<SHAPE>',
                # chemistry
                'NSPIN',
                'KVREL',
                'KEXCOR',
                'LAMBDA_XC',
                'NAT_LDAU',
                'LDAU_PARA',
                'KREADLDAU',
                '<ZATOM>',
                '<SOCSCL>',
                'NATYP',
                '<SITE>',
                '<CPA-CONC>',
                '<KAOEZL>',
                '<KAOEZR>',
                # external fields
                'LINIPOL',
                'HFIELD',
                'XINIPOL',
                'VCONST',
                # accuracy
                'LMAX',
                'BZDIVIDE',
                'EMIN',
                'EMAX',
                'TEMPR',
                'NPT1',
                'NPT2',
                'NPT3',
                'NPOL',
                'EBOTSEMI',
                'EMUSEMI',
                'TKSEMI',
                'NPOLSEMI',
                'N1SEMI',
                'N2SEMI',
                'N3SEMI',
                'FSEMICORE',
                'CPAINFO',
                'RCLUSTZ',
                'RCLUSTXY',
                '<RMTREF>',
                'NLEFTHOS',
                '<RMTREFL>',
                'NRIGHTHO',
                '<RMTREFR>',
                'INS',
                'ICST',
                'R_LOG',
                'NPAN_LOG',
                'NPAN_EQ',
                'NCHEB',
                '<FPRADIUS>',
                'RMAX',
                'GMAX',
                '<LLOYD>',
                '<DELTAE>',
                '<TOLRDIF>',
                # scf cycle
                'NSTEPS',
                'IMIX',
                'STRMIX',
                'ITDBRY',
                'FCM',
                'BRYMIX',
                'QBOUND',
                #file names
                'FILES',
                'DECIFILES'
            ]
        else:
            sorted_keylist = [
                'RUNFLAG', 'TESTFLAG', 'INS', 'KVREL', 'NSPIN', 'SCFSTEPS', 'IMIX', 'ITDBRY', 'MIXFAC', 'BRYMIX',
                'QBOUND', 'XC', 'ICST', 'SPINORBIT', 'NCOLL', 'NPAN_LOGPANELFAC', 'RADIUS_LOGPANELS', 'RADIUS_MIN',
                'NPAN_LOG', 'NPAN_EQ', 'NCHEB', 'HFIELD', 'CALCORBITALMOMENT', 'CALCFORCE', 'CALCJIJMAT'
            ]

        #add everything that was forgotten in sorted_keylist above
        for key in list(keywords.keys()):
            if key not in sorted_keylist:
                sorted_keylist += [key]

        # set accuracy of float writeouts
        # ensure high enough precision in inputcard writeout, limit to 12 places everything else is overkill
        for key in list(keyfmts.keys()):
            keyfmts[key] = keyfmts[key].replace('%f', '%21.12f')

        # write all set keys to file
        tmpl = ''
        for key in sorted_keylist:
            if keywords[key] is not None:
                if verbose:
                    print('writing', key, keywords[key])
                # go through different formatting options (first normal case then special cases)
                if (not key in list(self.__listargs.keys())) and (not key in self.__special_formatting):
                    tmpfmt = (keyfmts[key]).replace('%l', '%s')
                    try:
                        if self.__params_type == 'kkrimp' and key == 'XC':
                            # workaround to fix inconsistency of XC input between host and impurity code
                            keywords[key] = self.change_XC_val_kkrimp(keywords[key])
                        repltxt = tmpfmt % (keywords[key])
                    except:
                        #print(key, tmpfmt, keywords[key])
                        repltxt = ''
                        for i in range(len(tmpfmt)):
                            repltxt += ' ' + tmpfmt[i] % (keywords[key][i])
                    tmpl += f'{key}= {repltxt}\n'
                elif key == 'BRAVAIS':
                    self.values[key] = array(self.values[key])
                    tmpl += ('BRAVAIS\n' + keyfmts[key] +
                             '\n') % (self.values[key][0, 0], self.values[key][0, 1], self.values[key][0, 2],
                                      self.values[key][1, 0], self.values[key][1, 1], self.values[key][1, 2],
                                      self.values[key][2, 0], self.values[key][2, 1], self.values[key][2, 2])
                elif key == 'RUNOPT':
                    runops = keywords[key]
                    tmpl += 'RUNOPT\n'
                    for iop in range(len(runops)):
                        repltxt = runops[iop]
                        nblanks = 8 - len(repltxt)
                        if nblanks < 0:
                            print(f'WARNING for replacement of RUNOPTION {repltxt}: too long?')
                            print(f'RUNOPT {repltxt} is ignored and was not set!')
                        else:
                            repltxt = repltxt + ' ' * nblanks
                        tmpl += repltxt
                    tmpl += '\n'
                elif key == 'TESTOPT':
                    testops = keywords[key]
                    tmpl += 'TESTOPT\n'
                    for iop in range(len(testops)):
                        repltxt = testops[iop]
                        nblanks = 8 - len(repltxt)
                        if nblanks < 0:
                            print(f'WARNING for replacement of TESTOPTION {repltxt}: too long?')
                            print(f'TESTOPT {repltxt} is ignored and was not set!')
                        else:
                            repltxt = repltxt + ' ' * nblanks
                        tmpl += repltxt
                        if iop == 8:
                            tmpl += '\n'
                    tmpl += '\n'
                elif key == 'XINIPOL':
                    tmpl += f'{key}='
                    for ival in range(len(self.values[key])):
                        tmpl += f' {keyfmts[key]}' % self.values[key][ival]
                    tmpl += '\n'
                elif key == 'FILES':
                    files_changed = 0
                    if self.values[key][0] == '':
                        self.values[key][0] = 'potential'
                    else:
                        files_changed += 1
                    if self.values[key][1] == '':
                        self.values[key][1] = 'shapefun'
                    else:
                        files_changed += 1
                    if files_changed > 0 or 'DECIFILES' in self.values:  # force writing FILES line if DECIFILES should be set
                        if files_changed > 0:
                            print(
                                'Warning: Changing file name of potential file to "%s" and of shapefunction file to "%s"'
                                % (self.values[key][0], self.values[key][1]))
                        tmpl += 'FILES\n'
                        tmpl += '\n'
                        tmpl += f'{self.values[key][0]}\n'
                        tmpl += '\n'
                        tmpl += f'{self.values[key][1]}\n'
                        tmpl += 'scoef\n'
                elif key == 'DECIFILES':
                    tmpl += 'DECIFILES\n'
                    tmpl += f'{self.values[key][0]}\n'
                    tmpl += f'{self.values[key][1]}\n'
                elif key in ['JIJSITEI', 'JIJSITEJ']:
                    tmpl += f'{key}= '
                    jijsite = self.values[key]
                    tmpl += '%i ' % jijsite[0]
                    for isite in range(jijsite[0]):
                        tmpl += '%i ' % jijsite[1 + isite]
                    tmpl += '\n'
                elif self.__params_type == 'kkrimp' and key == 'RUNFLAG' or key == 'TESTFLAG':
                    # for kkrimp
                    ops = keywords[key]
                    tmpl += key + '='
                    for iop in range(len(ops)):
                        repltxt = ops[iop]
                        tmpl += ' ' + repltxt
                    tmpl += '\n'
                elif key in list(self.__listargs.keys()):
                    # keys that have array values
                    if key in ['<RBASIS>', '<RBLEFT>',
                               '<RBRIGHT>']:  # RBASIS needs special formatting since three numbers are filled per line
                        tmpl += f'{key}\n'
                        for ival in range(self.__listargs[key]):
                            tmpl += (keyfmts[key] + '\n') % (self.values[key][ival][0], self.values[key][ival][1],
                                                             self.values[key][ival][2])
                    elif key in ['CPAINFO', '<DELTAE>']:
                        tmpl += f'{key}= '
                        tmpl += (keyfmts[key] + '\n') % (self.values[key][0], self.values[key][1])
                    elif key in ['BZDIVIDE', 'ZPERIODL', 'ZPERIODR']:
                        tmpl += f'{key}= '
                        tmpl += (keyfmts[key] + '\n') % (self.values[key][0], self.values[key][1], self.values[key][2])
                    elif key in ['LDAU_PARA']:
                        tmpl += f'{key}= '
                        tmpl += (keyfmts[key] + '\n') % (self.values[key][0], self.values[key][1], self.values[key][2],
                                                         self.values[key][3], self.values[key][4])
                    elif self.__params_type == 'kkrimp' and key in ['HFIELD']:  # for kkrimp
                        tmpl += f'{key}= '
                        tmpl += (keyfmts[key] + '\n') % (self.values[key][0], self.values[key][1])
                    else:
                        #print(key, self.__listargs[key], len(self.values[key]))
                        tmpl += f'{key}\n'
                        for ival in range(self.__listargs[key]):
                            tmpl += (keyfmts[key] + '\n') % (self.values[key][ival])
                else:
                    print(f'Error trying to write keyword {key} but writing failed!')
                    raise ValueError

                # to make inputcard more readable insert some blank lines after certain keys
                if self.__params_type == 'kkrimp':
                    breaklines = ['TESTFLAG', 'NSPIN', 'QBOUND', 'NCHEB', 'HFIELD']
                else:
                    breaklines = [
                        'TESTOPT', 'CARTESIAN', '<RBASIS>', 'ZPERIODL', 'ZPERIODR', '<SHAPE>', 'KREADLDAU', '<ZATOM>',
                        '<SOCSCL>', '<CPA-CONC>', '<KAOEZR>', 'VCONST', 'BZDIVIDE', 'FSEMICORE', 'CPAINFO', 'RCLUSTXY',
                        '<RMTREF>', '<RMTREFR>', 'ICST', '<FPRADIUS>', 'GMAX', '<TOLRDIF>', 'QBOUND'
                    ]
                if key in breaklines:
                    tmpl += '\n'

        # finally write to file
        with open_general(output, u'w') as f:
            f.write(tmpl)

    def read_keywords_from_inputcard(self, inputcard='inputcard', verbose=False):
        """
        Read list of keywords from inputcard and extract values to keywords dict

        :example usage: p = kkrparams(); p.read_keywords_from_inputcard('inputcard')
        :note: converts '<RBLEFT>', '<RBRIGHT>', 'ZPERIODL', and 'ZPERIODR' automatically to Ang. units!
        """
        from numpy import shape, array
        from masci_tools.io.common_functions import get_aBohr2Ang

        debug = False
        if verbose:
            print(f'start reading {inputcard}')
            debug = True

        txt = open_general(inputcard, 'r').readlines()
        keywords = self.values
        keyfmts = self.__format

        #TODO loop over known keywords and fill with values found in inputcard
        # first read array dimensions
        read_first = ['NAEZ', 'NATYP', '<NLBASIS>', '<NRBASIS>', 'LMAX']
        read_already = []
        for key in read_first:
            valtxt = self._find_value(key, txt, debug=debug)
            if valtxt is None:  # try to read key without '<', '>'
                valtxt = self._find_value(key.replace('<', '').replace('>', ''), txt, debug=debug)
            # now set value in kkrparams
            if valtxt is not None:
                value = self.get_type(key)(valtxt)
                self.set_value(key, value)
                read_already.append(key)

        # then set self.__special_formatting and self.__listargs in _check_input_consistency
        # needs NAEZ, NATYP, NLBASIS, NRBASIS to be set to get array dimensions correct
        self._check_input_consistency(set_lists_only=True, verbose=verbose)

        # try to read keywords from inputcard and fill self.values
        for key in keywords:
            if key not in read_already:
                item, num = 1, 1  # starting column and number of columns that are read in

                if keyfmts[key].count('%') > 1:
                    num = keyfmts[key].count('%')

                if key not in self.__special_formatting:
                    # determine if more than one line is read in
                    if key in self.__listargs and key not in ['ZPERIODL', 'ZPERIODR', 'BZDIVIDE']:
                        itmp = self.__listargs[key]
                        if itmp is None:
                            itmp = 0
                        lines = list(range(1, itmp + 1))
                    else:
                        lines = [1]
                else:  # special formatting keys
                    if key == 'RUNOPT':
                        lines = [1]
                        num = 8
                        keyfmts[key] = '%s%s%s%s%s%s%s%s'
                    elif key == 'TESTOPT':
                        lines = [1, 2]
                        num = 8
                        keyfmts[key] = '%s%s%s%s%s%s%s%s'
                    elif key == 'BRAVAIS':
                        lines = [1, 2, 3]
                        num = 3
                        keyfmts[key] = '%f %f %f'
                    elif key == 'BZDIVIDE':
                        lines = [1]
                        num = 3
                        keyfmts[key] = '%f'
                    elif key == 'FILES':
                        lines = [2, 4]
                        num = 1
                        keyfmts[key] = '%s'
                    elif key == 'DECIFILES':
                        lines = [1, 2]
                        num = 1
                        keyfmts[key] = '%s'
                # read in all lines for this key
                values = []
                for iline in lines:
                    valtxt = self._find_value(key, txt, iline, item, num, debug=debug)
                    if valtxt is not None:
                        # first deal with run and testopts (needs to spearate keys)
                        if key == 'RUNOPT' or key == 'TESTOPT':
                            valtxt = self.split_kkr_options(valtxt)
                        # then continue with valtxt
                        if type(valtxt) == list:
                            tmp = []
                            for itmp in range(len(valtxt)):
                                tmptype = self.get_type(key)[itmp]
                                if tmptype == float and ('d' in valtxt[itmp] or 'D' in valtxt[itmp]):
                                    valtxt[itmp] = valtxt[itmp].replace('d', 'e').replace('D', 'e')
                                tmp.append(tmptype(valtxt[itmp]))
                        else:
                            tmptype = self.get_type(key)
                            if tmptype == float and ('d' in valtxt or 'D' in valtxt):
                                valtxt = valtxt.replace('d', 'e').replace('D', 'e')
                            if tmptype == bool:
                                if valtxt.upper() in ['F', 'FALSE', '.FALSE.', 'NO', '0']:
                                    valtxt = ''  # only empty string evaluates to False!!!
                                else:
                                    valtxt = 'True'
                            tmp = tmptype(valtxt)
                        values.append(tmp)
                if len(values) == 1:
                    values = values[0]

                if key == 'TESTOPT':  # flatten list
                    if shape(values)[0] == 2 and type(values[0]) == list:
                        tmp = []
                        for itmp in values:
                            for ii in itmp:
                                tmp.append(ii)
                        values = tmp

                # finally set values in kkrparams object
                if values != []:
                    self.set_value(key, values)

        # finally check if some input of the old style was given and read it in
        natyp = self.get_value('NATYP')
        if natyp is None:
            if debug:
                print('set NATYP=NAEZ')
            natyp = self.get_value('NAEZ')

        # look for old RBASIS input style
        if self.get_value('<RBASIS>') is None:
            if debug:
                print('look for RBASIS instead of <RBASIS>')
            rbasis = []
            for iatom in range(natyp):
                rbasis.append([float(i) for i in self._find_value('RBASIS', txt, 1 + iatom, 1, 3, debug=debug)])
            self.set_value('<RBASIS>', rbasis)

        # look for old atominfo input style
        atominfo_c = self._find_value('ATOMINFOC', txt, 2, debug=debug)
        if atominfo_c is None:
            atominfo_c = False
        else:
            atominfo_c = True
        atominfo = self._find_value('ATOMINFO', txt, 2, debug=debug)
        if atominfo is None:
            atominfo = False
        else:
            atominfo = True
        tmp = []
        if atominfo_c:
            if debug:
                print('read ATOMINFOC')
            for iatom in range(natyp):
                tmp.append(self._find_value('ATOMINFOC', txt, 2 + iatom, 1, 14, debug=debug))
        elif atominfo:
            if debug:
                print('read ATOMINFO')
            for iatom in range(natyp):
                tmp.append(self._find_value('ATOMINFO', txt, 2 + iatom, 1, 12, debug=debug))
        if atominfo_c or atominfo:
            tmp = array(tmp)
            cls_list = [int(i) for i in tmp[:, 6]]
            self.set_multiple_values(ZATOM=[float(i) for i in tmp[:, 0]],
                                     SHAPE=[int(i) for i in tmp[:, 8]],
                                     RMTREF=[float(i) for i in tmp[:, 11]])
            if atominfo_c:
                self.set_value('SITE', [int(i) for i in tmp[:, 12]])
                self.set_value('<CPA-CONC>', [float(i) for i in tmp[:, 13]])
        else:
            cls_list = list(range(1, natyp + 1))

        # look for old left/right basis input style
        if self.get_value('INTERFACE'):
            leftbasis = self._find_value('LEFTBASIS', txt, debug=debug)
            if leftbasis is None:
                leftbasis = False
            else:
                leftbasis = True
                nlbasis = self.get_value('<NLBASIS>')
            rightbasis = self._find_value('RIGHBASIS', txt, debug=debug)  # RIGHBASIS is no typo!!
            if rightbasis is None:
                rightbasis = False
            else:
                rightbasis = True
                nrbasis = self.get_value('<NRBASIS>')
            if leftbasis:
                tmp = []
                for iatom in range(nlbasis):
                    tmp.append(self._find_value('LEFTBASIS', txt, 1 + iatom, 1, 5, debug=debug))
                tmp = array(tmp)
                self.set_multiple_values(RBLEFT=[[float(i[j]) for j in range(3)] for i in tmp[:, 0:3]],
                                         KAOEZL=[int(i) for i in tmp[:, 3]])
                tmp2 = []
                for icls in tmp[:, 3]:
                    rmtref = self.get_value('<RMTREF>')[cls_list.index(int(icls))]
                    tmp2.append(rmtref)
                self.set_value('<RMTREFL>', tmp2)
            if rightbasis:
                tmp = []
                for iatom in range(nrbasis):
                    tmp.append(self._find_value('RIGHBASIS', txt, 1 + iatom, 1, 5, debug=debug))
                tmp = array(tmp)
                self.set_multiple_values(RBRIGHT=[[float(i[j]) for j in range(3)] for i in tmp[:, 0:3]],
                                         KAOEZR=[int(i) for i in tmp[:, 3]])
                tmp2 = []
                for icls in tmp[:, 3]:
                    rmtref = self.get_value('<RMTREF>')[cls_list.index(int(icls))]
                    tmp2.append(rmtref)
                self.set_value('<RMTREFR>', tmp2)

        # convert RBLEFT etc. from alat units to Ang. units (this is assumed in generate_inputcard)
        rbl = self.get_value('<RBLEFT>')
        rbr = self.get_value('<RBRIGHT>')
        zper_l = self.get_value('ZPERIODL')
        zper_r = self.get_value('ZPERIODR')
        alat2ang = self.get_value('ALATBASIS') * get_aBohr2Ang()
        if rbl is not None:
            self.set_value('<RBLEFT>', array(rbl) * alat2ang)
        if rbr is not None:
            self.set_value('<RBRIGHT>', array(rbr) * alat2ang)
        if zper_l is not None:
            self.set_value('ZPERIODL', array(zper_l) * alat2ang)
        if zper_r is not None:
            self.set_value('ZPERIODR', array(zper_r) * alat2ang)

        if debug:
            print(f'extracted parameters: {self.get_set_values()}')

    def _find_value(self, charkey, txt, line=1, item=1, num=1, debug=False):
        """
        Search charkey in txt and return value string

        parameter, input :: charkey         string that is search in txt
        parameter, input :: txt             text that is searched (output of readlines)
        parameter, input, optional :: line  index in which line to start reading after key was found
        parameter, input, optional :: item  index which column is read
        parameter, input, optional :: num   number of column that are read

        returns :: valtxt                   string or list of strings depending on num setting
        """
        if debug:
            print(f'find_value: {charkey}')
        try:
            iline = [ii for ii in range(len(txt)) if charkey in txt[ii]][0]
        except IndexError:
            iline = None
        if iline is not None:
            txtline = txt[iline]
            chkeq = charkey + '='
            if chkeq in txtline:
                valtxt = txtline.split(chkeq)[1].split()[item - 1:item - 1 + num]
            else:
                nextline = txt[iline + line]
                startpos = txtline.index(charkey)
                valtxt = nextline[startpos:].split()[item - 1:item - 1 + num]
            if debug:
                print(f'find_value found {valtxt}')
            if num == 1:
                return valtxt[0]
            else:
                return valtxt
        else:
            return None

    # redefine _update_mandatory for voronoi code
    def _update_mandatory_voronoi(self):
        """Change mandatory flags to match requirements of voronoi code"""
        # initialize all mandatory flags to False and update list afterwards
        for key in list(self.values.keys()):
            self._mandatory[key] = False

        runopts = []
        if self.values['RUNOPT'] is not None:
            for runopt in self.values['RUNOPT']:
                runopts.append(runopt.strip())

        #For a KKR calculation these keywords are always mandatory:
        mandatory_list = ['ALATBASIS', 'BRAVAIS', 'NAEZ', '<RBASIS>', 'NSPIN', 'LMAX', 'RCLUSTZ', '<ZATOM>']

        #Mandatory in 2D
        if self.values['INTERFACE']:
            mandatory_list += ['<NLBASIS>', '<RBLEFT>', 'ZPERIODL', '<NRBASIS>', '<RBRIGHT>', 'ZPERIODR']
        #Mandatory in CPA
        if self.values['NATYP'] is not None and self.values['NATYP'] > self.values['NAEZ']:
            mandatory_list += ['NATYP', '<SITE>', '<CPA-CONC>']

        for key in mandatory_list:
            self._mandatory[key] = True

    # redefine _update_mandatory for kkrim code
    def _update_mandatory_kkrimp(self):
        """Change mandatory flags to match requirements of kkrimp code"""
        # initialize all mandatory flags to False and update list afterwards
        for key in list(self.values.keys()):
            self._mandatory[key] = False

        runopts = []
        if self.values.get('RUNOPT', None) is not None:
            for runopt in self.values['RUNOPT']:
                runopts.append(runopt.strip())

        #For a KKR calculation these keywords are always mandatory:
        mandatory_list = []

        for key in mandatory_list:
            self._mandatory[key] = True

    def get_missing_keys(self, use_aiida=False):
        """Find list of mandatory keys that are not yet set"""
        setlist = list(dict(self.get_set_values()).keys())
        manlist = self.get_all_mandatory()
        missing = []
        autoset_list = ['BRAVAIS', '<RBASIS>', '<ZATOM>', 'ALATBASIS', 'NAEZ', '<SHAPE>', 'EMIN', 'RCLUSTZ']
        if self.__params_type == 'voronoi':
            autoset_list = ['BRAVAIS', '<RBASIS>', '<ZATOM>', 'ALATBASIS', 'NAEZ']
        for key in manlist:
            if key not in setlist:
                if not use_aiida:
                    missing.append(key)
                else:
                    if key not in autoset_list:
                        missing.append(key)
        return missing

    def update_to_voronoi(self):
        """
        Update parameter settings to match voronoi specification.
        Sets self.__params_type and calls _update_mandatory_voronoi()
        """
        self.__params_type = 'voronoi'
        self._update_mandatory_voronoi()

    def update_to_kkrimp(self):
        """
        Update parameter settings to match kkrimp specification.
        Sets self.__params_type and calls _update_mandatory_kkrimp()
        """
        self.__params_type = 'kkrimp'
        self._update_mandatory_kkrimp()

    def _create_keywords_dict_kkrimp(self, **kwargs):
        """
        Like create_keywords_dict but for changed keys of impurity code
        """

        default_keywords = self._DEFAULT_KEYS_KKRIMP

        for key in kwargs:
            key2 = self._add_brackets_to_key(key, default_keywords)
            default_keywords[key2][0] = kwargs[key]

        return default_keywords

    @classmethod
    def split_kkr_options(self, valtxt):
        """
        Split keywords after fixed length of 8
        :param valtxt: list of strings or single string
        :returns: List of keywords of maximal length 8
        """
        if type(valtxt) != list:
            valtxt = [valtxt]
        valtxt_tmp = []
        for itmp in valtxt:
            if len(itmp) > 8:
                Nsplitoff = int(len(itmp) // 8)
                for ii in range(Nsplitoff):
                    itmp_splitoff = itmp[ii * 8:(ii + 1) * 8]
                    valtxt_tmp.append(itmp_splitoff)
                itmp_splitoff = itmp[Nsplitoff * 8:]
                valtxt_tmp.append(itmp_splitoff)
            else:
                valtxt_tmp.append(itmp)
        valtxt = valtxt_tmp
        return valtxt

    def items(self):
        """make kkrparams.items() work"""
        return list(self.get_dict().items())

    def change_XC_val_kkrimp(self, val):
        """Convert integer value of KKRhost KEXCOR input to KKRimp XC string input."""
        if type(val) == int:
            if val == 0:
                val = 'LDA-MJW'
            if val == 1:
                val = 'LDA-vBH'
            if val == 2:
                val = 'LDA-VWN'
            if val == 3:
                val = 'GGA-PW91'
            if val == 4:
                val = 'GGA-PBE'
            if val == 5:
                val = 'GGA-PBEsol'
        return val

    def _add_brackets_to_key(self, key, key_dict):
        """Put '<' and '>' around the key expect for special keys defined in `__forbid_brackets__` list."""

        key2 = key
        if key not in list(key_dict.keys()) and key not in __forbid_brackets__:
            key2 = '<' + key + '>'

        return key2
