"""Holds the recipes (dictionaries) for different applications for the HDF file Reader module.

"""
import studentproject18w.hdf.output_types as load
from studentproject18w.hdf.output_types import *
from studentproject18w.hdf.input_transforms import *


class Recipes:
    """Recipes defining Extract-Transform-Load pipelines from HDF5 files for HDF Reader, for different application cases.

    Recipe Syntax: A recipe has two keys: "output_types" and "datasets".

    Value of "output_types": A list of types from :any:`output types module <output_types>`. One of those has to be a
    a class. The first class in the list will be the type of the reader output data. All other types - functions and
    classes - will be added as members to the created output instance. In case of classes, all methods will be added to
    the output instance. This enables modular output type construction from types defined for previous application
    cases. Note: when there is a name conflict, the program will abort with an error. As the attributes of the output
    type are added last at instance creation, they will overwrite any previously added attributes with same name
    without an error, but with a log warning.

    Value of "datasets": A dictionary of datasets. The keys specify the attribute names the transformed datasets will
    have when they will be added to the output type. The item with the empty key "" is ignored and can be used as
    template when creating new recipes.

    Value of "datasets" : attribute names : A dictionary with three keys "h5path" (obligatory), "description",
    "transforms" (optional). The "h5path" value is simply the absolute HDF5 path to the dataset in the HDF5 filee,
    for example "/foo/bar" for the dataset "bar". The "description" value is a string that can describe the dataset
    after transformation. The "transforms" value is a list [] of functions from the
    :any:`input transforms module <input_transforms>`. A function can either be referenced by type or by string.
    For example, [Transform.first_element] and ["Transform.first_element"] are equivalent. All valid transform functions
    have at least two arguments: name, dataset. For example: Transform.first_element(self,name,dataset). The reader
    will pass the output attribute name and the dataset itself automatically behind the scenes. If the function
    has more arguments, the function must be referenced as a list, where the first item is the function reference, and
    the remaining items are it's parameters. For example: [[Transform.slicer, "[4:-1]"]] on a 1D array will return
    the shortened array from the fifth tho the second-last element. Parameters should always be strings or enums.
    If more than one transform function is referenced, then they are applied sequentially. For example,
    [[TransformBands.coordinates, LatticeType.Bravais], [Transform.scale_with_constant, "bohr radius", "angstrom"]]
    will first apply a coordinate transformation, then scale the resulting dataset with the scipy physical_constant
    "Bohr_radius" in units of Angstrom. Since all transform classes are derived from one base class Transform, the
    last-mentioned could have also been referenced with TransformBands.scale_with_constant.

    Note that new Transform and data output classes and functions can of course be added. The reader and the recipe
    modules import everything from those modules, so name conflicts should be avoided.

    Note that the order in which the datasets in a recipe are specified does not matter. The reader and
    transforms take care of dependency checking behind the scenes.

    TODO
    =====
    Add support for read/write of recipes from/to file (de/serialize JSON) (Note: Reader already supports
    recipes using fct/cls strings instead of types, e.g. "TransformBands.k_distance" instead of TransformBands.k_distance,
    "DataBands" instead of DataBands, or "DataBands.count_atom_groups" instead of it's type equivalent. So should be
    pretty easy from here on.)

    """
    Template = {
        "output_types": [
            FleurData
        ],
        "datasets": {
            "": {  # example entry: empty key "" will be ignored
                "h5path": "/example/path",
                "description": f"This is a template recipe for writing new recipes.",
                "transforms": [Transform.id]
            }
        }
    }
    """Template recipe for writing new recipes."""

    FleurBands = {
        "output_types": [
            FleurBandData
        ],
        "datasets": {
            "atoms_elements":{
              "h5path": "/atoms/atomicNumbers",
                "description": f"Atomic numbers",
                "transforms": [Transform.periodic_elements]
            },
            "atoms_position": {
                "h5path": "/atoms/positions",
                "description": f"Atom coordinates per atom",
                "transforms": [[TransformBands.coordinates, LatticeType.Bravais]]
                # equivalent: [["TransformBands.coordinates", "bravais"]]
            },
            "atoms_group": {
                "h5path": "/atoms/equivAtomsGroup",
                "description": f"Atoms symmetry group per atom",
            },
            "bandUnfolding": {
                "h5path": "/general",
                "description": f"unfolding True/False",
                "transforms": [[Transform.attribute, 'bandUnfolding'],
                               [TransformBands.slicer, '[0]']]
            },
            "bandUnfolding_weights": {
                "h5path": "/bandUnfolding/weights",
                "description": f"weight for each E_n(k). Is None if no bandUnfolding.",
            },
            "bravaisMatrix": {
                "h5path": "/cell/bravaisMatrix",
                "description": f"Coordinate transformation internal to physical for atoms",
                "transforms": ['Transform.move_to_memory',
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
            "k_points": {
                "h5path": "/kpts/coordinates",
                "description": "bla",
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
    }
    """For Bandstructure Plots"""
