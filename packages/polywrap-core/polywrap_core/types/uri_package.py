"""This module contains the UriPackage type."""
from __future__ import annotations

from typing import Generic, TypeVar

from .uri import Uri
from .uri_like import UriLike
from .wrap_package import WrapPackage

T = TypeVar("T", bound=UriLike)


class UriPackage(Generic[T], Uri):
    """UriPackage is a dataclass that contains a URI and a wrap package.

    Attributes:
        package (WrapPackage): The wrap package.
    """

    _package: WrapPackage[T]

    def __init__(self, uri: Uri, package: WrapPackage[T]) -> None:
        """Initialize a new instance of UriPackage.

        Args:
            uri (Uri): The URI.
            package (WrapPackage): The wrap package.
        """
        super().__init__(uri.authority, uri.path)
        self._package = package

    @property
    def package(self) -> WrapPackage[T]:
        """Return the wrap package."""
        return self._package
