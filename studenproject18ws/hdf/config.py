"""Holds the Extract Configs (dictionaries) for different applications for the HDF Extractor class.

"""

from studenproject18ws.hdf.transform import Transform, TransformBands, LatticeType

class Extract:
    """
    Configs for Extract-Transforms from HDF5 files for MasciHdfExtractor.
    Add another ETL config for a new application case or variation.

    TODO
    =====
    Add support for read-in of config from file (de/serialize JSON).

    """

    Bands = {
        "atoms_position": {
            "h5path": "/atoms/positions",
            "description": f"Atom coordinates per atom",
            "transforms": [[TransformBands.coordinates, LatticeType.Bravais]]
            # equivalent: [["coordinates", "bravais"]]
        },
        "atoms_group": {
            "h5path": "/atoms/equivAtomsGroup",
            "description": f"Atoms symmetry group per atom",
        },
        "bandUnfolding": {
            "h5path": "/general",
            "description": f"unfolding True/False",
            "transforms": [[Transform.attribute, 'bandUnfolding'],
                           [Transform.slicer, '[0]']]
        },
        "bandUnfolding_weights": {
            "h5path": "/bandUnfolding/weights",
            "description": f"weight for each E_n(k). Is None if no bandUnfolding.",
        },
        "bravaisMatrix": {
            "h5path": "/cell/bravaisMatrix",
            "description": f"Coordinate transformation internal to physical for atoms",
            "transforms": [Transform.move_to_memory,
                           [Transform.scale_with_constant, "bohr radius", "angstrom"]]
        },
        "eigenvalues": {
            "h5path": "/eigenvalues/eigenvalues",
            "description": f"'E_n sampled at discrete k values stored in 'kpts'",
        },
        "fermi_energy": {
            "h5path": "/general",
            "description": f"fermi_energy of the system",
            "transforms": [[Transform.attribute, 'lastFermiEnergy'],
                           [Transform.slicer, '[0]']]
        },
        "k_distances": {
            "h5path": "/kpts/coordinates",
            "description": f"k spacing along the path in the Brillouin zone. "
                           f"(Note: k_points are currently not stored, but available after"
                           f"transform via transformer.k_points. k_points are 3d coordinates "
                           f"of the path along which E_n(kx, ky, kz) is sampled. See k_distance"
                           f"function if this should be changed.)"
                           f"",
            "transforms": [TransformBands.k_distance]
        },
        "k_special_points": {
            "h5path": "/kpts/specialPointIndices",
            "description": f"high symmetry points k-values",
            "transforms": [TransformBands.k_special_points]
        },
        "k_special_point_labels": {
            "h5path": "/kpts/specialPointLabels",
            "description": f"high symmetry points labels",
        },
        "llikecharge": {
            "h5path": "/eigenvalues/lLikeCharge",
            "description": f"Something related to the projection on s,p,d,f,... orbitals...",
        },
        "reciprocalCell": {
            "h5path": "/cell/reciprocalCell",
            "description": f"Coordinate transformation internal to physical for k_points",
            "transforms": [Transform.move_to_memory]
        },
        "unused_k_weights": {
            "h5path": "/kpts/weights",
        },
        "unused_jsym": {
            "h5path": "/eigenvalues/jsym",
            "transforms": [[Transform.slicer, "[0]"]]
        },
        "unused_ksym": {
            "h5path": "/eigenvalues/ksym",
            "transforms": [[Transform.slicer, "[0]"]]
        },
        "unused_numFoundEigenvalues": {
            "h5path": "/eigenvalues/numFoundEigenvals",
        },
        "": {  # template entry
            "h5path": "",
            "description": f"",
            "transforms": [Transform.id]
        },
    }
    """For Bandstructure Plots"""

    Template = {
        "": {  # example entry
            "h5path": "/example/path",
            "description": f"This is an example item for a dataset to be read (extract-transform) from a hdf file."
                           f"The key is the name the transformed dataset should have."
                           f"This example item has the empty key '' and is thus ignored."
                           f"Every item must have a valid 'h5path': the path to the dataset in the HDF file."
                           f"The 'description' is optional. It describes the dataset after transformation."
                           f"The 'transforms' is optional. If present,"
                           f"the 'transforms' is a list of transform functions to be applied. Inside a single Extract"
                           f"Config (dictionary), all transform functions in all items must belong to the same class."
                           f"A transform fct can be referenced as fct object or by string name. Meaning:"
                           f"'transforms': [Transforms.id]  ..is equivalent to.. 'transforms': ['id']."
                           f"All transform functions must belong to the same class."
                           f"An entry for a function with arguments is itself a list. The first element is the fct and"
                           f"the following elements it's arguments. "
                           f"The following 'transforms' value are equivalent to 'transforms' being absent:"
                           f"[Transforms.id], ['id'], Transforms.id, 'id', TransDerivedClass.id, ...",
            "transforms": [Transform.id]
        }
    }
    """Template for defining a new Extract Config."""


