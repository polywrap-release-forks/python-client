"""This module contains the utility for sanitizing and parsing Wrapper URIs."""
from __future__ import annotations

import re
from typing import Union

from .uri_like import UriLike


class Uri(UriLike):
    """Defines a wrapper URI and provides utilities for parsing and validating them.

    wrapper URIs are used to identify and resolve Polywrap wrappers. They are \
    based on [the URI standard](https://tools.ietf.org/html/rfc3986#section-3) \
    and follow the following format:
    
    `<scheme>://<authority>/<path>` where the scheme is always "wrap" and the \
    authority is the URI scheme of the underlying wrapper.

    Examples:
        >>> uri = Uri.from_str("ipfs/QmHASH")
        >>> uri.uri
        "wrap://ipfs/QmHASH"
        >>> uri = Uri.from_str("wrap://ipfs/QmHASH")
        >>> uri.uri
        "wrap://ipfs/QmHASH"
        >>> uri = Uri.from_str("ipfs")
        Traceback (most recent call last):
            ...
            ValueError: The provided URI has an invalid authority or path
        >>> uri = Uri.from_str("ipfs://QmHASH")
        Traceback (most recent call last):
            ...
            ValueError: The provided URI has an invalid scheme (must be 'wrap')
        >>> uri = Uri.from_str("")
        Traceback (most recent call last):
            ...
            ValueError: The provided URI is empty
        >>> uri = Uri.from_str(None)
        Traceback (most recent call last):
            ...
            TypeError: expected string or bytes-like object

    Attributes:
        scheme (str): The scheme of the URI. Defaults to "wrap". This helps \
            differentiate Polywrap URIs from other URI schemes.
        authority (str): The authority of the URI. This is used to determine \
            which URI resolver to use.
        path (str): The path of the URI. This is used to determine the \
            location of the wrapper.
    """

    URI_REGEX = re.compile(
        r"^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?"
    )  # https://www.rfc-editor.org/rfc/rfc3986#appendix-B

    _authority: str
    _path: str

    def __init__(self, authority: str, path: str):
        """Initialize a new instance of a wrapper URI.

        Args:
            authority: The authority of the URI.
            path: The path of the URI.
        """
        self._authority = authority
        self._path = path

    @property
    def authority(self) -> str:
        """Return the authority of the URI."""
        return self._authority

    @property
    def path(self) -> str:
        """Return the path of the URI."""
        return self._path

    @property
    def uri(self) -> str:
        """Return the canonical URI as a string."""
        return f"{self.scheme}://{self.authority}/{self.path}"

    @staticmethod
    def is_canonical_uri(uri: str) -> bool:
        """Return true if the provided URI is canonical.

        Args:
            uri: The URI as a string.

        Returns:
            True if the provided URI is canonical.
        """
        if not uri:
            raise ValueError("The provided URI is empty")

        matched_uri = Uri.URI_REGEX.match(uri)
        if not matched_uri:
            raise ValueError("The provided URI is malformed")

        uri_parts = matched_uri.groups()

        scheme: Union[str, None] = uri_parts[1]
        if scheme and scheme != "wrap":
            return False

        authority: Union[str, None] = uri_parts[3]
        path: Union[str, None] = uri_parts[4]

        return bool(path and path != "/") if authority else False

    @classmethod
    def from_str(cls, uri: str) -> Uri:
        """Create a new instance of a wrapper URI from a string.

        Args:
            uri: The URI as a string.

        Raises:
            ValueError: If the provided URI is empty or malformed.

        Returns:
            A new instance of a valid wrapper URI.
        """
        if not uri:
            raise ValueError("The provided URI is empty")

        matched_uri = cls.URI_REGEX.match(uri)
        if not matched_uri:
            raise ValueError("The provided URI is malformed")

        uri_parts = matched_uri.groups()

        scheme: Union[str, None] = uri_parts[1]
        authority: Union[str, None] = uri_parts[3]
        path: Union[str, None] = uri_parts[4]

        if scheme and scheme != "wrap":
            raise ValueError("The provided URI has an invalid scheme (must be 'wrap')")

        if authority and path and path.startswith("/"):
            path = path[1:]
        elif not authority and path and not path.startswith("/"):
            authority, path = path.split("/", 1)
        else:
            raise ValueError("The provided URI has an invalid authority or path")

        if not path:
            raise ValueError("The provided URI has an invalid path")

        return cls(authority, path)
