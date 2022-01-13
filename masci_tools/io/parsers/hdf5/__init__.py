"""
Here the functions from input_transforms are imported to trigger their decorators
This is needed to make the HDF5Reader aware of their existence
"""

from .reader import HDF5Reader
from .transforms import HDF5TransformationError

__all__ = ['HDF5Reader', 'HDF5TransformationError']
