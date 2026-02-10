import typing, clr, abc
from RobloxFiles.Tokens import IXmlPropertyToken
from System.Xml import XmlNode, XmlWriterSettings, XmlDocument
from RobloxFiles import Property, PropertyType, Instance, XmlRobloxFile

class XmlPropertyTokens(abc.ABC):
    # Skipped GetHandler due to it being static, abstract and generic.

    GetHandler : GetHandler_MethodGroup
    class GetHandler_MethodGroup:
        def __getitem__(self, t:typing.Type[GetHandler_1_T1]) -> GetHandler_1[GetHandler_1_T1]: ...

        GetHandler_1_T1 = typing.TypeVar('GetHandler_1_T1')
        class GetHandler_1(typing.Generic[GetHandler_1_T1]):
            GetHandler_1_T = XmlPropertyTokens.GetHandler_MethodGroup.GetHandler_1_T1
            def __call__(self) -> GetHandler_1_T:...

        def __call__(self, tokenName: str) -> IXmlPropertyToken:...

    # Skipped ReadPropertyGeneric due to it being static, abstract and generic.

    ReadPropertyGeneric : ReadPropertyGeneric_MethodGroup
    class ReadPropertyGeneric_MethodGroup:
        def __getitem__(self, t:typing.Type[ReadPropertyGeneric_1_T1]) -> ReadPropertyGeneric_1[ReadPropertyGeneric_1_T1]: ...

        ReadPropertyGeneric_1_T1 = typing.TypeVar('ReadPropertyGeneric_1_T1')
        class ReadPropertyGeneric_1(typing.Generic[ReadPropertyGeneric_1_T1]):
            ReadPropertyGeneric_1_T = XmlPropertyTokens.ReadPropertyGeneric_MethodGroup.ReadPropertyGeneric_1_T1
            @typing.overload
            def __call__(self, token: XmlNode, outValue: clr.Reference[ReadPropertyGeneric_1_T]) -> bool:...
            @typing.overload
            def __call__(self, prop: Property, propType: PropertyType, token: XmlNode) -> bool:...




class XmlRobloxFileReader(abc.ABC):
    @staticmethod
    def ReadInstance(instNode: XmlNode, file: XmlRobloxFile) -> Instance: ...
    @staticmethod
    def ReadMetadata(meta: XmlNode, file: XmlRobloxFile) -> None: ...
    @staticmethod
    def ReadProperties(instance: Instance, propsNode: XmlNode) -> None: ...
    @staticmethod
    def ReadSharedStrings(sharedStrings: XmlNode, file: XmlRobloxFile) -> None: ...


class XmlRobloxFileWriter(abc.ABC):
    Settings : XmlWriterSettings
    @staticmethod
    def CreateReferent() -> str: ...
    @staticmethod
    def WriteInstance(instance: Instance, doc: XmlDocument, file: XmlRobloxFile) -> XmlNode: ...
    @staticmethod
    def WriteProperty(prop: Property, doc: XmlDocument, file: XmlRobloxFile) -> XmlNode: ...
    @staticmethod
    def WriteSharedStrings(doc: XmlDocument, file: XmlRobloxFile) -> XmlNode: ...

