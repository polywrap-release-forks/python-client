from abc import ABC, abstractmethod
from typing import Optional

from polywrap_manifest import AnyWrapManifest
from polywrap_result import Result

from .client import GetManifestOptions
from .wrapper import Wrapper
from .wrap_package import IWrapPackage

class IWasmPackage(IWrapPackage, ABC):
    @abstractmethod
    async def get_wasm_module() -> Result[bytearray]:
        pass