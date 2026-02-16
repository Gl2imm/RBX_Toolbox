import typing, clr, abc
from RobloxStubs.Enums import AccessoryType, ModelLevelOfDetail, ModelStreamingMode, AdShape, NormalId, SelectionBehavior, ZIndexBehavior, AlignType, OrientationAlignmentMode, ForceLimitMode, ActuatorRelativeTo, PositionAlignmentMode, AnimationPriority, SensorUpdateType, AudioWindowSize, AudioChannelLayout, AccessModifierType, AudioSimulationFidelity, AudioFilterType, AudioSubType, AvatarSettingsAccessoryMode, AvatarSettingsCustomAccessoryMode, AvatarSettingsAccessoryLimitMethod, AvatarSettingsAnimationClipsMode, AvatarSettingsAnimationPacksMode, AvatarSettingsAppearanceMode, AvatarSettingsBuildMode, AvatarSettingsCustomBodyType, AvatarSettingsScaleMode, AvatarSettingsClothingMode, AvatarSettingsCustomClothingMode, AvatarSettingsCollisionMode, AvatarSettingsHitAndTouchDetectionMode, AvatarSettingsLegacyCollisionMode, GameAvatarType, SurfaceType, InputType, Material, RunContext, TextureMode, BodyPart, AdornCullingMode, Font, CameraType, FieldOfViewMode, AutomaticSize, BorderMode, SizeConstraint, KeyCode, HorizontalAlignment, VerticalAlignment, TonemapperPreset, SensorMode, ActuatorType, DialogBehaviorType, DialogPurpose, DialogTone, DragDetectorDragStyle, DragDetectorPermissionPolicy, DragDetectorResponseStyle, RotationOrder, ExplosionType, InOut, LeftRight, TopBottom, FormFactor, PartType, FrameStyle, ButtonStyle, SafeAreaCompatibility, ScreenInsets, HandlesStyle, HandRigDescriptionSide, HapticEffectType, HighlightDepthMode, BinType, HumanoidCollisionType, HumanoidDisplayDistanceType, HumanoidHealthDisplayType, NameOcclusion, HumanoidRigType, IKControlType, ResamplerMode, ScaleType, InputActionType, FluidFidelity, RenderFidelity, LightingStyle, Technology, VelocityConstraintMode, MaterialPattern, NegateOperationHiddenHistory, NoiseType, PoseEasingDirection, PoseEasingStyle, ParticleFlipbookLayout, ParticleFlipbookMode, ParticleOrientation, ParticleEmitterShape, ParticleEmitterShapeInOut, ParticleEmitterShapeStyle, PlayerDataLoadFailureBehavior, TriStateBoolean, ProximityPromptExclusivity, ProximityPromptStyle, ServiceVisibility, RenderingTestComparisonMethod, QualityLevel, FramerateManagerMode, GraphicsMode, MeshPartDetailLevel, ViewMode, ElasticBehavior, ScrollBarInset, ScrollingDirection, VerticalScrollBarPosition, RollOffMode, ReverbType, RolloutState, ListenerLocation, VolumetricAudio, MeshType, RtlTextSupport, ScreenOrientation, VirtualCursorMode, CameraMode, DevCameraOcclusionMode, DevComputerCameraMovementMode, DevComputerMovementMode, DevTouchCameraMovementMode, DevTouchMovementMode, LoadDynamicHeads, R15CollisionType, LoadCharacterLayeredClothing, CharacterControlMode, AlphaMode, SurfaceGuiSizingMode, ThreadPoolConfig, TerrainAcquisitionMethod, TerrainFace, TextDirection, TextTruncate, TextXAlignment, TextYAlignment, FontSize, ChatVersion, Style, AspectType, DominantAxis, UIDragDetectorBoundingBehavior, UIDragDetectorDragRelativity, UIDragDetectorDragSpace, UIDragDetectorDragStyle, UIDragDetectorResponseStyle, UIDragSpeedAxisMapping, UIFlexMode, ItemLineAlignment, FillDirection, SortOrder, StartCorner, UIFlexAlignment, EasingDirection, EasingStyle, ApplyStrokeMode, LineJoinMode, TableMajorAxis, MouseBehavior, VideoDeviceCaptureQuality, VoiceChatDistanceAttenuationType, AudioApiRollout, VRScaling, VRControllerModelMode, VRLaserPointerMode, AvatarUnificationMode, ClientAnimatorThrottlingMode, FluidForces, IKControlConstraintSupport, MeshPartHeadsAndAccessories, ModelStreamingBehavior, MoverConstraintRootBehaviorMode, PathfindingUseImprovedSearch, PhysicsSteppingMethod, PlayerCharacterDestroyBehavior, PrimalPhysicsSolver, RejectCharacterDeletions, RenderingCacheOptimizationMode, ReplicateInstanceDestroySetting, AnimatorRetargetingMode, SandboxedInstanceMode, SignalBehavior, StreamingIntegrityMode, StreamOutBehavior, WrapLayerAutoSkin
from RobloxFiles.DataTypes import CFrame, UniqueId, Vector3, SharedString, Optional_1, ContentId, BrickColor, Axes, Color3, NumberRange, ProtectedString, Color3uint8, PhysicalProperties, Content, ColorSequence, NumberSequence, UDim2, Vector2, FontFace, Faces, Rect, Ray, Vector3int16, UDim
from System.Collections.Generic import HashSet_1, IReadOnlyDictionary_2, IReadOnlyList_1, Dictionary_2, SortedDictionary_2, IComparer_1
from System import Array_1, Attribute, IDisposable
from RobloxFiles.BinaryFormat import BinaryRobloxFileChunk
from RobloxFiles.BinaryFormat.Chunks import INST, RbxSignature, PROP
from System.IO import Stream
from System.Threading.Tasks import Task_1, Task
from System.Xml import XmlDocument

class Accessory(Accoutrement):
    def __init__(self) -> None: ...
    AccessoryType : AccessoryType
    Archivable : bool
    AttachmentPoint : CFrame
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AccessoryDescription(Instance):
    def __init__(self) -> None: ...
    AccessoryType : AccessoryType
    Archivable : bool
    AssetId : int
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Instance : Instance
    IsLayered : bool
    Name : str
    Order : int
    Position : Vector3
    Puffiness : float
    Rotation : Vector3
    Scale : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AccountService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Accoutrement(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    AttachmentPoint : CFrame
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AchievementService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ActivityHistoryEventService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Actor(Model):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    LevelOfDetail : ModelLevelOfDetail
    ModelMeshCFrame : CFrame
    ModelMeshData : SharedString
    ModelMeshSize : Vector3
    ModelStreamingMode : ModelStreamingMode
    Name : str
    NeedsPivotMigration : bool
    PrimaryPart : BasePart
    ScaleFactor : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    WorldPivotData : Optional_1[CFrame]
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AdGui(SurfaceGuiBase):
    def __init__(self) -> None: ...
    Active : bool
    Adornee : Instance
    AdShape : AdShape
    Archivable : bool
    Attributes : RbxAttributes
    AutoLocalize : bool
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    EnableVideoAds : bool
    Face : NormalId
    FallbackImage : ContentId
    HistoryId : UniqueId
    Name : str
    ResetOnSpawn : bool
    RootLocalizationTable : LocalizationTable
    SelectionBehaviorDown : SelectionBehavior
    SelectionBehaviorLeft : SelectionBehavior
    SelectionBehaviorRight : SelectionBehavior
    SelectionBehaviorUp : SelectionBehavior
    SelectionGroup : bool
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    ZIndexBehavior : ZIndexBehavior
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Localize(self) -> bool: ...
    @Localize.setter
    def Localize(self, value: bool) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AdPortal(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AdService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AdvancedDragger(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AirController(ControllerBase):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    BalanceMaxTorque : float
    BalanceRigidityEnabled : bool
    BalanceSpeed : float
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    MaintainAngularMomentum : bool
    MaintainLinearMomentum : bool
    MoveMaxForce : float
    MoveSpeedFactor : float
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    TurnMaxTorque : float
    TurnSpeedFactor : float
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AlignOrientation(Constraint):
    def __init__(self) -> None: ...
    AlignType : AlignType
    Archivable : bool
    Attachment0 : Attachment
    Attachment1 : Attachment
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    CFrame : CFrame
    Color : BrickColor
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    MaxAngularVelocity : float
    MaxTorque : float
    Mode : OrientationAlignmentMode
    Name : str
    PrimaryAxisOnly : bool
    ReactionTorqueEnabled : bool
    Responsiveness : float
    RigidityEnabled : bool
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AlignPosition(Constraint):
    def __init__(self) -> None: ...
    ApplyAtCenterOfMass : bool
    Archivable : bool
    Attachment0 : Attachment
    Attachment1 : Attachment
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color : BrickColor
    DefinesCapabilities : bool
    Enabled : bool
    ForceLimitMode : ForceLimitMode
    ForceRelativeTo : ActuatorRelativeTo
    HistoryId : UniqueId
    MaxAxesForce : Vector3
    MaxForce : float
    MaxVelocity : float
    Mode : PositionAlignmentMode
    Name : str
    Position : Vector3
    ReactionForceEnabled : bool
    Responsiveness : float
    RigidityEnabled : bool
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AnalyticsService(Instance):
    def __init__(self) -> None: ...
    ApiKey : str
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AngularVelocity(Constraint):
    def __init__(self) -> None: ...
    AngularVelocity_ : Vector3
    Archivable : bool
    Attachment0 : Attachment
    Attachment1 : Attachment
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color : BrickColor
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    MaxTorque : float
    Name : str
    ReactionTorqueEnabled : bool
    RelativeTo : ActuatorRelativeTo
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Animation(Instance):
    def __init__(self) -> None: ...
    AnimationId : ContentId
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AnimationClip(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    GuidBinaryString : Array_1[int]
    HistoryId : UniqueId
    Loop : bool
    Name : str
    Priority : AnimationPriority
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AnimationClipProvider(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AnimationConstraint(Constraint):
    def __init__(self) -> None: ...
    Archivable : bool
    Attachment0 : Attachment
    Attachment1 : Attachment
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color : BrickColor
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    IsKinematic : bool
    MaxForce : float
    MaxTorque : float
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    Transform : CFrame
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AnimationController(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AnimationFromVideoCreatorService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AnimationFromVideoCreatorStudioService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AnimationRigData(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    label : Array_1[int]
    name : Array_1[int]
    Name : str
    parent : Array_1[int]
    postTransform : Array_1[int]
    preTransform : Array_1[int]
    SourceAssetId : int
    Tags : HashSet_1[str]
    transform : Array_1[int]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Animator(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    PreferLodEnabled : bool
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Annotation(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AnnotationsService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AppLifecycleObserverService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AppStorageService(LocalStorageService):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AppUpdateService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ArcHandles(HandlesBase):
    def __init__(self) -> None: ...
    Adornee : BasePart
    Archivable : bool
    Attributes : RbxAttributes
    Axes : Axes
    Capabilities : SecurityCapabilities
    Color3 : Color3
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    Transparency : float
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> BrickColor: ...
    @Color.setter
    def Color(self, value: BrickColor) -> BrickColor: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AssetCounterService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AssetDeliveryProxy(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Interface : str
    Name : str
    Port : int
    SourceAssetId : int
    StartServer : bool
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AssetImportService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AssetManagerService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AssetService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Atmosphere(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color : Color3
    Decay : Color3
    DefinesCapabilities : bool
    Density : float
    Glare : float
    Haze : float
    HistoryId : UniqueId
    Name : str
    Offset : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AtmosphereSensor(SensorBase):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    UpdateType : SensorUpdateType
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Attachment(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    CFrame : CFrame
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AttributeType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    String : AttributeType # 2
    Bool : AttributeType # 3
    Int : AttributeType # 4
    Float : AttributeType # 5
    Double : AttributeType # 6
    UDim : AttributeType # 9
    UDim2 : AttributeType # 10
    BrickColor : AttributeType # 14
    Color3 : AttributeType # 15
    Vector2 : AttributeType # 16
    Vector3 : AttributeType # 17
    CFrame : AttributeType # 20
    Enum : AttributeType # 21
    NumberSequence : AttributeType # 23
    ColorSequence : AttributeType # 25
    NumberRange : AttributeType # 27
    Rect : AttributeType # 28
    FontFace : AttributeType # 33


class AudioAnalyzer(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    SpectrumEnabled : bool
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    WindowSize : AudioWindowSize
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AudioChannelMixer(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Layout : AudioChannelLayout
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AudioChannelSplitter(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Layout : AudioChannelLayout
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AudioChorus(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Bypass : bool
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Depth : float
    HistoryId : UniqueId
    Mix : float
    Name : str
    Rate : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AudioCompressor(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attack : float
    Attributes : RbxAttributes
    Bypass : bool
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    MakeupGain : float
    Name : str
    Ratio : float
    Release : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    Threshold : float
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AudioDeviceInput(Instance):
    def __init__(self) -> None: ...
    AccessType : AccessModifierType
    Active : bool
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Muted : bool
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Volume : float
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AudioDeviceOutput(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AudioDistortion(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Bypass : bool
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Level : float
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AudioEcho(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Bypass : bool
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    DelayTime : float
    DryLevel : float
    Feedback : float
    HistoryId : UniqueId
    Name : str
    RampTime : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    WetLevel : float
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AudioEmitter(Instance):
    def __init__(self) -> None: ...
    AngleAttenuation : Array_1[int]
    Archivable : bool
    Attributes : RbxAttributes
    AudioInteractionGroup : str
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    DistanceAttenuation : Array_1[int]
    HistoryId : UniqueId
    Name : str
    SimulationFidelity : AudioSimulationFidelity
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AudioEqualizer(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Bypass : bool
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HighGain : float
    HistoryId : UniqueId
    LowGain : float
    MidGain : float
    MidRange : NumberRange
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AudioFader(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Bypass : bool
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Volume : float
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AudioFilter(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Bypass : bool
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    FilterType : AudioFilterType
    Frequency : float
    Gain : float
    HistoryId : UniqueId
    Name : str
    Q : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AudioFlanger(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Bypass : bool
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Depth : float
    HistoryId : UniqueId
    Mix : float
    Name : str
    Rate : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AudioFocusService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AudioLimiter(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Bypass : bool
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    MaxLevel : float
    Name : str
    Release : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AudioListener(Instance):
    def __init__(self) -> None: ...
    AngleAttenuation : Array_1[int]
    Archivable : bool
    Attributes : RbxAttributes
    AudioInteractionGroup : str
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    DistanceAttenuation : Array_1[int]
    HistoryId : UniqueId
    Name : str
    SimulationFidelity : AudioSimulationFidelity
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AudioPitchShifter(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Bypass : bool
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    Pitch : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    WindowSize : AudioWindowSize
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AudioPlayer(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Asset : ContentId
    Attributes : RbxAttributes
    AutoLoad : bool
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Looping : bool
    LoopRegion : NumberRange
    Name : str
    PlaybackRegion : NumberRange
    PlaybackSpeed : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    TimePosition : float
    UniqueId : UniqueId
    Volume : float
    @property
    def AssetId(self) -> str: ...
    @AssetId.setter
    def AssetId(self, value: str) -> str: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AudioRecorder(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    IsRecording : bool
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AudioReverb(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Bypass : bool
    Capabilities : SecurityCapabilities
    DecayRatio : float
    DecayTime : float
    DefinesCapabilities : bool
    Density : float
    Diffusion : float
    DryLevel : float
    EarlyDelayTime : float
    HighCutFrequency : float
    HistoryId : UniqueId
    LateDelayTime : float
    LowShelfFrequency : float
    LowShelfGain : float
    Name : str
    ReferenceFrequency : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    WetLevel : float
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AudioSearchParams(Instance):
    def __init__(self) -> None: ...
    Album : str
    Archivable : bool
    Artist : str
    Attributes : RbxAttributes
    AudioSubType : AudioSubType
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    MaxDuration : int
    MinDuration : int
    Name : str
    SearchKeyword : str
    SourceAssetId : int
    Tag : str
    Tags : HashSet_1[str]
    Title : str
    UniqueId : UniqueId
    @property
    def AudioSubtype(self) -> AudioSubType: ...
    @AudioSubtype.setter
    def AudioSubtype(self, value: AudioSubType) -> AudioSubType: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AudioTextToSpeech(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Looping : bool
    Name : str
    Pitch : float
    PlaybackSpeed : float
    SourceAssetId : int
    Speed : float
    Tags : HashSet_1[str]
    Text : str
    TimePosition : float
    UniqueId : UniqueId
    VoiceId : str
    Volume : float
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AuroraScript(LuaSourceContainer):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    EnableCulling : bool
    EnableLOD : bool
    HistoryId : UniqueId
    LODCriticality : int
    Name : str
    Priority : int
    ScriptGuid : str
    Source : ProtectedString
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AuroraScriptService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AuroraService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HashRoundingPoint : float
    HistoryId : UniqueId
    IgnoreRotation : bool
    Name : str
    RollbackOffset : int
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AvatarAccessoryRules(Instance):
    def __init__(self) -> None: ...
    AccessoryMode : AvatarSettingsAccessoryMode
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    CustomAccessoryMode : AvatarSettingsCustomAccessoryMode
    CustomBackAccessoryEnabled : bool
    CustomBackAccessoryId : int
    CustomFaceAccessoryEnabled : bool
    CustomFaceAccessoryId : int
    CustomFrontAccessoryEnabled : bool
    CustomFrontAccessoryId : int
    CustomHairAccessoryEnabled : bool
    CustomHairAccessoryId : int
    CustomHeadAccessoryEnabled : bool
    CustomHeadAccessoryId : int
    CustomNeckAccessoryEnabled : bool
    CustomNeckAccessoryId : int
    CustomShoulderAccessoryEnabled : bool
    CustomShoulderAccessoryId : int
    CustomWaistAccessoryEnabled : bool
    CustomWaistAccessoryId : int
    DefinesCapabilities : bool
    EnableSound : bool
    EnableVFX : bool
    HistoryId : UniqueId
    LimitBounds : Vector3
    LimitMethod : AvatarSettingsAccessoryLimitMethod
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AvatarAnimationRules(Instance):
    def __init__(self) -> None: ...
    AnimationClipsMode : AvatarSettingsAnimationClipsMode
    AnimationPacksMode : AvatarSettingsAnimationPacksMode
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    CustomClimbAnimationEnabled : bool
    CustomClimbAnimationId : int
    CustomFallAnimationEnabled : bool
    CustomFallAnimationId : int
    CustomIdleAlt1AnimationEnabled : bool
    CustomIdleAlt1AnimationId : int
    CustomIdleAlt2AnimationEnabled : bool
    CustomIdleAlt2AnimationId : int
    CustomIdleAnimationEnabled : bool
    CustomIdleAnimationId : int
    CustomJumpAnimationEnabled : bool
    CustomJumpAnimationId : int
    CustomRunAnimationEnabled : bool
    CustomRunAnimationId : int
    CustomSwimAnimationEnabled : bool
    CustomSwimAnimationId : int
    CustomSwimIdleAnimationEnabled : bool
    CustomSwimIdleAnimationId : int
    CustomWalkAnimationEnabled : bool
    CustomWalkAnimationId : int
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AvatarBodyRules(Instance):
    def __init__(self) -> None: ...
    AppearanceMode : AvatarSettingsAppearanceMode
    Archivable : bool
    Attributes : RbxAttributes
    BuildMode : AvatarSettingsBuildMode
    Capabilities : SecurityCapabilities
    CustomBodyBundleId : int
    CustomBodyType : AvatarSettingsCustomBodyType
    CustomBodyTypeScale : NumberRange
    CustomHeadEnabled : bool
    CustomHeadId : int
    CustomHeadScale : NumberRange
    CustomHeight : NumberRange
    CustomHeightScale : NumberRange
    CustomLeftArmEnabled : bool
    CustomLeftArmId : int
    CustomLeftLegEnabled : bool
    CustomLeftLegId : int
    CustomProportionsScale : NumberRange
    CustomRightArmEnabled : bool
    CustomRightArmId : int
    CustomRightLegEnabled : bool
    CustomRightLegId : int
    CustomTorsoEnabled : bool
    CustomTorsoId : int
    CustomWidthScale : NumberRange
    DefinesCapabilities : bool
    HistoryId : UniqueId
    KeepPlayerHead : bool
    Name : str
    ScaleMode : AvatarSettingsScaleMode
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AvatarChatService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AvatarClothingRules(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    ClothingMode : AvatarSettingsClothingMode
    CustomClassicPantsAccessoryEnabled : bool
    CustomClassicPantsAccessoryId : int
    CustomClassicShirtsAccessoryEnabled : bool
    CustomClassicShirtsAccessoryId : int
    CustomClassicTShirtsAccessoryEnabled : bool
    CustomClassicTShirtsAccessoryId : int
    CustomClothingMode : AvatarSettingsCustomClothingMode
    CustomDressSkirtAccessoryEnabled : bool
    CustomDressSkirtAccessoryId : int
    CustomJacketAccessoryEnabled : bool
    CustomJacketAccessoryId : int
    CustomLeftShoesAccessoryEnabled : bool
    CustomLeftShoesAccessoryId : int
    CustomPantsAccessoryEnabled : bool
    CustomPantsAccessoryId : int
    CustomRightShoesAccessoryEnabled : bool
    CustomRightShoesAccessoryId : int
    CustomShirtAccessoryEnabled : bool
    CustomShirtAccessoryId : int
    CustomShortsAccessoryEnabled : bool
    CustomShortsAccessoryId : int
    CustomSweaterAccessoryEnabled : bool
    CustomSweaterAccessoryId : int
    CustomTShirtAccessoryEnabled : bool
    CustomTShirtAccessoryId : int
    DefinesCapabilities : bool
    HistoryId : UniqueId
    LimitBounds : Vector3
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AvatarCollisionRules(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    CollisionMode : AvatarSettingsCollisionMode
    DefinesCapabilities : bool
    HistoryId : UniqueId
    HitAndTouchDetectionMode : AvatarSettingsHitAndTouchDetectionMode
    LegacyCollisionMode : AvatarSettingsLegacyCollisionMode
    Name : str
    SingleColliderSize : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AvatarCreationService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AvatarEditorService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AvatarImportService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AvatarPreloader(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AvatarRules(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    AvatarType : GameAvatarType
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class AvatarSettings(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Backpack(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BackpackItem(Model, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    LevelOfDetail : ModelLevelOfDetail
    ModelMeshCFrame : CFrame
    ModelMeshData : SharedString
    ModelMeshSize : Vector3
    ModelStreamingMode : ModelStreamingMode
    Name : str
    NeedsPivotMigration : bool
    PrimaryPart : BasePart
    ScaleFactor : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    TextureId : ContentId
    UniqueId : UniqueId
    WorldPivotData : Optional_1[CFrame]
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BadgeService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BallSocketConstraint(Constraint):
    def __init__(self) -> None: ...
    Archivable : bool
    Attachment0 : Attachment
    Attachment1 : Attachment
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color : BrickColor
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    LimitsEnabled : bool
    MaxFrictionTorqueXml : float
    Name : str
    Radius : float
    Restitution : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    TwistLimitsEnabled : bool
    TwistLowerAngle : float
    TwistUpperAngle : float
    UniqueId : UniqueId
    UpperAngle : float
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BasePart(PVInstance):
    Anchored : bool
    Archivable : bool
    Attributes : RbxAttributes
    AudioCanCollide : bool
    BackParamA : float
    BackParamB : float
    BackSurface : SurfaceType
    BackSurfaceInput : InputType
    BottomParamA : float
    BottomParamB : float
    BottomSurface : SurfaceType
    BottomSurfaceInput : InputType
    CanCollide : bool
    CanQuery : bool
    CanTouch : bool
    Capabilities : SecurityCapabilities
    CastShadow : bool
    CFrame : CFrame
    CollisionGroup : str
    CollisionGroupId : int
    Color3uint8 : Color3uint8
    CustomPhysicalProperties : PhysicalProperties
    DefinesCapabilities : bool
    Elasticity : float
    EnableFluidForces : bool
    Friction : float
    FrontParamA : float
    FrontParamB : float
    FrontSurface : SurfaceType
    FrontSurfaceInput : InputType
    HistoryId : UniqueId
    LeftParamA : float
    LeftParamB : float
    LeftSurface : SurfaceType
    LeftSurfaceInput : InputType
    Locked : bool
    Massless : bool
    Material : Material
    MaterialVariantSerialized : str
    Name : str
    PivotOffset : CFrame
    Reflectance : float
    RightParamA : float
    RightParamB : float
    RightSurface : SurfaceType
    RightSurfaceInput : InputType
    RootPriority : int
    RotVelocity : Vector3
    size : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    TopParamA : float
    TopParamB : float
    TopSurface : SurfaceType
    TopSurfaceInput : InputType
    Transparency : float
    UniqueId : UniqueId
    Velocity : Vector3
    @property
    def brickColor(self) -> BrickColor: ...
    @brickColor.setter
    def brickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BrickColor(self) -> BrickColor: ...
    @BrickColor.setter
    def BrickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> Color3: ...
    @Color.setter
    def Color(self, value: Color3) -> Color3: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Size(self) -> Vector3: ...
    @Size.setter
    def Size(self, value: Vector3) -> Vector3: ...


class BasePlayerGui(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BaseRemoteEvent(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BaseScript(LuaSourceContainer):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Disabled : bool
    HistoryId : UniqueId
    LinkedSource : ContentId
    Name : str
    RunContext : RunContext
    ScriptGuid : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BaseWrap(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    CageMeshContent : Content
    CageOrigin : CFrame
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    HSRAssetId : ContentId
    HSRData : SharedString
    HSRMeshIdData : SharedString
    ImportOrigin : CFrame
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    TemporaryCageMeshId : ContentId
    UniqueId : UniqueId
    @property
    def CageMeshId(self) -> ContentId: ...
    @CageMeshId.setter
    def CageMeshId(self, value: ContentId) -> ContentId: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Beam(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attachment0 : Attachment
    Attachment1 : Attachment
    Attributes : RbxAttributes
    Brightness : float
    Capabilities : SecurityCapabilities
    Color : ColorSequence
    CurveSize0 : float
    CurveSize1 : float
    DefinesCapabilities : bool
    Enabled : bool
    FaceCamera : bool
    HistoryId : UniqueId
    LightEmission : float
    LightInfluence : float
    Name : str
    Segments : int
    SourceAssetId : int
    Tags : HashSet_1[str]
    Texture : ContentId
    TextureLength : float
    TextureMode : TextureMode
    TextureSpeed : float
    Transparency : NumberSequence
    UniqueId : UniqueId
    Width0 : float
    Width1 : float
    ZOffset : float
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BevelMesh(DataModelMesh):
    Archivable : bool
    Attributes : RbxAttributes
    Bevel : float
    Bevel_Roundness : float
    Bulge : float
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    Offset : Vector3
    Scale : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    VertexColor : Vector3
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BillboardGui(LayerCollector):
    def __init__(self) -> None: ...
    Active : bool
    Adornee : Instance
    AlwaysOnTop : bool
    Archivable : bool
    Attributes : RbxAttributes
    AutoLocalize : bool
    Brightness : float
    Capabilities : SecurityCapabilities
    ClipsDescendants : bool
    DefinesCapabilities : bool
    DistanceLowerLimit : float
    DistanceStep : float
    DistanceUpperLimit : float
    Enabled : bool
    ExtentsOffset : Vector3
    ExtentsOffsetWorldSpace : Vector3
    HistoryId : UniqueId
    LightInfluence : float
    MaxDistance : float
    Name : str
    PlayerToHideFrom : Instance
    ResetOnSpawn : bool
    RootLocalizationTable : LocalizationTable
    SelectionBehaviorDown : SelectionBehavior
    SelectionBehaviorLeft : SelectionBehavior
    SelectionBehaviorRight : SelectionBehavior
    SelectionBehaviorUp : SelectionBehavior
    SelectionGroup : bool
    Size : UDim2
    SizeOffset : Vector2
    SourceAssetId : int
    StudsOffset : Vector3
    StudsOffsetWorldSpace : Vector3
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    ZIndexBehavior : ZIndexBehavior
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Localize(self) -> bool: ...
    @Localize.setter
    def Localize(self, value: bool) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BinaryRobloxFile(RobloxFile):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    MagicHeader : str
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def Chunks(self) -> IReadOnlyList_1[BinaryRobloxFileChunk]: ...
    @property
    def Classes(self) -> Array_1[INST]: ...
    @Classes.setter
    def Classes(self, value: Array_1[INST]) -> Array_1[INST]: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def HasMetadata(self) -> bool: ...
    @property
    def HasSharedStrings(self) -> bool: ...
    @property
    def HasSignatures(self) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Metadata(self) -> Dictionary_2[str, str]: ...
    @property
    def NumClasses(self) -> int: ...
    @NumClasses.setter
    def NumClasses(self, value: int) -> int: ...
    @property
    def NumObjects(self) -> int: ...
    @NumObjects.setter
    def NumObjects(self, value: int) -> int: ...
    @property
    def Objects(self) -> Array_1[RbxObject]: ...
    @Objects.setter
    def Objects(self, value: Array_1[RbxObject]) -> Array_1[RbxObject]: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Reserved(self) -> int: ...
    @Reserved.setter
    def Reserved(self, value: int) -> int: ...
    @property
    def SharedStrings(self) -> IReadOnlyDictionary_2[int, SharedString]: ...
    @property
    def Signatures(self) -> IReadOnlyList_1[RbxSignature]: ...
    @property
    def Version(self) -> int: ...
    @Version.setter
    def Version(self, value: int) -> int: ...
    def Save(self, stream: Stream) -> None: ...
    def ToString(self) -> str: ...


class BinaryStringValue(ValueBase):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Value : Array_1[int]
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BindableEvent(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BindableFunction(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BlockMesh(BevelMesh):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Bevel : float
    Bevel_Roundness : float
    Bulge : float
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    Offset : Vector3
    Scale : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    VertexColor : Vector3
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BloomEffect(PostEffect):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Intensity : float
    Name : str
    Size : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    Threshold : float
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BlurEffect(PostEffect):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    Size : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BodyAngularVelocity(BodyMover):
    def __init__(self) -> None: ...
    AngularVelocity : Vector3
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    MaxTorque : Vector3
    Name : str
    P : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def angularvelocity(self) -> Vector3: ...
    @angularvelocity.setter
    def angularvelocity(self, value: Vector3) -> Vector3: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def maxTorque(self) -> Vector3: ...
    @maxTorque.setter
    def maxTorque(self, value: Vector3) -> Vector3: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BodyColors(CharacterAppearance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HeadColor3 : Color3
    HistoryId : UniqueId
    LeftArmColor3 : Color3
    LeftLegColor3 : Color3
    Name : str
    RightArmColor3 : Color3
    RightLegColor3 : Color3
    SourceAssetId : int
    Tags : HashSet_1[str]
    TorsoColor3 : Color3
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def HeadColor(self) -> BrickColor: ...
    @HeadColor.setter
    def HeadColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def LeftArmColor(self) -> BrickColor: ...
    @LeftArmColor.setter
    def LeftArmColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def LeftLegColor(self) -> BrickColor: ...
    @LeftLegColor.setter
    def LeftLegColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def RightArmColor(self) -> BrickColor: ...
    @RightArmColor.setter
    def RightArmColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def RightLegColor(self) -> BrickColor: ...
    @RightLegColor.setter
    def RightLegColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def TorsoColor(self) -> BrickColor: ...
    @TorsoColor.setter
    def TorsoColor(self, value: BrickColor) -> BrickColor: ...


class BodyForce(BodyMover):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Force : Vector3
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def force(self) -> Vector3: ...
    @force.setter
    def force(self, value: Vector3) -> Vector3: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BodyGyro(BodyMover):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    CFrame : CFrame
    D : float
    DefinesCapabilities : bool
    HistoryId : UniqueId
    MaxTorque : Vector3
    Name : str
    P : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def cframe(self) -> CFrame: ...
    @cframe.setter
    def cframe(self, value: CFrame) -> CFrame: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def maxTorque(self) -> Vector3: ...
    @maxTorque.setter
    def maxTorque(self, value: Vector3) -> Vector3: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BodyMover(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BodyPartDescription(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    AssetId : int
    Attributes : RbxAttributes
    BodyPart : BodyPart
    Capabilities : SecurityCapabilities
    Color : Color3
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Instance : Instance
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BodyPosition(BodyMover):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    D : float
    DefinesCapabilities : bool
    HistoryId : UniqueId
    MaxForce : Vector3
    Name : str
    P : float
    Position : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def maxForce(self) -> Vector3: ...
    @maxForce.setter
    def maxForce(self, value: Vector3) -> Vector3: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def position(self) -> Vector3: ...
    @position.setter
    def position(self, value: Vector3) -> Vector3: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BodyThrust(BodyMover):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Force : Vector3
    HistoryId : UniqueId
    Location : Vector3
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def force(self) -> Vector3: ...
    @force.setter
    def force(self, value: Vector3) -> Vector3: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def location(self) -> Vector3: ...
    @location.setter
    def location(self, value: Vector3) -> Vector3: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BodyVelocity(BodyMover):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    MaxForce : Vector3
    Name : str
    P : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Velocity : Vector3
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def maxForce(self) -> Vector3: ...
    @maxForce.setter
    def maxForce(self, value: Vector3) -> Vector3: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def velocity(self) -> Vector3: ...
    @velocity.setter
    def velocity(self, value: Vector3) -> Vector3: ...


class Bone(Attachment):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    CFrame : CFrame
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BoolValue(ValueBase):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Value : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BoxHandleAdornment(HandleAdornment):
    def __init__(self) -> None: ...
    AdornCullingMode : AdornCullingMode
    Adornee : PVInstance
    AlwaysOnTop : bool
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    CFrame : CFrame
    Color3 : Color3
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    Size : Vector3
    SizeRelativeOffset : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    Transparency : float
    UniqueId : UniqueId
    Visible : bool
    ZIndex : int
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> BrickColor: ...
    @Color.setter
    def Color(self, value: BrickColor) -> BrickColor: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Breakpoint(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BrickColorValue(ValueBase):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Value : BrickColor
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BrowserService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BubbleChatConfiguration(TextChatConfigurations):
    def __init__(self) -> None: ...
    AdorneeName : str
    Archivable : bool
    Attributes : RbxAttributes
    BackgroundColor3 : Color3
    BackgroundTransparency : float
    BubbleDuration : float
    BubblesSpacing : float
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    Font : Font
    FontFace : FontFace
    HistoryId : UniqueId
    LocalPlayerStudsOffset : Vector3
    MaxBubbles : float
    MaxDistance : float
    MinimizeDistance : float
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    TailVisible : bool
    TextColor3 : Color3
    TextSize : int
    UniqueId : UniqueId
    VerticalStudsOffset : float
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BubbleChatMessageProperties(TextChatMessageProperties):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BugReporterService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BulkImportService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class BuoyancySensor(SensorBase):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    FullySubmerged : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    TouchingSurface : bool
    UniqueId : UniqueId
    UpdateType : SensorUpdateType
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CacheableContentProvider(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CalloutService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Camera(PVInstance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    CameraSubject : Instance
    CameraType : CameraType
    Capabilities : SecurityCapabilities
    CFrame : CFrame
    DefinesCapabilities : bool
    FieldOfView : float
    FieldOfViewMode : FieldOfViewMode
    Focus : CFrame
    HeadLocked : bool
    HeadScale : float
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    VRTiltAndRollEnabled : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def CoordinateFrame(self) -> CFrame: ...
    @CoordinateFrame.setter
    def CoordinateFrame(self, value: CFrame) -> CFrame: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def focus(self) -> CFrame: ...
    @focus.setter
    def focus(self, value: CFrame) -> CFrame: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CanvasGroup(GuiObject):
    def __init__(self) -> None: ...
    Active : bool
    AnchorPoint : Vector2
    Archivable : bool
    Attributes : RbxAttributes
    AutoLocalize : bool
    AutomaticSize : AutomaticSize
    BackgroundColor3 : Color3
    BackgroundTransparency : float
    BorderColor3 : Color3
    BorderMode : BorderMode
    BorderSizePixel : int
    Capabilities : SecurityCapabilities
    ClipsDescendants : bool
    DefinesCapabilities : bool
    Draggable : bool
    GroupColor3 : Color3
    GroupTransparency : float
    HistoryId : UniqueId
    Interactable : bool
    LayoutOrder : int
    Name : str
    NextSelectionDown : GuiObject
    NextSelectionLeft : GuiObject
    NextSelectionRight : GuiObject
    NextSelectionUp : GuiObject
    Position : UDim2
    RootLocalizationTable : LocalizationTable
    Rotation : float
    Selectable : bool
    SelectionBehaviorDown : SelectionBehavior
    SelectionBehaviorLeft : SelectionBehavior
    SelectionBehaviorRight : SelectionBehavior
    SelectionBehaviorUp : SelectionBehavior
    SelectionGroup : bool
    SelectionImageObject : GuiObject
    SelectionOrder : int
    Size : UDim2
    SizeConstraint : SizeConstraint
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Visible : bool
    ZIndex : int
    @property
    def BackgroundColor(self) -> BrickColor: ...
    @BackgroundColor.setter
    def BackgroundColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BorderColor(self) -> BrickColor: ...
    @BorderColor.setter
    def BorderColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Localize(self) -> bool: ...
    @Localize.setter
    def Localize(self, value: bool) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Transparency(self) -> float: ...
    @Transparency.setter
    def Transparency(self, value: float) -> float: ...


class CaptureService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CFrameValue(ValueBase):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Value : CFrame
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ChangeHistoryService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ChannelSelectorSoundEffect(CustomSoundEffect):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Channel : int
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    Priority : int
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ChannelTabsConfiguration(TextChatConfigurations):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    BackgroundColor3 : Color3
    BackgroundTransparency : float
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    FontFace : FontFace
    HistoryId : UniqueId
    HoverBackgroundColor3 : Color3
    Name : str
    SelectedTabTextColor3 : Color3
    SourceAssetId : int
    Tags : HashSet_1[str]
    TextColor3 : Color3
    TextSize : int
    TextStrokeColor3 : Color3
    TextStrokeTransparency : float
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CharacterAppearance(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CharacterMesh(CharacterAppearance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    BaseTextureId : int
    BodyPart : BodyPart
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    MeshId : int
    Name : str
    OverlayTextureId : int
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Chat(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    BubbleChatEnabled : bool
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    IsAutoMigrated : bool
    LoadDefaultChat : bool
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ChatbotUIService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ChatInputBarConfiguration(TextChatConfigurations):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    AutocompleteEnabled : bool
    BackgroundColor3 : Color3
    BackgroundTransparency : float
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    FontFace : FontFace
    HistoryId : UniqueId
    KeyboardKeyCode : KeyCode
    Name : str
    PlaceholderColor3 : Color3
    SourceAssetId : int
    Tags : HashSet_1[str]
    TargetTextChannel : TextChannel
    TextColor3 : Color3
    TextSize : int
    TextStrokeColor3 : Color3
    TextStrokeTransparency : float
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ChatWindowConfiguration(TextChatConfigurations):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    BackgroundColor3 : Color3
    BackgroundTransparency : float
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    FontFace : FontFace
    HeightScale : float
    HistoryId : UniqueId
    HorizontalAlignment : HorizontalAlignment
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    TextColor3 : Color3
    TextSize : int
    TextStrokeColor3 : Color3
    TextStrokeTransparency : float
    UniqueId : UniqueId
    VerticalAlignment : VerticalAlignment
    WidthScale : float
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ChorusSoundEffect(SoundEffect):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Depth : float
    Enabled : bool
    HistoryId : UniqueId
    Mix : float
    Name : str
    Priority : int
    Rate : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ClickDetector(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    CursorIcon : ContentId
    DefinesCapabilities : bool
    HistoryId : UniqueId
    MaxActivationDistance : float
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ClimbController(ControllerBase):
    def __init__(self) -> None: ...
    AccelerationTime : float
    Archivable : bool
    Attributes : RbxAttributes
    BalanceMaxTorque : float
    BalanceRigidityEnabled : bool
    BalanceSpeed : float
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    MoveMaxForce : float
    MoveSpeedFactor : float
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Clothing(CharacterAppearance):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color3 : Color3
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CloudCRUDService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Clouds(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color : Color3
    Cover : float
    DefinesCapabilities : bool
    Density : float
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ClusterPacketCache(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CollaboratorsService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CollectionService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Color3Value(ValueBase):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Value : Color3
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ColorCorrectionEffect(PostEffect):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Brightness : float
    Capabilities : SecurityCapabilities
    Contrast : float
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    Saturation : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    TintColor : Color3
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ColorGradingEffect(PostEffect):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    TonemapperPreset : TonemapperPreset
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CommandService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CommerceService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CompressorSoundEffect(SoundEffect):
    def __init__(self) -> None: ...
    Archivable : bool
    Attack : float
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    GainMakeup : float
    HistoryId : UniqueId
    Name : str
    Priority : int
    Ratio : float
    Release : float
    SideChain : Instance
    SourceAssetId : int
    Tags : HashSet_1[str]
    Threshold : float
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ConeHandleAdornment(HandleAdornment):
    def __init__(self) -> None: ...
    AdornCullingMode : AdornCullingMode
    Adornee : PVInstance
    AlwaysOnTop : bool
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    CFrame : CFrame
    Color3 : Color3
    DefinesCapabilities : bool
    Height : float
    HistoryId : UniqueId
    Name : str
    Radius : float
    SizeRelativeOffset : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    Transparency : float
    UniqueId : UniqueId
    Visible : bool
    ZIndex : int
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> BrickColor: ...
    @Color.setter
    def Color(self, value: BrickColor) -> BrickColor: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ConfigService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Configuration(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ConfigureServerService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ConnectivityService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Constraint(Instance, abc.ABC):
    Archivable : bool
    Attachment0 : Attachment
    Attachment1 : Attachment
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color : BrickColor
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ContentProvider(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ContextActionService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Controller(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ControllerBase(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    BalanceRigidityEnabled : bool
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    MoveSpeedFactor : float
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ControllerManager(Instance):
    def __init__(self) -> None: ...
    ActiveController : ControllerBase
    Archivable : bool
    Attributes : RbxAttributes
    BaseMoveSpeed : float
    BaseTurnSpeed : float
    Capabilities : SecurityCapabilities
    ClimbSensor : ControllerSensor
    DefinesCapabilities : bool
    FacingDirection : Vector3
    GroundSensor : ControllerSensor
    HistoryId : UniqueId
    MovingDirection : Vector3
    Name : str
    RootPart : BasePart
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    UpDirection : Vector3
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ControllerPartSensor(ControllerSensor):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    HitFrame : CFrame
    HitNormal : Vector3
    Name : str
    SearchDistance : float
    SensedPart : BasePart
    SensorMode : SensorMode
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    UpdateType : SensorUpdateType
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ControllerSensor(SensorBase):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    UpdateType : SensorUpdateType
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ControllerService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ConversationalAIAcceptanceService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CookiesService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CoreGui(BasePlayerGui):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SelectionImageObject : GuiObject
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CorePackages(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CoreScriptDebuggingManagerHelper(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CoreScriptSyncService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CornerWedgePart(BasePart):
    def __init__(self) -> None: ...
    Anchored : bool
    Archivable : bool
    Attributes : RbxAttributes
    AudioCanCollide : bool
    BackParamA : float
    BackParamB : float
    BackSurface : SurfaceType
    BackSurfaceInput : InputType
    BottomParamA : float
    BottomParamB : float
    BottomSurface : SurfaceType
    BottomSurfaceInput : InputType
    CanCollide : bool
    CanQuery : bool
    CanTouch : bool
    Capabilities : SecurityCapabilities
    CastShadow : bool
    CFrame : CFrame
    CollisionGroup : str
    CollisionGroupId : int
    Color3uint8 : Color3uint8
    CustomPhysicalProperties : PhysicalProperties
    DefinesCapabilities : bool
    Elasticity : float
    EnableFluidForces : bool
    Friction : float
    FrontParamA : float
    FrontParamB : float
    FrontSurface : SurfaceType
    FrontSurfaceInput : InputType
    HistoryId : UniqueId
    LeftParamA : float
    LeftParamB : float
    LeftSurface : SurfaceType
    LeftSurfaceInput : InputType
    Locked : bool
    Massless : bool
    Material : Material
    MaterialVariantSerialized : str
    Name : str
    PivotOffset : CFrame
    Reflectance : float
    RightParamA : float
    RightParamB : float
    RightSurface : SurfaceType
    RightSurfaceInput : InputType
    RootPriority : int
    RotVelocity : Vector3
    size : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    TopParamA : float
    TopParamB : float
    TopSurface : SurfaceType
    TopSurfaceInput : InputType
    Transparency : float
    UniqueId : UniqueId
    Velocity : Vector3
    @property
    def brickColor(self) -> BrickColor: ...
    @brickColor.setter
    def brickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BrickColor(self) -> BrickColor: ...
    @BrickColor.setter
    def BrickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> Color3: ...
    @Color.setter
    def Color(self, value: Color3) -> Color3: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Size(self) -> Vector3: ...
    @Size.setter
    def Size(self, value: Vector3) -> Vector3: ...


class CreationDBService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CreatorStoreService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CrossDMScriptChangeListener(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CSGDictionaryService(FlyweightService):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CurveAnimation(AnimationClip):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    GuidBinaryString : Array_1[int]
    HistoryId : UniqueId
    Loop : bool
    Name : str
    Priority : AnimationPriority
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CustomEvent(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    PersistedCurrentValue : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CustomEventReceiver(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    Source : Instance
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CustomLog(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CustomSoundEffect(SoundEffect):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    Priority : int
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CylinderHandleAdornment(HandleAdornment):
    def __init__(self) -> None: ...
    AdornCullingMode : AdornCullingMode
    Adornee : PVInstance
    AlwaysOnTop : bool
    Angle : float
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    CFrame : CFrame
    Color3 : Color3
    DefinesCapabilities : bool
    Height : float
    HistoryId : UniqueId
    InnerRadius : float
    Name : str
    Radius : float
    SizeRelativeOffset : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    Transparency : float
    UniqueId : UniqueId
    Visible : bool
    ZIndex : int
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> BrickColor: ...
    @Color.setter
    def Color(self, value: BrickColor) -> BrickColor: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CylinderMesh(BevelMesh):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Bevel : float
    Bevel_Roundness : float
    Bulge : float
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    Offset : Vector3
    Scale : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    VertexColor : Vector3
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class CylindricalConstraint(SlidingBallConstraint):
    def __init__(self) -> None: ...
    ActuatorType : ActuatorType
    AngularActuatorType : ActuatorType
    AngularLimitsEnabled : bool
    AngularResponsiveness : float
    AngularRestitution : float
    AngularSpeed : float
    AngularVelocity : float
    Archivable : bool
    Attachment0 : Attachment
    Attachment1 : Attachment
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color : BrickColor
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    InclinationAngle : float
    LimitsEnabled : bool
    LinearResponsiveness : float
    LowerAngle : float
    LowerLimit : float
    MotorMaxAcceleration : float
    MotorMaxAngularAcceleration : float
    MotorMaxForce : float
    MotorMaxTorque : float
    Name : str
    Restitution : float
    RotationAxisVisible : bool
    ServoMaxForce : float
    ServoMaxTorque : float
    Size : float
    SoftlockAngularServoUponReachingTarget : bool
    SoftlockServoUponReachingTarget : bool
    SourceAssetId : int
    Speed : float
    Tags : HashSet_1[str]
    TargetAngle : float
    TargetPosition : float
    UniqueId : UniqueId
    UpperAngle : float
    UpperLimit : float
    Velocity : float
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class DataModelMesh(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    Offset : Vector3
    Scale : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    VertexColor : Vector3
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class DataModelPatchService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class DataStoreGetOptions(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    UseCache : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class DataStoreIncrementOptions(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class DataStoreOptions(Instance):
    def __init__(self) -> None: ...
    AllScopes : bool
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class DataStoreService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    AutomaticRetry : bool
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    LegacyNamingScheme : bool
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class DataStoreSetOptions(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Debris(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    MaxItems : int
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class DebuggablePluginWatcher(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class DebuggerConnectionManager(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    Timeout : float
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class DebuggerManager(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class DebuggerUIService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class DebuggerWatch(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Expression : str
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Decal(FaceInstance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color3 : Color3
    DefinesCapabilities : bool
    Face : NormalId
    HistoryId : UniqueId
    Name : str
    Shiny : float
    SourceAssetId : int
    Specular : float
    Tags : HashSet_1[str]
    TextureContent : Content
    Transparency : float
    UniqueId : UniqueId
    ZIndex : int
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Texture(self) -> ContentId: ...
    @Texture.setter
    def Texture(self, value: ContentId) -> ContentId: ...


class DepthOfFieldEffect(PostEffect):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    FarIntensity : float
    FocusDistance : float
    HistoryId : UniqueId
    InFocusRadius : float
    Name : str
    NearIntensity : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class DeviceIdService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Dialog(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    BehaviorType : DialogBehaviorType
    Capabilities : SecurityCapabilities
    ConversationDistance : float
    DefinesCapabilities : bool
    GoodbyeChoiceActive : bool
    GoodbyeDialog : str
    HistoryId : UniqueId
    InitialPrompt : str
    Name : str
    Purpose : DialogPurpose
    SourceAssetId : int
    Tags : HashSet_1[str]
    Tone : DialogTone
    TriggerDistance : float
    TriggerOffset : Vector3
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class DialogChoice(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    GoodbyeChoiceActive : bool
    GoodbyeDialog : str
    HistoryId : UniqueId
    Name : str
    ResponseDialog : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    UserDialog : str
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class DistortionSoundEffect(SoundEffect):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Level : float
    Name : str
    Priority : int
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class DoubleConstrainedValue(ValueBase):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    MaxValue : float
    MinValue : float
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    value : float
    @property
    def ClassName(self) -> str: ...
    @property
    def ConstrainedValue(self) -> float: ...
    @ConstrainedValue.setter
    def ConstrainedValue(self, value: float) -> float: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Value(self) -> float: ...
    @Value.setter
    def Value(self, value: float) -> float: ...


class DraftsService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class DragDetector(ClickDetector):
    def __init__(self) -> None: ...
    ActivatedCursorIcon : ContentId
    ApplyAtCenterOfMass : bool
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    CursorIcon : ContentId
    DefinesCapabilities : bool
    DragFrame : CFrame
    DragStyle : DragDetectorDragStyle
    Enabled : bool
    GamepadModeSwitchKeyCode : KeyCode
    HistoryId : UniqueId
    KeyboardModeSwitchKeyCode : KeyCode
    MaxActivationDistance : float
    MaxDragAngle : float
    MaxDragTranslation : Vector3
    MaxForce : float
    MaxTorque : float
    MinDragAngle : float
    MinDragTranslation : Vector3
    Name : str
    Orientation : Vector3
    PermissionPolicy : DragDetectorPermissionPolicy
    ReferenceInstance : Instance
    ResponseStyle : DragDetectorResponseStyle
    Responsiveness : float
    RunLocally : bool
    SourceAssetId : int
    Tags : HashSet_1[str]
    TrackballRadialPullFactor : float
    TrackballRollFactor : float
    UniqueId : UniqueId
    VRSwitchKeyCode : KeyCode
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Dragger(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class DraggerService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class DynamicRotate(JointInstance):
    Archivable : bool
    Attributes : RbxAttributes
    BaseAngle : float
    C0 : CFrame
    C1 : CFrame
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    Part0 : BasePart
    Part1 : BasePart
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class EchoSoundEffect(SoundEffect):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Delay : float
    DryLevel : float
    Enabled : bool
    Feedback : float
    HistoryId : UniqueId
    Name : str
    Priority : int
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    WetLevel : float
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class EditableImage(RbxObject):
    def __init__(self) -> None: ...
    ImageData : Array_1[int]
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class EditableMesh(RbxObject):
    def __init__(self) -> None: ...
    MeshData : SharedString
    SkinningEnabled : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class EditableService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class EqualizerSoundEffect(SoundEffect):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HighGain : float
    HistoryId : UniqueId
    LowGain : float
    MidGain : float
    Name : str
    Priority : int
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class EulerRotationCurve(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    RotationOrder : RotationOrder
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class EventIngestService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ExampleService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ExperienceAuthService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ExperienceInviteOptions(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    InviteMessageId : str
    InviteUser : int
    LaunchData : str
    Name : str
    PromptMessage : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ExperienceNotificationService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ExperienceService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ExperienceStateCaptureService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ExplorerFilter(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ExplorerServiceVisibilityService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Explosion(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    BlastPressure : float
    BlastRadius : float
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    DestroyJointRadiusPercent : float
    ExplosionType : ExplosionType
    HistoryId : UniqueId
    Name : str
    Position : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    TimeScale : float
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class FaceAnimatorService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class FaceControls(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class FaceInstance(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Face : NormalId
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class FacialAgeEstimationService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class FacialAnimationRecordingService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class FacialAnimationStreamingServiceV2(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    ServiceState : int
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Feature(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    FaceId : NormalId
    HistoryId : UniqueId
    InOut : InOut
    LeftRight : LeftRight
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    TopBottom : TopBottom
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class FeatureRestrictionManager(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class FeedService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class FileMesh(DataModelMesh):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    MeshId : ContentId
    Name : str
    Offset : Vector3
    Scale : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    TextureId : ContentId
    UniqueId : UniqueId
    VertexColor : Vector3
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Fire(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color : Color3
    DefinesCapabilities : bool
    Enabled : bool
    heat_xml : float
    HistoryId : UniqueId
    Name : str
    SecondaryColor : Color3
    size_xml : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    TimeScale : float
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def Heat(self) -> float: ...
    @Heat.setter
    def Heat(self, value: float) -> float: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def size(self) -> float: ...
    @size.setter
    def size(self, value: float) -> float: ...
    @property
    def Size(self) -> float: ...
    @Size.setter
    def Size(self, value: float) -> float: ...


class Flag(Tool):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    CanBeDropped : bool
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    Grip : CFrame
    HistoryId : UniqueId
    LevelOfDetail : ModelLevelOfDetail
    ManualActivationOnly : bool
    ModelMeshCFrame : CFrame
    ModelMeshData : SharedString
    ModelMeshSize : Vector3
    ModelStreamingMode : ModelStreamingMode
    Name : str
    NeedsPivotMigration : bool
    PrimaryPart : BasePart
    RequiresHandle : bool
    ScaleFactor : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    TeamColor : BrickColor
    TextureId : ContentId
    ToolTip : str
    UniqueId : UniqueId
    WorldPivotData : Optional_1[CFrame]
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class FlagStand(Part):
    def __init__(self) -> None: ...
    Anchored : bool
    Archivable : bool
    Attributes : RbxAttributes
    AudioCanCollide : bool
    BackParamA : float
    BackParamB : float
    BackSurface : SurfaceType
    BackSurfaceInput : InputType
    BottomParamA : float
    BottomParamB : float
    BottomSurface : SurfaceType
    BottomSurfaceInput : InputType
    CanCollide : bool
    CanQuery : bool
    CanTouch : bool
    Capabilities : SecurityCapabilities
    CastShadow : bool
    CFrame : CFrame
    CollisionGroup : str
    CollisionGroupId : int
    Color3uint8 : Color3uint8
    CustomPhysicalProperties : PhysicalProperties
    DefinesCapabilities : bool
    Elasticity : float
    EnableFluidForces : bool
    formFactorRaw : FormFactor
    Friction : float
    FrontParamA : float
    FrontParamB : float
    FrontSurface : SurfaceType
    FrontSurfaceInput : InputType
    HistoryId : UniqueId
    LeftParamA : float
    LeftParamB : float
    LeftSurface : SurfaceType
    LeftSurfaceInput : InputType
    Locked : bool
    Massless : bool
    Material : Material
    MaterialVariantSerialized : str
    Name : str
    PivotOffset : CFrame
    Reflectance : float
    RightParamA : float
    RightParamB : float
    RightSurface : SurfaceType
    RightSurfaceInput : InputType
    RootPriority : int
    RotVelocity : Vector3
    shape : PartType
    size : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    TeamColor : BrickColor
    TopParamA : float
    TopParamB : float
    TopSurface : SurfaceType
    TopSurfaceInput : InputType
    Transparency : float
    UniqueId : UniqueId
    Velocity : Vector3
    @property
    def brickColor(self) -> BrickColor: ...
    @brickColor.setter
    def brickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BrickColor(self) -> BrickColor: ...
    @BrickColor.setter
    def BrickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> Color3: ...
    @Color.setter
    def Color(self, value: Color3) -> Color3: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def formFactor(self) -> FormFactor: ...
    @formFactor.setter
    def formFactor(self, value: FormFactor) -> FormFactor: ...
    @property
    def FormFactor(self) -> FormFactor: ...
    @FormFactor.setter
    def FormFactor(self, value: FormFactor) -> FormFactor: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Shape(self) -> PartType: ...
    @Shape.setter
    def Shape(self, value: PartType) -> PartType: ...
    @property
    def Size(self) -> Vector3: ...
    @Size.setter
    def Size(self, value: Vector3) -> Vector3: ...


class FlagStandService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class FlangeSoundEffect(SoundEffect):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Depth : float
    Enabled : bool
    HistoryId : UniqueId
    Mix : float
    Name : str
    Priority : int
    Rate : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class FloatCurve(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    ValuesAndTimes : Array_1[int]
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class FloorWire(GuiBase3d):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color3 : Color3
    CycleOffset : float
    DefinesCapabilities : bool
    From : BasePart
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    StudsBetweenTextures : float
    Tags : HashSet_1[str]
    Texture : ContentId
    TextureSize : Vector2
    To : BasePart
    Transparency : float
    UniqueId : UniqueId
    Velocity : float
    Visible : bool
    WireRadius : float
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> BrickColor: ...
    @Color.setter
    def Color(self, value: BrickColor) -> BrickColor: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class FluidForceSensor(SensorBase):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    UpdateType : SensorUpdateType
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class FlyweightService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Folder(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ForceField(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class FormFactorPart(BasePart):
    def __init__(self) -> None: ...
    Anchored : bool
    Archivable : bool
    Attributes : RbxAttributes
    AudioCanCollide : bool
    BackParamA : float
    BackParamB : float
    BackSurface : SurfaceType
    BackSurfaceInput : InputType
    BottomParamA : float
    BottomParamB : float
    BottomSurface : SurfaceType
    BottomSurfaceInput : InputType
    CanCollide : bool
    CanQuery : bool
    CanTouch : bool
    Capabilities : SecurityCapabilities
    CastShadow : bool
    CFrame : CFrame
    CollisionGroup : str
    CollisionGroupId : int
    Color3uint8 : Color3uint8
    CustomPhysicalProperties : PhysicalProperties
    DefinesCapabilities : bool
    Elasticity : float
    EnableFluidForces : bool
    formFactorRaw : FormFactor
    Friction : float
    FrontParamA : float
    FrontParamB : float
    FrontSurface : SurfaceType
    FrontSurfaceInput : InputType
    HistoryId : UniqueId
    LeftParamA : float
    LeftParamB : float
    LeftSurface : SurfaceType
    LeftSurfaceInput : InputType
    Locked : bool
    Massless : bool
    Material : Material
    MaterialVariantSerialized : str
    Name : str
    PivotOffset : CFrame
    Reflectance : float
    RightParamA : float
    RightParamB : float
    RightSurface : SurfaceType
    RightSurfaceInput : InputType
    RootPriority : int
    RotVelocity : Vector3
    size : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    TopParamA : float
    TopParamB : float
    TopSurface : SurfaceType
    TopSurfaceInput : InputType
    Transparency : float
    UniqueId : UniqueId
    Velocity : Vector3
    @property
    def brickColor(self) -> BrickColor: ...
    @brickColor.setter
    def brickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BrickColor(self) -> BrickColor: ...
    @BrickColor.setter
    def BrickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> Color3: ...
    @Color.setter
    def Color(self, value: Color3) -> Color3: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def formFactor(self) -> FormFactor: ...
    @formFactor.setter
    def formFactor(self, value: FormFactor) -> FormFactor: ...
    @property
    def FormFactor(self) -> FormFactor: ...
    @FormFactor.setter
    def FormFactor(self, value: FormFactor) -> FormFactor: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Size(self) -> Vector3: ...
    @Size.setter
    def Size(self, value: Vector3) -> Vector3: ...


class Frame(GuiObject):
    def __init__(self) -> None: ...
    Active : bool
    AnchorPoint : Vector2
    Archivable : bool
    Attributes : RbxAttributes
    AutoLocalize : bool
    AutomaticSize : AutomaticSize
    BackgroundColor3 : Color3
    BackgroundTransparency : float
    BorderColor3 : Color3
    BorderMode : BorderMode
    BorderSizePixel : int
    Capabilities : SecurityCapabilities
    ClipsDescendants : bool
    DefinesCapabilities : bool
    Draggable : bool
    HistoryId : UniqueId
    Interactable : bool
    LayoutOrder : int
    Name : str
    NextSelectionDown : GuiObject
    NextSelectionLeft : GuiObject
    NextSelectionRight : GuiObject
    NextSelectionUp : GuiObject
    Position : UDim2
    RootLocalizationTable : LocalizationTable
    Rotation : float
    Selectable : bool
    SelectionBehaviorDown : SelectionBehavior
    SelectionBehaviorLeft : SelectionBehavior
    SelectionBehaviorRight : SelectionBehavior
    SelectionBehaviorUp : SelectionBehavior
    SelectionGroup : bool
    SelectionImageObject : GuiObject
    SelectionOrder : int
    Size : UDim2
    SizeConstraint : SizeConstraint
    SourceAssetId : int
    Style : FrameStyle
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Visible : bool
    ZIndex : int
    @property
    def BackgroundColor(self) -> BrickColor: ...
    @BackgroundColor.setter
    def BackgroundColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BorderColor(self) -> BrickColor: ...
    @BorderColor.setter
    def BorderColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Localize(self) -> bool: ...
    @Localize.setter
    def Localize(self, value: bool) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Transparency(self) -> float: ...
    @Transparency.setter
    def Transparency(self, value: float) -> float: ...


class FriendService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class FunctionalTest(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Description : str
    HasMigratedSettingsToTestService : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class GamepadService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    GamepadCursorEnabled : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class GamePassService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class GenerationService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class GenericChallengeService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Geometry(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class GeometryService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class GetTextBoundsParams(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Font : FontFace
    HistoryId : UniqueId
    Name : str
    RichText : bool
    Size : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    Text : str
    UniqueId : UniqueId
    Width : float
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Glue(JointInstance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    C0 : CFrame
    C1 : CFrame
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    F0 : Vector3
    F1 : Vector3
    F2 : Vector3
    F3 : Vector3
    HistoryId : UniqueId
    Name : str
    Part0 : BasePart
    Part1 : BasePart
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class GroundController(ControllerBase):
    def __init__(self) -> None: ...
    AccelerationLean : float
    AccelerationTime : float
    Archivable : bool
    Attributes : RbxAttributes
    BalanceMaxTorque : float
    BalanceRigidityEnabled : bool
    BalanceSpeed : float
    Capabilities : SecurityCapabilities
    DecelerationTime : float
    DefinesCapabilities : bool
    Friction : float
    FrictionWeight : float
    GroundOffset : float
    HistoryId : UniqueId
    MoveSpeedFactor : float
    Name : str
    SourceAssetId : int
    StandForce : float
    StandSpeed : float
    Tags : HashSet_1[str]
    TurnSpeedFactor : float
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class GroupService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class GuiBase(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class GuiBase2d(GuiBase):
    Archivable : bool
    Attributes : RbxAttributes
    AutoLocalize : bool
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    RootLocalizationTable : LocalizationTable
    SelectionBehaviorDown : SelectionBehavior
    SelectionBehaviorLeft : SelectionBehavior
    SelectionBehaviorRight : SelectionBehavior
    SelectionBehaviorUp : SelectionBehavior
    SelectionGroup : bool
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Localize(self) -> bool: ...
    @Localize.setter
    def Localize(self, value: bool) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class GuiBase3d(GuiBase):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color3 : Color3
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    Transparency : float
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> BrickColor: ...
    @Color.setter
    def Color(self, value: BrickColor) -> BrickColor: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class GuiButton(GuiObject):
    def __init__(self) -> None: ...
    Active : bool
    AnchorPoint : Vector2
    Archivable : bool
    Attributes : RbxAttributes
    AutoButtonColor : bool
    AutoLocalize : bool
    AutomaticSize : AutomaticSize
    BackgroundColor3 : Color3
    BackgroundTransparency : float
    BorderColor3 : Color3
    BorderMode : BorderMode
    BorderSizePixel : int
    Capabilities : SecurityCapabilities
    ClipsDescendants : bool
    DefinesCapabilities : bool
    Draggable : bool
    HistoryId : UniqueId
    HoverHapticEffect : HapticEffect
    Interactable : bool
    LayoutOrder : int
    Modal : bool
    Name : str
    NextSelectionDown : GuiObject
    NextSelectionLeft : GuiObject
    NextSelectionRight : GuiObject
    NextSelectionUp : GuiObject
    Position : UDim2
    PressHapticEffect : HapticEffect
    RootLocalizationTable : LocalizationTable
    Rotation : float
    Selectable : bool
    Selected : bool
    SelectionBehaviorDown : SelectionBehavior
    SelectionBehaviorLeft : SelectionBehavior
    SelectionBehaviorRight : SelectionBehavior
    SelectionBehaviorUp : SelectionBehavior
    SelectionGroup : bool
    SelectionImageObject : GuiObject
    SelectionOrder : int
    Size : UDim2
    SizeConstraint : SizeConstraint
    SourceAssetId : int
    Style : ButtonStyle
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Visible : bool
    ZIndex : int
    @property
    def BackgroundColor(self) -> BrickColor: ...
    @BackgroundColor.setter
    def BackgroundColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BorderColor(self) -> BrickColor: ...
    @BorderColor.setter
    def BorderColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Localize(self) -> bool: ...
    @Localize.setter
    def Localize(self, value: bool) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Transparency(self) -> float: ...
    @Transparency.setter
    def Transparency(self, value: float) -> float: ...


class GuidRegistryService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class GuiLabel(GuiObject):
    def __init__(self) -> None: ...
    Active : bool
    AnchorPoint : Vector2
    Archivable : bool
    Attributes : RbxAttributes
    AutoLocalize : bool
    AutomaticSize : AutomaticSize
    BackgroundColor3 : Color3
    BackgroundTransparency : float
    BorderColor3 : Color3
    BorderMode : BorderMode
    BorderSizePixel : int
    Capabilities : SecurityCapabilities
    ClipsDescendants : bool
    DefinesCapabilities : bool
    Draggable : bool
    HistoryId : UniqueId
    Interactable : bool
    LayoutOrder : int
    Name : str
    NextSelectionDown : GuiObject
    NextSelectionLeft : GuiObject
    NextSelectionRight : GuiObject
    NextSelectionUp : GuiObject
    Position : UDim2
    RootLocalizationTable : LocalizationTable
    Rotation : float
    Selectable : bool
    SelectionBehaviorDown : SelectionBehavior
    SelectionBehaviorLeft : SelectionBehavior
    SelectionBehaviorRight : SelectionBehavior
    SelectionBehaviorUp : SelectionBehavior
    SelectionGroup : bool
    SelectionImageObject : GuiObject
    SelectionOrder : int
    Size : UDim2
    SizeConstraint : SizeConstraint
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Visible : bool
    ZIndex : int
    @property
    def BackgroundColor(self) -> BrickColor: ...
    @BackgroundColor.setter
    def BackgroundColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BorderColor(self) -> BrickColor: ...
    @BorderColor.setter
    def BorderColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Localize(self) -> bool: ...
    @Localize.setter
    def Localize(self, value: bool) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Transparency(self) -> float: ...
    @Transparency.setter
    def Transparency(self, value: float) -> float: ...


class GuiMain(ScreenGui):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    AutoLocalize : bool
    Capabilities : SecurityCapabilities
    ClipToDeviceSafeArea : bool
    DefinesCapabilities : bool
    DisplayOrder : int
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    ResetOnSpawn : bool
    RootLocalizationTable : LocalizationTable
    SafeAreaCompatibility : SafeAreaCompatibility
    ScreenInsets : ScreenInsets
    SelectionBehaviorDown : SelectionBehavior
    SelectionBehaviorLeft : SelectionBehavior
    SelectionBehaviorRight : SelectionBehavior
    SelectionBehaviorUp : SelectionBehavior
    SelectionGroup : bool
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    ZIndexBehavior : ZIndexBehavior
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Localize(self) -> bool: ...
    @Localize.setter
    def Localize(self, value: bool) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class GuiObject(GuiBase2d):
    Active : bool
    AnchorPoint : Vector2
    Archivable : bool
    Attributes : RbxAttributes
    AutoLocalize : bool
    AutomaticSize : AutomaticSize
    BackgroundColor3 : Color3
    BackgroundTransparency : float
    BorderColor3 : Color3
    BorderMode : BorderMode
    BorderSizePixel : int
    Capabilities : SecurityCapabilities
    ClipsDescendants : bool
    DefinesCapabilities : bool
    Draggable : bool
    HistoryId : UniqueId
    Interactable : bool
    LayoutOrder : int
    Name : str
    NextSelectionDown : GuiObject
    NextSelectionLeft : GuiObject
    NextSelectionRight : GuiObject
    NextSelectionUp : GuiObject
    Position : UDim2
    RootLocalizationTable : LocalizationTable
    Rotation : float
    Selectable : bool
    SelectionBehaviorDown : SelectionBehavior
    SelectionBehaviorLeft : SelectionBehavior
    SelectionBehaviorRight : SelectionBehavior
    SelectionBehaviorUp : SelectionBehavior
    SelectionGroup : bool
    SelectionImageObject : GuiObject
    SelectionOrder : int
    Size : UDim2
    SizeConstraint : SizeConstraint
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Visible : bool
    ZIndex : int
    @property
    def BackgroundColor(self) -> BrickColor: ...
    @BackgroundColor.setter
    def BackgroundColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BorderColor(self) -> BrickColor: ...
    @BorderColor.setter
    def BorderColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Localize(self) -> bool: ...
    @Localize.setter
    def Localize(self, value: bool) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Transparency(self) -> float: ...
    @Transparency.setter
    def Transparency(self, value: float) -> float: ...


class GuiService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    AutoSelectGuiEnabled : bool
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    GuiNavigationEnabled : bool
    HistoryId : UniqueId
    Name : str
    SelectedObject : GuiObject
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class HandleAdornment(PVAdornment):
    AdornCullingMode : AdornCullingMode
    Adornee : PVInstance
    AlwaysOnTop : bool
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    CFrame : CFrame
    Color3 : Color3
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SizeRelativeOffset : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    Transparency : float
    UniqueId : UniqueId
    Visible : bool
    ZIndex : int
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> BrickColor: ...
    @Color.setter
    def Color(self, value: BrickColor) -> BrickColor: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Handles(HandlesBase):
    def __init__(self) -> None: ...
    Adornee : BasePart
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color3 : Color3
    DefinesCapabilities : bool
    Faces : Faces
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Style : HandlesStyle
    Tags : HashSet_1[str]
    Transparency : float
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> BrickColor: ...
    @Color.setter
    def Color(self, value: BrickColor) -> BrickColor: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class HandlesBase(PartAdornment):
    Adornee : BasePart
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color3 : Color3
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    Transparency : float
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> BrickColor: ...
    @Color.setter
    def Color(self, value: BrickColor) -> BrickColor: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class HandRigDescription(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Index1 : Instance
    Index1TposeAdjustment : CFrame
    Index2 : Instance
    Index2TposeAdjustment : CFrame
    Index3 : Instance
    Index3TposeAdjustment : CFrame
    IndexRange : Vector3
    IndexSize : float
    Middle1 : Instance
    Middle1TposeAdjustment : CFrame
    Middle2 : Instance
    Middle2TposeAdjustment : CFrame
    Middle3 : Instance
    Middle3TposeAdjustment : CFrame
    MiddleRange : Vector3
    MiddleSize : float
    Name : str
    Pinky1 : Instance
    Pinky1TposeAdjustment : CFrame
    Pinky2 : Instance
    Pinky2TposeAdjustment : CFrame
    Pinky3 : Instance
    Pinky3TposeAdjustment : CFrame
    PinkyRange : Vector3
    PinkySize : float
    Ring1 : Instance
    Ring1TposeAdjustment : CFrame
    Ring2 : Instance
    Ring2TposeAdjustment : CFrame
    Ring3 : Instance
    Ring3TposeAdjustment : CFrame
    RingRange : Vector3
    RingSize : float
    Side : HandRigDescriptionSide
    SourceAssetId : int
    Tags : HashSet_1[str]
    Thumb1 : Instance
    Thumb1TposeAdjustment : CFrame
    Thumb2 : Instance
    Thumb2TposeAdjustment : CFrame
    Thumb3 : Instance
    Thumb3TposeAdjustment : CFrame
    ThumbRange : Vector3
    ThumbSize : float
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class HapticEffect(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Looped : bool
    Name : str
    Position : Vector3
    Radius : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    Type : HapticEffectType
    UniqueId : UniqueId
    Waveform : FloatCurve
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class HapticService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Hat(Accoutrement):
    def __init__(self) -> None: ...
    Archivable : bool
    AttachmentPoint : CFrame
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class HeapProfilerService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class HeatmapService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class HeightmapImporterService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class HiddenSurfaceRemovalAsset(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    HSRData : Array_1[int]
    HSRMeshIdData : Array_1[int]
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Highlight(Instance):
    def __init__(self) -> None: ...
    Adornee : Instance
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    DepthMode : HighlightDepthMode
    Enabled : bool
    FillColor : Color3
    FillTransparency : float
    HistoryId : UniqueId
    Name : str
    OutlineColor : Color3
    OutlineTransparency : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class HingeConstraint(Constraint):
    def __init__(self) -> None: ...
    ActuatorType : ActuatorType
    AngularResponsiveness : float
    AngularSpeed : float
    AngularVelocity : float
    Archivable : bool
    Attachment0 : Attachment
    Attachment1 : Attachment
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color : BrickColor
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    LimitsEnabled : bool
    LowerAngle : float
    MotorMaxAcceleration : float
    MotorMaxTorque : float
    Name : str
    Radius : float
    Restitution : float
    ServoMaxTorque : float
    SoftlockServoUponReachingTarget : bool
    SourceAssetId : int
    Tags : HashSet_1[str]
    TargetAngle : float
    UniqueId : UniqueId
    UpperAngle : float
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Hint(Message):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    Text : str
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Hole(Feature):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    FaceId : NormalId
    HistoryId : UniqueId
    InOut : InOut
    LeftRight : LeftRight
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    TopBottom : TopBottom
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Hopper(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class HopperBin(BackpackItem):
    def __init__(self) -> None: ...
    Active : bool
    Archivable : bool
    Attributes : RbxAttributes
    BinType : BinType
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    LevelOfDetail : ModelLevelOfDetail
    ModelMeshCFrame : CFrame
    ModelMeshData : SharedString
    ModelMeshSize : Vector3
    ModelStreamingMode : ModelStreamingMode
    Name : str
    NeedsPivotMigration : bool
    PrimaryPart : BasePart
    ScaleFactor : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    TextureId : ContentId
    UniqueId : UniqueId
    WorldPivotData : Optional_1[CFrame]
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class HSRDataContentProvider(CacheableContentProvider):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class HttpRbxApiService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class HttpService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    HttpEnabled : bool
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Humanoid(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    AutoJumpEnabled : bool
    AutomaticScalingEnabled : bool
    AutoRotate : bool
    BreakJointsOnDeath : bool
    Capabilities : SecurityCapabilities
    CollisionType : HumanoidCollisionType
    DefinesCapabilities : bool
    DisplayDistanceType : HumanoidDisplayDistanceType
    DisplayName : str
    EvaluateStateMachine : bool
    Health_XML : float
    HealthDisplayDistance : float
    HealthDisplayType : HumanoidHealthDisplayType
    HipHeight : float
    HistoryId : UniqueId
    InternalBodyScale : Vector3
    InternalHeadScale : float
    JumpHeight : float
    JumpPower : float
    LeftLeg : BasePart
    MaxHealth : float
    MaxSlopeAngle : float
    Name : str
    NameDisplayDistance : float
    NameOcclusion : NameOcclusion
    RequiresNeck : bool
    RightLeg : BasePart
    RigType : HumanoidRigType
    SourceAssetId : int
    Tags : HashSet_1[str]
    Torso : BasePart
    UniqueId : UniqueId
    UseJumpPower : bool
    WalkSpeed : float
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def Health(self) -> float: ...
    @Health.setter
    def Health(self, value: float) -> float: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def maxHealth(self) -> float: ...
    @maxHealth.setter
    def maxHealth(self, value: float) -> float: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class HumanoidController(Controller):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class HumanoidDescription(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    BodyTypeScale : float
    Capabilities : SecurityCapabilities
    ClimbAnimation : int
    DefinesCapabilities : bool
    DepthScale : float
    EmotesDataInternal : str
    EquippedEmotesDataInternal : str
    Face : int
    FallAnimation : int
    GraphicTShirt : int
    HeadScale : float
    HeightScale : float
    HistoryId : UniqueId
    IdleAnimation : int
    JumpAnimation : int
    MoodAnimation : int
    Name : str
    Pants : int
    ProportionScale : float
    RunAnimation : int
    Shirt : int
    SourceAssetId : int
    SwimAnimation : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    WalkAnimation : int
    WidthScale : float
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def Head(self) -> int: ...
    @Head.setter
    def Head(self, value: int) -> int: ...
    @property
    def HeadColor(self) -> Color3: ...
    @HeadColor.setter
    def HeadColor(self, value: Color3) -> Color3: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def LeftArm(self) -> int: ...
    @LeftArm.setter
    def LeftArm(self, value: int) -> int: ...
    @property
    def LeftArmColor(self) -> Color3: ...
    @LeftArmColor.setter
    def LeftArmColor(self, value: Color3) -> Color3: ...
    @property
    def LeftLeg(self) -> int: ...
    @LeftLeg.setter
    def LeftLeg(self, value: int) -> int: ...
    @property
    def LeftLegColor(self) -> Color3: ...
    @LeftLegColor.setter
    def LeftLegColor(self, value: Color3) -> Color3: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def RightArm(self) -> int: ...
    @RightArm.setter
    def RightArm(self, value: int) -> int: ...
    @property
    def RightArmColor(self) -> Color3: ...
    @RightArmColor.setter
    def RightArmColor(self, value: Color3) -> Color3: ...
    @property
    def RightLeg(self) -> int: ...
    @RightLeg.setter
    def RightLeg(self, value: int) -> int: ...
    @property
    def RightLegColor(self) -> Color3: ...
    @RightLegColor.setter
    def RightLegColor(self, value: Color3) -> Color3: ...
    @property
    def Torso(self) -> int: ...
    @Torso.setter
    def Torso(self, value: int) -> int: ...
    @property
    def TorsoColor(self) -> Color3: ...
    @TorsoColor.setter
    def TorsoColor(self, value: Color3) -> Color3: ...


class HumanoidRigDescription(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Chest : Instance
    ChestRangeMax : Vector3
    ChestRangeMin : Vector3
    ChestSize : float
    ChestTposeAdjustment : CFrame
    DefinesCapabilities : bool
    HeadBase : Instance
    HeadBaseRangeMax : Vector3
    HeadBaseRangeMin : Vector3
    HeadBaseSize : float
    HeadBaseTposeAdjustment : CFrame
    HistoryId : UniqueId
    LeftAnkle : Instance
    LeftAnkleRangeMax : Vector3
    LeftAnkleRangeMin : Vector3
    LeftAnkleSize : float
    LeftAnkleTposeAdjustment : CFrame
    LeftClavicle : Instance
    LeftClavicleRangeMax : Vector3
    LeftClavicleRangeMin : Vector3
    LeftClavicleSize : float
    LeftClavicleTposeAdjustment : CFrame
    LeftElbow : Instance
    LeftElbowRangeMax : Vector3
    LeftElbowRangeMin : Vector3
    LeftElbowSize : float
    LeftElbowTposeAdjustment : CFrame
    LeftHip : Instance
    LeftHipRangeMax : Vector3
    LeftHipRangeMin : Vector3
    LeftHipSize : float
    LeftHipTposeAdjustment : CFrame
    LeftKnee : Instance
    LeftKneeRangeMax : Vector3
    LeftKneeRangeMin : Vector3
    LeftKneeSize : float
    LeftKneeTposeAdjustment : CFrame
    LeftShoulder : Instance
    LeftShoulderRangeMax : Vector3
    LeftShoulderRangeMin : Vector3
    LeftShoulderSize : float
    LeftShoulderTposeAdjustment : CFrame
    LeftToes : Instance
    LeftToesRangeMax : Vector3
    LeftToesRangeMin : Vector3
    LeftToesSize : float
    LeftToesTposeAdjustment : CFrame
    LeftWrist : Instance
    LeftWristRangeMax : Vector3
    LeftWristRangeMin : Vector3
    LeftWristSize : float
    LeftWristTposeAdjustment : CFrame
    Name : str
    Neck : Instance
    NeckRangeMax : Vector3
    NeckRangeMin : Vector3
    NeckSize : float
    NeckTposeAdjustment : CFrame
    Pelvis : Instance
    PelvisRangeMax : Vector3
    PelvisRangeMin : Vector3
    PelvisSize : float
    PelvisTposeAdjustment : CFrame
    RightAnkle : Instance
    RightAnkleRangeMax : Vector3
    RightAnkleRangeMin : Vector3
    RightAnkleSize : float
    RightAnkleTposeAdjustment : CFrame
    RightClavicle : Instance
    RightClavicleRangeMax : Vector3
    RightClavicleRangeMin : Vector3
    RightClavicleSize : float
    RightClavicleTposeAdjustment : CFrame
    RightElbow : Instance
    RightElbowRangeMax : Vector3
    RightElbowRangeMin : Vector3
    RightElbowSize : float
    RightElbowTposeAdjustment : CFrame
    RightHip : Instance
    RightHipRangeMax : Vector3
    RightHipRangeMin : Vector3
    RightHipSize : float
    RightHipTposeAdjustment : CFrame
    RightKnee : Instance
    RightKneeRangeMax : Vector3
    RightKneeRangeMin : Vector3
    RightKneeSize : float
    RightKneeTposeAdjustment : CFrame
    RightShoulder : Instance
    RightShoulderRangeMax : Vector3
    RightShoulderRangeMin : Vector3
    RightShoulderSize : float
    RightShoulderTposeAdjustment : CFrame
    RightToes : Instance
    RightToesRangeMax : Vector3
    RightToesRangeMin : Vector3
    RightToesSize : float
    RightToesTposeAdjustment : CFrame
    RightWrist : Instance
    RightWristRangeMax : Vector3
    RightWristRangeMin : Vector3
    RightWristSize : float
    RightWristTposeAdjustment : CFrame
    Root : Instance
    RootRangeMax : Vector3
    RootRangeMin : Vector3
    RootSize : float
    RootTposeAdjustment : CFrame
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Waist : Instance
    WaistRangeMax : Vector3
    WaistRangeMin : Vector3
    WaistSize : float
    WaistTposeAdjustment : CFrame
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class IAttributeToken_GenericClasses(abc.ABCMeta):
    Generic_IAttributeToken_GenericClasses_IAttributeToken_1_T = typing.TypeVar('Generic_IAttributeToken_GenericClasses_IAttributeToken_1_T')
    def __getitem__(self, types : typing.Type[Generic_IAttributeToken_GenericClasses_IAttributeToken_1_T]) -> typing.Type[IAttributeToken_1[Generic_IAttributeToken_GenericClasses_IAttributeToken_1_T]]: ...

IAttributeToken : IAttributeToken_GenericClasses

IAttributeToken_1_T = typing.TypeVar('IAttributeToken_1_T')
class IAttributeToken_1(typing.Generic[IAttributeToken_1_T], typing.Protocol):
    @property
    def AttributeType(self) -> AttributeType: ...
    @abc.abstractmethod
    def ReadAttribute(self, attribute: RbxAttribute) -> IAttributeToken_1_T: ...
    @abc.abstractmethod
    def WriteAttribute(self, attribute: RbxAttribute, value: IAttributeToken_1_T) -> None: ...


class IKControl(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    ChainRoot : Instance
    DefinesCapabilities : bool
    Enabled : bool
    EndEffector : Instance
    EndEffectorOffset : CFrame
    HistoryId : UniqueId
    Name : str
    Offset : CFrame
    Pole : Instance
    Priority : int
    SmoothTime : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    Target : Instance
    Type : IKControlType
    UniqueId : UniqueId
    Weight : float
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ILegacyStudioBridge(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ImageButton(GuiButton):
    def __init__(self) -> None: ...
    Active : bool
    AnchorPoint : Vector2
    Archivable : bool
    Attributes : RbxAttributes
    AutoButtonColor : bool
    AutoLocalize : bool
    AutomaticSize : AutomaticSize
    BackgroundColor3 : Color3
    BackgroundTransparency : float
    BorderColor3 : Color3
    BorderMode : BorderMode
    BorderSizePixel : int
    Capabilities : SecurityCapabilities
    ClipsDescendants : bool
    DefinesCapabilities : bool
    Draggable : bool
    HistoryId : UniqueId
    HoverHapticEffect : HapticEffect
    HoverImageContent : Content
    ImageColor3 : Color3
    ImageContent : Content
    ImageRectOffset : Vector2
    ImageRectSize : Vector2
    ImageTransparency : float
    Interactable : bool
    LayoutOrder : int
    Modal : bool
    Name : str
    NextSelectionDown : GuiObject
    NextSelectionLeft : GuiObject
    NextSelectionRight : GuiObject
    NextSelectionUp : GuiObject
    Position : UDim2
    PressedImageContent : Content
    PressHapticEffect : HapticEffect
    ResampleMode : ResamplerMode
    RootLocalizationTable : LocalizationTable
    Rotation : float
    ScaleType : ScaleType
    Selectable : bool
    Selected : bool
    SelectionBehaviorDown : SelectionBehavior
    SelectionBehaviorLeft : SelectionBehavior
    SelectionBehaviorRight : SelectionBehavior
    SelectionBehaviorUp : SelectionBehavior
    SelectionGroup : bool
    SelectionImageObject : GuiObject
    SelectionOrder : int
    Size : UDim2
    SizeConstraint : SizeConstraint
    SliceCenter : Rect
    SliceScale : float
    SourceAssetId : int
    Style : ButtonStyle
    Tags : HashSet_1[str]
    TileSize : UDim2
    UniqueId : UniqueId
    Visible : bool
    ZIndex : int
    @property
    def BackgroundColor(self) -> BrickColor: ...
    @BackgroundColor.setter
    def BackgroundColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BorderColor(self) -> BrickColor: ...
    @BorderColor.setter
    def BorderColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def HoverImage(self) -> ContentId: ...
    @HoverImage.setter
    def HoverImage(self, value: ContentId) -> ContentId: ...
    @property
    def Image(self) -> ContentId: ...
    @Image.setter
    def Image(self, value: ContentId) -> ContentId: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Localize(self) -> bool: ...
    @Localize.setter
    def Localize(self, value: bool) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def PressedImage(self) -> ContentId: ...
    @PressedImage.setter
    def PressedImage(self, value: ContentId) -> ContentId: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Transparency(self) -> float: ...
    @Transparency.setter
    def Transparency(self, value: float) -> float: ...


class ImageHandleAdornment(HandleAdornment):
    def __init__(self) -> None: ...
    AdornCullingMode : AdornCullingMode
    Adornee : PVInstance
    AlwaysOnTop : bool
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    CFrame : CFrame
    Color3 : Color3
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Image : ContentId
    Name : str
    Size : Vector2
    SizeRelativeOffset : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    Transparency : float
    UniqueId : UniqueId
    Visible : bool
    ZIndex : int
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> BrickColor: ...
    @Color.setter
    def Color(self, value: BrickColor) -> BrickColor: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ImageLabel(GuiLabel):
    def __init__(self) -> None: ...
    Active : bool
    AnchorPoint : Vector2
    Archivable : bool
    Attributes : RbxAttributes
    AutoLocalize : bool
    AutomaticSize : AutomaticSize
    BackgroundColor3 : Color3
    BackgroundTransparency : float
    BorderColor3 : Color3
    BorderMode : BorderMode
    BorderSizePixel : int
    Capabilities : SecurityCapabilities
    ClipsDescendants : bool
    DefinesCapabilities : bool
    Draggable : bool
    HistoryId : UniqueId
    ImageColor3 : Color3
    ImageContent : Content
    ImageRectOffset : Vector2
    ImageRectSize : Vector2
    ImageTransparency : float
    Interactable : bool
    LayoutOrder : int
    Name : str
    NextSelectionDown : GuiObject
    NextSelectionLeft : GuiObject
    NextSelectionRight : GuiObject
    NextSelectionUp : GuiObject
    Position : UDim2
    ResampleMode : ResamplerMode
    RootLocalizationTable : LocalizationTable
    Rotation : float
    ScaleType : ScaleType
    Selectable : bool
    SelectionBehaviorDown : SelectionBehavior
    SelectionBehaviorLeft : SelectionBehavior
    SelectionBehaviorRight : SelectionBehavior
    SelectionBehaviorUp : SelectionBehavior
    SelectionGroup : bool
    SelectionImageObject : GuiObject
    SelectionOrder : int
    Size : UDim2
    SizeConstraint : SizeConstraint
    SliceCenter : Rect
    SliceScale : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    TileSize : UDim2
    UniqueId : UniqueId
    Visible : bool
    ZIndex : int
    @property
    def BackgroundColor(self) -> BrickColor: ...
    @BackgroundColor.setter
    def BackgroundColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BorderColor(self) -> BrickColor: ...
    @BorderColor.setter
    def BorderColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def Image(self) -> ContentId: ...
    @Image.setter
    def Image(self, value: ContentId) -> ContentId: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Localize(self) -> bool: ...
    @Localize.setter
    def Localize(self, value: bool) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Transparency(self) -> float: ...
    @Transparency.setter
    def Transparency(self, value: float) -> float: ...


class IncrementalPatchBuilder(Instance):
    def __init__(self) -> None: ...
    AddPathsToBundle : bool
    Archivable : bool
    Attributes : RbxAttributes
    BuildDebouncePeriod : float
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HighCompression : bool
    HistoryId : UniqueId
    Name : str
    SerializePatch : bool
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    ZstdCompression : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class InputAction(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    Type : InputActionType
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class InputBinding(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Down : KeyCode
    HistoryId : UniqueId
    KeyCode : KeyCode
    Left : KeyCode
    Name : str
    PressedThreshold : float
    ReleasedThreshold : float
    Right : KeyCode
    Scale : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UIButton : GuiButton
    UniqueId : UniqueId
    Up : KeyCode
    Vector2Scale : Vector2
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class InputContext(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    Priority : int
    Sink : bool
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class InsertService(Instance):
    def __init__(self) -> None: ...
    AllowClientInsertModels : bool
    AllowInsertFreeModels : bool
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Instance(RbxObject):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    def Clone(self) -> Instance: ...
    def Destroy(self) -> None: ...
    def GetChildren(self) -> Array_1[Instance]: ...
    def GetDescendants(self) -> Array_1[Instance]: ...
    def GetFullName(self, separator: str = ...) -> str: ...
    def IsAncestorOf(self, descendant: Instance) -> bool: ...
    def IsDescendantOf(self, ancestor: Instance) -> bool: ...
    def ToString(self) -> str: ...
    # Skipped FindFirstAncestor due to it being static, abstract and generic.

    FindFirstAncestor : FindFirstAncestor_MethodGroup
    class FindFirstAncestor_MethodGroup:
        def __getitem__(self, t:typing.Type[FindFirstAncestor_1_T1]) -> FindFirstAncestor_1[FindFirstAncestor_1_T1]: ...

        FindFirstAncestor_1_T1 = typing.TypeVar('FindFirstAncestor_1_T1')
        class FindFirstAncestor_1(typing.Generic[FindFirstAncestor_1_T1]):
            FindFirstAncestor_1_T = Instance.FindFirstAncestor_MethodGroup.FindFirstAncestor_1_T1
            def __call__(self, name: str) -> FindFirstAncestor_1_T:...

        def __call__(self, name: str) -> Instance:...

    # Skipped FindFirstAncestorOfClass due to it being static, abstract and generic.

    FindFirstAncestorOfClass : FindFirstAncestorOfClass_MethodGroup
    class FindFirstAncestorOfClass_MethodGroup:
        def __getitem__(self, t:typing.Type[FindFirstAncestorOfClass_1_T1]) -> FindFirstAncestorOfClass_1[FindFirstAncestorOfClass_1_T1]: ...

        FindFirstAncestorOfClass_1_T1 = typing.TypeVar('FindFirstAncestorOfClass_1_T1')
        class FindFirstAncestorOfClass_1(typing.Generic[FindFirstAncestorOfClass_1_T1]):
            FindFirstAncestorOfClass_1_T = Instance.FindFirstAncestorOfClass_MethodGroup.FindFirstAncestorOfClass_1_T1
            def __call__(self) -> FindFirstAncestorOfClass_1_T:...


    # Skipped FindFirstAncestorWhichIsA due to it being static, abstract and generic.

    FindFirstAncestorWhichIsA : FindFirstAncestorWhichIsA_MethodGroup
    class FindFirstAncestorWhichIsA_MethodGroup:
        def __getitem__(self, t:typing.Type[FindFirstAncestorWhichIsA_1_T1]) -> FindFirstAncestorWhichIsA_1[FindFirstAncestorWhichIsA_1_T1]: ...

        FindFirstAncestorWhichIsA_1_T1 = typing.TypeVar('FindFirstAncestorWhichIsA_1_T1')
        class FindFirstAncestorWhichIsA_1(typing.Generic[FindFirstAncestorWhichIsA_1_T1]):
            FindFirstAncestorWhichIsA_1_T = Instance.FindFirstAncestorWhichIsA_MethodGroup.FindFirstAncestorWhichIsA_1_T1
            def __call__(self) -> FindFirstAncestorWhichIsA_1_T:...


    # Skipped FindFirstChild due to it being static, abstract and generic.

    FindFirstChild : FindFirstChild_MethodGroup
    class FindFirstChild_MethodGroup:
        def __getitem__(self, t:typing.Type[FindFirstChild_1_T1]) -> FindFirstChild_1[FindFirstChild_1_T1]: ...

        FindFirstChild_1_T1 = typing.TypeVar('FindFirstChild_1_T1')
        class FindFirstChild_1(typing.Generic[FindFirstChild_1_T1]):
            FindFirstChild_1_T = Instance.FindFirstChild_MethodGroup.FindFirstChild_1_T1
            def __call__(self, name: str, recursive: bool = ...) -> FindFirstChild_1_T:...

        def __call__(self, name: str, recursive: bool = ...) -> Instance:...

    # Skipped FindFirstChildOfClass due to it being static, abstract and generic.

    FindFirstChildOfClass : FindFirstChildOfClass_MethodGroup
    class FindFirstChildOfClass_MethodGroup:
        def __getitem__(self, t:typing.Type[FindFirstChildOfClass_1_T1]) -> FindFirstChildOfClass_1[FindFirstChildOfClass_1_T1]: ...

        FindFirstChildOfClass_1_T1 = typing.TypeVar('FindFirstChildOfClass_1_T1')
        class FindFirstChildOfClass_1(typing.Generic[FindFirstChildOfClass_1_T1]):
            FindFirstChildOfClass_1_T = Instance.FindFirstChildOfClass_MethodGroup.FindFirstChildOfClass_1_T1
            def __call__(self, recursive: bool = ...) -> FindFirstChildOfClass_1_T:...


    # Skipped FindFirstChildWhichIsA due to it being static, abstract and generic.

    FindFirstChildWhichIsA : FindFirstChildWhichIsA_MethodGroup
    class FindFirstChildWhichIsA_MethodGroup:
        def __getitem__(self, t:typing.Type[FindFirstChildWhichIsA_1_T1]) -> FindFirstChildWhichIsA_1[FindFirstChildWhichIsA_1_T1]: ...

        FindFirstChildWhichIsA_1_T1 = typing.TypeVar('FindFirstChildWhichIsA_1_T1')
        class FindFirstChildWhichIsA_1(typing.Generic[FindFirstChildWhichIsA_1_T1]):
            FindFirstChildWhichIsA_1_T = Instance.FindFirstChildWhichIsA_MethodGroup.FindFirstChildWhichIsA_1_T1
            def __call__(self, recursive: bool = ...) -> FindFirstChildWhichIsA_1_T:...


    # Skipped GetAttribute due to it being static, abstract and generic.

    GetAttribute : GetAttribute_MethodGroup
    class GetAttribute_MethodGroup:
        def __getitem__(self, t:typing.Type[GetAttribute_1_T1]) -> GetAttribute_1[GetAttribute_1_T1]: ...

        GetAttribute_1_T1 = typing.TypeVar('GetAttribute_1_T1')
        class GetAttribute_1(typing.Generic[GetAttribute_1_T1]):
            GetAttribute_1_T = Instance.GetAttribute_MethodGroup.GetAttribute_1_T1
            def __call__(self, key: str, value: clr.Reference[GetAttribute_1_T]) -> bool:...


    # Skipped GetChildrenOfType due to it being static, abstract and generic.

    GetChildrenOfType : GetChildrenOfType_MethodGroup
    class GetChildrenOfType_MethodGroup:
        def __getitem__(self, t:typing.Type[GetChildrenOfType_1_T1]) -> GetChildrenOfType_1[GetChildrenOfType_1_T1]: ...

        GetChildrenOfType_1_T1 = typing.TypeVar('GetChildrenOfType_1_T1')
        class GetChildrenOfType_1(typing.Generic[GetChildrenOfType_1_T1]):
            GetChildrenOfType_1_T = Instance.GetChildrenOfType_MethodGroup.GetChildrenOfType_1_T1
            def __call__(self) -> Array_1[GetChildrenOfType_1_T]:...


    # Skipped GetDescendantsOfType due to it being static, abstract and generic.

    GetDescendantsOfType : GetDescendantsOfType_MethodGroup
    class GetDescendantsOfType_MethodGroup:
        def __getitem__(self, t:typing.Type[GetDescendantsOfType_1_T1]) -> GetDescendantsOfType_1[GetDescendantsOfType_1_T1]: ...

        GetDescendantsOfType_1_T1 = typing.TypeVar('GetDescendantsOfType_1_T1')
        class GetDescendantsOfType_1(typing.Generic[GetDescendantsOfType_1_T1]):
            GetDescendantsOfType_1_T = Instance.GetDescendantsOfType_MethodGroup.GetDescendantsOfType_1_T1
            def __call__(self) -> Array_1[GetDescendantsOfType_1_T]:...


    # Skipped SetAttribute due to it being static, abstract and generic.

    SetAttribute : SetAttribute_MethodGroup
    class SetAttribute_MethodGroup:
        def __getitem__(self, t:typing.Type[SetAttribute_1_T1]) -> SetAttribute_1[SetAttribute_1_T1]: ...

        SetAttribute_1_T1 = typing.TypeVar('SetAttribute_1_T1')
        class SetAttribute_1(typing.Generic[SetAttribute_1_T1]):
            SetAttribute_1_T = Instance.SetAttribute_MethodGroup.SetAttribute_1_T1
            def __call__(self, key: str, value: SetAttribute_1_T) -> bool:...




class InstanceAdornment(GuiBase3d):
    Adornee : Instance
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color3 : Color3
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    Transparency : float
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> BrickColor: ...
    @Color.setter
    def Color(self, value: BrickColor) -> BrickColor: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class IntConstrainedValue(ValueBase):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    MaxValue : int
    MinValue : int
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    value : int
    @property
    def ClassName(self) -> str: ...
    @property
    def ConstrainedValue(self) -> int: ...
    @ConstrainedValue.setter
    def ConstrainedValue(self, value: int) -> int: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Value(self) -> int: ...
    @Value.setter
    def Value(self, value: int) -> int: ...


class InternalSyncItem(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    AutoSync : bool
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    Path : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class InternalSyncService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class IntersectOperation(PartOperation):
    def __init__(self) -> None: ...
    AeroMeshData : SharedString
    Anchored : bool
    Archivable : bool
    AssetId : ContentId
    Attributes : RbxAttributes
    AudioCanCollide : bool
    BackParamA : float
    BackParamB : float
    BackSurface : SurfaceType
    BackSurfaceInput : InputType
    BottomParamA : float
    BottomParamB : float
    BottomSurface : SurfaceType
    BottomSurfaceInput : InputType
    CanCollide : bool
    CanQuery : bool
    CanTouch : bool
    Capabilities : SecurityCapabilities
    CastShadow : bool
    CFrame : CFrame
    ChildData : Array_1[int]
    ChildData2 : SharedString
    CollisionGroup : str
    CollisionGroupId : int
    Color3uint8 : Color3uint8
    ComponentIndex : int
    CustomPhysicalProperties : PhysicalProperties
    DefinesCapabilities : bool
    Elasticity : float
    EnableFluidForces : bool
    FluidFidelityInternal : FluidFidelity
    FormFactor : FormFactor
    Friction : float
    FrontParamA : float
    FrontParamB : float
    FrontSurface : SurfaceType
    FrontSurfaceInput : InputType
    HistoryId : UniqueId
    InitialSize : Vector3
    LeftParamA : float
    LeftParamB : float
    LeftSurface : SurfaceType
    LeftSurfaceInput : InputType
    Locked : bool
    Massless : bool
    Material : Material
    MaterialVariantSerialized : str
    MeshData : Array_1[int]
    MeshData2 : SharedString
    Name : str
    OffCentered : bool
    PhysicalConfigData : SharedString
    PhysicsData : Array_1[int]
    PivotOffset : CFrame
    Reflectance : float
    RenderFidelity : RenderFidelity
    RightParamA : float
    RightParamB : float
    RightSurface : SurfaceType
    RightSurfaceInput : InputType
    RootPriority : int
    RotVelocity : Vector3
    size : Vector3
    SmoothingAngle : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    TopParamA : float
    TopParamB : float
    TopSurface : SurfaceType
    TopSurfaceInput : InputType
    Transparency : float
    UniqueId : UniqueId
    UnscaledCofm : Vector3
    UnscaledVolInertiaDiags : Vector3
    UnscaledVolInertiaOffDiags : Vector3
    UnscaledVolume : float
    UsePartColor : bool
    Velocity : Vector3
    @property
    def brickColor(self) -> BrickColor: ...
    @brickColor.setter
    def brickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BrickColor(self) -> BrickColor: ...
    @BrickColor.setter
    def BrickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> Color3: ...
    @Color.setter
    def Color(self, value: Color3) -> Color3: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Size(self) -> Vector3: ...
    @Size.setter
    def Size(self, value: Vector3) -> Vector3: ...


class IntValue(ValueBase):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Value : int
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class IXPService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class JointInstance(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    C0 : CFrame
    C1 : CFrame
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    Part0 : BasePart
    Part1 : BasePart
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class JointsService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class KeyboardService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Keyframe(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    Time : float
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class KeyframeMarker(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Value : str
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class KeyframeSequence(AnimationClip):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    AuthoredHipHeight : float
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    GuidBinaryString : Array_1[int]
    HistoryId : UniqueId
    Loop : bool
    Name : str
    Priority : AnimationPriority
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class KeyframeSequenceProvider(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class LanguageService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class LayerCollector(GuiBase2d):
    Archivable : bool
    Attributes : RbxAttributes
    AutoLocalize : bool
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    ResetOnSpawn : bool
    RootLocalizationTable : LocalizationTable
    SelectionBehaviorDown : SelectionBehavior
    SelectionBehaviorLeft : SelectionBehavior
    SelectionBehaviorRight : SelectionBehavior
    SelectionBehaviorUp : SelectionBehavior
    SelectionGroup : bool
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    ZIndexBehavior : ZIndexBehavior
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Localize(self) -> bool: ...
    @Localize.setter
    def Localize(self, value: bool) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class LegacyStudioBridge(ILegacyStudioBridge):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Light(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    Brightness : float
    Capabilities : SecurityCapabilities
    Color : Color3
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    Shadows : bool
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Lighting(Instance):
    def __init__(self) -> None: ...
    Ambient : Color3
    Archivable : bool
    Attributes : RbxAttributes
    Brightness : float
    Capabilities : SecurityCapabilities
    ColorShift_Bottom : Color3
    ColorShift_Top : Color3
    DefinesCapabilities : bool
    EnvironmentDiffuseScale : float
    EnvironmentSpecularScale : float
    ExposureCompensation : float
    FogColor : Color3
    FogEnd : float
    FogStart : float
    GeographicLatitude : float
    GlobalShadows : bool
    HistoryId : UniqueId
    LightingStyle : LightingStyle
    Name : str
    OutdoorAmbient : Color3
    Outlines : bool
    PrioritizeLightingQuality : bool
    ShadowColor : Color3
    ShadowSoftness : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    Technology : Technology
    TimeOfDay : str
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class LinearVelocity(Constraint):
    def __init__(self) -> None: ...
    Archivable : bool
    Attachment0 : Attachment
    Attachment1 : Attachment
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color : BrickColor
    DefinesCapabilities : bool
    Enabled : bool
    ForceLimitMode : ForceLimitMode
    ForceLimitsEnabled : bool
    HistoryId : UniqueId
    LineDirection : Vector3
    LineVelocity : float
    MaxAxesForce : Vector3
    MaxForce : float
    MaxPlanarAxesForce : Vector2
    Name : str
    PlaneVelocity : Vector2
    PrimaryTangentAxis : Vector3
    ReactionForceEnabled : bool
    RelativeTo : ActuatorRelativeTo
    SecondaryTangentAxis : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    VectorVelocity : Vector3
    VelocityConstraintMode : VelocityConstraintMode
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class LineForce(Constraint):
    def __init__(self) -> None: ...
    ApplyAtCenterOfMass : bool
    Archivable : bool
    Attachment0 : Attachment
    Attachment1 : Attachment
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color : BrickColor
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    InverseSquareLaw : bool
    Magnitude : float
    MaxForce : float
    Name : str
    ReactionForceEnabled : bool
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class LineHandleAdornment(HandleAdornment):
    def __init__(self) -> None: ...
    AdornCullingMode : AdornCullingMode
    Adornee : PVInstance
    AlwaysOnTop : bool
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    CFrame : CFrame
    Color3 : Color3
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Length : float
    Name : str
    SizeRelativeOffset : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    Thickness : float
    Transparency : float
    UniqueId : UniqueId
    Visible : bool
    ZIndex : int
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> BrickColor: ...
    @Color.setter
    def Color(self, value: BrickColor) -> BrickColor: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class LinkingService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class LiveScriptingService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class LiveSyncService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class LocalizationService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class LocalizationTable(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Contents : str
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    SourceLocaleId : str
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def DevelopmentLanguage(self) -> str: ...
    @DevelopmentLanguage.setter
    def DevelopmentLanguage(self, value: str) -> str: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class LocalScript(Script):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Disabled : bool
    HistoryId : UniqueId
    LinkedSource : ContentId
    Name : str
    RunContext : RunContext
    ScriptGuid : str
    Source : ProtectedString
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class LocalStorageService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class LodDataService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class LoginService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class LogReporterService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class LogService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class LostEnumValue(Attribute):
    def __init__(self) -> None: ...
    @property
    def MapTo(self) -> int: ...
    @MapTo.setter
    def MapTo(self, value: int) -> int: ...
    @property
    def TypeId(self) -> typing.Any: ...


class LSPFileSyncService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class LuaSourceContainer(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    ScriptGuid : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class LuauScriptAnalyzerService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class LuaWebService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ManualGlue(ManualSurfaceJointInstance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    C0 : CFrame
    C1 : CFrame
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    Part0 : BasePart
    Part1 : BasePart
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ManualSurfaceJointInstance(JointInstance):
    Archivable : bool
    Attributes : RbxAttributes
    C0 : CFrame
    C1 : CFrame
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    Part0 : BasePart
    Part1 : BasePart
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ManualWeld(ManualSurfaceJointInstance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    C0 : CFrame
    C1 : CFrame
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    Part0 : BasePart
    Part1 : BasePart
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class MarkerCurve(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    ValuesAndTimes : Array_1[int]
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class MarketplaceService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class MatchmakingService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class MaterialGenerationService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class MaterialService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    AsphaltName : str
    Attributes : RbxAttributes
    BasaltName : str
    BrickName : str
    Capabilities : SecurityCapabilities
    CardboardName : str
    CarpetName : str
    CeramicTilesName : str
    ClayRoofTilesName : str
    CobblestoneName : str
    ConcreteName : str
    CorrodedMetalName : str
    CrackedLavaName : str
    DefinesCapabilities : bool
    DiamondPlateName : str
    FabricName : str
    FoilName : str
    GlacierName : str
    GraniteName : str
    GrassName : str
    GroundName : str
    HistoryId : UniqueId
    IceName : str
    LeafyGrassName : str
    LeatherName : str
    LimestoneName : str
    MarbleName : str
    MetalName : str
    MudName : str
    Name : str
    PavementName : str
    PebbleName : str
    PlasterName : str
    PlasticName : str
    RockName : str
    RoofShinglesName : str
    RubberName : str
    SaltName : str
    SandName : str
    SandstoneName : str
    SlateName : str
    SmoothPlasticName : str
    SnowName : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Use2022MaterialsXml : bool
    WoodName : str
    WoodPlanksName : str
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class MaterialVariant(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    BaseMaterial : Material
    Capabilities : SecurityCapabilities
    ColorMapContent : Content
    CustomPhysicalProperties : PhysicalProperties
    DefinesCapabilities : bool
    HistoryId : UniqueId
    MaterialPattern : MaterialPattern
    MetalnessMapContent : Content
    Name : str
    NormalMapContent : Content
    RoughnessMapContent : Content
    SourceAssetId : int
    StudsPerTile : float
    Tags : HashSet_1[str]
    TexturePack : ContentId
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def ColorMap(self) -> ContentId: ...
    @ColorMap.setter
    def ColorMap(self, value: ContentId) -> ContentId: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def MetalnessMap(self) -> ContentId: ...
    @MetalnessMap.setter
    def MetalnessMap(self, value: ContentId) -> ContentId: ...
    @property
    def NormalMap(self) -> ContentId: ...
    @NormalMap.setter
    def NormalMap(self, value: ContentId) -> ContentId: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def RoughnessMap(self) -> ContentId: ...
    @RoughnessMap.setter
    def RoughnessMap(self, value: ContentId) -> ContentId: ...


class MemoryStoreService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class MemStorageService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class MeshContentProvider(CacheableContentProvider):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class MeshPart(TriangleMeshPart):
    def __init__(self) -> None: ...
    AeroMeshData : SharedString
    Anchored : bool
    Archivable : bool
    Attributes : RbxAttributes
    AudioCanCollide : bool
    BackParamA : float
    BackParamB : float
    BackSurface : SurfaceType
    BackSurfaceInput : InputType
    BottomParamA : float
    BottomParamB : float
    BottomSurface : SurfaceType
    BottomSurfaceInput : InputType
    CanCollide : bool
    CanQuery : bool
    CanTouch : bool
    Capabilities : SecurityCapabilities
    CastShadow : bool
    CFrame : CFrame
    CollisionGroup : str
    CollisionGroupId : int
    Color3uint8 : Color3uint8
    CustomPhysicalProperties : PhysicalProperties
    DefinesCapabilities : bool
    DoubleSided : bool
    Elasticity : float
    EnableFluidForces : bool
    FluidFidelityInternal : FluidFidelity
    Friction : float
    FrontParamA : float
    FrontParamB : float
    FrontSurface : SurfaceType
    FrontSurfaceInput : InputType
    HasJointOffset : bool
    HasSkinnedMesh : bool
    HistoryId : UniqueId
    InitialSize : Vector3
    JointOffset : Vector3
    LeftParamA : float
    LeftParamB : float
    LeftSurface : SurfaceType
    LeftSurfaceInput : InputType
    Locked : bool
    Massless : bool
    Material : Material
    MaterialVariantSerialized : str
    MeshContent : Content
    Name : str
    PhysicalConfigData : SharedString
    PhysicsData : Array_1[int]
    PivotOffset : CFrame
    Reflectance : float
    RenderFidelity : RenderFidelity
    RightParamA : float
    RightParamB : float
    RightSurface : SurfaceType
    RightSurfaceInput : InputType
    RootPriority : int
    RotVelocity : Vector3
    size : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    TextureContent : Content
    TopParamA : float
    TopParamB : float
    TopSurface : SurfaceType
    TopSurfaceInput : InputType
    Transparency : float
    UniqueId : UniqueId
    UnscaledCofm : Vector3
    UnscaledVolInertiaDiags : Vector3
    UnscaledVolInertiaOffDiags : Vector3
    UnscaledVolume : float
    Velocity : Vector3
    VertexCount : int
    @property
    def brickColor(self) -> BrickColor: ...
    @brickColor.setter
    def brickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BrickColor(self) -> BrickColor: ...
    @BrickColor.setter
    def BrickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> Color3: ...
    @Color.setter
    def Color(self, value: Color3) -> Color3: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def MeshId(self) -> ContentId: ...
    @MeshId.setter
    def MeshId(self, value: ContentId) -> ContentId: ...
    @property
    def MeshID(self) -> ContentId: ...
    @MeshID.setter
    def MeshID(self, value: ContentId) -> ContentId: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Size(self) -> Vector3: ...
    @Size.setter
    def Size(self, value: Vector3) -> Vector3: ...
    @property
    def TextureID(self) -> ContentId: ...
    @TextureID.setter
    def TextureID(self, value: ContentId) -> ContentId: ...


class Message(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    Text : str
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class MessageBusService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class MessagingService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class MetaBreakpoint(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Condition : str
    ContinueExecution : bool
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Line : int
    LogMessage : str
    Name : str
    RemoveOnHit : bool
    Script : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class MetaBreakpointContext(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    ContextDataInternal : str
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class MetaBreakpointManager(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class MLModelDeliveryService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class MLService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Model(PVInstance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    LevelOfDetail : ModelLevelOfDetail
    ModelMeshCFrame : CFrame
    ModelMeshData : SharedString
    ModelMeshSize : Vector3
    ModelStreamingMode : ModelStreamingMode
    Name : str
    NeedsPivotMigration : bool
    PrimaryPart : BasePart
    ScaleFactor : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    WorldPivotData : Optional_1[CFrame]
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ModuleScript(LuaSourceContainer):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    LinkedSource : ContentId
    Name : str
    ScriptGuid : str
    Source : ProtectedString
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Motor(JointInstance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    C0 : CFrame
    C1 : CFrame
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    DesiredAngle : float
    Enabled : bool
    HistoryId : UniqueId
    MaxVelocity : float
    Name : str
    Part0 : BasePart
    Part1 : BasePart
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Motor6D(Motor):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    C0 : CFrame
    C1 : CFrame
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    DesiredAngle : float
    Enabled : bool
    HistoryId : UniqueId
    MaxVelocity : float
    Name : str
    Part0 : BasePart
    Part1 : BasePart
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class MotorFeature(Feature):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    FaceId : NormalId
    HistoryId : UniqueId
    InOut : InOut
    LeftRight : LeftRight
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    TopBottom : TopBottom
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class MouseService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class NegateOperation(PartOperation):
    def __init__(self) -> None: ...
    AeroMeshData : SharedString
    Anchored : bool
    Archivable : bool
    AssetId : ContentId
    Attributes : RbxAttributes
    AudioCanCollide : bool
    BackParamA : float
    BackParamB : float
    BackSurface : SurfaceType
    BackSurfaceInput : InputType
    BottomParamA : float
    BottomParamB : float
    BottomSurface : SurfaceType
    BottomSurfaceInput : InputType
    CanCollide : bool
    CanQuery : bool
    CanTouch : bool
    Capabilities : SecurityCapabilities
    CastShadow : bool
    CFrame : CFrame
    ChildData : Array_1[int]
    ChildData2 : SharedString
    CollisionGroup : str
    CollisionGroupId : int
    Color3uint8 : Color3uint8
    ComponentIndex : int
    CustomPhysicalProperties : PhysicalProperties
    DefinesCapabilities : bool
    Elasticity : float
    EnableFluidForces : bool
    FluidFidelityInternal : FluidFidelity
    FormFactor : FormFactor
    Friction : float
    FrontParamA : float
    FrontParamB : float
    FrontSurface : SurfaceType
    FrontSurfaceInput : InputType
    HistoryId : UniqueId
    InitialSize : Vector3
    LeftParamA : float
    LeftParamB : float
    LeftSurface : SurfaceType
    LeftSurfaceInput : InputType
    Locked : bool
    Massless : bool
    Material : Material
    MaterialVariantSerialized : str
    MeshData : Array_1[int]
    MeshData2 : SharedString
    Name : str
    OffCentered : bool
    PhysicalConfigData : SharedString
    PhysicsData : Array_1[int]
    PivotOffset : CFrame
    PreviousOperation : NegateOperationHiddenHistory
    Reflectance : float
    RenderFidelity : RenderFidelity
    RightParamA : float
    RightParamB : float
    RightSurface : SurfaceType
    RightSurfaceInput : InputType
    RootPriority : int
    RotVelocity : Vector3
    size : Vector3
    SmoothingAngle : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    TopParamA : float
    TopParamB : float
    TopSurface : SurfaceType
    TopSurfaceInput : InputType
    Transparency : float
    UniqueId : UniqueId
    UnscaledCofm : Vector3
    UnscaledVolInertiaDiags : Vector3
    UnscaledVolInertiaOffDiags : Vector3
    UnscaledVolume : float
    UsePartColor : bool
    Velocity : Vector3
    @property
    def brickColor(self) -> BrickColor: ...
    @brickColor.setter
    def brickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BrickColor(self) -> BrickColor: ...
    @BrickColor.setter
    def BrickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> Color3: ...
    @Color.setter
    def Color(self, value: Color3) -> Color3: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Size(self) -> Vector3: ...
    @Size.setter
    def Size(self, value: Vector3) -> Vector3: ...


class NetworkClient(NetworkPeer):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class NetworkPeer(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class NetworkServer(NetworkPeer):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class NetworkSettings(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    HttpProxyEnabled : bool
    HttpProxyURL : str
    IncomingReplicationLag : float
    Name : str
    PrintJoinSizeBreakdown : bool
    PrintPhysicsErrors : bool
    PrintStreamInstanceQuota : bool
    RandomizeJoinInstanceOrder : bool
    RenderStreamedRegions : bool
    ShowActiveAnimationAsset : bool
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class NoCollisionConstraint(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    Part0 : BasePart
    Part1 : BasePart
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Noise(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    NoiseType : NoiseType
    Seed : int
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class NonReplicatedCSGDictionaryService(FlyweightService):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class NotificationService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class NumberPose(PoseBase):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    EasingDirection : PoseEasingDirection
    EasingStyle : PoseEasingStyle
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Value : float
    Weight : float
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class NumberValue(ValueBase):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Value : float
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ObjectValue(ValueBase):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Value : Instance
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class OmniRecommendationsService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class OpenCloudService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class OperationGraph(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PackageLink(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    AutoUpdate : bool
    Capabilities : SecurityCapabilities
    DefaultName : str
    DefinesCapabilities : bool
    HistoryId : UniqueId
    ModifiedState : int
    Name : str
    PackageIdSerialize : ContentId
    SerializedDefaultAttributes : Array_1[int]
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    VersionIdSerialize : int
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PackageService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PackageUIService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Pants(Clothing):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color3 : Color3
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    PantsTemplate : ContentId
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ParabolaAdornment(PVAdornment):
    def __init__(self) -> None: ...
    Adornee : PVInstance
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color3 : Color3
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    Transparency : float
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> BrickColor: ...
    @Color.setter
    def Color(self, value: BrickColor) -> BrickColor: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Part(FormFactorPart):
    def __init__(self) -> None: ...
    Anchored : bool
    Archivable : bool
    Attributes : RbxAttributes
    AudioCanCollide : bool
    BackParamA : float
    BackParamB : float
    BackSurface : SurfaceType
    BackSurfaceInput : InputType
    BottomParamA : float
    BottomParamB : float
    BottomSurface : SurfaceType
    BottomSurfaceInput : InputType
    CanCollide : bool
    CanQuery : bool
    CanTouch : bool
    Capabilities : SecurityCapabilities
    CastShadow : bool
    CFrame : CFrame
    CollisionGroup : str
    CollisionGroupId : int
    Color3uint8 : Color3uint8
    CustomPhysicalProperties : PhysicalProperties
    DefinesCapabilities : bool
    Elasticity : float
    EnableFluidForces : bool
    formFactorRaw : FormFactor
    Friction : float
    FrontParamA : float
    FrontParamB : float
    FrontSurface : SurfaceType
    FrontSurfaceInput : InputType
    HistoryId : UniqueId
    LeftParamA : float
    LeftParamB : float
    LeftSurface : SurfaceType
    LeftSurfaceInput : InputType
    Locked : bool
    Massless : bool
    Material : Material
    MaterialVariantSerialized : str
    Name : str
    PivotOffset : CFrame
    Reflectance : float
    RightParamA : float
    RightParamB : float
    RightSurface : SurfaceType
    RightSurfaceInput : InputType
    RootPriority : int
    RotVelocity : Vector3
    shape : PartType
    size : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    TopParamA : float
    TopParamB : float
    TopSurface : SurfaceType
    TopSurfaceInput : InputType
    Transparency : float
    UniqueId : UniqueId
    Velocity : Vector3
    @property
    def brickColor(self) -> BrickColor: ...
    @brickColor.setter
    def brickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BrickColor(self) -> BrickColor: ...
    @BrickColor.setter
    def BrickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> Color3: ...
    @Color.setter
    def Color(self, value: Color3) -> Color3: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def formFactor(self) -> FormFactor: ...
    @formFactor.setter
    def formFactor(self, value: FormFactor) -> FormFactor: ...
    @property
    def FormFactor(self) -> FormFactor: ...
    @FormFactor.setter
    def FormFactor(self, value: FormFactor) -> FormFactor: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Shape(self) -> PartType: ...
    @Shape.setter
    def Shape(self, value: PartType) -> PartType: ...
    @property
    def Size(self) -> Vector3: ...
    @Size.setter
    def Size(self, value: Vector3) -> Vector3: ...


class PartAdornment(GuiBase3d):
    Adornee : BasePart
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color3 : Color3
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    Transparency : float
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> BrickColor: ...
    @Color.setter
    def Color(self, value: BrickColor) -> BrickColor: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ParticleEmitter(Instance):
    def __init__(self) -> None: ...
    Acceleration : Vector3
    Archivable : bool
    Attributes : RbxAttributes
    Brightness : float
    Capabilities : SecurityCapabilities
    Color : ColorSequence
    DefinesCapabilities : bool
    Drag : float
    EmissionDirection : NormalId
    Enabled : bool
    FlipbookFramerate : NumberRange
    FlipbookIncompatible : str
    FlipbookLayout : ParticleFlipbookLayout
    FlipbookMode : ParticleFlipbookMode
    FlipbookStartRandom : bool
    HistoryId : UniqueId
    Lifetime : NumberRange
    LightEmission : float
    LightInfluence : float
    LockedToPart : bool
    Name : str
    Orientation : ParticleOrientation
    Rate : float
    Rotation : NumberRange
    RotSpeed : NumberRange
    Shape : ParticleEmitterShape
    ShapeInOut : ParticleEmitterShapeInOut
    ShapePartial : float
    ShapeStyle : ParticleEmitterShapeStyle
    Size : NumberSequence
    SourceAssetId : int
    Speed : NumberRange
    SpreadAngle : Vector2
    Squash : NumberSequence
    Tags : HashSet_1[str]
    Texture : ContentId
    TimeScale : float
    Transparency : NumberSequence
    UniqueId : UniqueId
    VelocityInheritance : float
    WindAffectsDrag : bool
    ZOffset : float
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def VelocitySpread(self) -> float: ...
    @VelocitySpread.setter
    def VelocitySpread(self, value: float) -> float: ...


class PartOperation(TriangleMeshPart):
    def __init__(self) -> None: ...
    AeroMeshData : SharedString
    Anchored : bool
    Archivable : bool
    AssetId : ContentId
    Attributes : RbxAttributes
    AudioCanCollide : bool
    BackParamA : float
    BackParamB : float
    BackSurface : SurfaceType
    BackSurfaceInput : InputType
    BottomParamA : float
    BottomParamB : float
    BottomSurface : SurfaceType
    BottomSurfaceInput : InputType
    CanCollide : bool
    CanQuery : bool
    CanTouch : bool
    Capabilities : SecurityCapabilities
    CastShadow : bool
    CFrame : CFrame
    ChildData : Array_1[int]
    ChildData2 : SharedString
    CollisionGroup : str
    CollisionGroupId : int
    Color3uint8 : Color3uint8
    ComponentIndex : int
    CustomPhysicalProperties : PhysicalProperties
    DefinesCapabilities : bool
    Elasticity : float
    EnableFluidForces : bool
    FluidFidelityInternal : FluidFidelity
    FormFactor : FormFactor
    Friction : float
    FrontParamA : float
    FrontParamB : float
    FrontSurface : SurfaceType
    FrontSurfaceInput : InputType
    HistoryId : UniqueId
    InitialSize : Vector3
    LeftParamA : float
    LeftParamB : float
    LeftSurface : SurfaceType
    LeftSurfaceInput : InputType
    Locked : bool
    Massless : bool
    Material : Material
    MaterialVariantSerialized : str
    MeshData : Array_1[int]
    MeshData2 : SharedString
    Name : str
    OffCentered : bool
    PhysicalConfigData : SharedString
    PhysicsData : Array_1[int]
    PivotOffset : CFrame
    Reflectance : float
    RenderFidelity : RenderFidelity
    RightParamA : float
    RightParamB : float
    RightSurface : SurfaceType
    RightSurfaceInput : InputType
    RootPriority : int
    RotVelocity : Vector3
    size : Vector3
    SmoothingAngle : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    TopParamA : float
    TopParamB : float
    TopSurface : SurfaceType
    TopSurfaceInput : InputType
    Transparency : float
    UniqueId : UniqueId
    UnscaledCofm : Vector3
    UnscaledVolInertiaDiags : Vector3
    UnscaledVolInertiaOffDiags : Vector3
    UnscaledVolume : float
    UsePartColor : bool
    Velocity : Vector3
    @property
    def brickColor(self) -> BrickColor: ...
    @brickColor.setter
    def brickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BrickColor(self) -> BrickColor: ...
    @BrickColor.setter
    def BrickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> Color3: ...
    @Color.setter
    def Color(self, value: Color3) -> Color3: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Size(self) -> Vector3: ...
    @Size.setter
    def Size(self, value: Vector3) -> Vector3: ...


class PartOperationAsset(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    ChildData : Array_1[int]
    DefinesCapabilities : bool
    HistoryId : UniqueId
    MeshData : Array_1[int]
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PatchBundlerFileWatch(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Path2D(GuiBase):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Closed : bool
    Color3 : Color3
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    PropertiesSerialize : Array_1[int]
    SourceAssetId : int
    Tags : HashSet_1[str]
    Thickness : float
    Transparency : float
    UniqueId : UniqueId
    Visible : bool
    ZIndex : int
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PathfindingLink(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attachment0 : Attachment
    Attachment1 : Attachment
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    IsBidirectional : bool
    Label : str
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PathfindingModifier(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Label : str
    Name : str
    PassThrough : bool
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PathfindingService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    EmptyCutoff : float
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PerformanceControlService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PermissionsService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PhysicsService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PitchShiftSoundEffect(SoundEffect):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    Octave : float
    Priority : int
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PlaceAssetIdsService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PlacesService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PlaceStatsService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Plane(PlaneConstraint):
    def __init__(self) -> None: ...
    Archivable : bool
    Attachment0 : Attachment
    Attachment1 : Attachment
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color : BrickColor
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PlaneConstraint(Constraint):
    def __init__(self) -> None: ...
    Archivable : bool
    Attachment0 : Attachment
    Attachment1 : Attachment
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color : BrickColor
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PlatformCloudStorageService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PlatformFriendsService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PlayerDataService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    LoadFailureBehavior : PlayerDataLoadFailureBehavior
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PlayerEmulatorService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    CustomPoliciesEnabled : bool
    DefinesCapabilities : bool
    EmulatedCountryCode : str
    EmulatedGameLocale : str
    HistoryId : UniqueId
    Name : str
    PlayerEmulationEnabled : bool
    PseudolocalizationEnabled : bool
    SerializedEmulatedPolicyInfo : Array_1[int]
    SourceAssetId : int
    Tags : HashSet_1[str]
    TextElongationFactor : int
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PlayerHydrationService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Players(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    BanningEnabled : bool
    Capabilities : SecurityCapabilities
    CharacterAutoLoads : bool
    DefinesCapabilities : bool
    HistoryId : UniqueId
    MaxPlayersInternal : int
    Name : str
    PreferredPlayersInternal : int
    RespawnTime : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    UseStrafingAnimations : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PlayerViewService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PluginAction(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PluginCapabilities(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Manifest : str
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PluginDebugService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PluginGuiService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PluginManagementService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PluginPolicyService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PointLight(Light):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Brightness : float
    Capabilities : SecurityCapabilities
    Color : Color3
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    Range : float
    Shadows : bool
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PointsService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PolicyService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    IsLuobuServer : TriStateBoolean
    LuobuWhitelisted : TriStateBoolean
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Pose(PoseBase):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    CFrame : CFrame
    DefinesCapabilities : bool
    EasingDirection : PoseEasingDirection
    EasingStyle : PoseEasingStyle
    HistoryId : UniqueId
    MaskWeight : float
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Weight : float
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PoseBase(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    EasingDirection : PoseEasingDirection
    EasingStyle : PoseEasingStyle
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Weight : float
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PostEffect(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PrismaticConstraint(SlidingBallConstraint):
    def __init__(self) -> None: ...
    ActuatorType : ActuatorType
    Archivable : bool
    Attachment0 : Attachment
    Attachment1 : Attachment
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color : BrickColor
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    LimitsEnabled : bool
    LinearResponsiveness : float
    LowerLimit : float
    MotorMaxAcceleration : float
    MotorMaxForce : float
    Name : str
    Restitution : float
    ServoMaxForce : float
    Size : float
    SoftlockServoUponReachingTarget : bool
    SourceAssetId : int
    Speed : float
    Tags : HashSet_1[str]
    TargetPosition : float
    UniqueId : UniqueId
    UpperLimit : float
    Velocity : float
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ProcessInstancePhysicsService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Property:
    @typing.overload
    def __init__(self, name: str = ..., type: PropertyType = ..., obj: RbxObject = ...) -> None: ...
    @typing.overload
    def __init__(self, obj: RbxObject, property: PROP) -> None: ...
    Types : IReadOnlyDictionary_2[typing.Type[typing.Any], PropertyType]
    @property
    def HasRawBuffer(self) -> bool: ...
    @property
    def Name(self) -> str: ...
    @Name.setter
    def Name(self, value: str) -> str: ...
    @property
    def Object(self) -> RbxObject: ...
    @Object.setter
    def Object(self, value: RbxObject) -> RbxObject: ...
    @property
    def RawBuffer(self) -> Array_1[int]: ...
    @RawBuffer.setter
    def RawBuffer(self, value: Array_1[int]) -> Array_1[int]: ...
    @property
    def Type(self) -> PropertyType: ...
    @Type.setter
    def Type(self, value: PropertyType) -> PropertyType: ...
    @property
    def Value(self) -> typing.Any: ...
    @Value.setter
    def Value(self, value: typing.Any) -> typing.Any: ...
    @property
    def XmlToken(self) -> str: ...
    @XmlToken.setter
    def XmlToken(self, value: str) -> str: ...
    def GetFullName(self) -> str: ...
    def ToString(self) -> str: ...
    # Skipped CastValue due to it being static, abstract and generic.

    CastValue : CastValue_MethodGroup
    class CastValue_MethodGroup:
        def __getitem__(self, t:typing.Type[CastValue_1_T1]) -> CastValue_1[CastValue_1_T1]: ...

        CastValue_1_T1 = typing.TypeVar('CastValue_1_T1')
        class CastValue_1(typing.Generic[CastValue_1_T1]):
            CastValue_1_T = Property.CastValue_MethodGroup.CastValue_1_T1
            def __call__(self) -> CastValue_1_T:...




class PropertyType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Unknown : PropertyType # 0
    String : PropertyType # 1
    Bool : PropertyType # 2
    Int : PropertyType # 3
    Float : PropertyType # 4
    Double : PropertyType # 5
    UDim : PropertyType # 6
    UDim2 : PropertyType # 7
    Ray : PropertyType # 8
    Faces : PropertyType # 9
    Axes : PropertyType # 10
    BrickColor : PropertyType # 11
    Color3 : PropertyType # 12
    Vector2 : PropertyType # 13
    Vector3 : PropertyType # 14
    CFrame : PropertyType # 16
    Quaternion : PropertyType # 17
    Enum : PropertyType # 18
    Ref : PropertyType # 19
    Vector3int16 : PropertyType # 20
    NumberSequence : PropertyType # 21
    ColorSequence : PropertyType # 22
    NumberRange : PropertyType # 23
    Rect : PropertyType # 24
    PhysicalProperties : PropertyType # 25
    Color3uint8 : PropertyType # 26
    Int64 : PropertyType # 27
    SharedString : PropertyType # 28
    ProtectedString : PropertyType # 29
    OptionalCFrame : PropertyType # 30
    UniqueId : PropertyType # 31
    FontFace : PropertyType # 32
    SecurityCapabilities : PropertyType # 33
    Content : PropertyType # 34


class ProximityPrompt(Instance):
    def __init__(self) -> None: ...
    ActionText : str
    Archivable : bool
    Attributes : RbxAttributes
    AutoLocalize : bool
    Capabilities : SecurityCapabilities
    ClickablePrompt : bool
    DefinesCapabilities : bool
    Enabled : bool
    Exclusivity : ProximityPromptExclusivity
    GamepadKeyCode : KeyCode
    HistoryId : UniqueId
    HoldDuration : float
    KeyboardKeyCode : KeyCode
    MaxActivationDistance : float
    Name : str
    ObjectText : str
    RequiresLineOfSight : bool
    RootLocalizationTable : LocalizationTable
    SourceAssetId : int
    Style : ProximityPromptStyle
    Tags : HashSet_1[str]
    UIOffset : Vector2
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ProximityPromptService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    MaxPromptsVisible : int
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PublishService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PVAdornment(GuiBase3d):
    Adornee : PVInstance
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color3 : Color3
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    Transparency : float
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> BrickColor: ...
    @Color.setter
    def Color(self, value: BrickColor) -> BrickColor: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class PVInstance(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class RayValue(ValueBase):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Value : Ray
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class RbxAnalyticsService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class RbxAttribute(IDisposable):
    @property
    def DataType(self) -> AttributeType: ...
    @DataType.setter
    def DataType(self, value: AttributeType) -> AttributeType: ...
    @property
    def Value(self) -> typing.Any: ...
    @Value.setter
    def Value(self, value: typing.Any) -> typing.Any: ...
    def Dispose(self) -> None: ...
    def ToString(self) -> str: ...
    # Skipped SupportsType due to it being static, abstract and generic.

    SupportsType : SupportsType_MethodGroup
    class SupportsType_MethodGroup:
        def __getitem__(self, t:typing.Type[SupportsType_1_T1]) -> SupportsType_1[SupportsType_1_T1]: ...

        SupportsType_1_T1 = typing.TypeVar('SupportsType_1_T1')
        class SupportsType_1(typing.Generic[SupportsType_1_T1]):
            SupportsType_1_T = RbxAttribute.SupportsType_MethodGroup.SupportsType_1_T1
            def __call__(self) -> bool:...

        def __call__(self, type: typing.Type[typing.Any]) -> bool:...



class RbxAttributes(SortedDictionary_2[str, RbxAttribute]):
    def __init__(self) -> None: ...
    @property
    def Comparer(self) -> IComparer_1[str]: ...
    @property
    def Count(self) -> int: ...
    @property
    def Item(self) -> RbxAttribute: ...
    @Item.setter
    def Item(self, value: RbxAttribute) -> RbxAttribute: ...
    @property
    def Keys(self) -> SortedDictionary_2.KeyCollection_2[str, RbxAttribute]: ...
    @property
    def Values(self) -> SortedDictionary_2.ValueCollection_2[str, RbxAttribute]: ...


class RbxObject:
    def __init__(self) -> None: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    def Destroy(self) -> None: ...
    def GetProperty(self, name: str) -> Property: ...
    # Skipped Cast due to it being static, abstract and generic.

    Cast : Cast_MethodGroup
    class Cast_MethodGroup:
        def __getitem__(self, t:typing.Type[Cast_1_T1]) -> Cast_1[Cast_1_T1]: ...

        Cast_1_T1 = typing.TypeVar('Cast_1_T1')
        class Cast_1(typing.Generic[Cast_1_T1]):
            Cast_1_T = RbxObject.Cast_MethodGroup.Cast_1_T1
            def __call__(self) -> Cast_1_T:...


    # Skipped IsA due to it being static, abstract and generic.

    IsA : IsA_MethodGroup
    class IsA_MethodGroup:
        def __getitem__(self, t:typing.Type[IsA_1_T1]) -> IsA_1[IsA_1_T1]: ...

        IsA_1_T1 = typing.TypeVar('IsA_1_T1')
        class IsA_1(typing.Generic[IsA_1_T1]):
            IsA_1_T = RbxObject.IsA_MethodGroup.IsA_1_T1
            def __call__(self) -> bool:...




class RbxService(Attribute):
    def __init__(self) -> None: ...
    @property
    def IsRooted(self) -> bool: ...
    @IsRooted.setter
    def IsRooted(self, value: bool) -> bool: ...
    @property
    def TypeId(self) -> typing.Any: ...


class ReflectionMetadata(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ReflectionMetadataCallbacks(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ReflectionMetadataClass(ReflectionMetadataItem):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Browsable : bool
    Capabilities : SecurityCapabilities
    ClassCategory : str
    ClientOnly : bool
    Constraint : str
    DefinesCapabilities : bool
    Deprecated : bool
    EditingDisabled : bool
    EditorType : str
    ExplorerImageIndex : int
    ExplorerOrder : int
    FFlag : str
    HistoryId : UniqueId
    Insertable : bool
    IsBackend : bool
    Name : str
    PreferredParent : str
    PropertyOrder : int
    ScriptContext : str
    ServerOnly : bool
    ServiceVisibility : ServiceVisibility
    SliderScaling : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UIMaximum : float
    UIMinimum : float
    UINumTicks : float
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ReflectionMetadataClasses(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ReflectionMetadataEnum(ReflectionMetadataItem):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Browsable : bool
    Capabilities : SecurityCapabilities
    ClassCategory : str
    ClientOnly : bool
    Constraint : str
    DefinesCapabilities : bool
    Deprecated : bool
    EditingDisabled : bool
    EditorType : str
    FFlag : str
    HistoryId : UniqueId
    IsBackend : bool
    Name : str
    PropertyOrder : int
    ScriptContext : str
    ServerOnly : bool
    SliderScaling : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UIMaximum : float
    UIMinimum : float
    UINumTicks : float
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ReflectionMetadataEnumItem(ReflectionMetadataItem):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Browsable : bool
    Capabilities : SecurityCapabilities
    ClassCategory : str
    ClientOnly : bool
    Constraint : str
    DefinesCapabilities : bool
    Deprecated : bool
    EditingDisabled : bool
    EditorType : str
    FFlag : str
    HistoryId : UniqueId
    IsBackend : bool
    Name : str
    PropertyOrder : int
    ScriptContext : str
    ServerOnly : bool
    SliderScaling : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UIMaximum : float
    UIMinimum : float
    UINumTicks : float
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ReflectionMetadataEnums(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ReflectionMetadataEvents(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ReflectionMetadataFunctions(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ReflectionMetadataItem(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    Browsable : bool
    Capabilities : SecurityCapabilities
    ClassCategory : str
    ClientOnly : bool
    Constraint : str
    DefinesCapabilities : bool
    Deprecated : bool
    EditingDisabled : bool
    EditorType : str
    FFlag : str
    HistoryId : UniqueId
    IsBackend : bool
    Name : str
    PropertyOrder : int
    ScriptContext : str
    ServerOnly : bool
    SliderScaling : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UIMaximum : float
    UIMinimum : float
    UINumTicks : float
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ReflectionMetadataMember(ReflectionMetadataItem):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Browsable : bool
    Capabilities : SecurityCapabilities
    ClassCategory : str
    ClientOnly : bool
    Constraint : str
    DefinesCapabilities : bool
    Deprecated : bool
    EditingDisabled : bool
    EditorType : str
    FFlag : str
    HistoryId : UniqueId
    IsBackend : bool
    Name : str
    PropertyOrder : int
    ScriptContext : str
    ServerOnly : bool
    SliderScaling : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UIMaximum : float
    UIMinimum : float
    UINumTicks : float
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ReflectionMetadataProperties(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ReflectionMetadataYieldFunctions(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ReflectionService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class RelativeGui(GuiObject):
    def __init__(self) -> None: ...
    Active : bool
    AnchorPoint : Vector2
    Archivable : bool
    Attributes : RbxAttributes
    AutoLocalize : bool
    AutomaticSize : AutomaticSize
    BackgroundColor3 : Color3
    BackgroundTransparency : float
    BorderColor3 : Color3
    BorderMode : BorderMode
    BorderSizePixel : int
    Capabilities : SecurityCapabilities
    ClipsDescendants : bool
    DefinesCapabilities : bool
    Draggable : bool
    HistoryId : UniqueId
    Interactable : bool
    LayoutOrder : int
    Name : str
    NextSelectionDown : GuiObject
    NextSelectionLeft : GuiObject
    NextSelectionRight : GuiObject
    NextSelectionUp : GuiObject
    Position : UDim2
    RootLocalizationTable : LocalizationTable
    Rotation : float
    Selectable : bool
    SelectionBehaviorDown : SelectionBehavior
    SelectionBehaviorLeft : SelectionBehavior
    SelectionBehaviorRight : SelectionBehavior
    SelectionBehaviorUp : SelectionBehavior
    SelectionGroup : bool
    SelectionImageObject : GuiObject
    SelectionOrder : int
    Size : UDim2
    SizeConstraint : SizeConstraint
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Visible : bool
    ZIndex : int
    @property
    def BackgroundColor(self) -> BrickColor: ...
    @BackgroundColor.setter
    def BackgroundColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BorderColor(self) -> BrickColor: ...
    @BorderColor.setter
    def BorderColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Localize(self) -> bool: ...
    @Localize.setter
    def Localize(self, value: bool) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Transparency(self) -> float: ...
    @Transparency.setter
    def Transparency(self, value: float) -> float: ...


class RemoteCursorService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class RemoteDebuggerServer(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class RemoteEvent(BaseRemoteEvent):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class RemoteFunction(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class RenderingTest(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    CFrame : CFrame
    ComparisonDiffThreshold : int
    ComparisonMethod : RenderingTestComparisonMethod
    ComparisonPsnrThreshold : float
    DefinesCapabilities : bool
    Description : str
    FieldOfView : float
    HistoryId : UniqueId
    Name : str
    PerfTest : bool
    QualityAuto : bool
    QualityLevel : int
    RenderingTestFrameCount : int
    ShouldSkip : bool
    SourceAssetId : int
    Tags : HashSet_1[str]
    Ticket : str
    Timeout : int
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class RenderSettings(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    AutoFRMLevel : int
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    EagerBulkExecution : bool
    EditQualityLevel : QualityLevel
    Enable_VR_Mode : bool
    ExportMergeByMaterial : bool
    FrameRateManager : FramerateManagerMode
    GraphicsMode : GraphicsMode
    HistoryId : UniqueId
    MeshCacheSize : int
    MeshPartDetailLevel : MeshPartDetailLevel
    Name : str
    QualityLevel : QualityLevel
    ReloadAssets : bool
    RenderCSGTrianglesDebug : bool
    ShowBoundingBoxes : bool
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    ViewMode : ViewMode
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ReplicatedFirst(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ReplicatedStorage(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ReverbSoundEffect(SoundEffect):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DecayTime : float
    DefinesCapabilities : bool
    Density : float
    Diffusion : float
    DryLevel : float
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    Priority : int
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    WetLevel : float
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class RibbonNotificationService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class RigidConstraint(Constraint):
    def __init__(self) -> None: ...
    Archivable : bool
    Attachment0 : Attachment
    Attachment1 : Attachment
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color : BrickColor
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class RobloxFile(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    LogErrors : bool
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    # Skipped Open due to it being static, abstract and generic.

    Open : Open_MethodGroup
    class Open_MethodGroup:
        @typing.overload
        def __call__(self, buffer: Array_1[int]) -> RobloxFile:...
        @typing.overload
        def __call__(self, filePath: str) -> RobloxFile:...
        @typing.overload
        def __call__(self, stream: Stream) -> RobloxFile:...

    # Skipped OpenAsync due to it being static, abstract and generic.

    OpenAsync : OpenAsync_MethodGroup
    class OpenAsync_MethodGroup:
        @typing.overload
        def __call__(self, buffer: Array_1[int]) -> Task_1[RobloxFile]:...
        @typing.overload
        def __call__(self, filePath: str) -> Task_1[RobloxFile]:...
        @typing.overload
        def __call__(self, stream: Stream) -> Task_1[RobloxFile]:...

    # Skipped Save due to it being static, abstract and generic.

    Save : Save_MethodGroup
    class Save_MethodGroup:
        @typing.overload
        def __call__(self, filePath: str) -> None:...
        @typing.overload
        def __call__(self, stream: Stream) -> None:...

    # Skipped SaveAsync due to it being static, abstract and generic.

    SaveAsync : SaveAsync_MethodGroup
    class SaveAsync_MethodGroup:
        @typing.overload
        def __call__(self, filePath: str) -> Task:...
        @typing.overload
        def __call__(self, stream: Stream) -> Task:...



class RobloxPluginGuiService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class RobloxReplicatedStorage(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class RobloxSerializableInstance(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Data : Array_1[int]
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class RobloxServerStorage(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class RocketPropulsion(BodyMover):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    CartoonFactor : float
    DefinesCapabilities : bool
    HistoryId : UniqueId
    MaxSpeed : float
    MaxThrust : float
    MaxTorque : Vector3
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    Target : BasePart
    TargetOffset : Vector3
    TargetRadius : float
    ThrustD : float
    ThrustP : float
    TurnD : float
    TurnP : float
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class RodConstraint(Constraint):
    def __init__(self) -> None: ...
    Archivable : bool
    Attachment0 : Attachment
    Attachment1 : Attachment
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color : BrickColor
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Length : float
    LimitAngle0 : float
    LimitAngle1 : float
    LimitsEnabled : bool
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    Thickness : float
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class RomarkRbxAnalyticsService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class RomarkService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class RopeConstraint(Constraint):
    def __init__(self) -> None: ...
    Archivable : bool
    Attachment0 : Attachment
    Attachment1 : Attachment
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color : BrickColor
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Length : float
    Name : str
    Restitution : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    Thickness : float
    UniqueId : UniqueId
    Visible : bool
    WinchEnabled : bool
    WinchForce : float
    WinchResponsiveness : float
    WinchSpeed : float
    WinchTarget : float
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Rotate(JointInstance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    C0 : CFrame
    C1 : CFrame
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    Part0 : BasePart
    Part1 : BasePart
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class RotateP(DynamicRotate):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    BaseAngle : float
    C0 : CFrame
    C1 : CFrame
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    Part0 : BasePart
    Part1 : BasePart
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class RotateV(DynamicRotate):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    BaseAngle : float
    C0 : CFrame
    C1 : CFrame
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    Part0 : BasePart
    Part1 : BasePart
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class RotationCurve(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    ValuesAndTimes : Array_1[int]
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class RTAnimationTracker(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class RtMessagingService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class RunService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class RuntimeScriptService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SafetyService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    IsCaptureModeForReport : bool
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ScreenGui(LayerCollector):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    AutoLocalize : bool
    Capabilities : SecurityCapabilities
    ClipToDeviceSafeArea : bool
    DefinesCapabilities : bool
    DisplayOrder : int
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    ResetOnSpawn : bool
    RootLocalizationTable : LocalizationTable
    SafeAreaCompatibility : SafeAreaCompatibility
    ScreenInsets : ScreenInsets
    SelectionBehaviorDown : SelectionBehavior
    SelectionBehaviorLeft : SelectionBehavior
    SelectionBehaviorRight : SelectionBehavior
    SelectionBehaviorUp : SelectionBehavior
    SelectionGroup : bool
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    ZIndexBehavior : ZIndexBehavior
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Localize(self) -> bool: ...
    @Localize.setter
    def Localize(self, value: bool) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Script(BaseScript):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Disabled : bool
    HistoryId : UniqueId
    LinkedSource : ContentId
    Name : str
    RunContext : RunContext
    ScriptGuid : str
    Source : ProtectedString
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ScriptChangeService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ScriptCloneWatcher(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ScriptCloneWatcherHelper(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ScriptCommitService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ScriptContext(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ScriptDebugger(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    CoreScriptIdentifier : str
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    ScriptGuid : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ScriptEditorService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ScriptProfilerService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ScriptRegistrationService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ScriptService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ScrollingFrame(GuiObject):
    def __init__(self) -> None: ...
    Active : bool
    AnchorPoint : Vector2
    Archivable : bool
    Attributes : RbxAttributes
    AutoLocalize : bool
    AutomaticCanvasSize : AutomaticSize
    AutomaticSize : AutomaticSize
    BackgroundColor3 : Color3
    BackgroundTransparency : float
    BorderColor3 : Color3
    BorderMode : BorderMode
    BorderSizePixel : int
    BottomImage : ContentId
    CanvasPosition : Vector2
    CanvasSize : UDim2
    Capabilities : SecurityCapabilities
    ClipsDescendants : bool
    DefinesCapabilities : bool
    Draggable : bool
    ElasticBehavior : ElasticBehavior
    HistoryId : UniqueId
    HorizontalScrollBarInset : ScrollBarInset
    Interactable : bool
    LayoutOrder : int
    MidImage : ContentId
    Name : str
    NextSelectionDown : GuiObject
    NextSelectionLeft : GuiObject
    NextSelectionRight : GuiObject
    NextSelectionUp : GuiObject
    Position : UDim2
    RootLocalizationTable : LocalizationTable
    Rotation : float
    ScrollBarImageColor3 : Color3
    ScrollBarImageTransparency : float
    ScrollBarThickness : int
    ScrollingDirection : ScrollingDirection
    ScrollingEnabled : bool
    Selectable : bool
    SelectionBehaviorDown : SelectionBehavior
    SelectionBehaviorLeft : SelectionBehavior
    SelectionBehaviorRight : SelectionBehavior
    SelectionBehaviorUp : SelectionBehavior
    SelectionGroup : bool
    SelectionImageObject : GuiObject
    SelectionOrder : int
    Size : UDim2
    SizeConstraint : SizeConstraint
    SourceAssetId : int
    Tags : HashSet_1[str]
    TopImage : ContentId
    UniqueId : UniqueId
    VerticalScrollBarInset : ScrollBarInset
    VerticalScrollBarPosition : VerticalScrollBarPosition
    Visible : bool
    ZIndex : int
    @property
    def BackgroundColor(self) -> BrickColor: ...
    @BackgroundColor.setter
    def BackgroundColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BorderColor(self) -> BrickColor: ...
    @BorderColor.setter
    def BorderColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Localize(self) -> bool: ...
    @Localize.setter
    def Localize(self, value: bool) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Transparency(self) -> float: ...
    @Transparency.setter
    def Transparency(self, value: float) -> float: ...


class Seat(Part):
    def __init__(self) -> None: ...
    Anchored : bool
    Archivable : bool
    Attributes : RbxAttributes
    AudioCanCollide : bool
    BackParamA : float
    BackParamB : float
    BackSurface : SurfaceType
    BackSurfaceInput : InputType
    BottomParamA : float
    BottomParamB : float
    BottomSurface : SurfaceType
    BottomSurfaceInput : InputType
    CanCollide : bool
    CanQuery : bool
    CanTouch : bool
    Capabilities : SecurityCapabilities
    CastShadow : bool
    CFrame : CFrame
    CollisionGroup : str
    CollisionGroupId : int
    Color3uint8 : Color3uint8
    CustomPhysicalProperties : PhysicalProperties
    DefinesCapabilities : bool
    Disabled : bool
    Elasticity : float
    EnableFluidForces : bool
    formFactorRaw : FormFactor
    Friction : float
    FrontParamA : float
    FrontParamB : float
    FrontSurface : SurfaceType
    FrontSurfaceInput : InputType
    HistoryId : UniqueId
    LeftParamA : float
    LeftParamB : float
    LeftSurface : SurfaceType
    LeftSurfaceInput : InputType
    Locked : bool
    Massless : bool
    Material : Material
    MaterialVariantSerialized : str
    Name : str
    PivotOffset : CFrame
    Reflectance : float
    RightParamA : float
    RightParamB : float
    RightSurface : SurfaceType
    RightSurfaceInput : InputType
    RootPriority : int
    RotVelocity : Vector3
    shape : PartType
    size : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    TopParamA : float
    TopParamB : float
    TopSurface : SurfaceType
    TopSurfaceInput : InputType
    Transparency : float
    UniqueId : UniqueId
    Velocity : Vector3
    @property
    def brickColor(self) -> BrickColor: ...
    @brickColor.setter
    def brickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BrickColor(self) -> BrickColor: ...
    @BrickColor.setter
    def BrickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> Color3: ...
    @Color.setter
    def Color(self, value: Color3) -> Color3: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def formFactor(self) -> FormFactor: ...
    @formFactor.setter
    def formFactor(self, value: FormFactor) -> FormFactor: ...
    @property
    def FormFactor(self) -> FormFactor: ...
    @FormFactor.setter
    def FormFactor(self, value: FormFactor) -> FormFactor: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Shape(self) -> PartType: ...
    @Shape.setter
    def Shape(self, value: PartType) -> PartType: ...
    @property
    def Size(self) -> Vector3: ...
    @Size.setter
    def Size(self, value: Vector3) -> Vector3: ...


class SecurityCapabilities(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    RunClientScript : SecurityCapabilities # 1
    RunServerScript : SecurityCapabilities # 2
    AccessOutsideWrite : SecurityCapabilities # 4
    AssetRequire : SecurityCapabilities # 8
    LoadString : SecurityCapabilities # 16
    ScriptGlobals : SecurityCapabilities # 32
    CreateInstances : SecurityCapabilities # 64
    Basic : SecurityCapabilities # 128
    Audio : SecurityCapabilities # 256
    DataStore : SecurityCapabilities # 512
    Network : SecurityCapabilities # 1024
    Physics : SecurityCapabilities # 2048
    UI : SecurityCapabilities # 4096
    CSG : SecurityCapabilities # 8192
    Chat : SecurityCapabilities # 16384
    Animation : SecurityCapabilities # 32768
    Avatar : SecurityCapabilities # 65536
    Input : SecurityCapabilities # 131072
    Environment : SecurityCapabilities # 262144
    RemoteEvent : SecurityCapabilities # 524288
    LegacySound : SecurityCapabilities # 1048576
    Players : SecurityCapabilities # 2097152


class Selection(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SelectionBox(InstanceAdornment):
    def __init__(self) -> None: ...
    Adornee : Instance
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color3 : Color3
    DefinesCapabilities : bool
    HistoryId : UniqueId
    LineThickness : float
    Name : str
    SourceAssetId : int
    StudioSelectionBox : bool
    SurfaceColor3 : Color3
    SurfaceTransparency : float
    Tags : HashSet_1[str]
    Transparency : float
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> BrickColor: ...
    @Color.setter
    def Color(self, value: BrickColor) -> BrickColor: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def SurfaceColor(self) -> BrickColor: ...
    @SurfaceColor.setter
    def SurfaceColor(self, value: BrickColor) -> BrickColor: ...


class SelectionHighlightManager(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SelectionLasso(GuiBase3d):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color3 : Color3
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Humanoid : Humanoid
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    Transparency : float
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> BrickColor: ...
    @Color.setter
    def Color(self, value: BrickColor) -> BrickColor: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SelectionPartLasso(SelectionLasso):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color3 : Color3
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Humanoid : Humanoid
    Name : str
    Part : BasePart
    SourceAssetId : int
    Tags : HashSet_1[str]
    Transparency : float
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> BrickColor: ...
    @Color.setter
    def Color(self, value: BrickColor) -> BrickColor: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SelectionPointLasso(SelectionLasso):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color3 : Color3
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Humanoid : Humanoid
    Name : str
    Point : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    Transparency : float
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> BrickColor: ...
    @Color.setter
    def Color(self, value: BrickColor) -> BrickColor: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SelectionSphere(PVAdornment):
    def __init__(self) -> None: ...
    Adornee : PVInstance
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color3 : Color3
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    SurfaceColor3 : Color3
    SurfaceTransparency : float
    Tags : HashSet_1[str]
    Transparency : float
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> BrickColor: ...
    @Color.setter
    def Color(self, value: BrickColor) -> BrickColor: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def SurfaceColor(self) -> BrickColor: ...
    @SurfaceColor.setter
    def SurfaceColor(self, value: BrickColor) -> BrickColor: ...


class SensorBase(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    UpdateType : SensorUpdateType
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SerializationService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ServerScriptService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    LoadStringEnabled : bool
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ServerStorage(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ServiceVisibilityService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HiddenServices : Array_1[int]
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    VisibleServices : Array_1[int]
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SessionService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SharedTableRegistry(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Shirt(Clothing):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color3 : Color3
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    ShirtTemplate : ContentId
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ShirtGraphic(CharacterAppearance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color3 : Color3
    DefinesCapabilities : bool
    Graphic : ContentId
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SkateboardController(Controller):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SkateboardPlatform(Part):
    def __init__(self) -> None: ...
    Anchored : bool
    Archivable : bool
    Attributes : RbxAttributes
    AudioCanCollide : bool
    BackParamA : float
    BackParamB : float
    BackSurface : SurfaceType
    BackSurfaceInput : InputType
    BottomParamA : float
    BottomParamB : float
    BottomSurface : SurfaceType
    BottomSurfaceInput : InputType
    CanCollide : bool
    CanQuery : bool
    CanTouch : bool
    Capabilities : SecurityCapabilities
    CastShadow : bool
    CFrame : CFrame
    CollisionGroup : str
    CollisionGroupId : int
    Color3uint8 : Color3uint8
    CustomPhysicalProperties : PhysicalProperties
    DefinesCapabilities : bool
    Elasticity : float
    EnableFluidForces : bool
    formFactorRaw : FormFactor
    Friction : float
    FrontParamA : float
    FrontParamB : float
    FrontSurface : SurfaceType
    FrontSurfaceInput : InputType
    HistoryId : UniqueId
    LeftParamA : float
    LeftParamB : float
    LeftSurface : SurfaceType
    LeftSurfaceInput : InputType
    Locked : bool
    Massless : bool
    Material : Material
    MaterialVariantSerialized : str
    Name : str
    PivotOffset : CFrame
    Reflectance : float
    RightParamA : float
    RightParamB : float
    RightSurface : SurfaceType
    RightSurfaceInput : InputType
    RootPriority : int
    RotVelocity : Vector3
    shape : PartType
    size : Vector3
    SourceAssetId : int
    Steer : int
    StickyWheels : bool
    Tags : HashSet_1[str]
    Throttle : int
    TopParamA : float
    TopParamB : float
    TopSurface : SurfaceType
    TopSurfaceInput : InputType
    Transparency : float
    UniqueId : UniqueId
    Velocity : Vector3
    @property
    def brickColor(self) -> BrickColor: ...
    @brickColor.setter
    def brickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BrickColor(self) -> BrickColor: ...
    @BrickColor.setter
    def BrickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> Color3: ...
    @Color.setter
    def Color(self, value: Color3) -> Color3: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def formFactor(self) -> FormFactor: ...
    @formFactor.setter
    def formFactor(self, value: FormFactor) -> FormFactor: ...
    @property
    def FormFactor(self) -> FormFactor: ...
    @FormFactor.setter
    def FormFactor(self, value: FormFactor) -> FormFactor: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Shape(self) -> PartType: ...
    @Shape.setter
    def Shape(self, value: PartType) -> PartType: ...
    @property
    def Size(self) -> Vector3: ...
    @Size.setter
    def Size(self, value: Vector3) -> Vector3: ...


class Skin(CharacterAppearance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SkinColor : BrickColor
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Sky(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    CelestialBodiesShown : bool
    DefinesCapabilities : bool
    HistoryId : UniqueId
    MoonAngularSize : float
    MoonTextureId : ContentId
    Name : str
    SkyboxBk : ContentId
    SkyboxDn : ContentId
    SkyboxFt : ContentId
    SkyboxLf : ContentId
    SkyboxOrientation : Vector3
    SkyboxRt : ContentId
    SkyboxUp : ContentId
    SourceAssetId : int
    StarCount : int
    SunAngularSize : float
    SunTextureId : ContentId
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SlidingBallConstraint(Constraint):
    def __init__(self) -> None: ...
    ActuatorType : ActuatorType
    Archivable : bool
    Attachment0 : Attachment
    Attachment1 : Attachment
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color : BrickColor
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    LimitsEnabled : bool
    LinearResponsiveness : float
    LowerLimit : float
    MotorMaxAcceleration : float
    MotorMaxForce : float
    Name : str
    Restitution : float
    ServoMaxForce : float
    Size : float
    SoftlockServoUponReachingTarget : bool
    SourceAssetId : int
    Speed : float
    Tags : HashSet_1[str]
    TargetPosition : float
    UniqueId : UniqueId
    UpperLimit : float
    Velocity : float
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SlimContentProvider(CacheableContentProvider):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Smoke(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color : Color3
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    opacity_xml : float
    riseVelocity_xml : float
    size_xml : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    TimeScale : float
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Opacity(self) -> float: ...
    @Opacity.setter
    def Opacity(self, value: float) -> float: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def RiseVelocity(self) -> float: ...
    @RiseVelocity.setter
    def RiseVelocity(self, value: float) -> float: ...
    @property
    def Size(self) -> float: ...
    @Size.setter
    def Size(self, value: float) -> float: ...


class SmoothVoxelsUpgraderService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Snap(JointInstance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    C0 : CFrame
    C1 : CFrame
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    Part0 : BasePart
    Part1 : BasePart
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SnippetService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SocialService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SolidModelContentProvider(CacheableContentProvider):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Sound(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    EmitterSize : float
    HistoryId : UniqueId
    Looped : bool
    LoopRegion : NumberRange
    Name : str
    PlaybackRegion : NumberRange
    PlaybackRegionsEnabled : bool
    PlaybackSpeed : float
    Playing : bool
    PlayOnRemove : bool
    RollOffMaxDistance : float
    RollOffMinDistance : float
    RollOffMode : RollOffMode
    SoundGroup : SoundGroup
    SoundId : ContentId
    SourceAssetId : int
    Tags : HashSet_1[str]
    TimePosition : float
    UniqueId : UniqueId
    Volume : float
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def MinDistance(self) -> float: ...
    @MinDistance.setter
    def MinDistance(self, value: float) -> float: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Pitch(self) -> float: ...
    @Pitch.setter
    def Pitch(self, value: float) -> float: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def xmlRead_MaxDistance_3(self) -> float: ...
    @xmlRead_MaxDistance_3.setter
    def xmlRead_MaxDistance_3(self, value: float) -> float: ...
    @property
    def xmlRead_MinDistance_3(self) -> float: ...
    @xmlRead_MinDistance_3.setter
    def xmlRead_MinDistance_3(self, value: float) -> float: ...


class SoundEffect(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    Priority : int
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SoundGroup(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Volume : float
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SoundService(Instance):
    def __init__(self) -> None: ...
    AmbientReverb : ReverbType
    Archivable : bool
    Attributes : RbxAttributes
    AudioApiByDefault : RolloutState
    Capabilities : SecurityCapabilities
    CharacterSoundsUseNewApi : RolloutState
    DefaultListenerLocation : ListenerLocation
    DefinesCapabilities : bool
    DistanceFactor : float
    DopplerScale : float
    HistoryId : UniqueId
    IsNewExpForAudioApiByDefault : bool
    Name : str
    RespectFilteringEnabled : bool
    RolloffScale : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    VolumetricAudio : VolumetricAudio
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Sparkles(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    SparkleColor : Color3
    Tags : HashSet_1[str]
    TimeScale : float
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> Color3: ...
    @Color.setter
    def Color(self, value: Color3) -> Color3: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SpawnerService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SpawnLocation(Part):
    def __init__(self) -> None: ...
    AllowTeamChangeOnTouch : bool
    Anchored : bool
    Archivable : bool
    Attributes : RbxAttributes
    AudioCanCollide : bool
    BackParamA : float
    BackParamB : float
    BackSurface : SurfaceType
    BackSurfaceInput : InputType
    BottomParamA : float
    BottomParamB : float
    BottomSurface : SurfaceType
    BottomSurfaceInput : InputType
    CanCollide : bool
    CanQuery : bool
    CanTouch : bool
    Capabilities : SecurityCapabilities
    CastShadow : bool
    CFrame : CFrame
    CollisionGroup : str
    CollisionGroupId : int
    Color3uint8 : Color3uint8
    CustomPhysicalProperties : PhysicalProperties
    DefinesCapabilities : bool
    Duration : int
    Elasticity : float
    Enabled : bool
    EnableFluidForces : bool
    formFactorRaw : FormFactor
    Friction : float
    FrontParamA : float
    FrontParamB : float
    FrontSurface : SurfaceType
    FrontSurfaceInput : InputType
    HistoryId : UniqueId
    LeftParamA : float
    LeftParamB : float
    LeftSurface : SurfaceType
    LeftSurfaceInput : InputType
    Locked : bool
    Massless : bool
    Material : Material
    MaterialVariantSerialized : str
    Name : str
    Neutral : bool
    PivotOffset : CFrame
    Reflectance : float
    RightParamA : float
    RightParamB : float
    RightSurface : SurfaceType
    RightSurfaceInput : InputType
    RootPriority : int
    RotVelocity : Vector3
    shape : PartType
    size : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    TeamColor : BrickColor
    TopParamA : float
    TopParamB : float
    TopSurface : SurfaceType
    TopSurfaceInput : InputType
    Transparency : float
    UniqueId : UniqueId
    Velocity : Vector3
    @property
    def brickColor(self) -> BrickColor: ...
    @brickColor.setter
    def brickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BrickColor(self) -> BrickColor: ...
    @BrickColor.setter
    def BrickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> Color3: ...
    @Color.setter
    def Color(self, value: Color3) -> Color3: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def formFactor(self) -> FormFactor: ...
    @formFactor.setter
    def formFactor(self, value: FormFactor) -> FormFactor: ...
    @property
    def FormFactor(self) -> FormFactor: ...
    @FormFactor.setter
    def FormFactor(self, value: FormFactor) -> FormFactor: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Shape(self) -> PartType: ...
    @Shape.setter
    def Shape(self, value: PartType) -> PartType: ...
    @property
    def Size(self) -> Vector3: ...
    @Size.setter
    def Size(self, value: Vector3) -> Vector3: ...


class SpecialMesh(FileMesh):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    MeshId : ContentId
    MeshType : MeshType
    Name : str
    Offset : Vector3
    Scale : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    TextureId : ContentId
    UniqueId : UniqueId
    VertexColor : Vector3
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SphereHandleAdornment(HandleAdornment):
    def __init__(self) -> None: ...
    AdornCullingMode : AdornCullingMode
    Adornee : PVInstance
    AlwaysOnTop : bool
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    CFrame : CFrame
    Color3 : Color3
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    Radius : float
    SizeRelativeOffset : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    Transparency : float
    UniqueId : UniqueId
    Visible : bool
    ZIndex : int
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> BrickColor: ...
    @Color.setter
    def Color(self, value: BrickColor) -> BrickColor: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SpotLight(Light):
    def __init__(self) -> None: ...
    Angle : float
    Archivable : bool
    Attributes : RbxAttributes
    Brightness : float
    Capabilities : SecurityCapabilities
    Color : Color3
    DefinesCapabilities : bool
    Enabled : bool
    Face : NormalId
    HistoryId : UniqueId
    Name : str
    Range : float
    Shadows : bool
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SpringConstraint(Constraint):
    def __init__(self) -> None: ...
    Archivable : bool
    Attachment0 : Attachment
    Attachment1 : Attachment
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Coils : float
    Color : BrickColor
    Damping : float
    DefinesCapabilities : bool
    Enabled : bool
    FreeLength : float
    HistoryId : UniqueId
    LimitsEnabled : bool
    MaxForce : float
    MaxLength : float
    MinLength : float
    Name : str
    Radius : float
    SourceAssetId : int
    Stiffness : float
    Tags : HashSet_1[str]
    Thickness : float
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StandalonePluginScripts(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StarterCharacterScripts(StarterPlayerScripts):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StarterGear(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StarterGui(BasePlayerGui):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    ResetPlayerGuiOnSpawn : bool
    RtlTextSupport : RtlTextSupport
    ScreenOrientation : ScreenOrientation
    ShowDevelopmentGui : bool
    SourceAssetId : int
    StudioDefaultStyleSheet : StyleSheet
    StudioInsertWidgetLayerCollectorAutoLinkStyleSheet : StyleSheet
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    VirtualCursorMode : VirtualCursorMode
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StarterPack(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StarterPlayer(Instance):
    def __init__(self) -> None: ...
    AllowCustomAnimations : bool
    Archivable : bool
    Attributes : RbxAttributes
    AutoJumpEnabled : bool
    AvatarJointUpgrade_SerializedRollout : RolloutState
    CameraMaxZoomDistance : float
    CameraMinZoomDistance : float
    CameraMode : CameraMode
    Capabilities : SecurityCapabilities
    CharacterJumpHeight : float
    CharacterJumpPower : float
    CharacterMaxSlopeAngle : float
    CharacterUseJumpPower : bool
    CharacterWalkSpeed : float
    ClassicDeath : bool
    DefinesCapabilities : bool
    DevCameraOcclusionMode : DevCameraOcclusionMode
    DevComputerCameraMovementMode : DevComputerCameraMovementMode
    DevComputerMovementMode : DevComputerMovementMode
    DevTouchCameraMovementMode : DevTouchCameraMovementMode
    DevTouchMovementMode : DevTouchMovementMode
    EnableDynamicHeads : LoadDynamicHeads
    EnableMouseLockOption : bool
    GameSettingsAssetIDFace : int
    GameSettingsAssetIDHead : int
    GameSettingsAssetIDLeftArm : int
    GameSettingsAssetIDLeftLeg : int
    GameSettingsAssetIDPants : int
    GameSettingsAssetIDRightArm : int
    GameSettingsAssetIDRightLeg : int
    GameSettingsAssetIDShirt : int
    GameSettingsAssetIDTeeShirt : int
    GameSettingsAssetIDTorso : int
    GameSettingsAvatar : GameAvatarType
    GameSettingsR15Collision : R15CollisionType
    GameSettingsScaleRangeBodyType : NumberRange
    GameSettingsScaleRangeHead : NumberRange
    GameSettingsScaleRangeHeight : NumberRange
    GameSettingsScaleRangeProportion : NumberRange
    GameSettingsScaleRangeWidth : NumberRange
    HealthDisplayDistance : float
    HistoryId : UniqueId
    LoadCharacterAppearance : bool
    LoadCharacterLayeredClothing : LoadCharacterLayeredClothing
    LuaCharacterController : CharacterControlMode
    Name : str
    NameDisplayDistance : float
    RagdollDeath : bool
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    UserEmotesEnabled : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StarterPlayerScripts(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StartPageService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StartupMessageService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Stats(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StopWatchReporter(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StreamingService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StringValue(ValueBase):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Value : str
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StudioAssetService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StudioAttachment(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    AutoHideParent : bool
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    IsArrowVisible : bool
    Name : str
    Offset : Vector2
    SourceAnchorPoint : Vector2
    SourceAssetId : int
    Tags : HashSet_1[str]
    TargetAnchorPoint : Vector2
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StudioCallout(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StudioCameraService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    LockCameraSpeed : bool
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StudioData(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    EnableScriptCollabByDefaultOnLoad : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StudioDeviceEmulatorService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StudioPublishService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    PublishLocked : bool
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StudioScriptDebugEventListener(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StudioSdkService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StudioService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    Secrets : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StudioUserService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StudioWidgetsService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StyleBase(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StyleDerive(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    Priority : int
    SourceAssetId : int
    StyleSheet : StyleSheet
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StyleLink(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    StyleSheet : StyleSheet
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StyleRule(StyleBase):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    Priority : int
    PropertiesSerialize : Array_1[int]
    Selector : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StyleSheet(StyleBase):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class StylingService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SunRaysEffect(PostEffect):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Intensity : float
    Name : str
    SourceAssetId : int
    Spread : float
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SurfaceAppearance(Instance):
    def __init__(self) -> None: ...
    AlphaMode : AlphaMode
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color : Color3
    ColorMapContent : Content
    DefinesCapabilities : bool
    HistoryId : UniqueId
    MetalnessMapContent : Content
    Name : str
    NormalMapContent : Content
    RoughnessMapContent : Content
    SourceAssetId : int
    Tags : HashSet_1[str]
    TexturePack : ContentId
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def ColorMap(self) -> ContentId: ...
    @ColorMap.setter
    def ColorMap(self, value: ContentId) -> ContentId: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def MetalnessMap(self) -> ContentId: ...
    @MetalnessMap.setter
    def MetalnessMap(self, value: ContentId) -> ContentId: ...
    @property
    def NormalMap(self) -> ContentId: ...
    @NormalMap.setter
    def NormalMap(self, value: ContentId) -> ContentId: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def RoughnessMap(self) -> ContentId: ...
    @RoughnessMap.setter
    def RoughnessMap(self, value: ContentId) -> ContentId: ...


class SurfaceGui(SurfaceGuiBase):
    def __init__(self) -> None: ...
    Active : bool
    Adornee : Instance
    AlwaysOnTop : bool
    Archivable : bool
    Attributes : RbxAttributes
    AutoLocalize : bool
    Brightness : float
    CanvasSize : Vector2
    Capabilities : SecurityCapabilities
    ClipsDescendants : bool
    DefinesCapabilities : bool
    Enabled : bool
    Face : NormalId
    HistoryId : UniqueId
    LightInfluence : float
    MaxDistance : float
    Name : str
    PixelsPerStud : float
    ResetOnSpawn : bool
    RootLocalizationTable : LocalizationTable
    SelectionBehaviorDown : SelectionBehavior
    SelectionBehaviorLeft : SelectionBehavior
    SelectionBehaviorRight : SelectionBehavior
    SelectionBehaviorUp : SelectionBehavior
    SelectionGroup : bool
    SizingMode : SurfaceGuiSizingMode
    SourceAssetId : int
    Tags : HashSet_1[str]
    ToolPunchThroughDistance : float
    UniqueId : UniqueId
    ZIndexBehavior : ZIndexBehavior
    ZOffset : float
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Localize(self) -> bool: ...
    @Localize.setter
    def Localize(self, value: bool) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SurfaceGuiBase(LayerCollector):
    Active : bool
    Adornee : Instance
    Archivable : bool
    Attributes : RbxAttributes
    AutoLocalize : bool
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    Face : NormalId
    HistoryId : UniqueId
    Name : str
    ResetOnSpawn : bool
    RootLocalizationTable : LocalizationTable
    SelectionBehaviorDown : SelectionBehavior
    SelectionBehaviorLeft : SelectionBehavior
    SelectionBehaviorRight : SelectionBehavior
    SelectionBehaviorUp : SelectionBehavior
    SelectionGroup : bool
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    ZIndexBehavior : ZIndexBehavior
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Localize(self) -> bool: ...
    @Localize.setter
    def Localize(self, value: bool) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SurfaceLight(Light):
    def __init__(self) -> None: ...
    Angle : float
    Archivable : bool
    Attributes : RbxAttributes
    Brightness : float
    Capabilities : SecurityCapabilities
    Color : Color3
    DefinesCapabilities : bool
    Enabled : bool
    Face : NormalId
    HistoryId : UniqueId
    Name : str
    Range : float
    Shadows : bool
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SurfaceSelection(PartAdornment):
    def __init__(self) -> None: ...
    Adornee : BasePart
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color3 : Color3
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    TargetSurface : NormalId
    Transparency : float
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> BrickColor: ...
    @Color.setter
    def Color(self, value: BrickColor) -> BrickColor: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SwimController(ControllerBase):
    def __init__(self) -> None: ...
    AccelerationTime : float
    Archivable : bool
    Attributes : RbxAttributes
    BalanceRigidityEnabled : bool
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    MoveSpeedFactor : float
    Name : str
    PitchMaxTorque : float
    PitchSpeedFactor : float
    RollMaxTorque : float
    RollSpeedFactor : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class SystemThemeService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class TaskScheduler(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    ThreadPoolConfig : ThreadPoolConfig
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Team(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    AutoAssignable : bool
    AutoColorCharacters : bool
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    Score : int
    SourceAssetId : int
    Tags : HashSet_1[str]
    TeamColor : BrickColor
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class TeamCreateData(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class TeamCreatePublishService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class TeamCreateService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Teams(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class TelemetryService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class TeleportOptions(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    ReservedServerAccessCode : str
    ServerInstanceId : str
    ShouldReserveServer : bool
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class TeleportService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    CustomizedTeleportUI : bool
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class TemporaryCageMeshProvider(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class TemporaryScriptService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Terrain(BasePart):
    def __init__(self) -> None: ...
    AcquisitionMethod : TerrainAcquisitionMethod
    Anchored : bool
    Archivable : bool
    Attributes : RbxAttributes
    AudioCanCollide : bool
    BackParamA : float
    BackParamB : float
    BackSurface : SurfaceType
    BackSurfaceInput : InputType
    BottomParamA : float
    BottomParamB : float
    BottomSurface : SurfaceType
    BottomSurfaceInput : InputType
    CanCollide : bool
    CanQuery : bool
    CanTouch : bool
    Capabilities : SecurityCapabilities
    CastShadow : bool
    CFrame : CFrame
    CollisionGroup : str
    CollisionGroupId : int
    Color3uint8 : Color3uint8
    CustomPhysicalProperties : PhysicalProperties
    Decoration : bool
    DefinesCapabilities : bool
    Elasticity : float
    EnableFluidForces : bool
    Friction : float
    FrontParamA : float
    FrontParamB : float
    FrontSurface : SurfaceType
    FrontSurfaceInput : InputType
    GrassLength : float
    HistoryId : UniqueId
    LeftParamA : float
    LeftParamB : float
    LeftSurface : SurfaceType
    LeftSurfaceInput : InputType
    Locked : bool
    Massless : bool
    Material : Material
    MaterialColors : Array_1[int]
    MaterialVariantSerialized : str
    Name : str
    PhysicsGrid : Array_1[int]
    PivotOffset : CFrame
    Reflectance : float
    RightParamA : float
    RightParamB : float
    RightSurface : SurfaceType
    RightSurfaceInput : InputType
    RootPriority : int
    RotVelocity : Vector3
    size : Vector3
    SmoothGrid : Array_1[int]
    SmoothVoxelsUpgraded : bool
    SourceAssetId : int
    Tags : HashSet_1[str]
    TopParamA : float
    TopParamB : float
    TopSurface : SurfaceType
    TopSurfaceInput : InputType
    Transparency : float
    UniqueId : UniqueId
    Velocity : Vector3
    WaterColor : Color3
    WaterReflectance : float
    WaterTransparency : float
    WaterWaveSize : float
    WaterWaveSpeed : float
    @property
    def brickColor(self) -> BrickColor: ...
    @brickColor.setter
    def brickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BrickColor(self) -> BrickColor: ...
    @BrickColor.setter
    def BrickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> Color3: ...
    @Color.setter
    def Color(self, value: Color3) -> Color3: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Size(self) -> Vector3: ...
    @Size.setter
    def Size(self, value: Vector3) -> Vector3: ...


class TerrainDetail(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    ColorMapContent : Content
    DefinesCapabilities : bool
    Face : TerrainFace
    HistoryId : UniqueId
    MaterialPattern : MaterialPattern
    MetalnessMapContent : Content
    Name : str
    NormalMapContent : Content
    RoughnessMapContent : Content
    SourceAssetId : int
    StudsPerTile : float
    Tags : HashSet_1[str]
    TexturePack : ContentId
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def ColorMap(self) -> ContentId: ...
    @ColorMap.setter
    def ColorMap(self, value: ContentId) -> ContentId: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def MetalnessMap(self) -> ContentId: ...
    @MetalnessMap.setter
    def MetalnessMap(self, value: ContentId) -> ContentId: ...
    @property
    def NormalMap(self) -> ContentId: ...
    @NormalMap.setter
    def NormalMap(self, value: ContentId) -> ContentId: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def RoughnessMap(self) -> ContentId: ...
    @RoughnessMap.setter
    def RoughnessMap(self, value: ContentId) -> ContentId: ...


class TerrainRegion(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    ExtentsMax : Vector3int16
    ExtentsMin : Vector3int16
    HistoryId : UniqueId
    Name : str
    SmoothGrid : Array_1[int]
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class TestService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    AutoRuns : bool
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Description : str
    ExecuteWithStudioRun : bool
    HistoryId : UniqueId
    Is30FpsThrottleEnabled : bool
    IsPhysicsEnvironmentalThrottled : bool
    IsSleepAllowed : bool
    Name : str
    NumberOfPlayers : int
    SimulateSecondsLag : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    ThrottlePhysicsToRealtime : bool
    Timeout : float
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class TextBox(GuiObject):
    def __init__(self) -> None: ...
    Active : bool
    AnchorPoint : Vector2
    Archivable : bool
    Attributes : RbxAttributes
    AutoLocalize : bool
    AutomaticSize : AutomaticSize
    BackgroundColor3 : Color3
    BackgroundTransparency : float
    BorderColor3 : Color3
    BorderMode : BorderMode
    BorderSizePixel : int
    Capabilities : SecurityCapabilities
    ClearTextOnFocus : bool
    ClipsDescendants : bool
    DefinesCapabilities : bool
    Draggable : bool
    FontFace : FontFace
    HistoryId : UniqueId
    Interactable : bool
    LayoutOrder : int
    LineHeight : float
    LocalizationMatchedSourceText : str
    LocalizationMatchIdentifier : str
    MaxVisibleGraphemes : int
    MultiLine : bool
    Name : str
    NextSelectionDown : GuiObject
    NextSelectionLeft : GuiObject
    NextSelectionRight : GuiObject
    NextSelectionUp : GuiObject
    OpenTypeFeatures : str
    PlaceholderColor3 : Color3
    PlaceholderText : str
    Position : UDim2
    RichText : bool
    RootLocalizationTable : LocalizationTable
    Rotation : float
    Selectable : bool
    SelectionBehaviorDown : SelectionBehavior
    SelectionBehaviorLeft : SelectionBehavior
    SelectionBehaviorRight : SelectionBehavior
    SelectionBehaviorUp : SelectionBehavior
    SelectionGroup : bool
    SelectionImageObject : GuiObject
    SelectionOrder : int
    ShowNativeInput : bool
    Size : UDim2
    SizeConstraint : SizeConstraint
    SourceAssetId : int
    Tags : HashSet_1[str]
    Text : str
    TextColor3 : Color3
    TextDirection : TextDirection
    TextEditable : bool
    TextScaled : bool
    TextSize : float
    TextStrokeColor3 : Color3
    TextStrokeTransparency : float
    TextTransparency : float
    TextTruncate : TextTruncate
    TextWrapped : bool
    TextXAlignment : TextXAlignment
    TextYAlignment : TextYAlignment
    UniqueId : UniqueId
    Visible : bool
    ZIndex : int
    @property
    def BackgroundColor(self) -> BrickColor: ...
    @BackgroundColor.setter
    def BackgroundColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BorderColor(self) -> BrickColor: ...
    @BorderColor.setter
    def BorderColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def Font(self) -> Font: ...
    @Font.setter
    def Font(self, value: Font) -> Font: ...
    @property
    def FontSize(self) -> FontSize: ...
    @FontSize.setter
    def FontSize(self, value: FontSize) -> FontSize: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Localize(self) -> bool: ...
    @Localize.setter
    def Localize(self, value: bool) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def TextColor(self) -> BrickColor: ...
    @TextColor.setter
    def TextColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def TextWrap(self) -> bool: ...
    @TextWrap.setter
    def TextWrap(self, value: bool) -> bool: ...
    @property
    def Transparency(self) -> float: ...
    @Transparency.setter
    def Transparency(self, value: float) -> float: ...


class TextBoxService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class TextButton(GuiButton):
    def __init__(self) -> None: ...
    Active : bool
    AnchorPoint : Vector2
    Archivable : bool
    Attributes : RbxAttributes
    AutoButtonColor : bool
    AutoLocalize : bool
    AutomaticSize : AutomaticSize
    BackgroundColor3 : Color3
    BackgroundTransparency : float
    BorderColor3 : Color3
    BorderMode : BorderMode
    BorderSizePixel : int
    Capabilities : SecurityCapabilities
    ClipsDescendants : bool
    DefinesCapabilities : bool
    Draggable : bool
    FontFace : FontFace
    HistoryId : UniqueId
    HoverHapticEffect : HapticEffect
    Interactable : bool
    LayoutOrder : int
    LineHeight : float
    LocalizationMatchedSourceText : str
    LocalizationMatchIdentifier : str
    MaxVisibleGraphemes : int
    Modal : bool
    Name : str
    NextSelectionDown : GuiObject
    NextSelectionLeft : GuiObject
    NextSelectionRight : GuiObject
    NextSelectionUp : GuiObject
    OpenTypeFeatures : str
    Position : UDim2
    PressHapticEffect : HapticEffect
    RichText : bool
    RootLocalizationTable : LocalizationTable
    Rotation : float
    Selectable : bool
    Selected : bool
    SelectionBehaviorDown : SelectionBehavior
    SelectionBehaviorLeft : SelectionBehavior
    SelectionBehaviorRight : SelectionBehavior
    SelectionBehaviorUp : SelectionBehavior
    SelectionGroup : bool
    SelectionImageObject : GuiObject
    SelectionOrder : int
    Size : UDim2
    SizeConstraint : SizeConstraint
    SourceAssetId : int
    Style : ButtonStyle
    Tags : HashSet_1[str]
    Text : str
    TextColor3 : Color3
    TextDirection : TextDirection
    TextScaled : bool
    TextSize : float
    TextStrokeColor3 : Color3
    TextStrokeTransparency : float
    TextTransparency : float
    TextTruncate : TextTruncate
    TextWrapped : bool
    TextXAlignment : TextXAlignment
    TextYAlignment : TextYAlignment
    UniqueId : UniqueId
    Visible : bool
    ZIndex : int
    @property
    def BackgroundColor(self) -> BrickColor: ...
    @BackgroundColor.setter
    def BackgroundColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BorderColor(self) -> BrickColor: ...
    @BorderColor.setter
    def BorderColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def Font(self) -> Font: ...
    @Font.setter
    def Font(self, value: Font) -> Font: ...
    @property
    def FontSize(self) -> FontSize: ...
    @FontSize.setter
    def FontSize(self, value: FontSize) -> FontSize: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Localize(self) -> bool: ...
    @Localize.setter
    def Localize(self, value: bool) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def TextColor(self) -> BrickColor: ...
    @TextColor.setter
    def TextColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def TextWrap(self) -> bool: ...
    @TextWrap.setter
    def TextWrap(self, value: bool) -> bool: ...
    @property
    def Transparency(self) -> float: ...
    @Transparency.setter
    def Transparency(self, value: float) -> float: ...


class TextChannel(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class TextChatCommand(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    AutocompleteVisible : bool
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    PrimaryAlias : str
    SecondaryAlias : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class TextChatConfigurations(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class TextChatMessageProperties(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class TextChatService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    ChatTranslationFTUXShown : bool
    ChatTranslationToggleEnabled : bool
    ChatVersion : ChatVersion
    CreateDefaultCommands : bool
    CreateDefaultTextChannels : bool
    DefinesCapabilities : bool
    HasSeenDeprecationDialog : bool
    HistoryId : UniqueId
    isLegacyChatDisabled : bool
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class TextLabel(GuiLabel):
    def __init__(self) -> None: ...
    Active : bool
    AnchorPoint : Vector2
    Archivable : bool
    Attributes : RbxAttributes
    AutoLocalize : bool
    AutomaticSize : AutomaticSize
    BackgroundColor3 : Color3
    BackgroundTransparency : float
    BorderColor3 : Color3
    BorderMode : BorderMode
    BorderSizePixel : int
    Capabilities : SecurityCapabilities
    ClipsDescendants : bool
    DefinesCapabilities : bool
    Draggable : bool
    FontFace : FontFace
    HistoryId : UniqueId
    Interactable : bool
    LayoutOrder : int
    LineHeight : float
    LocalizationMatchedSourceText : str
    LocalizationMatchIdentifier : str
    MaxVisibleGraphemes : int
    Name : str
    NextSelectionDown : GuiObject
    NextSelectionLeft : GuiObject
    NextSelectionRight : GuiObject
    NextSelectionUp : GuiObject
    OpenTypeFeatures : str
    Position : UDim2
    RichText : bool
    RootLocalizationTable : LocalizationTable
    Rotation : float
    Selectable : bool
    SelectionBehaviorDown : SelectionBehavior
    SelectionBehaviorLeft : SelectionBehavior
    SelectionBehaviorRight : SelectionBehavior
    SelectionBehaviorUp : SelectionBehavior
    SelectionGroup : bool
    SelectionImageObject : GuiObject
    SelectionOrder : int
    Size : UDim2
    SizeConstraint : SizeConstraint
    SourceAssetId : int
    Tags : HashSet_1[str]
    Text : str
    TextColor3 : Color3
    TextDirection : TextDirection
    TextScaled : bool
    TextSize : float
    TextStrokeColor3 : Color3
    TextStrokeTransparency : float
    TextTransparency : float
    TextTruncate : TextTruncate
    TextWrapped : bool
    TextXAlignment : TextXAlignment
    TextYAlignment : TextYAlignment
    UniqueId : UniqueId
    Visible : bool
    ZIndex : int
    @property
    def BackgroundColor(self) -> BrickColor: ...
    @BackgroundColor.setter
    def BackgroundColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BorderColor(self) -> BrickColor: ...
    @BorderColor.setter
    def BorderColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def Font(self) -> Font: ...
    @Font.setter
    def Font(self, value: Font) -> Font: ...
    @property
    def FontSize(self) -> FontSize: ...
    @FontSize.setter
    def FontSize(self, value: FontSize) -> FontSize: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Localize(self) -> bool: ...
    @Localize.setter
    def Localize(self, value: bool) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def TextColor(self) -> BrickColor: ...
    @TextColor.setter
    def TextColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def TextWrap(self) -> bool: ...
    @TextWrap.setter
    def TextWrap(self, value: bool) -> bool: ...
    @property
    def Transparency(self) -> float: ...
    @Transparency.setter
    def Transparency(self, value: float) -> float: ...


class TextService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Texture(Decal):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color3 : Color3
    DefinesCapabilities : bool
    Face : NormalId
    HistoryId : UniqueId
    Name : str
    OffsetStudsU : float
    OffsetStudsV : float
    Shiny : float
    SourceAssetId : int
    Specular : float
    StudsPerTileU : float
    StudsPerTileV : float
    Tags : HashSet_1[str]
    TextureContent : Content
    Transparency : float
    UniqueId : UniqueId
    ZIndex : int
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Texture(self) -> ContentId: ...
    @Texture.setter
    def Texture(self, value: ContentId) -> ContentId: ...


class TextureGenerationService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ThirdPartyUserService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class TimerService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ToastNotificationService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Tool(BackpackItem):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    CanBeDropped : bool
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    Grip : CFrame
    HistoryId : UniqueId
    LevelOfDetail : ModelLevelOfDetail
    ManualActivationOnly : bool
    ModelMeshCFrame : CFrame
    ModelMeshData : SharedString
    ModelMeshSize : Vector3
    ModelStreamingMode : ModelStreamingMode
    Name : str
    NeedsPivotMigration : bool
    PrimaryPart : BasePart
    RequiresHandle : bool
    ScaleFactor : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    TextureId : ContentId
    ToolTip : str
    UniqueId : UniqueId
    WorldPivotData : Optional_1[CFrame]
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Torque(Constraint):
    def __init__(self) -> None: ...
    Archivable : bool
    Attachment0 : Attachment
    Attachment1 : Attachment
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color : BrickColor
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    RelativeTo : ActuatorRelativeTo
    SourceAssetId : int
    Tags : HashSet_1[str]
    Torque_ : Vector3
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class TorsionSpringConstraint(Constraint):
    def __init__(self) -> None: ...
    Archivable : bool
    Attachment0 : Attachment
    Attachment1 : Attachment
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Coils : float
    Color : BrickColor
    Damping : float
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    LimitEnabled : bool
    LimitsEnabled : bool
    MaxAngle : float
    MaxTorque : float
    Name : str
    Radius : float
    Restitution : float
    SourceAssetId : int
    Stiffness : float
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class TouchInputService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class TracerService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class TrackerStreamAnimation(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Trail(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attachment0 : Attachment
    Attachment1 : Attachment
    Attributes : RbxAttributes
    Brightness : float
    Capabilities : SecurityCapabilities
    Color : ColorSequence
    DefinesCapabilities : bool
    Enabled : bool
    FaceCamera : bool
    HistoryId : UniqueId
    Lifetime : float
    LightEmission : float
    LightInfluence : float
    MaxLength : float
    MinLength : float
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    Texture : ContentId
    TextureLength : float
    TextureMode : TextureMode
    Transparency : NumberSequence
    UniqueId : UniqueId
    WidthScale : NumberSequence
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class TremoloSoundEffect(SoundEffect):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Depth : float
    Duty : float
    Enabled : bool
    Frequency : float
    HistoryId : UniqueId
    Name : str
    Priority : int
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class TriangleMeshPart(BasePart):
    def __init__(self) -> None: ...
    AeroMeshData : SharedString
    Anchored : bool
    Archivable : bool
    Attributes : RbxAttributes
    AudioCanCollide : bool
    BackParamA : float
    BackParamB : float
    BackSurface : SurfaceType
    BackSurfaceInput : InputType
    BottomParamA : float
    BottomParamB : float
    BottomSurface : SurfaceType
    BottomSurfaceInput : InputType
    CanCollide : bool
    CanQuery : bool
    CanTouch : bool
    Capabilities : SecurityCapabilities
    CastShadow : bool
    CFrame : CFrame
    CollisionGroup : str
    CollisionGroupId : int
    Color3uint8 : Color3uint8
    CustomPhysicalProperties : PhysicalProperties
    DefinesCapabilities : bool
    Elasticity : float
    EnableFluidForces : bool
    FluidFidelityInternal : FluidFidelity
    Friction : float
    FrontParamA : float
    FrontParamB : float
    FrontSurface : SurfaceType
    FrontSurfaceInput : InputType
    HistoryId : UniqueId
    LeftParamA : float
    LeftParamB : float
    LeftSurface : SurfaceType
    LeftSurfaceInput : InputType
    Locked : bool
    Massless : bool
    Material : Material
    MaterialVariantSerialized : str
    Name : str
    PhysicalConfigData : SharedString
    PivotOffset : CFrame
    Reflectance : float
    RightParamA : float
    RightParamB : float
    RightSurface : SurfaceType
    RightSurfaceInput : InputType
    RootPriority : int
    RotVelocity : Vector3
    size : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    TopParamA : float
    TopParamB : float
    TopSurface : SurfaceType
    TopSurfaceInput : InputType
    Transparency : float
    UniqueId : UniqueId
    UnscaledCofm : Vector3
    UnscaledVolInertiaDiags : Vector3
    UnscaledVolInertiaOffDiags : Vector3
    UnscaledVolume : float
    Velocity : Vector3
    @property
    def brickColor(self) -> BrickColor: ...
    @brickColor.setter
    def brickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BrickColor(self) -> BrickColor: ...
    @BrickColor.setter
    def BrickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> Color3: ...
    @Color.setter
    def Color(self, value: Color3) -> Color3: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Size(self) -> Vector3: ...
    @Size.setter
    def Size(self, value: Vector3) -> Vector3: ...


class TrussPart(BasePart):
    def __init__(self) -> None: ...
    Anchored : bool
    Archivable : bool
    Attributes : RbxAttributes
    AudioCanCollide : bool
    BackParamA : float
    BackParamB : float
    BackSurface : SurfaceType
    BackSurfaceInput : InputType
    BottomParamA : float
    BottomParamB : float
    BottomSurface : SurfaceType
    BottomSurfaceInput : InputType
    CanCollide : bool
    CanQuery : bool
    CanTouch : bool
    Capabilities : SecurityCapabilities
    CastShadow : bool
    CFrame : CFrame
    CollisionGroup : str
    CollisionGroupId : int
    Color3uint8 : Color3uint8
    CustomPhysicalProperties : PhysicalProperties
    DefinesCapabilities : bool
    Elasticity : float
    EnableFluidForces : bool
    Friction : float
    FrontParamA : float
    FrontParamB : float
    FrontSurface : SurfaceType
    FrontSurfaceInput : InputType
    HistoryId : UniqueId
    LeftParamA : float
    LeftParamB : float
    LeftSurface : SurfaceType
    LeftSurfaceInput : InputType
    Locked : bool
    Massless : bool
    Material : Material
    MaterialVariantSerialized : str
    Name : str
    PivotOffset : CFrame
    Reflectance : float
    RightParamA : float
    RightParamB : float
    RightSurface : SurfaceType
    RightSurfaceInput : InputType
    RootPriority : int
    RotVelocity : Vector3
    size : Vector3
    SourceAssetId : int
    style : Style
    Tags : HashSet_1[str]
    TopParamA : float
    TopParamB : float
    TopSurface : SurfaceType
    TopSurfaceInput : InputType
    Transparency : float
    UniqueId : UniqueId
    Velocity : Vector3
    @property
    def brickColor(self) -> BrickColor: ...
    @brickColor.setter
    def brickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BrickColor(self) -> BrickColor: ...
    @BrickColor.setter
    def BrickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> Color3: ...
    @Color.setter
    def Color(self, value: Color3) -> Color3: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Size(self) -> Vector3: ...
    @Size.setter
    def Size(self, value: Vector3) -> Vector3: ...
    @property
    def Style(self) -> Style: ...
    @Style.setter
    def Style(self, value: Style) -> Style: ...


class TutorialService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Tween(TweenBase):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class TweenBase(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class TweenService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UGCAvatarService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UGCValidationService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UIAspectRatioConstraint(UIConstraint):
    def __init__(self) -> None: ...
    Archivable : bool
    AspectRatio : float
    AspectType : AspectType
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    DominantAxis : DominantAxis
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UIBase(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UIComponent(UIBase):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UIConstraint(UIComponent):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UICorner(UIComponent):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    CornerRadius : UDim
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UIDragDetector(UIComponent):
    def __init__(self) -> None: ...
    ActivatedCursorIcon : ContentId
    Archivable : bool
    Attributes : RbxAttributes
    BoundingBehavior : UIDragDetectorBoundingBehavior
    BoundingUI : GuiBase2d
    Capabilities : SecurityCapabilities
    CursorIcon : ContentId
    DefinesCapabilities : bool
    DragAxis : Vector2
    DragRelativity : UIDragDetectorDragRelativity
    DragRotation : float
    DragSpace : UIDragDetectorDragSpace
    DragStyle : UIDragDetectorDragStyle
    DragUDim2 : UDim2
    Enabled : bool
    HistoryId : UniqueId
    MaxDragAngle : float
    MaxDragTranslation : UDim2
    MinDragAngle : float
    MinDragTranslation : UDim2
    Name : str
    ReferenceUIInstance : GuiObject
    ResponseStyle : UIDragDetectorResponseStyle
    SelectionModeDragSpeed : UDim2
    SelectionModeRotateSpeed : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UIDragSpeedAxisMapping : UIDragSpeedAxisMapping
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UIDragDetectorService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UIFlexItem(UIComponent):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    FlexMode : UIFlexMode
    GrowRatio : float
    HistoryId : UniqueId
    ItemLineAlignment : ItemLineAlignment
    Name : str
    ShrinkRatio : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UIGradient(UIComponent):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color : ColorSequence
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    Offset : Vector2
    Rotation : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    Transparency : NumberSequence
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UIGridLayout(UIGridStyleLayout):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    CellPadding : UDim2
    CellSize : UDim2
    DefinesCapabilities : bool
    FillDirection : FillDirection
    FillDirectionMaxCells : int
    HistoryId : UniqueId
    HorizontalAlignment : HorizontalAlignment
    Name : str
    SortOrder : SortOrder
    SourceAssetId : int
    StartCorner : StartCorner
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    VerticalAlignment : VerticalAlignment
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UIGridStyleLayout(UILayout):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    FillDirection : FillDirection
    HistoryId : UniqueId
    HorizontalAlignment : HorizontalAlignment
    Name : str
    SortOrder : SortOrder
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    VerticalAlignment : VerticalAlignment
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UILayout(UIComponent):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UIListLayout(UIGridStyleLayout):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    FillDirection : FillDirection
    HistoryId : UniqueId
    HorizontalAlignment : HorizontalAlignment
    HorizontalFlex : UIFlexAlignment
    ItemLineAlignment : ItemLineAlignment
    Name : str
    Padding : UDim
    SortOrder : SortOrder
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    VerticalAlignment : VerticalAlignment
    VerticalFlex : UIFlexAlignment
    Wraps : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UIPadding(UIComponent):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    PaddingBottom : UDim
    PaddingLeft : UDim
    PaddingRight : UDim
    PaddingTop : UDim
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UIPageLayout(UIGridStyleLayout):
    def __init__(self) -> None: ...
    Animated : bool
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Circular : bool
    DefinesCapabilities : bool
    EasingDirection : EasingDirection
    EasingStyle : EasingStyle
    FillDirection : FillDirection
    GamepadInputEnabled : bool
    HistoryId : UniqueId
    HorizontalAlignment : HorizontalAlignment
    Name : str
    Padding : UDim
    ScrollWheelInputEnabled : bool
    SortOrder : SortOrder
    SourceAssetId : int
    Tags : HashSet_1[str]
    TouchInputEnabled : bool
    TweenTime : float
    UniqueId : UniqueId
    VerticalAlignment : VerticalAlignment
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UIScale(UIComponent):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    Scale : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UISizeConstraint(UIConstraint):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    MaxSize : Vector2
    MinSize : Vector2
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UIStroke(UIComponent):
    def __init__(self) -> None: ...
    ApplyStrokeMode : ApplyStrokeMode
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color : Color3
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    LineJoinMode : LineJoinMode
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    Thickness : float
    Transparency : float
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UITableLayout(UIGridStyleLayout):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    FillDirection : FillDirection
    FillEmptySpaceColumns : bool
    FillEmptySpaceRows : bool
    HistoryId : UniqueId
    HorizontalAlignment : HorizontalAlignment
    MajorAxis : TableMajorAxis
    Name : str
    Padding : UDim2
    SortOrder : SortOrder
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    VerticalAlignment : VerticalAlignment
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UITextSizeConstraint(UIConstraint):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    MaxTextSize : int
    MinTextSize : int
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UnionOperation(PartOperation):
    def __init__(self) -> None: ...
    AeroMeshData : SharedString
    Anchored : bool
    Archivable : bool
    AssetId : ContentId
    Attributes : RbxAttributes
    AudioCanCollide : bool
    BackParamA : float
    BackParamB : float
    BackSurface : SurfaceType
    BackSurfaceInput : InputType
    BottomParamA : float
    BottomParamB : float
    BottomSurface : SurfaceType
    BottomSurfaceInput : InputType
    CanCollide : bool
    CanQuery : bool
    CanTouch : bool
    Capabilities : SecurityCapabilities
    CastShadow : bool
    CFrame : CFrame
    ChildData : Array_1[int]
    ChildData2 : SharedString
    CollisionGroup : str
    CollisionGroupId : int
    Color3uint8 : Color3uint8
    ComponentIndex : int
    CustomPhysicalProperties : PhysicalProperties
    DefinesCapabilities : bool
    Elasticity : float
    EnableFluidForces : bool
    FluidFidelityInternal : FluidFidelity
    FormFactor : FormFactor
    Friction : float
    FrontParamA : float
    FrontParamB : float
    FrontSurface : SurfaceType
    FrontSurfaceInput : InputType
    HistoryId : UniqueId
    InitialSize : Vector3
    LeftParamA : float
    LeftParamB : float
    LeftSurface : SurfaceType
    LeftSurfaceInput : InputType
    Locked : bool
    Massless : bool
    Material : Material
    MaterialVariantSerialized : str
    MeshData : Array_1[int]
    MeshData2 : SharedString
    Name : str
    OffCentered : bool
    PhysicalConfigData : SharedString
    PhysicsData : Array_1[int]
    PivotOffset : CFrame
    Reflectance : float
    RenderFidelity : RenderFidelity
    RightParamA : float
    RightParamB : float
    RightSurface : SurfaceType
    RightSurfaceInput : InputType
    RootPriority : int
    RotVelocity : Vector3
    size : Vector3
    SmoothingAngle : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    TopParamA : float
    TopParamB : float
    TopSurface : SurfaceType
    TopSurfaceInput : InputType
    Transparency : float
    UniqueId : UniqueId
    UnscaledCofm : Vector3
    UnscaledVolInertiaDiags : Vector3
    UnscaledVolInertiaOffDiags : Vector3
    UnscaledVolume : float
    UsePartColor : bool
    Velocity : Vector3
    @property
    def brickColor(self) -> BrickColor: ...
    @brickColor.setter
    def brickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BrickColor(self) -> BrickColor: ...
    @BrickColor.setter
    def BrickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> Color3: ...
    @Color.setter
    def Color(self, value: Color3) -> Color3: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Size(self) -> Vector3: ...
    @Size.setter
    def Size(self, value: Vector3) -> Vector3: ...


class UniqueIdLookupService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UniversalConstraint(Constraint):
    def __init__(self) -> None: ...
    Archivable : bool
    Attachment0 : Attachment
    Attachment1 : Attachment
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color : BrickColor
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    LimitsEnabled : bool
    MaxAngle : float
    Name : str
    Radius : float
    Restitution : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UnreliableRemoteEvent(BaseRemoteEvent):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UnvalidatedAssetService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    CachedData : str
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UserInputService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    LegacyInputEventsEnabled : bool
    MouseBehavior : MouseBehavior
    MouseIcon : ContentId
    MouseIconEnabled : bool
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UserService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class UserStorageService(LocalStorageService):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ValueBase(Instance, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Vector3Curve(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Vector3Value(ValueBase):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Value : Vector3
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class VectorForce(Constraint):
    def __init__(self) -> None: ...
    ApplyAtCenterOfMass : bool
    Archivable : bool
    Attachment0 : Attachment
    Attachment1 : Attachment
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    Color : BrickColor
    DefinesCapabilities : bool
    Enabled : bool
    Force : Vector3
    HistoryId : UniqueId
    Name : str
    RelativeTo : ActuatorRelativeTo
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Visible : bool
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class VehicleController(Controller):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class VehicleSeat(BasePart):
    def __init__(self) -> None: ...
    Anchored : bool
    Archivable : bool
    Attributes : RbxAttributes
    AudioCanCollide : bool
    BackParamA : float
    BackParamB : float
    BackSurface : SurfaceType
    BackSurfaceInput : InputType
    BottomParamA : float
    BottomParamB : float
    BottomSurface : SurfaceType
    BottomSurfaceInput : InputType
    CanCollide : bool
    CanQuery : bool
    CanTouch : bool
    Capabilities : SecurityCapabilities
    CastShadow : bool
    CFrame : CFrame
    CollisionGroup : str
    CollisionGroupId : int
    Color3uint8 : Color3uint8
    CustomPhysicalProperties : PhysicalProperties
    DefinesCapabilities : bool
    Disabled : bool
    Elasticity : float
    EnableFluidForces : bool
    Friction : float
    FrontParamA : float
    FrontParamB : float
    FrontSurface : SurfaceType
    FrontSurfaceInput : InputType
    HeadsUpDisplay : bool
    HistoryId : UniqueId
    LeftParamA : float
    LeftParamB : float
    LeftSurface : SurfaceType
    LeftSurfaceInput : InputType
    Locked : bool
    Massless : bool
    Material : Material
    MaterialVariantSerialized : str
    MaxSpeed : float
    Name : str
    PivotOffset : CFrame
    Reflectance : float
    RightParamA : float
    RightParamB : float
    RightSurface : SurfaceType
    RightSurfaceInput : InputType
    RootPriority : int
    RotVelocity : Vector3
    size : Vector3
    SourceAssetId : int
    Steer : int
    SteerFloat : float
    Tags : HashSet_1[str]
    Throttle : int
    ThrottleFloat : float
    TopParamA : float
    TopParamB : float
    TopSurface : SurfaceType
    TopSurfaceInput : InputType
    Torque : float
    Transparency : float
    TurnSpeed : float
    UniqueId : UniqueId
    Velocity : Vector3
    @property
    def brickColor(self) -> BrickColor: ...
    @brickColor.setter
    def brickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BrickColor(self) -> BrickColor: ...
    @BrickColor.setter
    def BrickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> Color3: ...
    @Color.setter
    def Color(self, value: Color3) -> Color3: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Size(self) -> Vector3: ...
    @Size.setter
    def Size(self, value: Vector3) -> Vector3: ...


class VelocityMotor(JointInstance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    C0 : CFrame
    C1 : CFrame
    Capabilities : SecurityCapabilities
    CurrentAngle : float
    DefinesCapabilities : bool
    DesiredAngle : float
    Enabled : bool
    HistoryId : UniqueId
    Hole : Hole
    MaxVelocity : float
    Name : str
    Part0 : BasePart
    Part1 : BasePart
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class VersionControlService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class VideoCaptureService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class VideoDeviceInput(Instance):
    def __init__(self) -> None: ...
    Active : bool
    Archivable : bool
    Attributes : RbxAttributes
    CameraId : str
    Capabilities : SecurityCapabilities
    CaptureQuality : VideoDeviceCaptureQuality
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class VideoDisplay(GuiObject):
    def __init__(self) -> None: ...
    Active : bool
    AnchorPoint : Vector2
    Archivable : bool
    Attributes : RbxAttributes
    AutoLocalize : bool
    AutomaticSize : AutomaticSize
    BackgroundColor3 : Color3
    BackgroundTransparency : float
    BorderColor3 : Color3
    BorderMode : BorderMode
    BorderSizePixel : int
    Capabilities : SecurityCapabilities
    ClipsDescendants : bool
    DefinesCapabilities : bool
    Draggable : bool
    HistoryId : UniqueId
    Interactable : bool
    LayoutOrder : int
    Name : str
    NextSelectionDown : GuiObject
    NextSelectionLeft : GuiObject
    NextSelectionRight : GuiObject
    NextSelectionUp : GuiObject
    Position : UDim2
    ResampleMode : ResamplerMode
    RootLocalizationTable : LocalizationTable
    Rotation : float
    ScaleType : ScaleType
    Selectable : bool
    SelectionBehaviorDown : SelectionBehavior
    SelectionBehaviorLeft : SelectionBehavior
    SelectionBehaviorRight : SelectionBehavior
    SelectionBehaviorUp : SelectionBehavior
    SelectionGroup : bool
    SelectionImageObject : GuiObject
    SelectionOrder : int
    Size : UDim2
    SizeConstraint : SizeConstraint
    SourceAssetId : int
    Tags : HashSet_1[str]
    TileSize : UDim2
    UniqueId : UniqueId
    VideoColor3 : Color3
    VideoRectOffset : Vector2
    VideoRectSize : Vector2
    VideoTransparency : float
    Visible : bool
    ZIndex : int
    @property
    def BackgroundColor(self) -> BrickColor: ...
    @BackgroundColor.setter
    def BackgroundColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BorderColor(self) -> BrickColor: ...
    @BorderColor.setter
    def BorderColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Localize(self) -> bool: ...
    @Localize.setter
    def Localize(self, value: bool) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Transparency(self) -> float: ...
    @Transparency.setter
    def Transparency(self, value: float) -> float: ...


class VideoFrame(GuiObject):
    def __init__(self) -> None: ...
    Active : bool
    AnchorPoint : Vector2
    Archivable : bool
    Attributes : RbxAttributes
    AutoLocalize : bool
    AutomaticSize : AutomaticSize
    BackgroundColor3 : Color3
    BackgroundTransparency : float
    BorderColor3 : Color3
    BorderMode : BorderMode
    BorderSizePixel : int
    Capabilities : SecurityCapabilities
    ClipsDescendants : bool
    DefinesCapabilities : bool
    Draggable : bool
    HistoryId : UniqueId
    Interactable : bool
    LayoutOrder : int
    Looped : bool
    Name : str
    NextSelectionDown : GuiObject
    NextSelectionLeft : GuiObject
    NextSelectionRight : GuiObject
    NextSelectionUp : GuiObject
    Playing : bool
    Position : UDim2
    RootLocalizationTable : LocalizationTable
    Rotation : float
    Selectable : bool
    SelectionBehaviorDown : SelectionBehavior
    SelectionBehaviorLeft : SelectionBehavior
    SelectionBehaviorRight : SelectionBehavior
    SelectionBehaviorUp : SelectionBehavior
    SelectionGroup : bool
    SelectionImageObject : GuiObject
    SelectionOrder : int
    Size : UDim2
    SizeConstraint : SizeConstraint
    SourceAssetId : int
    Tags : HashSet_1[str]
    TimePosition : float
    UniqueId : UniqueId
    Video : ContentId
    VideoContent : Content
    Visible : bool
    Volume : float
    ZIndex : int
    @property
    def BackgroundColor(self) -> BrickColor: ...
    @BackgroundColor.setter
    def BackgroundColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BorderColor(self) -> BrickColor: ...
    @BorderColor.setter
    def BorderColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Localize(self) -> bool: ...
    @Localize.setter
    def Localize(self, value: bool) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Transparency(self) -> float: ...
    @Transparency.setter
    def Transparency(self, value: float) -> float: ...


class VideoPlayer(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Asset : ContentId
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Looping : bool
    Name : str
    PlaybackSpeed : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    TimePosition : float
    UniqueId : UniqueId
    Volume : float
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class VideoService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class ViewportFrame(GuiObject):
    def __init__(self) -> None: ...
    Active : bool
    Ambient : Color3
    AnchorPoint : Vector2
    Archivable : bool
    Attributes : RbxAttributes
    AutoLocalize : bool
    AutomaticSize : AutomaticSize
    BackgroundColor3 : Color3
    BackgroundTransparency : float
    BorderColor3 : Color3
    BorderMode : BorderMode
    BorderSizePixel : int
    CameraCFrame : CFrame
    CameraFieldOfView : float
    Capabilities : SecurityCapabilities
    ClipsDescendants : bool
    DefinesCapabilities : bool
    Draggable : bool
    HistoryId : UniqueId
    ImageColor3 : Color3
    ImageTransparency : float
    Interactable : bool
    LayoutOrder : int
    LightColor : Color3
    LightDirection : Vector3
    Name : str
    NextSelectionDown : GuiObject
    NextSelectionLeft : GuiObject
    NextSelectionRight : GuiObject
    NextSelectionUp : GuiObject
    Position : UDim2
    RootLocalizationTable : LocalizationTable
    Rotation : float
    Selectable : bool
    SelectionBehaviorDown : SelectionBehavior
    SelectionBehaviorLeft : SelectionBehavior
    SelectionBehaviorRight : SelectionBehavior
    SelectionBehaviorUp : SelectionBehavior
    SelectionGroup : bool
    SelectionImageObject : GuiObject
    SelectionOrder : int
    Size : UDim2
    SizeConstraint : SizeConstraint
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    Visible : bool
    ZIndex : int
    @property
    def BackgroundColor(self) -> BrickColor: ...
    @BackgroundColor.setter
    def BackgroundColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BorderColor(self) -> BrickColor: ...
    @BorderColor.setter
    def BorderColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Localize(self) -> bool: ...
    @Localize.setter
    def Localize(self, value: bool) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Transparency(self) -> float: ...
    @Transparency.setter
    def Transparency(self, value: float) -> float: ...


class VirtualInputManager(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class VirtualUser(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class VisibilityCheckDispatcher(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Visit(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class VisualizationMode(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    Title : str
    ToolTip : str
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class VisualizationModeCategory(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    Title : str
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class VisualizationModeService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class VoiceChatInternal(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class VoiceChatService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefaultDistanceAttenuation : VoiceChatDistanceAttenuationType
    DefinesCapabilities : bool
    EnableDefaultVoice : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    UseAudioApi : AudioApiRollout
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class VRService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    AutomaticScaling : VRScaling
    AvatarGestures : bool
    Capabilities : SecurityCapabilities
    ControllerModels : VRControllerModelMode
    DefinesCapabilities : bool
    FadeOutViewOnCollision : bool
    HistoryId : UniqueId
    LaserPointer : VRLaserPointerMode
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class VRStatusService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class WebSocketService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class WebViewService(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class WedgePart(FormFactorPart):
    def __init__(self) -> None: ...
    Anchored : bool
    Archivable : bool
    Attributes : RbxAttributes
    AudioCanCollide : bool
    BackParamA : float
    BackParamB : float
    BackSurface : SurfaceType
    BackSurfaceInput : InputType
    BottomParamA : float
    BottomParamB : float
    BottomSurface : SurfaceType
    BottomSurfaceInput : InputType
    CanCollide : bool
    CanQuery : bool
    CanTouch : bool
    Capabilities : SecurityCapabilities
    CastShadow : bool
    CFrame : CFrame
    CollisionGroup : str
    CollisionGroupId : int
    Color3uint8 : Color3uint8
    CustomPhysicalProperties : PhysicalProperties
    DefinesCapabilities : bool
    Elasticity : float
    EnableFluidForces : bool
    formFactorRaw : FormFactor
    Friction : float
    FrontParamA : float
    FrontParamB : float
    FrontSurface : SurfaceType
    FrontSurfaceInput : InputType
    HistoryId : UniqueId
    LeftParamA : float
    LeftParamB : float
    LeftSurface : SurfaceType
    LeftSurfaceInput : InputType
    Locked : bool
    Massless : bool
    Material : Material
    MaterialVariantSerialized : str
    Name : str
    PivotOffset : CFrame
    Reflectance : float
    RightParamA : float
    RightParamB : float
    RightSurface : SurfaceType
    RightSurfaceInput : InputType
    RootPriority : int
    RotVelocity : Vector3
    size : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    TopParamA : float
    TopParamB : float
    TopSurface : SurfaceType
    TopSurfaceInput : InputType
    Transparency : float
    UniqueId : UniqueId
    Velocity : Vector3
    @property
    def brickColor(self) -> BrickColor: ...
    @brickColor.setter
    def brickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def BrickColor(self) -> BrickColor: ...
    @BrickColor.setter
    def BrickColor(self, value: BrickColor) -> BrickColor: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> Color3: ...
    @Color.setter
    def Color(self, value: Color3) -> Color3: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def formFactor(self) -> FormFactor: ...
    @formFactor.setter
    def formFactor(self, value: FormFactor) -> FormFactor: ...
    @property
    def FormFactor(self) -> FormFactor: ...
    @FormFactor.setter
    def FormFactor(self, value: FormFactor) -> FormFactor: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    @property
    def Size(self) -> Vector3: ...
    @Size.setter
    def Size(self, value: Vector3) -> Vector3: ...


class Weld(JointInstance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    C0 : CFrame
    C1 : CFrame
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    Name : str
    Part0 : BasePart
    Part1 : BasePart
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class WeldConstraint(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    CFrame0 : CFrame
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    Part0Internal : BasePart
    Part1Internal : BasePart
    SourceAssetId : int
    State : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Part0(self) -> BasePart: ...
    @Part0.setter
    def Part0(self, value: BasePart) -> BasePart: ...
    @property
    def Part1(self) -> BasePart: ...
    @Part1.setter
    def Part1(self, value: BasePart) -> BasePart: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Wire(Instance):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    SourceInstance : Instance
    SourceName : str
    Tags : HashSet_1[str]
    TargetInstance : Instance
    TargetName : str
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class WireframeHandleAdornment(HandleAdornment):
    def __init__(self) -> None: ...
    AdornCullingMode : AdornCullingMode
    Adornee : PVInstance
    AlwaysOnTop : bool
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    CFrame : CFrame
    Color3 : Color3
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    Scale : Vector3
    SizeRelativeOffset : Vector3
    SourceAssetId : int
    Tags : HashSet_1[str]
    Thickness : float
    Transparency : float
    UniqueId : UniqueId
    Visible : bool
    ZIndex : int
    @property
    def ClassName(self) -> str: ...
    @property
    def Color(self) -> BrickColor: ...
    @Color.setter
    def Color(self, value: BrickColor) -> BrickColor: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class Workspace(WorldRoot):
    def __init__(self) -> None: ...
    AirDensity : float
    AllowThirdPartySales : bool
    Archivable : bool
    Attributes : RbxAttributes
    AvatarUnificationMode : AvatarUnificationMode
    Capabilities : SecurityCapabilities
    ClientAnimatorThrottling : ClientAnimatorThrottlingMode
    CollisionGroupData : Array_1[int]
    CurrentCamera : Camera
    DefinesCapabilities : bool
    DistributedGameTime : float
    ExplicitAutoJoints : bool
    FallenPartsDestroyHeight : float
    FallHeightEnabled : bool
    FluidForces : FluidForces
    GlobalWind : Vector3
    Gravity : float
    HistoryId : UniqueId
    IKControlConstraintSupport : IKControlConstraintSupport
    LevelOfDetail : ModelLevelOfDetail
    MeshPartHeadsAndAccessories : MeshPartHeadsAndAccessories
    ModelMeshCFrame : CFrame
    ModelMeshData : SharedString
    ModelMeshSize : Vector3
    ModelStreamingBehavior : ModelStreamingBehavior
    ModelStreamingMode : ModelStreamingMode
    MoverConstraintRootBehavior : MoverConstraintRootBehaviorMode
    Name : str
    NeedsPivotMigration : bool
    PathfindingUseImprovedSearch : PathfindingUseImprovedSearch
    PhysicsImprovedSleep : RolloutState
    PhysicsSteppingMethod : PhysicsSteppingMethod
    PlayerCharacterDestroyBehavior : PlayerCharacterDestroyBehavior
    PrimalPhysicsSolver : PrimalPhysicsSolver
    PrimaryPart : BasePart
    RejectCharacterDeletions : RejectCharacterDeletions
    RenderingCacheOptimizations : RenderingCacheOptimizationMode
    ReplicateInstanceDestroySetting : ReplicateInstanceDestroySetting
    Retargeting : AnimatorRetargetingMode
    SandboxedInstanceMode : SandboxedInstanceMode
    ScaleFactor : float
    SignalBehavior2 : SignalBehavior
    SourceAssetId : int
    StreamingEnabled : bool
    StreamingIntegrityMode : StreamingIntegrityMode
    StreamingMinRadius : int
    StreamingTargetRadius : int
    StreamOutBehavior : StreamOutBehavior
    Tags : HashSet_1[str]
    TerrainWeldsFixed : bool
    TouchesUseCollisionGroups : bool
    TouchEventsUseCollisionGroups : RolloutState
    UniqueId : UniqueId
    WorldPivotData : Optional_1[CFrame]
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class WorkspaceAnnotation(Annotation):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class WorldModel(WorldRoot):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    LevelOfDetail : ModelLevelOfDetail
    ModelMeshCFrame : CFrame
    ModelMeshData : SharedString
    ModelMeshSize : Vector3
    ModelStreamingMode : ModelStreamingMode
    Name : str
    NeedsPivotMigration : bool
    PrimaryPart : BasePart
    ScaleFactor : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    WorldPivotData : Optional_1[CFrame]
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class WorldRoot(Model, abc.ABC):
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    LevelOfDetail : ModelLevelOfDetail
    ModelMeshCFrame : CFrame
    ModelMeshData : SharedString
    ModelMeshSize : Vector3
    ModelStreamingMode : ModelStreamingMode
    Name : str
    NeedsPivotMigration : bool
    PrimaryPart : BasePart
    ScaleFactor : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    WorldPivotData : Optional_1[CFrame]
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class WrapDeformer(BaseWrap):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    CageMeshContent : Content
    CageOrigin : CFrame
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    HSRAssetId : ContentId
    HSRData : SharedString
    HSRMeshIdData : SharedString
    ImportOrigin : CFrame
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    TemporaryCageMeshId : ContentId
    UniqueId : UniqueId
    @property
    def CageMeshId(self) -> ContentId: ...
    @CageMeshId.setter
    def CageMeshId(self, value: ContentId) -> ContentId: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class WrapLayer(BaseWrap):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    AutoSkin : WrapLayerAutoSkin
    BindOffset : CFrame
    CageMeshContent : Content
    CageOrigin : CFrame
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    Enabled : bool
    HistoryId : UniqueId
    HSRAssetId : ContentId
    HSRData : SharedString
    HSRMeshIdData : SharedString
    ImportOrigin : CFrame
    MaxSize : Vector3
    Name : str
    Offset : Vector3
    Order : int
    Puffiness : float
    ReferenceMeshContent : Content
    ReferenceOrigin : CFrame
    ShrinkFactor : float
    SourceAssetId : int
    Tags : HashSet_1[str]
    TemporaryCageMeshId : ContentId
    TemporaryReferenceId : ContentId
    UniqueId : UniqueId
    @property
    def CageMeshId(self) -> ContentId: ...
    @CageMeshId.setter
    def CageMeshId(self, value: ContentId) -> ContentId: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def ReferenceMeshId(self) -> ContentId: ...
    @ReferenceMeshId.setter
    def ReferenceMeshId(self, value: ContentId) -> ContentId: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class WrapTarget(BaseWrap):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    CageMeshContent : Content
    CageOrigin : CFrame
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    HSRAssetId : ContentId
    HSRData : SharedString
    HSRMeshIdData : SharedString
    ImportOrigin : CFrame
    Name : str
    SourceAssetId : int
    Stiffness : float
    Tags : HashSet_1[str]
    TemporaryCageMeshId : ContentId
    UniqueId : UniqueId
    @property
    def CageMeshId(self) -> ContentId: ...
    @CageMeshId.setter
    def CageMeshId(self, value: ContentId) -> ContentId: ...
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...


class XmlRobloxFile(RobloxFile):
    def __init__(self) -> None: ...
    Archivable : bool
    Attributes : RbxAttributes
    Capabilities : SecurityCapabilities
    DefinesCapabilities : bool
    HistoryId : UniqueId
    Name : str
    SourceAssetId : int
    Tags : HashSet_1[str]
    UniqueId : UniqueId
    XmlDocument : XmlDocument
    @property
    def ClassName(self) -> str: ...
    @property
    def Destroyed(self) -> bool: ...
    @Destroyed.setter
    def Destroyed(self, value: bool) -> bool: ...
    @property
    def IsService(self) -> bool: ...
    @property
    def Metadata(self) -> Dictionary_2[str, str]: ...
    @Metadata.setter
    def Metadata(self, value: Dictionary_2[str, str]) -> Dictionary_2[str, str]: ...
    @property
    def Parent(self) -> Instance: ...
    @Parent.setter
    def Parent(self, value: Instance) -> Instance: ...
    @property
    def ParentLocked(self) -> bool: ...
    @ParentLocked.setter
    def ParentLocked(self, value: bool) -> bool: ...
    @property
    def Properties(self) -> IReadOnlyDictionary_2[str, Property]: ...
    @property
    def Referent(self) -> str: ...
    @Referent.setter
    def Referent(self, value: str) -> str: ...
    def Save(self, stream: Stream) -> None: ...

