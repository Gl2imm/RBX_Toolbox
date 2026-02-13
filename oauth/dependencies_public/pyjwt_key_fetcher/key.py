import collections.abc
from typing import Any, Dict, Iterator

from jwt import PyJWK


class Key(collections.abc.Mapping):
    """
    Wrapper for the JWT key and algorithm.
    """

    def __init__(self, jwk_data: Dict[str, Any]) -> None:
        """
        :param jwk_data: The data from the JWKs JSON for a key.
        """
        pyjwt = PyJWK(jwk_data)

        self.__kid = pyjwt.key_id

        self.key: PyJWK = pyjwt.key
        self.algorithms = []
        if "alg" in jwk_data:
            self.algorithms.append(jwk_data["alg"])

    @property
    def dct(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(key=<{self.key.__class__.__name__}, kid: "
            f"{self.__kid}>, algorithms={self.algorithms})"
        )

    def __getitem__(self, item):
        return self.dct.__getitem__(item)

    def __iter__(self) -> Iterator:
        return self.dct.__iter__()

    def __len__(self) -> int:
        return self.dct.__len__()
