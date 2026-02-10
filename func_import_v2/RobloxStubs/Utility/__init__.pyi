import typing, clr, abc
from RobloxFiles import Instance, Property
from System.Collections.Generic import IReadOnlyDictionary_2
from RobloxFiles.Enums import Font, FontSize, Material
from RobloxFiles.DataTypes import FontFace

class DefaultProperty(abc.ABC):
    # Skipped Get due to it being static, abstract and generic.

    Get : Get_MethodGroup
    class Get_MethodGroup:
        @typing.overload
        def __call__(self, className: str, propName: str) -> typing.Any:...
        @typing.overload
        def __call__(self, inst: Instance, propName: str) -> typing.Any:...
        @typing.overload
        def __call__(self, className: str, prop: Property) -> typing.Any:...
        @typing.overload
        def __call__(self, inst: Instance, prop: Property) -> typing.Any:...



class FontUtility(abc.ABC):
    FontFaces : IReadOnlyDictionary_2[Font, FontFace]
    FontSizes : IReadOnlyDictionary_2[int, FontSize]
    @staticmethod
    def GetLegacyFont(face: FontFace) -> Font: ...
    @staticmethod
    def TryGetFontFace(font: Font, face: clr.Reference[FontFace]) -> bool: ...
    # Skipped GetFontSize due to it being static, abstract and generic.

    GetFontSize : GetFontSize_MethodGroup
    class GetFontSize_MethodGroup:
        @typing.overload
        def __call__(self, size: float) -> FontSize:...
        # Method GetFontSize(fontSize : Int32) was skipped since it collides with above method
        @typing.overload
        def __call__(self, fontSize: FontSize) -> int:...



class PhysicalPropertyData(abc.ABC):
    Materials : IReadOnlyDictionary_2[Material, PhysicalPropertyInfo]


class PhysicalPropertyInfo:
    def __init__(self, density: float, friction: float, elasticity: float, frictionWeight: float, elasticityWeight: float) -> None: ...
    Density : float
    Elasticity : float
    ElasticityWeight : float
    Friction : float
    FrictionWeight : float

