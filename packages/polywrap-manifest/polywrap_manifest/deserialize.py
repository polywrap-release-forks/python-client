"""
This file was automatically generated by scripts/templates/deserialize.py.jinja2.
DO NOT MODIFY IT BY HAND. Instead, modify scripts/templates/deserialize.py.jinja2,
and run python ./scripts/generate.py to regenerate this file.
"""

from typing import Optional

from polywrap_msgpack import msgpack_decode

from .manifest import *


def deserialize_wrap_manifest(
    manifest: bytes, options: Optional[DeserializeManifestOptions] = None
) -> AnyWrapManifest:
    decoded_manifest = msgpack_decode(manifest)
    if not decoded_manifest.get("version"):
        raise ValueError("Expected manifest version to be defined!")

    no_validate = options and options.no_validate
    manifest_version = WrapManifestVersions(decoded_manifest["version"])
    match manifest_version.value:
        case "0.1.0":
            return (
                WrapManifest_0_1.construct(**decoded_manifest)
                if no_validate
                else WrapManifest_0_1(**decoded_manifest)
            )
        case "0.1":
            return WrapManifest_0_1(**decoded_manifest)
        case _:
            raise ValueError(f"Invalid wrap manifest version: {manifest_version}")