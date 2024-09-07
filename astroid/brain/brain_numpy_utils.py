# Licensed under the LGPL: https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html
# For details: https://github.com/pylint-dev/astroid/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/astroid/blob/main/CONTRIBUTORS.txt

"""Different utilities for the numpy brains."""

from __future__ import annotations

from astroid.builder import extract_node
from astroid.context import InferenceContext
from astroid.nodes.node_classes import Attribute, Import, Name

# Class subscript is available in numpy starting with version 1.20.0
NUMPY_VERSION_TYPE_HINTS_SUPPORT = ("1", "20", "0")


def numpy_supports_type_hints() -> bool:
    """Returns True if numpy supports type hints."""
    np_ver = _get_numpy_version()
    return np_ver and np_ver > NUMPY_VERSION_TYPE_HINTS_SUPPORT


def _get_numpy_version() -> tuple[str, str, str]:
    """
    Return the numpy version number if numpy can be imported.

    Otherwise returns ('0', '0', '0')
    """
    try:
        import numpy  # pylint: disable=import-outside-toplevel

        return tuple(numpy.version.version.split("."))
    except (ImportError, AttributeError):
        return ("0", "0", "0")


def infer_numpy_name(
    sources: dict[str, str], node: Name, context: InferenceContext | None = None
):
    extracted_node = extract_node(sources[node.name])
    return extracted_node.infer(context=context)


def infer_numpy_attribute(
    sources: dict[str, str], node: Attribute, context: InferenceContext | None = None
):
    extracted_node = extract_node(sources[node.attrname])
    return extracted_node.infer(context=context)


# TODO: Deprecate and remove this function
def infer_numpy_member(src, node, context: InferenceContext | None = None):
    node = extract_node(src)
    return node.infer(context=context)


def _is_a_numpy_module(node: Name) -> bool:
    """
    Returns True if the node is a representation of a numpy module.

    For example in :
        import numpy as np
        x = np.linspace(1, 2)
    The node <Name.np> is a representation of the numpy module.

    :param node: node to test
    :return: True if the node is a representation of the numpy module.
    """
    module_nickname = node.name
    potential_import_target = [
        x for x in node.lookup(module_nickname)[1] if isinstance(x, Import)
    ]
    return any(
        ("numpy", module_nickname) in target.names or ("numpy", None) in target.names
        for target in potential_import_target
    )


def member_name_looks_like_numpy_member(
    member_names: frozenset[str], node: Name
) -> bool:
    """
    Returns True if the Name node's name matches a member name from numpy
    """
    return node.name in member_names and node.root().name.startswith("numpy")


def attribute_name_looks_like_numpy_member(
    member_names: frozenset[str], node: Attribute
) -> bool:
    """
    Returns True if the Attribute node's name matches a member name from numpy
    """
    return (
        node.attrname in member_names
        and isinstance(node.expr, Name)
        and _is_a_numpy_module(node.expr)
    )


# TODO: Deprecate and remove this function
def name_looks_like_numpy_member(member_name: str, node: Name) -> bool:
    """
    Returns True if the Name is a member of numpy whose
    name is member_name.
    """
    return node.name == member_name and node.root().name.startswith("numpy")


# TODO: Deprecate and remove this function
def attribute_looks_like_numpy_member(member_name: str, node: Attribute) -> bool:
    """
    Returns True if the Attribute is a member of numpy whose
    name is member_name.
    """
    return (
        node.attrname == member_name
        and isinstance(node.expr, Name)
        and _is_a_numpy_module(node.expr)
    )
