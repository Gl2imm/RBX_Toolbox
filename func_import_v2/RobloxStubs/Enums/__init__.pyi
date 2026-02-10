import typing

class AccessModifierType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Allow : AccessModifierType # 0
    Deny : AccessModifierType # 1


class AccessoryType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Unknown : AccessoryType # 0
    Hat : AccessoryType # 1
    Hair : AccessoryType # 2
    Face : AccessoryType # 3
    Neck : AccessoryType # 4
    Shoulder : AccessoryType # 5
    Front : AccessoryType # 6
    Back : AccessoryType # 7
    Waist : AccessoryType # 8
    TShirt : AccessoryType # 9
    TeeShirt : AccessoryType # 9
    Shirt : AccessoryType # 10
    Pants : AccessoryType # 11
    Jacket : AccessoryType # 12
    Sweater : AccessoryType # 13
    Shorts : AccessoryType # 14
    LeftShoe : AccessoryType # 15
    RightShoe : AccessoryType # 16
    DressSkirt : AccessoryType # 17
    Eyebrow : AccessoryType # 18
    Eyelash : AccessoryType # 19


class ActionOnAutoResumeSync(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    DontResume : ActionOnAutoResumeSync # 0
    KeepStudio : ActionOnAutoResumeSync # 1
    KeepLocal : ActionOnAutoResumeSync # 2


class ActionOnStopSync(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    AlwaysAsk : ActionOnStopSync # 0
    KeepLocalFiles : ActionOnStopSync # 1
    DeleteLocalFiles : ActionOnStopSync # 2


class ActionType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Nothing : ActionType # 0
    Pause : ActionType # 1
    Lose : ActionType # 2
    Draw : ActionType # 3
    Win : ActionType # 4


class ActuatorRelativeTo(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Attachment0 : ActuatorRelativeTo # 0
    Attachment1 : ActuatorRelativeTo # 1
    World : ActuatorRelativeTo # 2


class ActuatorType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : ActuatorType # 0
    Motor : ActuatorType # 1
    Servo : ActuatorType # 2


class AdAvailabilityResult(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    IsAvailable : AdAvailabilityResult # 1
    DeviceIneligible : AdAvailabilityResult # 2
    ExperienceIneligible : AdAvailabilityResult # 3
    InternalError : AdAvailabilityResult # 4
    NoFill : AdAvailabilityResult # 5
    PlayerIneligible : AdAvailabilityResult # 6
    PublisherIneligible : AdAvailabilityResult # 7


class AdEventType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    VideoLoaded : AdEventType # 0
    VideoRemoved : AdEventType # 1
    UserCompletedVideo : AdEventType # 2
    RewardedAdLoaded : AdEventType # 3
    RewardedAdGrant : AdEventType # 4
    RewardedAdUnloaded : AdEventType # 5


class AdFormat(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    RewardedVideo : AdFormat # 0


class AdornCullingMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Automatic : AdornCullingMode # 0
    Never : AdornCullingMode # 1


class AdShape(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    HorizontalRectangle : AdShape # 1


class AdTeleportMethod(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Undefined : AdTeleportMethod # 0
    PortalForward : AdTeleportMethod # 1
    InGameMenuBackButton : AdTeleportMethod # 2
    UIBackButton : AdTeleportMethod # 3


class AdUIEventType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    AdLabelClicked : AdUIEventType # 0
    VolumeButtonClicked : AdUIEventType # 1
    FullscreenButtonClicked : AdUIEventType # 2
    PlayButtonClicked : AdUIEventType # 3
    PauseButtonClicked : AdUIEventType # 4
    CloseButtonClicked : AdUIEventType # 5
    WhyThisAdClicked : AdUIEventType # 6
    PlayEventTriggered : AdUIEventType # 7
    PauseEventTriggered : AdUIEventType # 8


class AdUIType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : AdUIType # 0
    Image : AdUIType # 1
    Video : AdUIType # 2


class AdUnitStatus(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Inactive : AdUnitStatus # 0
    Active : AdUnitStatus # 1


class AlignType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Parallel : AlignType # 0
    Perpendicular : AlignType # 1
    PrimaryAxisParallel : AlignType # 2
    PrimaryAxisPerpendicular : AlignType # 3
    PrimaryAxisLookAt : AlignType # 4
    AllAxes : AlignType # 5


class AlphaMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Overlay : AlphaMode # 0
    Transparency : AlphaMode # 1
    TintMask : AlphaMode # 2


class AnalyticsCustomFieldKeys(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    CustomField01 : AnalyticsCustomFieldKeys # 0
    CustomField02 : AnalyticsCustomFieldKeys # 1
    CustomField03 : AnalyticsCustomFieldKeys # 2


class AnalyticsEconomyAction(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : AnalyticsEconomyAction # 0
    Acquire : AnalyticsEconomyAction # 1
    Spend : AnalyticsEconomyAction # 2


class AnalyticsEconomyFlowType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Sink : AnalyticsEconomyFlowType # 0
    Source : AnalyticsEconomyFlowType # 1


class AnalyticsEconomyTransactionType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    IAP : AnalyticsEconomyTransactionType # 0
    Shop : AnalyticsEconomyTransactionType # 1
    Gameplay : AnalyticsEconomyTransactionType # 2
    ContextualPurchase : AnalyticsEconomyTransactionType # 3
    TimedReward : AnalyticsEconomyTransactionType # 4
    Onboarding : AnalyticsEconomyTransactionType # 5


class AnalyticsLogLevel(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Trace : AnalyticsLogLevel # 0
    Debug : AnalyticsLogLevel # 1
    Information : AnalyticsLogLevel # 2
    Warning : AnalyticsLogLevel # 3
    Error : AnalyticsLogLevel # 4
    Fatal : AnalyticsLogLevel # 5


class AnalyticsProgressionStatus(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : AnalyticsProgressionStatus # 0
    Begin : AnalyticsProgressionStatus # 1
    Complete : AnalyticsProgressionStatus # 2
    Abandon : AnalyticsProgressionStatus # 3
    Fail : AnalyticsProgressionStatus # 4


class AnalyticsProgressionType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Custom : AnalyticsProgressionType # 0
    Start : AnalyticsProgressionType # 1
    Fail : AnalyticsProgressionType # 2
    Complete : AnalyticsProgressionType # 3


class AnimationClipFromVideoStatus(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Initializing : AnimationClipFromVideoStatus # 0
    Pending : AnimationClipFromVideoStatus # 1
    Processing : AnimationClipFromVideoStatus # 2
    ErrorGeneric : AnimationClipFromVideoStatus # 4
    Success : AnimationClipFromVideoStatus # 6
    ErrorVideoTooLong : AnimationClipFromVideoStatus # 7
    ErrorNoPersonDetected : AnimationClipFromVideoStatus # 8
    ErrorVideoUnstable : AnimationClipFromVideoStatus # 9
    Timeout : AnimationClipFromVideoStatus # 10
    Cancelled : AnimationClipFromVideoStatus # 11
    ErrorMultiplePeople : AnimationClipFromVideoStatus # 12
    ErrorUploadingVideo : AnimationClipFromVideoStatus # 2001


class AnimationPriority(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Idle : AnimationPriority # 0
    Movement : AnimationPriority # 1
    Action : AnimationPriority # 2
    Action2 : AnimationPriority # 3
    Action3 : AnimationPriority # 4
    Action4 : AnimationPriority # 5
    Core : AnimationPriority # 1000


class AnimatorRetargetingMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : AnimatorRetargetingMode # 0
    Disabled : AnimatorRetargetingMode # 1
    Enabled : AnimatorRetargetingMode # 2


class AnnotationEditingMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : AnnotationEditingMode # 0
    PlacingNew : AnnotationEditingMode # 1
    WritingNew : AnnotationEditingMode # 2


class AnnotationRequestStatus(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Success : AnnotationRequestStatus # 0
    Loading : AnnotationRequestStatus # 1
    ErrorInternalFailure : AnnotationRequestStatus # 2
    ErrorNotFound : AnnotationRequestStatus # 3
    ErrorModerated : AnnotationRequestStatus # 4


class AnnotationRequestType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Unknown : AnnotationRequestType # 0
    Create : AnnotationRequestType # 1
    Resolve : AnnotationRequestType # 2
    Delete : AnnotationRequestType # 3
    Edit : AnnotationRequestType # 4


class AppLifecycleManagerState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Detached : AppLifecycleManagerState # 0
    Active : AppLifecycleManagerState # 1
    Inactive : AppLifecycleManagerState # 2
    Hidden : AppLifecycleManagerState # 3


class ApplyStrokeMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Contextual : ApplyStrokeMode # 0
    Border : ApplyStrokeMode # 1


class AppShellActionType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : AppShellActionType # 0
    OpenApp : AppShellActionType # 1
    TapChatTab : AppShellActionType # 2
    TapConversationEntry : AppShellActionType # 3
    TapAvatarTab : AppShellActionType # 4
    ReadConversation : AppShellActionType # 5
    TapGamePageTab : AppShellActionType # 6
    TapHomePageTab : AppShellActionType # 7
    GamePageLoaded : AppShellActionType # 8
    HomePageLoaded : AppShellActionType # 9
    AvatarEditorPageLoaded : AppShellActionType # 10


class AppShellFeature(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : AppShellFeature # 0
    Chat : AppShellFeature # 1
    AvatarEditor : AppShellFeature # 2
    GamePage : AppShellFeature # 3
    HomePage : AppShellFeature # 4
    More : AppShellFeature # 5
    Landing : AppShellFeature # 6


class AppUpdateStatus(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Unknown : AppUpdateStatus # 0
    NotSupported : AppUpdateStatus # 1
    Failed : AppUpdateStatus # 2
    NotAvailable : AppUpdateStatus # 3
    Available : AppUpdateStatus # 4
    AvailableBoundChannel : AppUpdateStatus # 5


class AspectType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    FitWithinMaxSize : AspectType # 0
    ScaleWithParentSize : AspectType # 1


class AssetCreatorType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    User : AssetCreatorType # 0
    Group : AssetCreatorType # 1


class AssetFetchStatus(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Success : AssetFetchStatus # 0
    Failure : AssetFetchStatus # 1
    None_ : AssetFetchStatus # 2
    Loading : AssetFetchStatus # 3
    TimedOut : AssetFetchStatus # 4


class AssetType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Image : AssetType # 1
    TShirt : AssetType # 2
    TeeShirt : AssetType # 2
    Audio : AssetType # 3
    Mesh : AssetType # 4
    Lua : AssetType # 5
    Hat : AssetType # 8
    Place : AssetType # 9
    Model : AssetType # 10
    Shirt : AssetType # 11
    Pants : AssetType # 12
    Decal : AssetType # 13
    Head : AssetType # 17
    Face : AssetType # 18
    Gear : AssetType # 19
    Badge : AssetType # 21
    Animation : AssetType # 24
    Torso : AssetType # 27
    RightArm : AssetType # 28
    LeftArm : AssetType # 29
    LeftLeg : AssetType # 30
    RightLeg : AssetType # 31
    Package : AssetType # 32
    GamePass : AssetType # 34
    Plugin : AssetType # 38
    MeshPart : AssetType # 40
    HairAccessory : AssetType # 41
    FaceAccessory : AssetType # 42
    NeckAccessory : AssetType # 43
    ShoulderAccessory : AssetType # 44
    FrontAccessory : AssetType # 45
    BackAccessory : AssetType # 46
    WaistAccessory : AssetType # 47
    ClimbAnimation : AssetType # 48
    DeathAnimation : AssetType # 49
    FallAnimation : AssetType # 50
    IdleAnimation : AssetType # 51
    JumpAnimation : AssetType # 52
    RunAnimation : AssetType # 53
    SwimAnimation : AssetType # 54
    WalkAnimation : AssetType # 55
    PoseAnimation : AssetType # 56
    EarAccessory : AssetType # 57
    EyeAccessory : AssetType # 58
    EmoteAnimation : AssetType # 61
    Video : AssetType # 62
    TeeShirtAccessory : AssetType # 64
    TShirtAccessory : AssetType # 64
    ShirtAccessory : AssetType # 65
    PantsAccessory : AssetType # 66
    JacketAccessory : AssetType # 67
    SweaterAccessory : AssetType # 68
    ShortsAccessory : AssetType # 69
    LeftShoeAccessory : AssetType # 70
    RightShoeAccessory : AssetType # 71
    DressSkirtAccessory : AssetType # 72
    FontFamily : AssetType # 73
    EyebrowAccessory : AssetType # 76
    EyelashAccessory : AssetType # 77
    MoodAnimation : AssetType # 78
    DynamicHead : AssetType # 79


class AssetTypeVerification(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : AssetTypeVerification # 1
    ClientOnly : AssetTypeVerification # 2
    Always : AssetTypeVerification # 3


class AudioApiRollout(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Disabled : AudioApiRollout # 0
    Automatic : AudioApiRollout # 1
    Enabled : AudioApiRollout # 2


class AudioCaptureMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:


class AudioChannelLayout(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Mono : AudioChannelLayout # 0
    Stereo : AudioChannelLayout # 1
    Quad : AudioChannelLayout # 2
    Surround_5 : AudioChannelLayout # 3
    Surround_5_1 : AudioChannelLayout # 4
    Surround_7_1 : AudioChannelLayout # 5
    Surround_7_1_4 : AudioChannelLayout # 6


class AudioFilterType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Peak : AudioFilterType # 0
    LowShelf : AudioFilterType # 1
    HighShelf : AudioFilterType # 2
    Lowpass12dB : AudioFilterType # 3
    Lowpass24dB : AudioFilterType # 4
    Lowpass48dB : AudioFilterType # 5
    Highpass12dB : AudioFilterType # 6
    Highpass24dB : AudioFilterType # 7
    Highpass48dB : AudioFilterType # 8
    Bandpass : AudioFilterType # 9
    Notch : AudioFilterType # 10
    Lowpass6dB : AudioFilterType # 11


class AudioSimulationFidelity(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : AudioSimulationFidelity # 0
    Automatic : AudioSimulationFidelity # 1


class AudioSubType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Music : AudioSubType # 1
    SoundEffect : AudioSubType # 2


class AudioWindowSize(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Small : AudioWindowSize # 0
    Medium : AudioWindowSize # 1
    Large : AudioWindowSize # 2


class AutoIndentRule(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Off : AutoIndentRule # 0
    Absolute : AutoIndentRule # 1
    Relative : AutoIndentRule # 2


class AutomaticSize(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : AutomaticSize # 0
    X : AutomaticSize # 1
    Y : AutomaticSize # 2
    XY : AutomaticSize # 3


class AvatarAssetType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    TShirt : AvatarAssetType # 2
    Hat : AvatarAssetType # 8
    Shirt : AvatarAssetType # 11
    Pants : AvatarAssetType # 12
    Head : AvatarAssetType # 17
    Face : AvatarAssetType # 18
    Gear : AvatarAssetType # 19
    Torso : AvatarAssetType # 27
    RightArm : AvatarAssetType # 28
    LeftArm : AvatarAssetType # 29
    LeftLeg : AvatarAssetType # 30
    RightLeg : AvatarAssetType # 31
    HairAccessory : AvatarAssetType # 41
    FaceAccessory : AvatarAssetType # 42
    NeckAccessory : AvatarAssetType # 43
    ShoulderAccessory : AvatarAssetType # 44
    FrontAccessory : AvatarAssetType # 45
    BackAccessory : AvatarAssetType # 46
    WaistAccessory : AvatarAssetType # 47
    ClimbAnimation : AvatarAssetType # 48
    FallAnimation : AvatarAssetType # 50
    IdleAnimation : AvatarAssetType # 51
    JumpAnimation : AvatarAssetType # 52
    RunAnimation : AvatarAssetType # 53
    SwimAnimation : AvatarAssetType # 54
    WalkAnimation : AvatarAssetType # 55
    EmoteAnimation : AvatarAssetType # 61
    TShirtAccessory : AvatarAssetType # 64
    TeeShirtAccessory : AvatarAssetType # 64
    ShirtAccessory : AvatarAssetType # 65
    PantsAccessory : AvatarAssetType # 66
    JacketAccessory : AvatarAssetType # 67
    SweaterAccessory : AvatarAssetType # 68
    ShortsAccessory : AvatarAssetType # 69
    LeftShoeAccessory : AvatarAssetType # 70
    RightShoeAccessory : AvatarAssetType # 71
    DressSkirtAccessory : AvatarAssetType # 72
    EyebrowAccessory : AvatarAssetType # 76
    EyelashAccessory : AvatarAssetType # 77
    MoodAnimation : AvatarAssetType # 78
    DynamicHead : AvatarAssetType # 79


class AvatarChatServiceFeature(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : AvatarChatServiceFeature # 0
    UniverseAudio : AvatarChatServiceFeature # 1
    UniverseVideo : AvatarChatServiceFeature # 2
    PlaceAudio : AvatarChatServiceFeature # 4
    PlaceVideo : AvatarChatServiceFeature # 8
    UserAudioEligible : AvatarChatServiceFeature # 16
    UserAudio : AvatarChatServiceFeature # 32
    UserVideoEligible : AvatarChatServiceFeature # 64
    UserVideo : AvatarChatServiceFeature # 128
    UserBanned : AvatarChatServiceFeature # 256
    UserVerifiedForVoice : AvatarChatServiceFeature # 512


class AvatarContextMenuOption(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Friend : AvatarContextMenuOption # 0
    Chat : AvatarContextMenuOption # 1
    Emote : AvatarContextMenuOption # 2
    InspectMenu : AvatarContextMenuOption # 3


class AvatarGenerationError(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : AvatarGenerationError # 0
    Unknown : AvatarGenerationError # 1
    DownloadFailed : AvatarGenerationError # 2
    Canceled : AvatarGenerationError # 3
    Offensive : AvatarGenerationError # 4
    Timeout : AvatarGenerationError # 5
    JobNotFound : AvatarGenerationError # 6


class AvatarItemType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Asset : AvatarItemType # 1
    Bundle : AvatarItemType # 2


class AvatarPromptResult(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Success : AvatarPromptResult # 1
    PermissionDenied : AvatarPromptResult # 2
    Failed : AvatarPromptResult # 3


class AvatarSettingsAccessoryLimitMethod(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Scale : AvatarSettingsAccessoryLimitMethod # 0
    Remove : AvatarSettingsAccessoryLimitMethod # 1


class AvatarSettingsAccessoryMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    PlayerChoice : AvatarSettingsAccessoryMode # 0
    CustomLimit : AvatarSettingsAccessoryMode # 1


class AvatarSettingsAnimationClipsMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    PlayerChoice : AvatarSettingsAnimationClipsMode # 0
    CustomClips : AvatarSettingsAnimationClipsMode # 1


class AvatarSettingsAnimationPacksMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    PlayerChoice : AvatarSettingsAnimationPacksMode # 0
    StandardR15 : AvatarSettingsAnimationPacksMode # 1
    StandardR6 : AvatarSettingsAnimationPacksMode # 2


class AvatarSettingsAppearanceMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    PlayerChoice : AvatarSettingsAppearanceMode # 0
    CustomParts : AvatarSettingsAppearanceMode # 1
    CustomBody : AvatarSettingsAppearanceMode # 2


class AvatarSettingsBuildMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    PlayerChoice : AvatarSettingsBuildMode # 0
    CustomBuild : AvatarSettingsBuildMode # 1


class AvatarSettingsClothingMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    PlayerChoice : AvatarSettingsClothingMode # 0
    CustomLimit : AvatarSettingsClothingMode # 1


class AvatarSettingsCollisionMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : AvatarSettingsCollisionMode # 0
    SingleCollider : AvatarSettingsCollisionMode # 1
    Legacy : AvatarSettingsCollisionMode # 2


class AvatarSettingsCustomAccessoryMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    PlayerChoice : AvatarSettingsCustomAccessoryMode # 0
    CustomAccessories : AvatarSettingsCustomAccessoryMode # 1


class AvatarSettingsCustomBodyType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    AvatarReference : AvatarSettingsCustomBodyType # 0
    BundleId : AvatarSettingsCustomBodyType # 1


class AvatarSettingsCustomClothingMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    PlayerChoice : AvatarSettingsCustomClothingMode # 0
    CustomClothing : AvatarSettingsCustomClothingMode # 1


class AvatarSettingsHitAndTouchDetectionMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    UseParts : AvatarSettingsHitAndTouchDetectionMode # 0
    UseCollider : AvatarSettingsHitAndTouchDetectionMode # 1


class AvatarSettingsJumpMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    JumpHeight : AvatarSettingsJumpMode # 0
    JumpPower : AvatarSettingsJumpMode # 1


class AvatarSettingsLegacyCollisionMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    R6Colliders : AvatarSettingsLegacyCollisionMode # 0
    InnerBoxColliders : AvatarSettingsLegacyCollisionMode # 1


class AvatarSettingsScaleMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    PlayerChoice : AvatarSettingsScaleMode # 0
    CustomScale : AvatarSettingsScaleMode # 1


class AvatarThumbnailCustomizationType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Closeup : AvatarThumbnailCustomizationType # 1
    FullBody : AvatarThumbnailCustomizationType # 2


class AvatarUnificationMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : AvatarUnificationMode # 0
    Disabled : AvatarUnificationMode # 1
    Enabled : AvatarUnificationMode # 2


class Axis(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    X : Axis # 0
    Right : Axis # 0
    Left : Axis # 0
    Bottom : Axis # 1
    Top : Axis # 1
    Y : Axis # 1
    Z : Axis # 2
    Back : Axis # 2
    Front : Axis # 2


class BenefitType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    DeveloperProduct : BenefitType # 0
    AvatarAsset : BenefitType # 1
    AvatarBundle : BenefitType # 2


class BinType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    _Slingshot : BinType # 0
    _Rocket : BinType # 0
    Script : BinType # 0
    _Laser : BinType # 0
    GameTool : BinType # 1
    Grab : BinType # 2
    Clone : BinType # 3
    Hammer : BinType # 4


class BodyPart(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Head : BodyPart # 0
    Torso : BodyPart # 1
    LeftArm : BodyPart # 2
    RightArm : BodyPart # 3
    LeftLeg : BodyPart # 4
    RightLeg : BodyPart # 5


class BodyPartR15(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Head : BodyPartR15 # 0
    UpperTorso : BodyPartR15 # 1
    LowerTorso : BodyPartR15 # 2
    LeftFoot : BodyPartR15 # 3
    LeftLowerLeg : BodyPartR15 # 4
    LeftUpperLeg : BodyPartR15 # 5
    RightFoot : BodyPartR15 # 6
    RightLowerLeg : BodyPartR15 # 7
    RightUpperLeg : BodyPartR15 # 8
    LeftHand : BodyPartR15 # 9
    LeftLowerArm : BodyPartR15 # 10
    LeftUpperArm : BodyPartR15 # 11
    RightHand : BodyPartR15 # 12
    RightLowerArm : BodyPartR15 # 13
    RightUpperArm : BodyPartR15 # 14
    RootPart : BodyPartR15 # 15
    Unknown : BodyPartR15 # 17


class BorderMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Outline : BorderMode # 0
    Middle : BorderMode # 1
    Inset : BorderMode # 2


class BreakpointRemoveReason(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Requested : BreakpointRemoveReason # 0
    ScriptChanged : BreakpointRemoveReason # 1
    ScriptRemoved : BreakpointRemoveReason # 2


class BreakReason(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Other : BreakReason # 0
    Error : BreakReason # 1
    SpecialBreakpoint : BreakReason # 2
    UserBreakpoint : BreakReason # 3


class BulkMoveMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    FireAllEvents : BulkMoveMode # 0
    FireCFrameChanged : BulkMoveMode # 1


class BundleType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    BodyParts : BundleType # 1
    Animations : BundleType # 2
    Shoes : BundleType # 3
    DynamicHead : BundleType # 4
    DynamicHeadAvatar : BundleType # 5


class Button(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Dismount : Button # 8
    Jump : Button # 32


class ButtonStyle(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Custom : ButtonStyle # 0
    RobloxButtonDefault : ButtonStyle # 1
    RobloxButton : ButtonStyle # 2
    RobloxRoundButton : ButtonStyle # 3
    RobloxRoundDefaultButton : ButtonStyle # 4
    RobloxRoundDropdownButton : ButtonStyle # 5


class CageType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Inner : CageType # 0
    Outer : CageType # 1


class CameraMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Classic : CameraMode # 0
    LockFirstPerson : CameraMode # 1


class CameraPanMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Classic : CameraPanMode # 0
    EdgeBump : CameraPanMode # 1


class CameraSpeedAdjustBinding(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : CameraSpeedAdjustBinding # 0
    RmbScroll : CameraSpeedAdjustBinding # 1
    AltScroll : CameraSpeedAdjustBinding # 2


class CameraType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Fixed : CameraType # 0
    Attach : CameraType # 1
    Watch : CameraType # 2
    Track : CameraType # 3
    Follow : CameraType # 4
    Custom : CameraType # 5
    Scriptable : CameraType # 6
    Orbital : CameraType # 7


class CaptureType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Screenshot : CaptureType # 0
    Video : CaptureType # 1


class CatalogCategoryFilter(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : CatalogCategoryFilter # 1
    Featured : CatalogCategoryFilter # 2
    Collectibles : CatalogCategoryFilter # 3
    CommunityCreations : CatalogCategoryFilter # 4
    Premium : CatalogCategoryFilter # 5
    Recommended : CatalogCategoryFilter # 6


class CatalogSortAggregation(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Past12Hours : CatalogSortAggregation # 1
    PastDay : CatalogSortAggregation # 2
    Past3Days : CatalogSortAggregation # 3
    PastWeek : CatalogSortAggregation # 4
    PastMonth : CatalogSortAggregation # 5
    AllTime : CatalogSortAggregation # 6


class CatalogSortType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Relevance : CatalogSortType # 1
    PriceHighToLow : CatalogSortType # 2
    PriceLowToHigh : CatalogSortType # 3
    MostFavorited : CatalogSortType # 5
    RecentlyUpdated : CatalogSortType # 6
    RecentlyCreated : CatalogSortType # 6
    Bestselling : CatalogSortType # 7


class CellBlock(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Solid : CellBlock # 0
    VerticalWedge : CellBlock # 1
    CornerWedge : CellBlock # 2
    InverseCornerWedge : CellBlock # 3
    HorizontalWedge : CellBlock # 4


class CellMaterial(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Empty : CellMaterial # 0
    Grass : CellMaterial # 1
    Sand : CellMaterial # 2
    Brick : CellMaterial # 3
    Granite : CellMaterial # 4
    Asphalt : CellMaterial # 5
    Iron : CellMaterial # 6
    Aluminum : CellMaterial # 7
    Gold : CellMaterial # 8
    WoodPlank : CellMaterial # 9
    WoodLog : CellMaterial # 10
    Gravel : CellMaterial # 11
    CinderBlock : CellMaterial # 12
    MossyStone : CellMaterial # 13
    Cement : CellMaterial # 14
    RedPlastic : CellMaterial # 15
    BluePlastic : CellMaterial # 16
    Water : CellMaterial # 17


class CellOrientation(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    NegZ : CellOrientation # 0
    X : CellOrientation # 1
    Z : CellOrientation # 2
    NegX : CellOrientation # 3


class CenterDialogType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    UnsolicitedDialog : CenterDialogType # 1
    PlayerInitiatedDialog : CenterDialogType # 2
    ModalDialog : CenterDialogType # 3
    QuitDialog : CenterDialogType # 4


class CharacterControlMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : CharacterControlMode # 0
    Legacy : CharacterControlMode # 1
    NoCharacterController : CharacterControlMode # 2
    LuaCharacterController : CharacterControlMode # 3


class ChatCallbackType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    OnCreatingChatWindow : ChatCallbackType # 1
    OnClientSendingMessage : ChatCallbackType # 2
    OnClientFormattingMessage : ChatCallbackType # 3
    OnServerReceivingMessage : ChatCallbackType # 17


class ChatColor(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Blue : ChatColor # 0
    Green : ChatColor # 1
    Red : ChatColor # 2
    White : ChatColor # 3


class ChatMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Menu : ChatMode # 0
    TextAndMenu : ChatMode # 1


class ChatPrivacyMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    AllUsers : ChatPrivacyMode # 0
    NoOne : ChatPrivacyMode # 1
    Friends : ChatPrivacyMode # 2


class ChatRestrictionStatus(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Unknown : ChatRestrictionStatus # 0
    NotRestricted : ChatRestrictionStatus # 1
    Restricted : ChatRestrictionStatus # 2


class ChatStyle(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Classic : ChatStyle # 0
    Bubble : ChatStyle # 1
    ClassicAndBubble : ChatStyle # 2


class ChatVersion(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    LegacyChatService : ChatVersion # 0
    TextChatService : ChatVersion # 1


class ClientAnimatorThrottlingMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : ClientAnimatorThrottlingMode # 0
    Disabled : ClientAnimatorThrottlingMode # 1
    Enabled : ClientAnimatorThrottlingMode # 2


class CloseReason(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Unknown : CloseReason # 0
    RobloxMaintenance : CloseReason # 1
    DeveloperShutdown : CloseReason # 2
    DeveloperUpdate : CloseReason # 3
    ServerEmpty : CloseReason # 4
    OutOfMemory : CloseReason # 5


class CollaboratorStatus(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : CollaboratorStatus # 0
    Editing3D : CollaboratorStatus # 1
    Scripting : CollaboratorStatus # 2
    PrivateScripting : CollaboratorStatus # 3


class CollisionFidelity(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : CollisionFidelity # 0
    Hull : CollisionFidelity # 1
    Box : CollisionFidelity # 2
    PreciseConvexDecomposition : CollisionFidelity # 3


class CommandPermission(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Plugin : CommandPermission # 0
    LocalUser : CommandPermission # 1


class CompileTarget(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Client : CompileTarget # 0
    CoreScript : CompileTarget # 1
    Studio : CompileTarget # 2
    CoreScriptRaw : CompileTarget # 3


class CompletionAcceptanceBehavior(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Insert : CompletionAcceptanceBehavior # 0
    Replace : CompletionAcceptanceBehavior # 1
    ReplaceOnEnterInsertOnTab : CompletionAcceptanceBehavior # 2
    InsertOnEnterReplaceOnTab : CompletionAcceptanceBehavior # 3


class CompletionItemKind(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Text : CompletionItemKind # 1
    Method : CompletionItemKind # 2
    Function : CompletionItemKind # 3
    Constructor : CompletionItemKind # 4
    Field : CompletionItemKind # 5
    Variable : CompletionItemKind # 6
    Class : CompletionItemKind # 7
    Interface : CompletionItemKind # 8
    Module : CompletionItemKind # 9
    Property : CompletionItemKind # 10
    Unit : CompletionItemKind # 11
    Value : CompletionItemKind # 12
    Enum : CompletionItemKind # 13
    Keyword : CompletionItemKind # 14
    Snippet : CompletionItemKind # 15
    Color : CompletionItemKind # 16
    File : CompletionItemKind # 17
    Reference : CompletionItemKind # 18
    Folder : CompletionItemKind # 19
    EnumMember : CompletionItemKind # 20
    Constant : CompletionItemKind # 21
    Struct : CompletionItemKind # 22
    Event : CompletionItemKind # 23
    Operator : CompletionItemKind # 24
    TypeParameter : CompletionItemKind # 25


class CompletionItemTag(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Deprecated : CompletionItemTag # 1
    IncorrectIndexType : CompletionItemTag # 2
    PluginPermissions : CompletionItemTag # 3
    CommandLinePermissions : CompletionItemTag # 4
    RobloxPermissions : CompletionItemTag # 5
    AddParens : CompletionItemTag # 6
    PutCursorInParens : CompletionItemTag # 7
    TypeCorrect : CompletionItemTag # 8
    ClientServerBoundaryViolation : CompletionItemTag # 9
    Invalidated : CompletionItemTag # 10
    PutCursorBeforeEnd : CompletionItemTag # 11


class CompletionTriggerKind(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Invoked : CompletionTriggerKind # 1
    TriggerCharacter : CompletionTriggerKind # 2
    TriggerForIncompleteCompletions : CompletionTriggerKind # 3


class ComputerCameraMovementMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : ComputerCameraMovementMode # 0
    Classic : ComputerCameraMovementMode # 1
    Follow : ComputerCameraMovementMode # 2
    Orbital : ComputerCameraMovementMode # 3
    CameraToggle : ComputerCameraMovementMode # 4


class ComputerMovementMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : ComputerMovementMode # 0
    KeyboardMouse : ComputerMovementMode # 1
    ClickToMove : ComputerMovementMode # 2


class ConfigSnapshotErrorState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : ConfigSnapshotErrorState # 0
    LoadFailed : ConfigSnapshotErrorState # 1


class ConnectionError(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    OK : ConnectionError # 0
    Unknown : ConnectionError # 1
    DisconnectErrors : ConnectionError # 256
    DisconnectBadhash : ConnectionError # 257
    DisconnectSecurityKeyMismatch : ConnectionError # 258
    DisconnectProtocolMismatch : ConnectionError # 259
    DisconnectReceivePacketError : ConnectionError # 260
    DisconnectReceivePacketStreamError : ConnectionError # 261
    DisconnectSendPacketError : ConnectionError # 262
    DisconnectIllegalTeleport : ConnectionError # 263
    DisconnectDuplicatePlayer : ConnectionError # 264
    DisconnectDuplicateTicket : ConnectionError # 265
    DisconnectTimeout : ConnectionError # 266
    DisconnectLuaKick : ConnectionError # 267
    DisconnectOnRemoteSysStats : ConnectionError # 268
    DisconnectHashTimeout : ConnectionError # 269
    DisconnectCloudEditKick : ConnectionError # 270
    DisconnectPlayerless : ConnectionError # 271
    DisconnectNewSecurityKeyMismatch : ConnectionError # 272
    DisconnectEvicted : ConnectionError # 273
    DisconnectDevMaintenance : ConnectionError # 274
    DisconnectRobloxMaintenance : ConnectionError # 275
    DisconnectRejoin : ConnectionError # 276
    DisconnectConnectionLost : ConnectionError # 277
    DisconnectIdle : ConnectionError # 278
    DisconnectRaknetErrors : ConnectionError # 279
    DisconnectWrongVersion : ConnectionError # 280
    DisconnectBySecurityPolicy : ConnectionError # 281
    DisconnectBlockedIP : ConnectionError # 282
    DisconnectClientFailure : ConnectionError # 284
    DisconnectClientRequest : ConnectionError # 285
    DisconnectPrivateServerKickout : ConnectionError # 286
    DisconnectModeratedGame : ConnectionError # 287
    ServerShutdown : ConnectionError # 288
    ReplicatorTimeout : ConnectionError # 290
    PlayerRemoved : ConnectionError # 291
    DisconnectOutOfMemoryKeepPlayingLeave : ConnectionError # 292
    DisconnectRomarkEndOfTest : ConnectionError # 293
    DisconnectCollaboratorPermissionRevoked : ConnectionError # 294
    DisconnectCollaboratorUnderage : ConnectionError # 295
    NetworkInternal : ConnectionError # 296
    NetworkSend : ConnectionError # 297
    NetworkTimeout : ConnectionError # 298
    NetworkMisbehavior : ConnectionError # 299
    NetworkSecurity : ConnectionError # 300
    ReplacementReady : ConnectionError # 301
    ServerEmpty : ConnectionError # 302
    PhantomFreeze : ConnectionError # 303
    AndroidAnticheatKick : ConnectionError # 304
    AndroidEmulatorKick : ConnectionError # 305
    PlacelaunchErrors : ConnectionError # 512
    PlacelaunchDisabled : ConnectionError # 515
    PlacelaunchError : ConnectionError # 516
    PlacelaunchGameEnded : ConnectionError # 517
    PlacelaunchGameFull : ConnectionError # 518
    PlacelaunchUserLeft : ConnectionError # 522
    PlacelaunchRestricted : ConnectionError # 523
    PlacelaunchUnauthorized : ConnectionError # 524
    PlacelaunchFlooded : ConnectionError # 525
    PlacelaunchHashExpired : ConnectionError # 526
    PlacelaunchHashException : ConnectionError # 527
    PlacelaunchPartyCannotFit : ConnectionError # 528
    PlacelaunchHttpError : ConnectionError # 529
    PlacelaunchUserPrivacyUnauthorized : ConnectionError # 533
    PlacelaunchCreatorBan : ConnectionError # 600
    PlacelaunchCustomMessage : ConnectionError # 610
    PlacelaunchOtherError : ConnectionError # 611
    TeleportErrors : ConnectionError # 768
    TeleportFailure : ConnectionError # 769
    TeleportGameNotFound : ConnectionError # 770
    TeleportGameEnded : ConnectionError # 771
    TeleportGameFull : ConnectionError # 772
    TeleportUnauthorized : ConnectionError # 773
    TeleportFlooded : ConnectionError # 774
    TeleportIsTeleporting : ConnectionError # 775


class ConnectionState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Connected : ConnectionState # 0
    Disconnected : ConnectionState # 1


class ContentSourceType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : ContentSourceType # 0
    Uri : ContentSourceType # 1
    Object : ContentSourceType # 2


class ContextActionPriority(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Low : ContextActionPriority # 1000
    Medium : ContextActionPriority # 2000
    Default : ContextActionPriority # 2000
    High : ContextActionPriority # 3000


class ContextActionResult(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Sink : ContextActionResult # 0
    Pass : ContextActionResult # 1


class ControlMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Classic : ControlMode # 0
    MouseLockSwitch : ControlMode # 1
    Mouse_Lock_Switch : ControlMode # 1


class CoreGuiType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    PlayerList : CoreGuiType # 0
    Health : CoreGuiType # 1
    Backpack : CoreGuiType # 2
    Chat : CoreGuiType # 3
    All : CoreGuiType # 4
    EmotesMenu : CoreGuiType # 5
    SelfView : CoreGuiType # 6
    Captures : CoreGuiType # 7


class CreateAssetResult(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Success : CreateAssetResult # 1
    PermissionDenied : CreateAssetResult # 2
    UploadFailed : CreateAssetResult # 3
    Unknown : CreateAssetResult # 4


class CreateOutfitFailure(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    InvalidName : CreateOutfitFailure # 1
    OutfitLimitReached : CreateOutfitFailure # 2
    Other : CreateOutfitFailure # 3


class CreatorType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    User : CreatorType # 0
    Group : CreatorType # 1


class CreatorTypeFilter(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    User : CreatorTypeFilter # 0
    Group : CreatorTypeFilter # 1
    All : CreatorTypeFilter # 2


class CurrencyType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : CurrencyType # 0
    Robux : CurrencyType # 1
    Tix : CurrencyType # 2


class CustomCameraMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : CustomCameraMode # 0
    Classic : CustomCameraMode # 1
    Follow : CustomCameraMode # 2


class DataStoreRequestType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    GetAsync : DataStoreRequestType # 0
    SetIncrementAsync : DataStoreRequestType # 1
    UpdateAsync : DataStoreRequestType # 2
    GetSortedAsync : DataStoreRequestType # 3
    SetIncrementSortedAsync : DataStoreRequestType # 4
    OnUpdate : DataStoreRequestType # 5
    ListAsync : DataStoreRequestType # 6
    GetVersionAsync : DataStoreRequestType # 7
    RemoveVersionAsync : DataStoreRequestType # 8


class DebuggerEndReason(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    ClientRequest : DebuggerEndReason # 0
    Timeout : DebuggerEndReason # 1
    InvalidHost : DebuggerEndReason # 2
    Disconnected : DebuggerEndReason # 3
    ServerShutdown : DebuggerEndReason # 4
    ServerProtocolMismatch : DebuggerEndReason # 5
    ConfigurationFailed : DebuggerEndReason # 6
    RpcError : DebuggerEndReason # 7


class DebuggerExceptionBreakMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Never : DebuggerExceptionBreakMode # 0
    Always : DebuggerExceptionBreakMode # 1
    Unhandled : DebuggerExceptionBreakMode # 2


class DebuggerFrameType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    C : DebuggerFrameType # 0
    Lua : DebuggerFrameType # 1


class DebuggerPauseReason(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Unknown : DebuggerPauseReason # 0
    Requested : DebuggerPauseReason # 1
    Breakpoint : DebuggerPauseReason # 2
    Exception : DebuggerPauseReason # 3
    SingleStep : DebuggerPauseReason # 4
    Entrypoint : DebuggerPauseReason # 5


class DebuggerStatus(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Success : DebuggerStatus # 0
    Timeout : DebuggerStatus # 1
    ConnectionLost : DebuggerStatus # 2
    InvalidResponse : DebuggerStatus # 3
    InternalError : DebuggerStatus # 4
    InvalidState : DebuggerStatus # 5
    RpcError : DebuggerStatus # 6
    InvalidArgument : DebuggerStatus # 7
    ConnectionClosed : DebuggerStatus # 8


class DevCameraOcclusionMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Zoom : DevCameraOcclusionMode # 0
    Invisicam : DevCameraOcclusionMode # 1


class DevComputerCameraMovementMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    UserChoice : DevComputerCameraMovementMode # 0
    Classic : DevComputerCameraMovementMode # 1
    Follow : DevComputerCameraMovementMode # 2
    Orbital : DevComputerCameraMovementMode # 3
    CameraToggle : DevComputerCameraMovementMode # 4


class DevComputerMovementMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    UserChoice : DevComputerMovementMode # 0
    KeyboardMouse : DevComputerMovementMode # 1
    ClickToMove : DevComputerMovementMode # 2
    Scriptable : DevComputerMovementMode # 3


class DeveloperMemoryTag(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Internal : DeveloperMemoryTag # 0
    HttpCache : DeveloperMemoryTag # 1
    Instances : DeveloperMemoryTag # 2
    Signals : DeveloperMemoryTag # 3
    LuaHeap : DeveloperMemoryTag # 4
    Script : DeveloperMemoryTag # 5
    PhysicsCollision : DeveloperMemoryTag # 6
    PhysicsParts : DeveloperMemoryTag # 7
    GraphicsSolidModels : DeveloperMemoryTag # 8
    GraphicsMeshParts : DeveloperMemoryTag # 10
    GraphicsParticles : DeveloperMemoryTag # 11
    GraphicsParts : DeveloperMemoryTag # 12
    GraphicsSpatialHash : DeveloperMemoryTag # 13
    GraphicsTerrain : DeveloperMemoryTag # 14
    GraphicsTexture : DeveloperMemoryTag # 15
    GraphicsTextureCharacter : DeveloperMemoryTag # 16
    Sounds : DeveloperMemoryTag # 17
    StreamingSounds : DeveloperMemoryTag # 18
    TerrainVoxels : DeveloperMemoryTag # 19
    Gui : DeveloperMemoryTag # 21
    Animation : DeveloperMemoryTag # 22
    Navigation : DeveloperMemoryTag # 23
    GeometryCSG : DeveloperMemoryTag # 24
    GraphicsSlimModels : DeveloperMemoryTag # 25


class DeviceFeatureType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    DeviceCapture : DeviceFeatureType # 0


class DeviceForm(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Console : DeviceForm # 0
    Phone : DeviceForm # 1
    Tablet : DeviceForm # 2
    Desktop : DeviceForm # 3
    VR : DeviceForm # 4


class DeviceLevel(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Low : DeviceLevel # 0
    Medium : DeviceLevel # 1
    High : DeviceLevel # 2


class DeviceType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Unknown : DeviceType # 0
    Desktop : DeviceType # 1
    Tablet : DeviceType # 2
    Phone : DeviceType # 3


class DevTouchCameraMovementMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    UserChoice : DevTouchCameraMovementMode # 0
    Classic : DevTouchCameraMovementMode # 1
    Follow : DevTouchCameraMovementMode # 2
    Orbital : DevTouchCameraMovementMode # 3


class DevTouchMovementMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    UserChoice : DevTouchMovementMode # 0
    Thumbstick : DevTouchMovementMode # 1
    DPad : DevTouchMovementMode # 2
    Thumbpad : DevTouchMovementMode # 3
    ClickToMove : DevTouchMovementMode # 4
    Scriptable : DevTouchMovementMode # 5
    DynamicThumbstick : DevTouchMovementMode # 6


class DialogBehaviorType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    SinglePlayer : DialogBehaviorType # 0
    MultiplePlayers : DialogBehaviorType # 1


class DialogPurpose(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Quest : DialogPurpose # 0
    Help : DialogPurpose # 1
    Shop : DialogPurpose # 2


class DialogTone(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Neutral : DialogTone # 0
    Friendly : DialogTone # 1
    Enemy : DialogTone # 2


class DominantAxis(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Width : DominantAxis # 0
    Height : DominantAxis # 1


class DraftStatusCode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    OK : DraftStatusCode # 0
    DraftOutdated : DraftStatusCode # 1
    ScriptRemoved : DraftStatusCode # 2
    DraftCommitted : DraftStatusCode # 3


class DragDetectorDragStyle(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    TranslateLine : DragDetectorDragStyle # 0
    TranslatePlane : DragDetectorDragStyle # 1
    TranslatePlaneOrLine : DragDetectorDragStyle # 2
    TranslateLineOrPlane : DragDetectorDragStyle # 3
    TranslateViewPlane : DragDetectorDragStyle # 4
    RotateAxis : DragDetectorDragStyle # 5
    RotateTrackball : DragDetectorDragStyle # 6
    Scriptable : DragDetectorDragStyle # 7
    BestForDevice : DragDetectorDragStyle # 8


class DragDetectorPermissionPolicy(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Nobody : DragDetectorPermissionPolicy # 0
    Everybody : DragDetectorPermissionPolicy # 1
    Scriptable : DragDetectorPermissionPolicy # 2


class DragDetectorResponseStyle(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Geometric : DragDetectorResponseStyle # 0
    Physical : DragDetectorResponseStyle # 1
    Custom : DragDetectorResponseStyle # 2


class DraggerCoordinateSpace(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Object : DraggerCoordinateSpace # 0
    World : DraggerCoordinateSpace # 1


class DraggerMovementMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Geometric : DraggerMovementMode # 0
    Physical : DraggerMovementMode # 1


class DraggingScrollBar(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : DraggingScrollBar # 0
    Horizontal : DraggingScrollBar # 1
    Vertical : DraggingScrollBar # 2


class EasingDirection(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    In : EasingDirection # 0
    Out : EasingDirection # 1
    InOut : EasingDirection # 2


class EasingStyle(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Linear : EasingStyle # 0
    Sine : EasingStyle # 1
    Back : EasingStyle # 2
    Quad : EasingStyle # 3
    Quart : EasingStyle # 4
    Quint : EasingStyle # 5
    Bounce : EasingStyle # 6
    Elastic : EasingStyle # 7
    Exponential : EasingStyle # 8
    Circular : EasingStyle # 9
    Cubic : EasingStyle # 10


class EditableStatus(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Unknown : EditableStatus # 0
    Allowed : EditableStatus # 1
    Disallowed : EditableStatus # 2


class ElasticBehavior(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    WhenScrollable : ElasticBehavior # 0
    Always : ElasticBehavior # 1
    Never : ElasticBehavior # 2


class EnviromentalPhysicsThrottle(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    DefaultAuto : EnviromentalPhysicsThrottle # 0
    Disabled : EnviromentalPhysicsThrottle # 1
    Always : EnviromentalPhysicsThrottle # 2
    Skip2 : EnviromentalPhysicsThrottle # 3
    Skip4 : EnviromentalPhysicsThrottle # 4
    Skip8 : EnviromentalPhysicsThrottle # 5
    Skip16 : EnviromentalPhysicsThrottle # 6


class ExperienceAuthScope(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    DefaultScope : ExperienceAuthScope # 0
    CreatorAssetsCreate : ExperienceAuthScope # 1


class ExplosionType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    NoCraters : ExplosionType # 0
    Craters : ExplosionType # 1
    CratersAndDebris : ExplosionType # 1


class FacialAgeEstimationResultType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Complete : FacialAgeEstimationResultType # 0
    Cancel : FacialAgeEstimationResultType # 1
    Error : FacialAgeEstimationResultType # 2


class FacialAnimationStreamingState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : FacialAnimationStreamingState # 0
    Audio : FacialAnimationStreamingState # 1
    Video : FacialAnimationStreamingState # 2
    Place : FacialAnimationStreamingState # 4
    Server : FacialAnimationStreamingState # 8


class FacsActionUnit(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    ChinRaiserUpperLip : FacsActionUnit # 0
    ChinRaiser : FacsActionUnit # 1
    FlatPucker : FacsActionUnit # 2
    Funneler : FacsActionUnit # 3
    LowerLipSuck : FacsActionUnit # 4
    LipPresser : FacsActionUnit # 5
    LipsTogether : FacsActionUnit # 6
    MouthLeft : FacsActionUnit # 7
    MouthRight : FacsActionUnit # 8
    Pucker : FacsActionUnit # 9
    UpperLipSuck : FacsActionUnit # 10
    LeftCheekPuff : FacsActionUnit # 11
    LeftDimpler : FacsActionUnit # 12
    LeftLipCornerDown : FacsActionUnit # 13
    LeftLowerLipDepressor : FacsActionUnit # 14
    LeftLipCornerPuller : FacsActionUnit # 15
    LeftLipStretcher : FacsActionUnit # 16
    LeftUpperLipRaiser : FacsActionUnit # 17
    RightCheekPuff : FacsActionUnit # 18
    RightDimpler : FacsActionUnit # 19
    RightLipCornerDown : FacsActionUnit # 20
    RightLowerLipDepressor : FacsActionUnit # 21
    RightLipCornerPuller : FacsActionUnit # 22
    RightLipStretcher : FacsActionUnit # 23
    RightUpperLipRaiser : FacsActionUnit # 24
    JawDrop : FacsActionUnit # 25
    JawLeft : FacsActionUnit # 26
    JawRight : FacsActionUnit # 27
    Corrugator : FacsActionUnit # 28
    LeftBrowLowerer : FacsActionUnit # 29
    LeftOuterBrowRaiser : FacsActionUnit # 30
    LeftNoseWrinkler : FacsActionUnit # 31
    LeftInnerBrowRaiser : FacsActionUnit # 32
    RightBrowLowerer : FacsActionUnit # 33
    RightOuterBrowRaiser : FacsActionUnit # 34
    RightInnerBrowRaiser : FacsActionUnit # 35
    RightNoseWrinkler : FacsActionUnit # 36
    EyesLookDown : FacsActionUnit # 37
    EyesLookLeft : FacsActionUnit # 38
    EyesLookUp : FacsActionUnit # 39
    EyesLookRight : FacsActionUnit # 40
    LeftCheekRaiser : FacsActionUnit # 41
    LeftEyeUpperLidRaiser : FacsActionUnit # 42
    LeftEyeClosed : FacsActionUnit # 43
    RightCheekRaiser : FacsActionUnit # 44
    RightEyeUpperLidRaiser : FacsActionUnit # 45
    RightEyeClosed : FacsActionUnit # 46
    TongueDown : FacsActionUnit # 47
    TongueOut : FacsActionUnit # 48
    TongueUp : FacsActionUnit # 49


class FACSDataLod(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    LOD0 : FACSDataLod # 0
    LOD1 : FACSDataLod # 1
    LODCount : FACSDataLod # 2


class FeedRankingScoreType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Content : FeedRankingScoreType # 0
    Final : FeedRankingScoreType # 1
    GameJoin : FeedRankingScoreType # 2
    Interaction : FeedRankingScoreType # 3
    Sharing : FeedRankingScoreType # 4


class FieldOfViewMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Vertical : FieldOfViewMode # 0
    Diagonal : FieldOfViewMode # 1
    MaxAxis : FieldOfViewMode # 2


class FillDirection(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Horizontal : FillDirection # 0
    Vertical : FillDirection # 1


class FilterErrorType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    BackslashNotEscapingAnything : FilterErrorType # 0
    BadBespokeFilter : FilterErrorType # 1
    BadName : FilterErrorType # 2
    IncompleteOr : FilterErrorType # 3
    IncompleteParenthesis : FilterErrorType # 4
    InvalidDoubleStar : FilterErrorType # 5
    InvalidTilde : FilterErrorType # 6
    PropertyBadOperator : FilterErrorType # 7
    PropertyDoesNotExist : FilterErrorType # 8
    PropertyInvalidField : FilterErrorType # 9
    PropertyInvalidValue : FilterErrorType # 10
    PropertyUnsupportedFields : FilterErrorType # 11
    PropertyUnsupportedProperty : FilterErrorType # 12
    UnexpectedNameIndex : FilterErrorType # 13
    UnexpectedToken : FilterErrorType # 14
    UnfinishedBinaryOperator : FilterErrorType # 15
    UnfinishedQuote : FilterErrorType # 16
    UnknownBespokeFilter : FilterErrorType # 17
    WildcardInProperty : FilterErrorType # 18


class FilterResult(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Accepted : FilterResult # 0
    Rejected : FilterResult # 1


class FinishRecordingOperation(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Cancel : FinishRecordingOperation # 0
    Commit : FinishRecordingOperation # 1
    Append : FinishRecordingOperation # 2


class FluidFidelity(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Automatic : FluidFidelity # 0
    UseCollisionGeometry : FluidFidelity # 1
    UsePreciseGeometry : FluidFidelity # 2


class FluidForces(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : FluidForces # 0
    Experimental : FluidForces # 1


class Font(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Legacy : Font # 0
    Arial : Font # 1
    ArialBold : Font # 2
    SourceSans : Font # 3
    SourceSansBold : Font # 4
    SourceSansLight : Font # 5
    SourceSansItalic : Font # 6
    Bodoni : Font # 7
    Garamond : Font # 8
    Cartoon : Font # 9
    Code : Font # 10
    Highway : Font # 11
    SciFi : Font # 12
    Arcade : Font # 13
    Fantasy : Font # 14
    Antique : Font # 15
    SourceSansSemibold : Font # 16
    Montserrat : Font # 17
    Gotham : Font # 17
    GothamSemibold : Font # 18
    MontserratMedium : Font # 18
    GothamMedium : Font # 18
    MontserratBold : Font # 19
    GothamBold : Font # 19
    MontserratBlack : Font # 20
    GothamBlack : Font # 20
    AmaticSC : Font # 21
    Bangers : Font # 22
    Creepster : Font # 23
    DenkOne : Font # 24
    Fondamento : Font # 25
    FredokaOne : Font # 26
    GrenzeGotisch : Font # 27
    IndieFlower : Font # 28
    JosefinSans : Font # 29
    Jura : Font # 30
    Kalam : Font # 31
    LuckiestGuy : Font # 32
    Merriweather : Font # 33
    Michroma : Font # 34
    Nunito : Font # 35
    Oswald : Font # 36
    PatrickHand : Font # 37
    PermanentMarker : Font # 38
    Roboto : Font # 39
    RobotoCondensed : Font # 40
    RobotoMono : Font # 41
    Sarpanch : Font # 42
    SpecialElite : Font # 43
    TitilliumWeb : Font # 44
    Ubuntu : Font # 45
    BuilderSans : Font # 46
    BuilderSansMedium : Font # 47
    BuilderSansBold : Font # 48
    BuilderSansExtraBold : Font # 49
    Arimo : Font # 50
    ArimoBold : Font # 51
    Unknown : Font # 100


class FontSize(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Size8 : FontSize # 0
    Size9 : FontSize # 1
    Size10 : FontSize # 2
    Size11 : FontSize # 3
    Size12 : FontSize # 4
    Size14 : FontSize # 5
    Size18 : FontSize # 6
    Size24 : FontSize # 7
    Size36 : FontSize # 8
    Size48 : FontSize # 9
    Size28 : FontSize # 10
    Size32 : FontSize # 11
    Size42 : FontSize # 12
    Size60 : FontSize # 13
    Size96 : FontSize # 14


class FontStyle(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Normal : FontStyle # 0
    Italic : FontStyle # 1


class FontWeight(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Thin : FontWeight # 100
    ExtraLight : FontWeight # 200
    Light : FontWeight # 300
    Regular : FontWeight # 400
    Medium : FontWeight # 500
    SemiBold : FontWeight # 600
    Bold : FontWeight # 700
    ExtraBold : FontWeight # 800
    Heavy : FontWeight # 900


class ForceLimitMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Magnitude : ForceLimitMode # 0
    PerAxis : ForceLimitMode # 1


class FormFactor(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Symmetric : FormFactor # 0
    Brick : FormFactor # 1
    Block : FormFactor # 1
    Plate : FormFactor # 2
    Custom : FormFactor # 3


class FramerateManagerMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Automatic : FramerateManagerMode # 0
    On : FramerateManagerMode # 1
    Off : FramerateManagerMode # 2


class FrameStyle(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Custom : FrameStyle # 0
    ChatBlue : FrameStyle # 1
    RobloxSquare : FrameStyle # 2
    RobloxRound : FrameStyle # 3
    ChatGreen : FrameStyle # 4
    ChatRed : FrameStyle # 5
    DropShadow : FrameStyle # 6


class FriendRequestEvent(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Issue : FriendRequestEvent # 0
    Revoke : FriendRequestEvent # 1
    Accept : FriendRequestEvent # 2
    Deny : FriendRequestEvent # 3


class FriendStatus(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Unknown : FriendStatus # 0
    NotFriend : FriendStatus # 1
    Friend : FriendStatus # 2
    FriendRequestSent : FriendStatus # 3
    FriendRequestReceived : FriendStatus # 4


class FunctionalTestResult(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Passed : FunctionalTestResult # 0
    Warning : FunctionalTestResult # 1
    Error : FunctionalTestResult # 2


class GameAvatarType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    R6 : GameAvatarType # 0
    R15 : GameAvatarType # 1
    PlayerChoice : GameAvatarType # 2


class GamepadType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Unknown : GamepadType # 0
    PS4 : GamepadType # 1
    PS5 : GamepadType # 2
    XboxOne : GamepadType # 3


class GearGenreSetting(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    AllGenres : GearGenreSetting # 0
    MatchingGenreOnly : GearGenreSetting # 1


class GearType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    MeleeWeapons : GearType # 0
    RangedWeapons : GearType # 1
    Explosives : GearType # 2
    PowerUps : GearType # 3
    NavigationEnhancers : GearType # 4
    MusicalInstruments : GearType # 5
    SocialItems : GearType # 6
    BuildingTools : GearType # 7
    Transport : GearType # 8


class Genre(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    All : Genre # 0
    TownAndCity : Genre # 1
    Fantasy : Genre # 2
    SciFi : Genre # 3
    Ninja : Genre # 4
    Scary : Genre # 5
    Pirate : Genre # 6
    Adventure : Genre # 7
    Sports : Genre # 8
    Funny : Genre # 9
    WildWest : Genre # 10
    War : Genre # 11
    SkatePark : Genre # 12
    Tutorial : Genre # 13


class GraphicsMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Automatic : GraphicsMode # 1
    Direct3D11 : GraphicsMode # 2
    OpenGL : GraphicsMode # 4
    Metal : GraphicsMode # 5
    Vulkan : GraphicsMode # 6
    NoGraphics : GraphicsMode # 9


class GraphicsOptimizationMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Performance : GraphicsOptimizationMode # 0
    Balanced : GraphicsOptimizationMode # 1
    Quality : GraphicsOptimizationMode # 2


class GuiState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Idle : GuiState # 0
    Hover : GuiState # 1
    Press : GuiState # 2
    NonInteractable : GuiState # 3


class GuiType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Core : GuiType # 0
    Custom : GuiType # 1
    PlayerNameplates : GuiType # 2
    CustomBillboards : GuiType # 3
    CoreBillboards : GuiType # 4


class HandlesStyle(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Resize : HandlesStyle # 0
    Movement : HandlesStyle # 1


class HandRigDescriptionSide(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : HandRigDescriptionSide # 0
    Left : HandRigDescriptionSide # 1
    Right : HandRigDescriptionSide # 2


class HapticEffectType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Custom : HapticEffectType # 0
    UIHover : HapticEffectType # 1
    UIClick : HapticEffectType # 2
    UINotification : HapticEffectType # 3
    GameplayExplosion : HapticEffectType # 4
    GameplayCollision : HapticEffectType # 5


class HighlightDepthMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    AlwaysOnTop : HighlightDepthMode # 0
    Occluded : HighlightDepthMode # 1


class HorizontalAlignment(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Center : HorizontalAlignment # 0
    Left : HorizontalAlignment # 1
    Right : HorizontalAlignment # 2


class HoverAnimateSpeed(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    VerySlow : HoverAnimateSpeed # 0
    Slow : HoverAnimateSpeed # 1
    Medium : HoverAnimateSpeed # 2
    Fast : HoverAnimateSpeed # 3
    VeryFast : HoverAnimateSpeed # 4


class HttpCachePolicy(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : HttpCachePolicy # 0
    Full : HttpCachePolicy # 1
    DataOnly : HttpCachePolicy # 2
    Default : HttpCachePolicy # 3
    InternalRedirectRefresh : HttpCachePolicy # 4


class HttpCompression(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : HttpCompression # 0
    Gzip : HttpCompression # 1


class HttpContentType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    ApplicationJson : HttpContentType # 0
    ApplicationXml : HttpContentType # 1
    ApplicationUrlEncoded : HttpContentType # 2
    TextPlain : HttpContentType # 3
    TextXml : HttpContentType # 4


class HttpError(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    OK : HttpError # 0
    InvalidUrl : HttpError # 1
    DnsResolve : HttpError # 2
    ConnectFail : HttpError # 3
    OutOfMemory : HttpError # 4
    TimedOut : HttpError # 5
    TooManyRedirects : HttpError # 6
    InvalidRedirect : HttpError # 7
    NetFail : HttpError # 8
    Aborted : HttpError # 9
    SslConnectFail : HttpError # 10
    SslVerificationFail : HttpError # 11
    Unknown : HttpError # 12
    ConnectionClosed : HttpError # 13
    ServerProtocolError : HttpError # 14


class HttpRequestType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : HttpRequestType # 0
    MarketplaceService : HttpRequestType # 2
    Players : HttpRequestType # 7
    Chat : HttpRequestType # 15
    Avatar : HttpRequestType # 16
    Analytics : HttpRequestType # 23
    Localization : HttpRequestType # 25


class HumanoidCollisionType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    OuterBox : HumanoidCollisionType # 0
    InnerBox : HumanoidCollisionType # 1


class HumanoidDisplayDistanceType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Viewer : HumanoidDisplayDistanceType # 0
    Subject : HumanoidDisplayDistanceType # 1
    None_ : HumanoidDisplayDistanceType # 2


class HumanoidHealthDisplayType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    DisplayWhenDamaged : HumanoidHealthDisplayType # 0
    AlwaysOn : HumanoidHealthDisplayType # 1
    AlwaysOff : HumanoidHealthDisplayType # 2


class HumanoidRigType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    R6 : HumanoidRigType # 0
    R15 : HumanoidRigType # 1


class HumanoidStateType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    FallingDown : HumanoidStateType # 0
    Ragdoll : HumanoidStateType # 1
    GettingUp : HumanoidStateType # 2
    Jumping : HumanoidStateType # 3
    Swimming : HumanoidStateType # 4
    Freefall : HumanoidStateType # 5
    Flying : HumanoidStateType # 6
    Landed : HumanoidStateType # 7
    Running : HumanoidStateType # 8
    RunningNoPhysics : HumanoidStateType # 10
    StrafingNoPhysics : HumanoidStateType # 11
    Climbing : HumanoidStateType # 12
    Seated : HumanoidStateType # 13
    PlatformStanding : HumanoidStateType # 14
    Dead : HumanoidStateType # 15
    Physics : HumanoidStateType # 16
    None_ : HumanoidStateType # 18


class IKCollisionsMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    NoCollisions : IKCollisionsMode # 0
    OtherMechanismsAnchored : IKCollisionsMode # 1
    IncludeContactedMechanisms : IKCollisionsMode # 2


class IKControlConstraintSupport(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : IKControlConstraintSupport # 0
    Disabled : IKControlConstraintSupport # 1
    Enabled : IKControlConstraintSupport # 2


class IKControlType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Transform : IKControlType # 0
    Position : IKControlType # 1
    Rotation : IKControlType # 2
    LookAt : IKControlType # 3


class ImageAlphaType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : ImageAlphaType # 1
    LockCanvasAlpha : ImageAlphaType # 2
    LockCanvasColor : ImageAlphaType # 3


class ImageCombineType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    BlendSourceOver : ImageCombineType # 1
    Overwrite : ImageCombineType # 2
    Add : ImageCombineType # 3
    Multiply : ImageCombineType # 4
    AlphaBlend : ImageCombineType # 5


class InfoType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Asset : InfoType # 0
    Product : InfoType # 1
    GamePass : InfoType # 2
    Subscription : InfoType # 3
    Bundle : InfoType # 4


class InitialDockState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Top : InitialDockState # 0
    Bottom : InitialDockState # 1
    Left : InitialDockState # 2
    Right : InitialDockState # 3
    Float : InitialDockState # 4


class InOut(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Edge : InOut # 0
    Inset : InOut # 1
    Center : InOut # 2


class InputActionType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Bool : InputActionType # 0
    Direction1D : InputActionType # 1
    Direction2D : InputActionType # 2


class InputType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    _Action4 : InputType # 0
    _Action5 : InputType # 0
    NoInput : InputType # 0
    _LeftTread : InputType # 0
    _Action1 : InputType # 0
    _RightTread : InputType # 0
    _Action3 : InputType # 0
    _Steer : InputType # 0
    _Action2 : InputType # 0
    Throtle : InputType # 0
    _UpDown : InputType # 0
    _Throttle : InputType # 0
    Constant : InputType # 12
    Sin : InputType # 13


class IntermediateMeshGenerationResult(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    HighQualityMesh : IntermediateMeshGenerationResult # 0


class InterpolationThrottlingMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : InterpolationThrottlingMode # 0
    Disabled : InterpolationThrottlingMode # 1
    Enabled : InterpolationThrottlingMode # 2


class InviteState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Placed : InviteState # 0
    Accepted : InviteState # 1
    Declined : InviteState # 2
    Missed : InviteState # 3


class ItemLineAlignment(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Automatic : ItemLineAlignment # 0
    Start : ItemLineAlignment # 1
    Center : ItemLineAlignment # 2
    End : ItemLineAlignment # 3
    Stretch : ItemLineAlignment # 4


class IXPLoadingStatus(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : IXPLoadingStatus # 0
    Pending : IXPLoadingStatus # 1
    Initialized : IXPLoadingStatus # 2
    ErrorInvalidUser : IXPLoadingStatus # 3
    ErrorConnection : IXPLoadingStatus # 4
    ErrorJsonParse : IXPLoadingStatus # 5
    ErrorTimedOut : IXPLoadingStatus # 6


class JoinSource(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    CreatedItemAttribution : JoinSource # 1


class JointCreationMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    All : JointCreationMode # 0
    Surface : JointCreationMode # 1
    None_ : JointCreationMode # 2


class KeyCode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Unknown : KeyCode # 0
    Backspace : KeyCode # 8
    Tab : KeyCode # 9
    Clear : KeyCode # 12
    Return : KeyCode # 13
    Pause : KeyCode # 19
    Escape : KeyCode # 27
    Space : KeyCode # 32
    QuotedDouble : KeyCode # 34
    Hash : KeyCode # 35
    Dollar : KeyCode # 36
    Percent : KeyCode # 37
    Ampersand : KeyCode # 38
    Quote : KeyCode # 39
    LeftParenthesis : KeyCode # 40
    RightParenthesis : KeyCode # 41
    Asterisk : KeyCode # 42
    Plus : KeyCode # 43
    Comma : KeyCode # 44
    Minus : KeyCode # 45
    Period : KeyCode # 46
    Slash : KeyCode # 47
    Zero : KeyCode # 48
    One : KeyCode # 49
    Two : KeyCode # 50
    Three : KeyCode # 51
    Four : KeyCode # 52
    Five : KeyCode # 53
    Six : KeyCode # 54
    Seven : KeyCode # 55
    Eight : KeyCode # 56
    Nine : KeyCode # 57
    Colon : KeyCode # 58
    Semicolon : KeyCode # 59
    LessThan : KeyCode # 60
    Equals : KeyCode # 61
    GreaterThan : KeyCode # 62
    Question : KeyCode # 63
    At : KeyCode # 64
    LeftBracket : KeyCode # 91
    BackSlash : KeyCode # 92
    RightBracket : KeyCode # 93
    Caret : KeyCode # 94
    Underscore : KeyCode # 95
    Backquote : KeyCode # 96
    A : KeyCode # 97
    B : KeyCode # 98
    C : KeyCode # 99
    D : KeyCode # 100
    E : KeyCode # 101
    F : KeyCode # 102
    G : KeyCode # 103
    H : KeyCode # 104
    I : KeyCode # 105
    J : KeyCode # 106
    K : KeyCode # 107
    L : KeyCode # 108
    M : KeyCode # 109
    N : KeyCode # 110
    O : KeyCode # 111
    P : KeyCode # 112
    Q : KeyCode # 113
    R : KeyCode # 114
    S : KeyCode # 115
    T : KeyCode # 116
    U : KeyCode # 117
    V : KeyCode # 118
    W : KeyCode # 119
    X : KeyCode # 120
    Y : KeyCode # 121
    Z : KeyCode # 122
    LeftCurly : KeyCode # 123
    Pipe : KeyCode # 124
    RightCurly : KeyCode # 125
    Tilde : KeyCode # 126
    Delete : KeyCode # 127
    World0 : KeyCode # 160
    World1 : KeyCode # 161
    World2 : KeyCode # 162
    World3 : KeyCode # 163
    World4 : KeyCode # 164
    World5 : KeyCode # 165
    World6 : KeyCode # 166
    World7 : KeyCode # 167
    World8 : KeyCode # 168
    World9 : KeyCode # 169
    World10 : KeyCode # 170
    World11 : KeyCode # 171
    World12 : KeyCode # 172
    World13 : KeyCode # 173
    World14 : KeyCode # 174
    World15 : KeyCode # 175
    World16 : KeyCode # 176
    World17 : KeyCode # 177
    World18 : KeyCode # 178
    World19 : KeyCode # 179
    World20 : KeyCode # 180
    World21 : KeyCode # 181
    World22 : KeyCode # 182
    World23 : KeyCode # 183
    World24 : KeyCode # 184
    World25 : KeyCode # 185
    World26 : KeyCode # 186
    World27 : KeyCode # 187
    World28 : KeyCode # 188
    World29 : KeyCode # 189
    World30 : KeyCode # 190
    World31 : KeyCode # 191
    World32 : KeyCode # 192
    World33 : KeyCode # 193
    World34 : KeyCode # 194
    World35 : KeyCode # 195
    World36 : KeyCode # 196
    World37 : KeyCode # 197
    World38 : KeyCode # 198
    World39 : KeyCode # 199
    World40 : KeyCode # 200
    World41 : KeyCode # 201
    World42 : KeyCode # 202
    World43 : KeyCode # 203
    World44 : KeyCode # 204
    World45 : KeyCode # 205
    World46 : KeyCode # 206
    World47 : KeyCode # 207
    World48 : KeyCode # 208
    World49 : KeyCode # 209
    World50 : KeyCode # 210
    World51 : KeyCode # 211
    World52 : KeyCode # 212
    World53 : KeyCode # 213
    World54 : KeyCode # 214
    World55 : KeyCode # 215
    World56 : KeyCode # 216
    World57 : KeyCode # 217
    World58 : KeyCode # 218
    World59 : KeyCode # 219
    World60 : KeyCode # 220
    World61 : KeyCode # 221
    World62 : KeyCode # 222
    World63 : KeyCode # 223
    World64 : KeyCode # 224
    World65 : KeyCode # 225
    World66 : KeyCode # 226
    World67 : KeyCode # 227
    World68 : KeyCode # 228
    World69 : KeyCode # 229
    World70 : KeyCode # 230
    World71 : KeyCode # 231
    World72 : KeyCode # 232
    World73 : KeyCode # 233
    World74 : KeyCode # 234
    World75 : KeyCode # 235
    World76 : KeyCode # 236
    World77 : KeyCode # 237
    World78 : KeyCode # 238
    World79 : KeyCode # 239
    World80 : KeyCode # 240
    World81 : KeyCode # 241
    World82 : KeyCode # 242
    World83 : KeyCode # 243
    World84 : KeyCode # 244
    World85 : KeyCode # 245
    World86 : KeyCode # 246
    World87 : KeyCode # 247
    World88 : KeyCode # 248
    World89 : KeyCode # 249
    World90 : KeyCode # 250
    World91 : KeyCode # 251
    World92 : KeyCode # 252
    World93 : KeyCode # 253
    World94 : KeyCode # 254
    World95 : KeyCode # 255
    KeypadZero : KeyCode # 256
    KeypadOne : KeyCode # 257
    KeypadTwo : KeyCode # 258
    KeypadThree : KeyCode # 259
    KeypadFour : KeyCode # 260
    KeypadFive : KeyCode # 261
    KeypadSix : KeyCode # 262
    KeypadSeven : KeyCode # 263
    KeypadEight : KeyCode # 264
    KeypadNine : KeyCode # 265
    KeypadPeriod : KeyCode # 266
    KeypadDivide : KeyCode # 267
    KeypadMultiply : KeyCode # 268
    KeypadMinus : KeyCode # 269
    KeypadPlus : KeyCode # 270
    KeypadEnter : KeyCode # 271
    KeypadEquals : KeyCode # 272
    Up : KeyCode # 273
    Down : KeyCode # 274
    Right : KeyCode # 275
    Left : KeyCode # 276
    Insert : KeyCode # 277
    Home : KeyCode # 278
    End : KeyCode # 279
    PageUp : KeyCode # 280
    PageDown : KeyCode # 281
    F1 : KeyCode # 282
    F2 : KeyCode # 283
    F3 : KeyCode # 284
    F4 : KeyCode # 285
    F5 : KeyCode # 286
    F6 : KeyCode # 287
    F7 : KeyCode # 288
    F8 : KeyCode # 289
    F9 : KeyCode # 290
    F10 : KeyCode # 291
    F11 : KeyCode # 292
    F12 : KeyCode # 293
    F13 : KeyCode # 294
    F14 : KeyCode # 295
    F15 : KeyCode # 296
    NumLock : KeyCode # 300
    CapsLock : KeyCode # 301
    ScrollLock : KeyCode # 302
    RightShift : KeyCode # 303
    LeftShift : KeyCode # 304
    RightControl : KeyCode # 305
    LeftControl : KeyCode # 306
    RightAlt : KeyCode # 307
    LeftAlt : KeyCode # 308
    RightMeta : KeyCode # 309
    LeftMeta : KeyCode # 310
    LeftSuper : KeyCode # 311
    RightSuper : KeyCode # 312
    Mode : KeyCode # 313
    Compose : KeyCode # 314
    Help : KeyCode # 315
    Print : KeyCode # 316
    SysReq : KeyCode # 317
    Break : KeyCode # 318
    Menu : KeyCode # 319
    Power : KeyCode # 320
    Euro : KeyCode # 321
    Undo : KeyCode # 322
    ButtonX : KeyCode # 1000
    ButtonY : KeyCode # 1001
    ButtonA : KeyCode # 1002
    ButtonB : KeyCode # 1003
    ButtonR1 : KeyCode # 1004
    ButtonL1 : KeyCode # 1005
    ButtonR2 : KeyCode # 1006
    ButtonL2 : KeyCode # 1007
    ButtonR3 : KeyCode # 1008
    ButtonL3 : KeyCode # 1009
    ButtonStart : KeyCode # 1010
    ButtonSelect : KeyCode # 1011
    DPadLeft : KeyCode # 1012
    DPadRight : KeyCode # 1013
    DPadUp : KeyCode # 1014
    DPadDown : KeyCode # 1015
    Thumbstick1 : KeyCode # 1016
    Thumbstick2 : KeyCode # 1017
    MouseLeftButton : KeyCode # 1018
    MouseRightButton : KeyCode # 1019
    MouseMiddleButton : KeyCode # 1020
    MouseBackButton : KeyCode # 1021
    MouseNoButton : KeyCode # 1022
    MouseX : KeyCode # 1023
    MouseY : KeyCode # 1024


class KeyInterpolationMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Constant : KeyInterpolationMode # 0
    Linear : KeyInterpolationMode # 1
    Cubic : KeyInterpolationMode # 2


class KeywordFilterType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Include : KeywordFilterType # 0
    Exclude : KeywordFilterType # 1


class Language(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : Language # 0


class LeftRight(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Left : LeftRight # 0
    Center : LeftRight # 1
    Right : LeftRight # 2


class LexemeType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Eof : LexemeType # 0
    Name : LexemeType # 1
    QuotedString : LexemeType # 2
    Number : LexemeType # 3
    And : LexemeType # 4
    Or : LexemeType # 5
    Equal : LexemeType # 6
    TildeEqual : LexemeType # 7
    GreaterThan : LexemeType # 8
    GreaterThanEqual : LexemeType # 9
    LessThan : LexemeType # 10
    LessThanEqual : LexemeType # 11
    Colon : LexemeType # 12
    Dot : LexemeType # 13
    LeftParenthesis : LexemeType # 14
    RightParenthesis : LexemeType # 15
    Star : LexemeType # 16
    DoubleStar : LexemeType # 17
    ReservedSpecial : LexemeType # 18


class LightingStyle(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Realistic : LightingStyle # 0
    Soft : LightingStyle # 1


class Limb(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Head : Limb # 0
    Torso : Limb # 1
    LeftArm : Limb # 2
    RightArm : Limb # 3
    LeftLeg : Limb # 4
    RightLeg : Limb # 5
    Unknown : Limb # 6


class LineJoinMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Round : LineJoinMode # 0
    Bevel : LineJoinMode # 1
    Miter : LineJoinMode # 2


class ListDisplayMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Horizontal : ListDisplayMode # 0
    Vertical : ListDisplayMode # 1


class ListenerLocation(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : ListenerLocation # 0
    None_ : ListenerLocation # 1
    Character : ListenerLocation # 2
    Camera : ListenerLocation # 3


class ListenerType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Camera : ListenerType # 0
    CFrame : ListenerType # 1
    ObjectPosition : ListenerType # 2
    ObjectCFrame : ListenerType # 3


class LiveEditingAtomicUpdateResponse(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Success : LiveEditingAtomicUpdateResponse # 0
    FailureGuidNotFound : LiveEditingAtomicUpdateResponse # 1
    FailureHashMismatch : LiveEditingAtomicUpdateResponse # 2
    FailureOperationIllegal : LiveEditingAtomicUpdateResponse # 3


class LiveEditingBroadcastMessageType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Normal : LiveEditingBroadcastMessageType # 0
    Warning : LiveEditingBroadcastMessageType # 1
    Error : LiveEditingBroadcastMessageType # 2


class LoadCharacterLayeredClothing(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : LoadCharacterLayeredClothing # 0
    Disabled : LoadCharacterLayeredClothing # 1
    Enabled : LoadCharacterLayeredClothing # 2


class LoadDynamicHeads(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : LoadDynamicHeads # 0
    Disabled : LoadDynamicHeads # 1
    Enabled : LoadDynamicHeads # 2


class LocationType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Character : LocationType # 0
    Camera : LocationType # 1
    ObjectPosition : LocationType # 2


class MarketplaceBulkPurchasePromptStatus(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Completed : MarketplaceBulkPurchasePromptStatus # 1
    Aborted : MarketplaceBulkPurchasePromptStatus # 2
    Error : MarketplaceBulkPurchasePromptStatus # 3


class MarketplaceItemPurchaseStatus(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Success : MarketplaceItemPurchaseStatus # 1
    SystemError : MarketplaceItemPurchaseStatus # 2
    AlreadyOwned : MarketplaceItemPurchaseStatus # 3
    InsufficientRobux : MarketplaceItemPurchaseStatus # 4
    QuantityLimitExceeded : MarketplaceItemPurchaseStatus # 5
    QuotaExceeded : MarketplaceItemPurchaseStatus # 6
    NotForSale : MarketplaceItemPurchaseStatus # 7
    NotAvailableForPurchaser : MarketplaceItemPurchaseStatus # 8
    PriceMismatch : MarketplaceItemPurchaseStatus # 9
    SoldOut : MarketplaceItemPurchaseStatus # 10
    PurchaserIsSeller : MarketplaceItemPurchaseStatus # 11
    InsufficientMembership : MarketplaceItemPurchaseStatus # 12
    PlaceInvalid : MarketplaceItemPurchaseStatus # 13


class MarketplaceProductType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    AvatarAsset : MarketplaceProductType # 1
    AvatarBundle : MarketplaceProductType # 2


class MarkupKind(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    PlainText : MarkupKind # 0
    Markdown : MarkupKind # 1


class MatchmakingType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : MatchmakingType # 1
    XboxOnly : MatchmakingType # 2
    PlayStationOnly : MatchmakingType # 3


class Material(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Plastic : Material # 256
    SmoothPlastic : Material # 272
    Neon : Material # 288
    Wood : Material # 512
    WoodPlanks : Material # 528
    Marble : Material # 784
    Basalt : Material # 788
    Slate : Material # 800
    CrackedLava : Material # 804
    Concrete : Material # 816
    Limestone : Material # 820
    Granite : Material # 832
    Pavement : Material # 836
    Brick : Material # 848
    Pebble : Material # 864
    Cobblestone : Material # 880
    Rock : Material # 896
    Sandstone : Material # 912
    CorrodedMetal : Material # 1040
    Corroded_Metal : Material # 1040
    DiamondPlate : Material # 1056
    Foil : Material # 1072
    Aluminum : Material # 1072
    Metal : Material # 1088
    Grass : Material # 1280
    LeafyGrass : Material # 1284
    Sand : Material # 1296
    Fabric : Material # 1312
    Snow : Material # 1328
    Mud : Material # 1344
    Ground : Material # 1360
    Asphalt : Material # 1376
    Salt : Material # 1392
    Ice : Material # 1536
    Glacier : Material # 1552
    Glass : Material # 1568
    ForceField : Material # 1584
    Air : Material # 1792
    Water : Material # 2048
    Cardboard : Material # 2304
    Carpet : Material # 2305
    CeramicTiles : Material # 2306
    ClayRoofTiles : Material # 2307
    RoofShingles : Material # 2308
    Leather : Material # 2309
    Plaster : Material # 2310
    Rubber : Material # 2311


class MaterialPattern(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Regular : MaterialPattern # 0
    Organic : MaterialPattern # 1


class MembershipType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : MembershipType # 0
    BuildersClub : MembershipType # 1
    TurboBuildersClub : MembershipType # 2
    OutrageousBuildersClub : MembershipType # 3
    Premium : MembershipType # 4


class MeshPartDetailLevel(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    DistanceBased : MeshPartDetailLevel # 0
    Level00 : MeshPartDetailLevel # 1
    Level01 : MeshPartDetailLevel # 2
    Level02 : MeshPartDetailLevel # 3
    Level03 : MeshPartDetailLevel # 4
    Level04 : MeshPartDetailLevel # 5


class MeshPartHeadsAndAccessories(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : MeshPartHeadsAndAccessories # 0
    Disabled : MeshPartHeadsAndAccessories # 1
    Enabled : MeshPartHeadsAndAccessories # 2


class MeshScaleUnit(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Stud : MeshScaleUnit # 0
    Meter : MeshScaleUnit # 1
    CM : MeshScaleUnit # 2
    MM : MeshScaleUnit # 3
    Foot : MeshScaleUnit # 4
    Inch : MeshScaleUnit # 5


class MeshType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Head : MeshType # 0
    Torso : MeshType # 1
    Wedge : MeshType # 2
    Sphere : MeshType # 3
    Cylinder : MeshType # 4
    FileMesh : MeshType # 5
    Brick : MeshType # 6
    Prism : MeshType # 7
    Pyramid : MeshType # 8
    ParallelRamp : MeshType # 9
    RightAngleRamp : MeshType # 10
    CornerWedge : MeshType # 11


class MessageType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    MessageOutput : MessageType # 0
    MessageInfo : MessageType # 1
    MessageWarning : MessageType # 2
    MessageError : MessageType # 3


class ModelLevelOfDetail(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Automatic : ModelLevelOfDetail # 0
    StreamingMesh : ModelLevelOfDetail # 1
    Disabled : ModelLevelOfDetail # 2


class ModelStreamingBehavior(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : ModelStreamingBehavior # 0
    Legacy : ModelStreamingBehavior # 1
    Improved : ModelStreamingBehavior # 2


class ModelStreamingMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : ModelStreamingMode # 0
    Atomic : ModelStreamingMode # 1
    Persistent : ModelStreamingMode # 2
    PersistentPerPlayer : ModelStreamingMode # 3
    Nonatomic : ModelStreamingMode # 4


class ModerationStatus(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    ReviewedApproved : ModerationStatus # 1
    ReviewedRejected : ModerationStatus # 2
    NotReviewed : ModerationStatus # 3
    NotApplicable : ModerationStatus # 4
    Invalid : ModerationStatus # 5


class ModifierKey(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Shift : ModifierKey # 0
    Ctrl : ModifierKey # 1
    Alt : ModifierKey # 2
    Meta : ModifierKey # 3


class MouseBehavior(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : MouseBehavior # 0
    LockCenter : MouseBehavior # 1
    LockCurrentPosition : MouseBehavior # 2


class MoverConstraintRootBehaviorMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : MoverConstraintRootBehaviorMode # 0
    Disabled : MoverConstraintRootBehaviorMode # 1
    Enabled : MoverConstraintRootBehaviorMode # 2


class MoveState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Stopped : MoveState # 0
    Coasting : MoveState # 1
    Pushing : MoveState # 2
    Stopping : MoveState # 3
    AirFree : MoveState # 4


class MuteState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Unmuted : MuteState # 0
    Muted : MuteState # 1


class NameOcclusion(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    NoOcclusion : NameOcclusion # 0
    EnemyOcclusion : NameOcclusion # 1
    OccludeAll : NameOcclusion # 2


class NegateOperationHiddenHistory(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : NegateOperationHiddenHistory # 0
    NegatedUnion : NegateOperationHiddenHistory # 1
    NegatedIntersection : NegateOperationHiddenHistory # 2


class NetworkOwnership(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Automatic : NetworkOwnership # 0
    Manual : NetworkOwnership # 1
    OnContact : NetworkOwnership # 2


class NetworkStatus(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Unknown : NetworkStatus # 0
    Connected : NetworkStatus # 1
    Disconnected : NetworkStatus # 2


class NoiseType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    SimplexGabor : NoiseType # 0


class NormalId(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Right : NormalId # 0
    Top : NormalId # 1
    Back : NormalId # 2
    Left : NormalId # 3
    Bottom : NormalId # 4
    Front : NormalId # 5


class NotificationButtonType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Primary : NotificationButtonType # 0
    Secondary : NotificationButtonType # 1


class OperationType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Null : OperationType # 0
    Union : OperationType # 1
    Subtraction : OperationType # 2
    Intersection : OperationType # 3
    Primitive : OperationType # 4


class OrientationAlignmentMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    OneAttachment : OrientationAlignmentMode # 0
    TwoAttachment : OrientationAlignmentMode # 1


class OutfitSource(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    All : OutfitSource # 1
    Created : OutfitSource # 2
    Purchased : OutfitSource # 3


class OutfitType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    All : OutfitType # 1
    Avatar : OutfitType # 2
    DynamicHead : OutfitType # 3


class OutputLayoutMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Horizontal : OutputLayoutMode # 0
    Vertical : OutputLayoutMode # 1


class OverrideMouseIconBehavior(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : OverrideMouseIconBehavior # 0
    ForceShow : OverrideMouseIconBehavior # 1
    ForceHide : OverrideMouseIconBehavior # 2


class PackagePermission(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : PackagePermission # 0
    NoAccess : PackagePermission # 1
    Revoked : PackagePermission # 2
    UseView : PackagePermission # 3
    Edit : PackagePermission # 4
    Own : PackagePermission # 5


class ParticleEmitterShape(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Box : ParticleEmitterShape # 0
    Sphere : ParticleEmitterShape # 1
    Cylinder : ParticleEmitterShape # 2
    Disc : ParticleEmitterShape # 3


class ParticleEmitterShapeInOut(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Outward : ParticleEmitterShapeInOut # 0
    Inward : ParticleEmitterShapeInOut # 1
    InAndOut : ParticleEmitterShapeInOut # 2


class ParticleEmitterShapeStyle(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Volume : ParticleEmitterShapeStyle # 0
    Surface : ParticleEmitterShapeStyle # 1


class ParticleFlipbookLayout(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : ParticleFlipbookLayout # 0
    Grid2x2 : ParticleFlipbookLayout # 1
    Grid4x4 : ParticleFlipbookLayout # 2
    Grid8x8 : ParticleFlipbookLayout # 3


class ParticleFlipbookMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Loop : ParticleFlipbookMode # 0
    OneShot : ParticleFlipbookMode # 1
    PingPong : ParticleFlipbookMode # 2
    Random : ParticleFlipbookMode # 3


class ParticleFlipbookTextureCompatible(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    NotCompatible : ParticleFlipbookTextureCompatible # 0
    Compatible : ParticleFlipbookTextureCompatible # 1
    Unknown : ParticleFlipbookTextureCompatible # 2


class ParticleOrientation(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    FacingCamera : ParticleOrientation # 0
    FacingCameraWorldUp : ParticleOrientation # 1
    VelocityParallel : ParticleOrientation # 2
    VelocityPerpendicular : ParticleOrientation # 3


class PartType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Ball : PartType # 0
    Block : PartType # 1
    Cylinder : PartType # 2
    Wedge : PartType # 3
    CornerWedge : PartType # 4


class PathfindingUseImprovedSearch(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : PathfindingUseImprovedSearch # 0
    Disabled : PathfindingUseImprovedSearch # 1
    Enabled : PathfindingUseImprovedSearch # 2


class PathStatus(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Success : PathStatus # 0
    ClosestNoPath : PathStatus # 1
    ClosestOutOfRange : PathStatus # 2
    FailStartNotEmpty : PathStatus # 3
    FailFinishNotEmpty : PathStatus # 4
    NoPath : PathStatus # 5


class PathWaypointAction(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Walk : PathWaypointAction # 0
    Jump : PathWaypointAction # 1
    Custom : PathWaypointAction # 2


class PermissionLevelShown(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Game : PermissionLevelShown # 0
    RobloxGame : PermissionLevelShown # 1
    RobloxScript : PermissionLevelShown # 2
    Studio : PermissionLevelShown # 3
    Roblox : PermissionLevelShown # 4


class PhysicsSimulationRate(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Fixed240Hz : PhysicsSimulationRate # 0
    Fixed120Hz : PhysicsSimulationRate # 1
    Fixed60Hz : PhysicsSimulationRate # 2


class PhysicsSteppingMethod(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : PhysicsSteppingMethod # 0
    Fixed : PhysicsSteppingMethod # 1
    Adaptive : PhysicsSteppingMethod # 2


class Platform(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Windows : Platform # 0
    OSX : Platform # 1
    IOS : Platform # 2
    Android : Platform # 3
    XBoxOne : Platform # 4
    PS4 : Platform # 5
    PS3 : Platform # 6
    XBox360 : Platform # 7
    WiiU : Platform # 8
    NX : Platform # 9
    Ouya : Platform # 10
    AndroidTV : Platform # 11
    Chromecast : Platform # 12
    Linux : Platform # 13
    SteamOS : Platform # 14
    WebOS : Platform # 15
    DOS : Platform # 16
    BeOS : Platform # 17
    UWP : Platform # 18
    PS5 : Platform # 19
    MetaOS : Platform # 20
    None_ : Platform # 21


class PlaybackState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Begin : PlaybackState # 0
    Delayed : PlaybackState # 1
    Playing : PlaybackState # 2
    Paused : PlaybackState # 3
    Completed : PlaybackState # 4
    Cancelled : PlaybackState # 5


class PlayerActions(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    CharacterForward : PlayerActions # 0
    CharacterBackward : PlayerActions # 1
    CharacterLeft : PlayerActions # 2
    CharacterRight : PlayerActions # 3
    CharacterJump : PlayerActions # 4


class PlayerCharacterDestroyBehavior(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : PlayerCharacterDestroyBehavior # 0
    Disabled : PlayerCharacterDestroyBehavior # 1
    Enabled : PlayerCharacterDestroyBehavior # 2


class PlayerChatType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    All : PlayerChatType # 0
    Team : PlayerChatType # 1
    Whisper : PlayerChatType # 2


class PlayerDataErrorState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    LoadFailed : PlayerDataErrorState # 0
    FlushFailed : PlayerDataErrorState # 1
    ReleaseFailed : PlayerDataErrorState # 2
    None_ : PlayerDataErrorState # 3


class PlayerDataLoadFailureBehavior(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Failure : PlayerDataLoadFailureBehavior # 0
    FallbackToDefault : PlayerDataLoadFailureBehavior # 1
    Kick : PlayerDataLoadFailureBehavior # 2


class PoseEasingDirection(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    In : PoseEasingDirection # 0
    Out : PoseEasingDirection # 1
    InOut : PoseEasingDirection # 2


class PoseEasingStyle(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Linear : PoseEasingStyle # 0
    Constant : PoseEasingStyle # 1
    Elastic : PoseEasingStyle # 2
    Cubic : PoseEasingStyle # 3
    Bounce : PoseEasingStyle # 4
    CubicV2 : PoseEasingStyle # 5


class PositionAlignmentMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    OneAttachment : PositionAlignmentMode # 0
    TwoAttachment : PositionAlignmentMode # 1


class PreferredInput(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    KeyboardAndMouse : PreferredInput # 0
    Gamepad : PreferredInput # 1
    Touch : PreferredInput # 2


class PreferredTextSize(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Medium : PreferredTextSize # 1
    Large : PreferredTextSize # 2
    Larger : PreferredTextSize # 3
    Largest : PreferredTextSize # 4


class PrimalPhysicsSolver(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : PrimalPhysicsSolver # 0
    Experimental : PrimalPhysicsSolver # 1
    Disabled : PrimalPhysicsSolver # 2


class PrimitiveType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Null : PrimitiveType # 0
    Ball : PrimitiveType # 1
    Cylinder : PrimitiveType # 2
    Block : PrimitiveType # 3
    Wedge : PrimitiveType # 4
    CornerWedge : PrimitiveType # 5


class PrivilegeType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Banned : PrivilegeType # 0
    Visitor : PrivilegeType # 10
    Member : PrivilegeType # 128
    Admin : PrivilegeType # 240
    Owner : PrivilegeType # 255


class ProductLocationRestriction(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    AvatarShop : ProductLocationRestriction # 0
    AllowedGames : ProductLocationRestriction # 1
    AllGames : ProductLocationRestriction # 2


class ProductPurchaseChannel(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    InExperience : ProductPurchaseChannel # 1
    ExperienceDetailsPage : ProductPurchaseChannel # 2
    AdReward : ProductPurchaseChannel # 3
    CommerceProduct : ProductPurchaseChannel # 4


class ProductPurchaseDecision(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    NotProcessedYet : ProductPurchaseDecision # 0
    PurchaseGranted : ProductPurchaseDecision # 1


class PromptCreateAssetResult(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Success : PromptCreateAssetResult # 1
    PermissionDenied : PromptCreateAssetResult # 2
    Timeout : PromptCreateAssetResult # 3
    UploadFailed : PromptCreateAssetResult # 4
    NoUserInput : PromptCreateAssetResult # 5
    UnknownFailure : PromptCreateAssetResult # 6


class PromptCreateAvatarResult(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Success : PromptCreateAvatarResult # 1
    PermissionDenied : PromptCreateAvatarResult # 2
    Timeout : PromptCreateAvatarResult # 3
    UploadFailed : PromptCreateAvatarResult # 4
    NoUserInput : PromptCreateAvatarResult # 5
    InvalidHumanoidDescription : PromptCreateAvatarResult # 6
    UGCValidationFailed : PromptCreateAvatarResult # 7
    ModeratedName : PromptCreateAvatarResult # 8
    MaxOutfits : PromptCreateAvatarResult # 9
    PurchaseFailure : PromptCreateAvatarResult # 10
    UnknownFailure : PromptCreateAvatarResult # 11
    TokenInvalid : PromptCreateAvatarResult # 12


class PromptPublishAssetResult(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Success : PromptPublishAssetResult # 1
    PermissionDenied : PromptPublishAssetResult # 2
    Timeout : PromptPublishAssetResult # 3
    UploadFailed : PromptPublishAssetResult # 4
    NoUserInput : PromptPublishAssetResult # 5
    UnknownFailure : PromptPublishAssetResult # 6


class PropertyStatus(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Ok : PropertyStatus # 0
    Warning : PropertyStatus # 1
    Error : PropertyStatus # 2


class ProximityPromptExclusivity(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    OnePerButton : ProximityPromptExclusivity # 0
    OneGlobally : ProximityPromptExclusivity # 1
    AlwaysShow : ProximityPromptExclusivity # 2


class ProximityPromptInputType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Keyboard : ProximityPromptInputType # 0
    Gamepad : ProximityPromptInputType # 1
    Touch : ProximityPromptInputType # 2


class ProximityPromptStyle(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : ProximityPromptStyle # 0
    Custom : ProximityPromptStyle # 1


class QualityLevel(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Automatic : QualityLevel # 0
    Level01 : QualityLevel # 1
    Level__1 : QualityLevel # 1
    Level02 : QualityLevel # 2
    Level__2 : QualityLevel # 2
    Level03 : QualityLevel # 3
    Level__3 : QualityLevel # 3
    Level04 : QualityLevel # 4
    Level__4 : QualityLevel # 4
    Level05 : QualityLevel # 5
    Level__5 : QualityLevel # 5
    Level06 : QualityLevel # 6
    Level__6 : QualityLevel # 6
    Level07 : QualityLevel # 7
    Level__7 : QualityLevel # 7
    Level08 : QualityLevel # 8
    Level__8 : QualityLevel # 8
    Level09 : QualityLevel # 9
    Level__9 : QualityLevel # 9
    Level10 : QualityLevel # 10
    Level_10 : QualityLevel # 10
    Level11 : QualityLevel # 11
    Level_11 : QualityLevel # 11
    Level12 : QualityLevel # 12
    Level_12 : QualityLevel # 12
    Level13 : QualityLevel # 13
    Level_13 : QualityLevel # 13
    Level14 : QualityLevel # 14
    Level_14 : QualityLevel # 14
    Level15 : QualityLevel # 15
    Level_15 : QualityLevel # 15
    Level16 : QualityLevel # 16
    Level_16 : QualityLevel # 16
    Level17 : QualityLevel # 17
    Level_17 : QualityLevel # 17
    Level18 : QualityLevel # 18
    Level_18 : QualityLevel # 18
    Level19 : QualityLevel # 19
    Level_19 : QualityLevel # 19
    Level20 : QualityLevel # 20
    Level_20 : QualityLevel # 20
    Level21 : QualityLevel # 21
    Level_21 : QualityLevel # 21


class R15CollisionType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    OuterBox : R15CollisionType # 0
    InnerBox : R15CollisionType # 1


class RaycastFilterType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Blacklist : RaycastFilterType # 0
    Exclude : RaycastFilterType # 0
    Include : RaycastFilterType # 1
    Whitelist : RaycastFilterType # 1


class RejectCharacterDeletions(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : RejectCharacterDeletions # 0
    Disabled : RejectCharacterDeletions # 1
    Enabled : RejectCharacterDeletions # 2


class RenderFidelity(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Automatic : RenderFidelity # 0
    Precise : RenderFidelity # 1
    Performance : RenderFidelity # 2


class RenderingCacheOptimizationMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : RenderingCacheOptimizationMode # 0
    Disabled : RenderingCacheOptimizationMode # 1
    Enabled : RenderingCacheOptimizationMode # 2


class RenderingTestComparisonMethod(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    psnr : RenderingTestComparisonMethod # 0
    diff : RenderingTestComparisonMethod # 1


class RenderPriority(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    First : RenderPriority # 0
    Input : RenderPriority # 100
    Camera : RenderPriority # 200
    Character : RenderPriority # 300
    Last : RenderPriority # 2000


class ReplicateInstanceDestroySetting(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : ReplicateInstanceDestroySetting # 0
    Disabled : ReplicateInstanceDestroySetting # 1
    Enabled : ReplicateInstanceDestroySetting # 2


class ResamplerMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : ResamplerMode # 0
    Pixelated : ResamplerMode # 1


class ReservedHighlightId(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Standard : ReservedHighlightId # 0
    Active : ReservedHighlightId # 131072
    Hover : ReservedHighlightId # 262144
    Selection : ReservedHighlightId # 524288


class RestPose(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : RestPose # 0
    RotationsReset : RestPose # 1
    Custom : RestPose # 2


class ReturnKeyType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : ReturnKeyType # 0
    Done : ReturnKeyType # 1
    Go : ReturnKeyType # 2
    Next : ReturnKeyType # 3
    Search : ReturnKeyType # 4
    Send : ReturnKeyType # 5


class ReverbType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    NoReverb : ReverbType # 0
    GenericReverb : ReverbType # 1
    PaddedCell : ReverbType # 2
    Room : ReverbType # 3
    Bathroom : ReverbType # 4
    LivingRoom : ReverbType # 5
    StoneRoom : ReverbType # 6
    Auditorium : ReverbType # 7
    ConcertHall : ReverbType # 8
    Cave : ReverbType # 9
    Arena : ReverbType # 10
    Hangar : ReverbType # 11
    CarpettedHallway : ReverbType # 12
    Hallway : ReverbType # 13
    StoneCorridor : ReverbType # 14
    Alley : ReverbType # 15
    Forest : ReverbType # 16
    City : ReverbType # 17
    Mountains : ReverbType # 18
    Quarry : ReverbType # 19
    Plain : ReverbType # 20
    ParkingLot : ReverbType # 21
    SewerPipe : ReverbType # 22
    UnderWater : ReverbType # 23


class RibbonTool(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Select : RibbonTool # 0
    Scale : RibbonTool # 1
    Rotate : RibbonTool # 2
    Move : RibbonTool # 3
    Transform : RibbonTool # 4
    ColorPicker : RibbonTool # 5
    MaterialPicker : RibbonTool # 6
    Group : RibbonTool # 7
    Ungroup : RibbonTool # 8
    None_ : RibbonTool # 9
    PivotEditor : RibbonTool # 10


class RigScale(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : RigScale # 0
    Rthro : RigScale # 1
    RthroNarrow : RigScale # 2


class RigType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    R15 : RigType # 0
    Custom : RigType # 1
    None_ : RigType # 2


class RollOffMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Inverse : RollOffMode # 0
    Linear : RollOffMode # 1
    LinearSquare : RollOffMode # 2
    InverseTapered : RollOffMode # 3


class RolloutState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : RolloutState # 0
    Disabled : RolloutState # 1
    Enabled : RolloutState # 2


class RotationOrder(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    XYZ : RotationOrder # 0
    XZY : RotationOrder # 1
    YZX : RotationOrder # 2
    YXZ : RotationOrder # 3
    ZXY : RotationOrder # 4
    ZYX : RotationOrder # 5


class RotationType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    MovementRelative : RotationType # 0
    CameraRelative : RotationType # 1


class RtlTextSupport(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : RtlTextSupport # 0
    Disabled : RtlTextSupport # 1
    Enabled : RtlTextSupport # 2


class RunContext(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Legacy : RunContext # 0
    Server : RunContext # 1
    Client : RunContext # 2
    Plugin : RunContext # 3


class RunState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Stopped : RunState # 0
    Running : RunState # 1
    Paused : RunState # 2


class RuntimeUndoBehavior(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Aggregate : RuntimeUndoBehavior # 0
    Snapshot : RuntimeUndoBehavior # 1
    Hybrid : RuntimeUndoBehavior # 2


class SafeAreaCompatibility(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : SafeAreaCompatibility # 0
    FullscreenExtension : SafeAreaCompatibility # 1


class SalesTypeFilter(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    All : SalesTypeFilter # 1
    Collectibles : SalesTypeFilter # 2
    Premium : SalesTypeFilter # 3


class SandboxedInstanceMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : SandboxedInstanceMode # 0
    Experimental : SandboxedInstanceMode # 1


class SaveAvatarThumbnailCustomizationFailure(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    BadThumbnailType : SaveAvatarThumbnailCustomizationFailure # 1
    BadYRotDeg : SaveAvatarThumbnailCustomizationFailure # 2
    BadFieldOfViewDeg : SaveAvatarThumbnailCustomizationFailure # 3
    BadDistanceScale : SaveAvatarThumbnailCustomizationFailure # 4
    Other : SaveAvatarThumbnailCustomizationFailure # 5
    Throttled : SaveAvatarThumbnailCustomizationFailure # 6


class SavedQualitySetting(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Automatic : SavedQualitySetting # 0
    QualityLevel1 : SavedQualitySetting # 1
    QualityLevel2 : SavedQualitySetting # 2
    QualityLevel3 : SavedQualitySetting # 3
    QualityLevel4 : SavedQualitySetting # 4
    QualityLevel5 : SavedQualitySetting # 5
    QualityLevel6 : SavedQualitySetting # 6
    QualityLevel7 : SavedQualitySetting # 7
    QualityLevel8 : SavedQualitySetting # 8
    QualityLevel9 : SavedQualitySetting # 9
    QualityLevel10 : SavedQualitySetting # 10


class SaveFilter(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    SaveWorld : SaveFilter # 0
    SaveGame : SaveFilter # 1
    SaveAll : SaveFilter # 2


class ScaleType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Stretch : ScaleType # 0
    Slice : ScaleType # 1
    Tile : ScaleType # 2
    Fit : ScaleType # 3
    Crop : ScaleType # 4


class ScopeCheckResult(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    ConsentAccepted : ScopeCheckResult # 0
    InvalidScopes : ScopeCheckResult # 1
    Timeout : ScopeCheckResult # 2
    NoUserInput : ScopeCheckResult # 3
    BackendError : ScopeCheckResult # 4
    UnexpectedError : ScopeCheckResult # 5
    InvalidArgument : ScopeCheckResult # 6
    ConsentDenied : ScopeCheckResult # 7


class ScreenInsets(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : ScreenInsets # 0
    DeviceSafeInsets : ScreenInsets # 1
    CoreUISafeInsets : ScreenInsets # 2
    TopbarSafeInsets : ScreenInsets # 3


class ScreenOrientation(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    LandscapeLeft : ScreenOrientation # 0
    LandscapeRight : ScreenOrientation # 1
    LandscapeSensor : ScreenOrientation # 2
    Portrait : ScreenOrientation # 3
    Sensor : ScreenOrientation # 4


class ScrollBarInset(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : ScrollBarInset # 0
    ScrollBar : ScrollBarInset # 1
    Always : ScrollBarInset # 2


class ScrollingDirection(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    X : ScrollingDirection # 1
    Y : ScrollingDirection # 2
    XY : ScrollingDirection # 4


class SecurityCapability(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    RunClientScript : SecurityCapability # 0
    RunServerScript : SecurityCapability # 1
    AccessOutsideWrite : SecurityCapability # 2
    AssetRequire : SecurityCapability # 3
    LoadString : SecurityCapability # 4
    ScriptGlobals : SecurityCapability # 5
    CreateInstances : SecurityCapability # 6
    Basic : SecurityCapability # 7
    Audio : SecurityCapability # 8
    DataStore : SecurityCapability # 9
    Network : SecurityCapability # 10
    Physics : SecurityCapability # 11
    UI : SecurityCapability # 12
    CSG : SecurityCapability # 13
    Chat : SecurityCapability # 14
    Animation : SecurityCapability # 15
    Avatar : SecurityCapability # 16
    Input : SecurityCapability # 17
    Environment : SecurityCapability # 18
    RemoteEvent : SecurityCapability # 19
    LegacySound : SecurityCapability # 20
    Players : SecurityCapability # 21
    CapabilityControl : SecurityCapability # 22


class SelectionBehavior(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Escape : SelectionBehavior # 0
    Stop : SelectionBehavior # 1


class SelectionRenderMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Outlines : SelectionRenderMode # 0
    BoundingBoxes : SelectionRenderMode # 1
    Both : SelectionRenderMode # 2


class SelfViewPosition(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    LastPosition : SelfViewPosition # 0
    TopLeft : SelfViewPosition # 1
    TopRight : SelfViewPosition # 2
    BottomLeft : SelfViewPosition # 3
    BottomRight : SelfViewPosition # 4


class SensorMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Floor : SensorMode # 0
    Ladder : SensorMode # 1


class SensorUpdateType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    OnRead : SensorUpdateType # 0
    Manual : SensorUpdateType # 1


class ServerLiveEditingMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Uninitialized : ServerLiveEditingMode # 0
    Enabled : ServerLiveEditingMode # 1
    Disabled : ServerLiveEditingMode # 2


class ServiceVisibility(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Always : ServiceVisibility # 0
    Off : ServiceVisibility # 1
    WithChildren : ServiceVisibility # 2


class Severity(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Error : Severity # 1
    Warning : Severity # 2
    Information : Severity # 3
    Hint : Severity # 4


class ShowAdResult(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    ShowCompleted : ShowAdResult # 1
    AdNotReady : ShowAdResult # 2
    AdAlreadyShowing : ShowAdResult # 3
    InternalError : ShowAdResult # 4
    ShowInterrupted : ShowAdResult # 5
    InsufficientMemory : ShowAdResult # 6


class SignalBehavior(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : SignalBehavior # 0
    Immediate : SignalBehavior # 1
    Deferred : SignalBehavior # 2
    AncestryDeferred : SignalBehavior # 3


class SizeConstraint(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    RelativeXY : SizeConstraint # 0
    RelativeXX : SizeConstraint # 1
    RelativeYY : SizeConstraint # 2


class SolverConvergenceMetricType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    IterationBased : SolverConvergenceMetricType # 0
    AlgorithmAgnostic : SolverConvergenceMetricType # 1


class SolverConvergenceVisualizationMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Disabled : SolverConvergenceVisualizationMode # 0
    PerIsland : SolverConvergenceVisualizationMode # 1
    PerEdge : SolverConvergenceVisualizationMode # 2


class SortDirection(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Ascending : SortDirection # 0
    Descending : SortDirection # 1


class SortOrder(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Name : SortOrder # 0
    Custom : SortOrder # 1
    LayoutOrder : SortOrder # 2


class SpecialKey(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Insert : SpecialKey # 0
    Home : SpecialKey # 1
    End : SpecialKey # 2
    PageUp : SpecialKey # 3
    PageDown : SpecialKey # 4
    ChatHotkey : SpecialKey # 5


class StartCorner(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    TopLeft : StartCorner # 0
    TopRight : StartCorner # 1
    BottomLeft : StartCorner # 2
    BottomRight : StartCorner # 3


class StateObjectFieldType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Boolean : StateObjectFieldType # 0
    CFrame : StateObjectFieldType # 1
    Color3 : StateObjectFieldType # 2
    Float : StateObjectFieldType # 3
    Instance : StateObjectFieldType # 4
    Random : StateObjectFieldType # 5
    Vector2 : StateObjectFieldType # 6
    Vector3 : StateObjectFieldType # 7
    INVALID : StateObjectFieldType # 8


class Status(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Poison : Status # 0
    Confusion : Status # 1


class StreamingIntegrityMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : StreamingIntegrityMode # 0
    Disabled : StreamingIntegrityMode # 1
    MinimumRadiusPause : StreamingIntegrityMode # 2
    PauseOutsideLoadedArea : StreamingIntegrityMode # 3


class StreamingPauseMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : StreamingPauseMode # 0
    Disabled : StreamingPauseMode # 1
    ClientPhysicsPause : StreamingPauseMode # 2


class StreamOutBehavior(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : StreamOutBehavior # 0
    LowMemory : StreamOutBehavior # 1
    Opportunistic : StreamOutBehavior # 2


class StudioCloseMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : StudioCloseMode # 0
    CloseStudio : StudioCloseMode # 1
    CloseDoc : StudioCloseMode # 2
    LogOut : StudioCloseMode # 3


class StudioDataModelType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Edit : StudioDataModelType # 0
    PlayClient : StudioDataModelType # 1
    PlayServer : StudioDataModelType # 2
    Standalone : StudioDataModelType # 3
    None_ : StudioDataModelType # 4


class StudioPlaceUpdateFailureReason(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Other : StudioPlaceUpdateFailureReason # 0
    TeamCreateConflict : StudioPlaceUpdateFailureReason # 1


class StudioScriptEditorColorCategories(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : StudioScriptEditorColorCategories # 0
    Operator : StudioScriptEditorColorCategories # 1
    Number : StudioScriptEditorColorCategories # 2
    String : StudioScriptEditorColorCategories # 3
    Comment : StudioScriptEditorColorCategories # 4
    Keyword : StudioScriptEditorColorCategories # 5
    Builtin : StudioScriptEditorColorCategories # 6
    Method : StudioScriptEditorColorCategories # 7
    Property : StudioScriptEditorColorCategories # 8
    Nil : StudioScriptEditorColorCategories # 9
    Bool : StudioScriptEditorColorCategories # 10
    Function : StudioScriptEditorColorCategories # 11
    Local : StudioScriptEditorColorCategories # 12
    Self : StudioScriptEditorColorCategories # 13
    LuauKeyword : StudioScriptEditorColorCategories # 14
    FunctionName : StudioScriptEditorColorCategories # 15
    TODO : StudioScriptEditorColorCategories # 16
    Background : StudioScriptEditorColorCategories # 17
    SelectionText : StudioScriptEditorColorCategories # 18
    SelectionBackground : StudioScriptEditorColorCategories # 19
    FindSelectionBackground : StudioScriptEditorColorCategories # 20
    MatchingWordBackground : StudioScriptEditorColorCategories # 21
    Warning : StudioScriptEditorColorCategories # 22
    Error : StudioScriptEditorColorCategories # 23
    Info : StudioScriptEditorColorCategories # 24
    Hint : StudioScriptEditorColorCategories # 25
    Whitespace : StudioScriptEditorColorCategories # 26
    ActiveLine : StudioScriptEditorColorCategories # 27
    DebuggerCurrentLine : StudioScriptEditorColorCategories # 28
    DebuggerErrorLine : StudioScriptEditorColorCategories # 29
    Ruler : StudioScriptEditorColorCategories # 30
    Bracket : StudioScriptEditorColorCategories # 31
    Type : StudioScriptEditorColorCategories # 32
    MenuPrimaryText : StudioScriptEditorColorCategories # 33
    MenuSecondaryText : StudioScriptEditorColorCategories # 34
    MenuSelectedText : StudioScriptEditorColorCategories # 35
    MenuBackground : StudioScriptEditorColorCategories # 36
    MenuSelectedBackground : StudioScriptEditorColorCategories # 37
    MenuScrollbarBackground : StudioScriptEditorColorCategories # 38
    MenuScrollbarHandle : StudioScriptEditorColorCategories # 39
    MenuBorder : StudioScriptEditorColorCategories # 40
    DocViewCodeBackground : StudioScriptEditorColorCategories # 41
    AICOOverlayText : StudioScriptEditorColorCategories # 42
    AICOOverlayButtonBackground : StudioScriptEditorColorCategories # 43
    AICOOverlayButtonBackgroundHover : StudioScriptEditorColorCategories # 44
    AICOOverlayButtonBackgroundPressed : StudioScriptEditorColorCategories # 45
    IndentationRuler : StudioScriptEditorColorCategories # 46


class StudioScriptEditorColorPresets(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    RobloxDefault : StudioScriptEditorColorPresets # 0
    Extra1 : StudioScriptEditorColorPresets # 1
    Extra2 : StudioScriptEditorColorPresets # 2
    Custom : StudioScriptEditorColorPresets # 3


class StudioStyleGuideColor(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    MainBackground : StudioStyleGuideColor # 0
    Titlebar : StudioStyleGuideColor # 1
    Dropdown : StudioStyleGuideColor # 2
    Tooltip : StudioStyleGuideColor # 3
    Notification : StudioStyleGuideColor # 4
    ScrollBar : StudioStyleGuideColor # 5
    ScrollBarBackground : StudioStyleGuideColor # 6
    TabBar : StudioStyleGuideColor # 7
    Tab : StudioStyleGuideColor # 8
    FilterButtonDefault : StudioStyleGuideColor # 9
    FilterButtonHover : StudioStyleGuideColor # 10
    FilterButtonChecked : StudioStyleGuideColor # 11
    FilterButtonAccent : StudioStyleGuideColor # 12
    FilterButtonBorder : StudioStyleGuideColor # 13
    FilterButtonBorderAlt : StudioStyleGuideColor # 14
    RibbonTab : StudioStyleGuideColor # 15
    RibbonTabTopBar : StudioStyleGuideColor # 16
    Button : StudioStyleGuideColor # 17
    MainButton : StudioStyleGuideColor # 18
    RibbonButton : StudioStyleGuideColor # 19
    ViewPortBackground : StudioStyleGuideColor # 20
    InputFieldBackground : StudioStyleGuideColor # 21
    Item : StudioStyleGuideColor # 22
    TableItem : StudioStyleGuideColor # 23
    CategoryItem : StudioStyleGuideColor # 24
    GameSettingsTableItem : StudioStyleGuideColor # 25
    GameSettingsTooltip : StudioStyleGuideColor # 26
    EmulatorBar : StudioStyleGuideColor # 27
    EmulatorDropDown : StudioStyleGuideColor # 28
    ColorPickerFrame : StudioStyleGuideColor # 29
    CurrentMarker : StudioStyleGuideColor # 30
    Border : StudioStyleGuideColor # 31
    DropShadow : StudioStyleGuideColor # 32
    Shadow : StudioStyleGuideColor # 33
    Light : StudioStyleGuideColor # 34
    Dark : StudioStyleGuideColor # 35
    Mid : StudioStyleGuideColor # 36
    MainText : StudioStyleGuideColor # 37
    SubText : StudioStyleGuideColor # 38
    TitlebarText : StudioStyleGuideColor # 39
    BrightText : StudioStyleGuideColor # 40
    DimmedText : StudioStyleGuideColor # 41
    LinkText : StudioStyleGuideColor # 42
    WarningText : StudioStyleGuideColor # 43
    ErrorText : StudioStyleGuideColor # 44
    InfoText : StudioStyleGuideColor # 45
    SensitiveText : StudioStyleGuideColor # 46
    ScriptSideWidget : StudioStyleGuideColor # 47
    ScriptBackground : StudioStyleGuideColor # 48
    ScriptText : StudioStyleGuideColor # 49
    ScriptSelectionText : StudioStyleGuideColor # 50
    ScriptSelectionBackground : StudioStyleGuideColor # 51
    ScriptFindSelectionBackground : StudioStyleGuideColor # 52
    ScriptMatchingWordSelectionBackground : StudioStyleGuideColor # 53
    ScriptOperator : StudioStyleGuideColor # 54
    ScriptNumber : StudioStyleGuideColor # 55
    ScriptString : StudioStyleGuideColor # 56
    ScriptComment : StudioStyleGuideColor # 57
    ScriptKeyword : StudioStyleGuideColor # 58
    ScriptBuiltInFunction : StudioStyleGuideColor # 59
    ScriptWarning : StudioStyleGuideColor # 60
    ScriptError : StudioStyleGuideColor # 61
    ScriptInformation : StudioStyleGuideColor # 62
    ScriptHint : StudioStyleGuideColor # 63
    ScriptWhitespace : StudioStyleGuideColor # 64
    ScriptRuler : StudioStyleGuideColor # 65
    DocViewCodeBackground : StudioStyleGuideColor # 66
    DebuggerCurrentLine : StudioStyleGuideColor # 67
    DebuggerErrorLine : StudioStyleGuideColor # 68
    DiffFilePathText : StudioStyleGuideColor # 69
    DiffTextHunkInfo : StudioStyleGuideColor # 70
    DiffTextNoChange : StudioStyleGuideColor # 71
    DiffTextAddition : StudioStyleGuideColor # 72
    DiffTextDeletion : StudioStyleGuideColor # 73
    DiffTextSeparatorBackground : StudioStyleGuideColor # 74
    DiffTextNoChangeBackground : StudioStyleGuideColor # 75
    DiffTextAdditionBackground : StudioStyleGuideColor # 76
    DiffTextDeletionBackground : StudioStyleGuideColor # 77
    DiffLineNum : StudioStyleGuideColor # 78
    DiffLineNumSeparatorBackground : StudioStyleGuideColor # 79
    DiffLineNumNoChangeBackground : StudioStyleGuideColor # 80
    DiffLineNumAdditionBackground : StudioStyleGuideColor # 81
    DiffLineNumDeletionBackground : StudioStyleGuideColor # 82
    DiffFilePathBackground : StudioStyleGuideColor # 83
    DiffFilePathBorder : StudioStyleGuideColor # 84
    ChatIncomingBgColor : StudioStyleGuideColor # 85
    ChatIncomingTextColor : StudioStyleGuideColor # 86
    ChatOutgoingBgColor : StudioStyleGuideColor # 87
    ChatOutgoingTextColor : StudioStyleGuideColor # 88
    ChatModeratedMessageColor : StudioStyleGuideColor # 89
    Separator : StudioStyleGuideColor # 90
    ButtonBorder : StudioStyleGuideColor # 91
    ButtonText : StudioStyleGuideColor # 92
    InputFieldBorder : StudioStyleGuideColor # 93
    CheckedFieldBackground : StudioStyleGuideColor # 94
    CheckedFieldBorder : StudioStyleGuideColor # 95
    CheckedFieldIndicator : StudioStyleGuideColor # 96
    HeaderSection : StudioStyleGuideColor # 97
    Midlight : StudioStyleGuideColor # 98
    StatusBar : StudioStyleGuideColor # 99
    DialogButton : StudioStyleGuideColor # 100
    DialogButtonText : StudioStyleGuideColor # 101
    DialogButtonBorder : StudioStyleGuideColor # 102
    DialogMainButton : StudioStyleGuideColor # 103
    DialogMainButtonText : StudioStyleGuideColor # 104
    InfoBarWarningBackground : StudioStyleGuideColor # 105
    InfoBarWarningText : StudioStyleGuideColor # 106
    ScriptEditorCurrentLine : StudioStyleGuideColor # 107
    ScriptMethod : StudioStyleGuideColor # 108
    ScriptProperty : StudioStyleGuideColor # 109
    ScriptNil : StudioStyleGuideColor # 110
    ScriptBool : StudioStyleGuideColor # 111
    ScriptFunction : StudioStyleGuideColor # 112
    ScriptLocal : StudioStyleGuideColor # 113
    ScriptSelf : StudioStyleGuideColor # 114
    ScriptLuauKeyword : StudioStyleGuideColor # 115
    ScriptFunctionName : StudioStyleGuideColor # 116
    ScriptTodo : StudioStyleGuideColor # 117
    ScriptBracket : StudioStyleGuideColor # 118
    AttributeCog : StudioStyleGuideColor # 119
    AICOOverlayText : StudioStyleGuideColor # 128
    AICOOverlayButtonBackground : StudioStyleGuideColor # 129
    AICOOverlayButtonBackgroundHover : StudioStyleGuideColor # 130
    AICOOverlayButtonBackgroundPressed : StudioStyleGuideColor # 131
    OnboardingCover : StudioStyleGuideColor # 132
    OnboardingHighlight : StudioStyleGuideColor # 133
    OnboardingShadow : StudioStyleGuideColor # 134
    BreakpointMarker : StudioStyleGuideColor # 136
    DiffLineNumHover : StudioStyleGuideColor # 137
    DiffLineNumSeparatorBackgroundHover : StudioStyleGuideColor # 138


class StudioStyleGuideModifier(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : StudioStyleGuideModifier # 0
    Selected : StudioStyleGuideModifier # 1
    Pressed : StudioStyleGuideModifier # 2
    Disabled : StudioStyleGuideModifier # 3
    Hover : StudioStyleGuideModifier # 4


class Style(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Alternating_Supports : Style # 0
    AlternatingSupports : Style # 0
    BridgeStyleSupports : Style # 1
    Bridge_Style_Supports : Style # 1
    NoSupports : Style # 2
    No_Supports : Style # 2


class SubscriptionExpirationReason(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    ProductInactive : SubscriptionExpirationReason # 0
    ProductDeleted : SubscriptionExpirationReason # 1
    SubscriberCancelled : SubscriptionExpirationReason # 2
    SubscriberRefunded : SubscriptionExpirationReason # 3
    Lapsed : SubscriptionExpirationReason # 4


class SubscriptionPaymentStatus(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Paid : SubscriptionPaymentStatus # 0
    Refunded : SubscriptionPaymentStatus # 1


class SubscriptionPeriod(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Month : SubscriptionPeriod # 0


class SubscriptionState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    NeverSubscribed : SubscriptionState # 0
    SubscribedWillRenew : SubscriptionState # 1
    SubscribedWillNotRenew : SubscriptionState # 2
    SubscribedRenewalPaymentPending : SubscriptionState # 3
    Expired : SubscriptionState # 4


class SurfaceConstraint(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : SurfaceConstraint # 0
    Hinge : SurfaceConstraint # 1
    SteppingMotor : SurfaceConstraint # 2
    Motor : SurfaceConstraint # 3


class SurfaceGuiShape(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Flat : SurfaceGuiShape # 0
    CurvedHorizontally : SurfaceGuiShape # 1


class SurfaceGuiSizingMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    FixedSize : SurfaceGuiSizingMode # 0
    PixelsPerStud : SurfaceGuiSizingMode # 1


class SurfaceType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Smooth : SurfaceType # 0
    _Unjoinable : SurfaceType # 0
    Spawn : SurfaceType # 0
    Bumps : SurfaceType # 1
    Glue : SurfaceType # 1
    Weld : SurfaceType # 2
    Studs : SurfaceType # 3
    Inlet : SurfaceType # 4
    Universal : SurfaceType # 5
    Hinge : SurfaceType # 6
    Motor : SurfaceType # 7
    SteppingMotor : SurfaceType # 8
    SmoothNoOutlines : SurfaceType # 10


class SwipeDirection(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Right : SwipeDirection # 0
    Left : SwipeDirection # 1
    Up : SwipeDirection # 2
    Down : SwipeDirection # 3
    None_ : SwipeDirection # 4


class SystemThemeValue(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    error : SystemThemeValue # 0
    light : SystemThemeValue # 1
    dark : SystemThemeValue # 2
    systemLight : SystemThemeValue # 3
    systemDark : SystemThemeValue # 4


class TableMajorAxis(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    RowMajor : TableMajorAxis # 0
    ColumnMajor : TableMajorAxis # 1


class TeamCreateErrorState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    PlaceSizeTooLarge : TeamCreateErrorState # 0
    PlaceSizeApproachingLimit : TeamCreateErrorState # 1
    NoError : TeamCreateErrorState # 2


class Technology(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Legacy : Technology # 0
    Voxel : Technology # 1
    Compatibility : Technology # 2
    ShadowMap : Technology # 3
    Future : Technology # 4
    Unified : Technology # 5


class TeleportMethod(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    TeleportToSpawnByName : TeleportMethod # 0
    TeleportToPlaceInstance : TeleportMethod # 1
    TeleportToPrivateServer : TeleportMethod # 2
    TeleportPartyAsync : TeleportMethod # 3
    TeleportToVIPServer : TeleportMethod # 4
    TeleportToInstanceBack : TeleportMethod # 5
    TeleportUnknown : TeleportMethod # 6


class TeleportResult(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Success : TeleportResult # 0
    Failure : TeleportResult # 1
    GameNotFound : TeleportResult # 2
    GameEnded : TeleportResult # 3
    GameFull : TeleportResult # 4
    Unauthorized : TeleportResult # 5
    Flooded : TeleportResult # 6
    IsTeleporting : TeleportResult # 7


class TeleportState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    RequestedFromServer : TeleportState # 0
    Started : TeleportState # 1
    WaitingForServer : TeleportState # 2
    Failed : TeleportState # 3
    InProgress : TeleportState # 4


class TeleportType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    ToPlace : TeleportType # 0
    ToInstance : TeleportType # 1
    ToReservedServer : TeleportType # 2
    ToVIPServer : TeleportType # 3
    ToInstanceBack : TeleportType # 4


class TerrainAcquisitionMethod(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : TerrainAcquisitionMethod # 0
    Legacy : TerrainAcquisitionMethod # 1
    Template : TerrainAcquisitionMethod # 2
    Generate : TerrainAcquisitionMethod # 3
    Import : TerrainAcquisitionMethod # 4
    Convert : TerrainAcquisitionMethod # 5
    EditAddTool : TerrainAcquisitionMethod # 6
    EditSeaLevelTool : TerrainAcquisitionMethod # 7
    EditReplaceTool : TerrainAcquisitionMethod # 8
    RegionFillTool : TerrainAcquisitionMethod # 9
    RegionPasteTool : TerrainAcquisitionMethod # 10
    Other : TerrainAcquisitionMethod # 11


class TerrainFace(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Top : TerrainFace # 0
    Side : TerrainFace # 1
    Bottom : TerrainFace # 2


class TextChatMessageStatus(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Unknown : TextChatMessageStatus # 1
    Success : TextChatMessageStatus # 2
    Sending : TextChatMessageStatus # 3
    TextFilterFailed : TextChatMessageStatus # 4
    Floodchecked : TextChatMessageStatus # 5
    InvalidPrivacySettings : TextChatMessageStatus # 6
    InvalidTextChannelPermissions : TextChatMessageStatus # 7
    MessageTooLong : TextChatMessageStatus # 8
    ModerationTimeout : TextChatMessageStatus # 9


class TextDirection(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Auto : TextDirection # 0
    LeftToRight : TextDirection # 1
    RightToLeft : TextDirection # 2


class TextFilterContext(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    PublicChat : TextFilterContext # 1
    PrivateChat : TextFilterContext # 2


class TextInputType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : TextInputType # 0
    NoSuggestions : TextInputType # 1
    Number : TextInputType # 2
    Email : TextInputType # 3
    Phone : TextInputType # 4
    Password : TextInputType # 5
    PasswordShown : TextInputType # 6
    Username : TextInputType # 7
    OneTimePassword : TextInputType # 8


class TextTruncate(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : TextTruncate # 0
    AtEnd : TextTruncate # 1
    SplitWord : TextTruncate # 2


class TextureMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Stretch : TextureMode # 0
    Wrap : TextureMode # 1
    Static : TextureMode # 2


class TextureQueryType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    NonHumanoid : TextureQueryType # 0
    NonHumanoidOrphaned : TextureQueryType # 1
    Humanoid : TextureQueryType # 2
    HumanoidOrphaned : TextureQueryType # 3


class TextXAlignment(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Left : TextXAlignment # 0
    Right : TextXAlignment # 1
    Center : TextXAlignment # 2


class TextYAlignment(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Top : TextYAlignment # 0
    Center : TextYAlignment # 1
    Bottom : TextYAlignment # 2


class ThreadPoolConfig(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    PartialThread : ThreadPoolConfig # 0
    Auto : ThreadPoolConfig # 0
    Threads1 : ThreadPoolConfig # 1
    Threads2 : ThreadPoolConfig # 2
    Threads3 : ThreadPoolConfig # 3
    Threads4 : ThreadPoolConfig # 4
    Threads8 : ThreadPoolConfig # 8
    Threads16 : ThreadPoolConfig # 16
    PerCore1 : ThreadPoolConfig # 101
    PerCore2 : ThreadPoolConfig # 102
    PerCore3 : ThreadPoolConfig # 103
    PerCore4 : ThreadPoolConfig # 104


class ThrottlingPriority(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : ThrottlingPriority # 0
    ElevatedOnServer : ThrottlingPriority # 1
    Extreme : ThrottlingPriority # 2


class ThumbnailSize(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Size48x48 : ThumbnailSize # 0
    Size180x180 : ThumbnailSize # 1
    Size420x420 : ThumbnailSize # 2
    Size60x60 : ThumbnailSize # 3
    Size100x100 : ThumbnailSize # 4
    Size150x150 : ThumbnailSize # 5
    Size352x352 : ThumbnailSize # 6


class ThumbnailType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    HeadShot : ThumbnailType # 0
    AvatarBust : ThumbnailType # 1
    AvatarThumbnail : ThumbnailType # 2


class TickCountSampleMethod(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Fast : TickCountSampleMethod # 0
    Benchmark : TickCountSampleMethod # 1
    Precise : TickCountSampleMethod # 2


class TonemapperPreset(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : TonemapperPreset # 0
    Retro : TonemapperPreset # 1


class TopBottom(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Top : TopBottom # 0
    Center : TopBottom # 1
    Bottom : TopBottom # 2


class TouchCameraMovementMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : TouchCameraMovementMode # 0
    Classic : TouchCameraMovementMode # 1
    Follow : TouchCameraMovementMode # 2
    Orbital : TouchCameraMovementMode # 3


class TouchMovementMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : TouchMovementMode # 0
    Thumbstick : TouchMovementMode # 1
    DPad : TouchMovementMode # 2
    Thumbpad : TouchMovementMode # 3
    ClickToMove : TouchMovementMode # 4
    DynamicThumbstick : TouchMovementMode # 5


class TrackerError(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Ok : TrackerError # 0
    NoService : TrackerError # 1
    InitFailed : TrackerError # 2
    NoVideo : TrackerError # 3
    VideoError : TrackerError # 4
    VideoNoPermission : TrackerError # 5
    VideoUnsupported : TrackerError # 6
    NoAudio : TrackerError # 7
    AudioError : TrackerError # 8
    AudioNoPermission : TrackerError # 9
    UnsupportedDevice : TrackerError # 10


class TrackerExtrapolationFlagMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    ForceDisabled : TrackerExtrapolationFlagMode # 0
    ExtrapolateFacsAndPose : TrackerExtrapolationFlagMode # 1
    ExtrapolateFacsOnly : TrackerExtrapolationFlagMode # 2
    Auto : TrackerExtrapolationFlagMode # 3


class TrackerFaceTrackingStatus(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    FaceTrackingSuccess : TrackerFaceTrackingStatus # 0
    FaceTrackingNoFaceFound : TrackerFaceTrackingStatus # 1
    FaceTrackingUnknown : TrackerFaceTrackingStatus # 2
    FaceTrackingLost : TrackerFaceTrackingStatus # 3
    FaceTrackingHasTrackingError : TrackerFaceTrackingStatus # 4
    FaceTrackingIsOccluded : TrackerFaceTrackingStatus # 5
    FaceTrackingUninitialized : TrackerFaceTrackingStatus # 6


class TrackerLodFlagMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    ForceFalse : TrackerLodFlagMode # 0
    ForceTrue : TrackerLodFlagMode # 1
    Auto : TrackerLodFlagMode # 2


class TrackerLodValueMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Force0 : TrackerLodValueMode # 0
    Force1 : TrackerLodValueMode # 1
    Auto : TrackerLodValueMode # 2


class TrackerMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : TrackerMode # 0
    Audio : TrackerMode # 1
    Video : TrackerMode # 2
    AudioVideo : TrackerMode # 3


class TrackerPromptEvent(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    LODCameraRecommendDisable : TrackerPromptEvent # 0


class TrackerType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : TrackerType # 0
    Face : TrackerType # 1
    UpperBody : TrackerType # 2


class TriStateBoolean(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Unknown : TriStateBoolean # 0
    True : TriStateBoolean # 1
    False : TriStateBoolean # 2


class TweenStatus(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Canceled : TweenStatus # 0
    Completed : TweenStatus # 1


class UICaptureMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    All : UICaptureMode # 0
    None_ : UICaptureMode # 1


class UIDragDetectorBoundingBehavior(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Automatic : UIDragDetectorBoundingBehavior # 0
    EntireObject : UIDragDetectorBoundingBehavior # 1
    HitPoint : UIDragDetectorBoundingBehavior # 2


class UIDragDetectorDragRelativity(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Absolute : UIDragDetectorDragRelativity # 0
    Relative : UIDragDetectorDragRelativity # 1


class UIDragDetectorDragSpace(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Parent : UIDragDetectorDragSpace # 0
    LayerCollector : UIDragDetectorDragSpace # 1
    Reference : UIDragDetectorDragSpace # 2


class UIDragDetectorDragStyle(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    TranslatePlane : UIDragDetectorDragStyle # 0
    TranslateLine : UIDragDetectorDragStyle # 1
    Rotate : UIDragDetectorDragStyle # 2
    Scriptable : UIDragDetectorDragStyle # 3


class UIDragDetectorResponseStyle(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Offset : UIDragDetectorResponseStyle # 0
    Scale : UIDragDetectorResponseStyle # 1
    CustomOffset : UIDragDetectorResponseStyle # 2
    CustomScale : UIDragDetectorResponseStyle # 3


class UIDragSpeedAxisMapping(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    XY : UIDragSpeedAxisMapping # 0
    XX : UIDragSpeedAxisMapping # 1
    YY : UIDragSpeedAxisMapping # 2


class UIFlexAlignment(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : UIFlexAlignment # 0
    Fill : UIFlexAlignment # 1
    SpaceAround : UIFlexAlignment # 2
    SpaceBetween : UIFlexAlignment # 3
    SpaceEvenly : UIFlexAlignment # 4


class UIFlexMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : UIFlexMode # 0
    Grow : UIFlexMode # 1
    Shrink : UIFlexMode # 2
    Fill : UIFlexMode # 3
    Custom : UIFlexMode # 4


class UiMessageType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    UiMessageError : UiMessageType # 0
    UiMessageInfo : UiMessageType # 1


class UITheme(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Light : UITheme # 0
    Dark : UITheme # 1


class UsageContext(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : UsageContext # 0
    Preview : UsageContext # 1


class UserCFrame(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Head : UserCFrame # 0
    LeftHand : UserCFrame # 1
    RightHand : UserCFrame # 2
    Floor : UserCFrame # 3


class UserInputState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Begin : UserInputState # 0
    Change : UserInputState # 1
    End : UserInputState # 2
    Cancel : UserInputState # 3
    None_ : UserInputState # 4


class UserInputType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    MouseButton1 : UserInputType # 0
    MouseButton2 : UserInputType # 1
    MouseButton3 : UserInputType # 2
    MouseWheel : UserInputType # 3
    MouseMovement : UserInputType # 4
    Touch : UserInputType # 7
    Keyboard : UserInputType # 8
    Focus : UserInputType # 9
    Accelerometer : UserInputType # 10
    Gyro : UserInputType # 11
    Gamepad1 : UserInputType # 12
    Gamepad2 : UserInputType # 13
    Gamepad3 : UserInputType # 14
    Gamepad4 : UserInputType # 15
    Gamepad5 : UserInputType # 16
    Gamepad6 : UserInputType # 17
    Gamepad7 : UserInputType # 18
    Gamepad8 : UserInputType # 19
    TextInput : UserInputType # 20
    InputMethod : UserInputType # 21
    None_ : UserInputType # 22


class VelocityConstraintMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Line : VelocityConstraintMode # 0
    Plane : VelocityConstraintMode # 1
    Vector : VelocityConstraintMode # 2


class VerticalAlignment(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Center : VerticalAlignment # 0
    Top : VerticalAlignment # 1
    Bottom : VerticalAlignment # 2


class VerticalScrollBarPosition(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Right : VerticalScrollBarPosition # 0
    Left : VerticalScrollBarPosition # 1


class VibrationMotor(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Large : VibrationMotor # 0
    Small : VibrationMotor # 1
    LeftTrigger : VibrationMotor # 2
    RightTrigger : VibrationMotor # 3
    LeftHand : VibrationMotor # 4
    RightHand : VibrationMotor # 5


class VideoCaptureResult(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Success : VideoCaptureResult # 0
    OtherError : VideoCaptureResult # 1
    ScreenSizeChanged : VideoCaptureResult # 2
    TimeLimitReached : VideoCaptureResult # 3


class VideoCaptureStartedResult(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Success : VideoCaptureStartedResult # 0
    OtherError : VideoCaptureStartedResult # 1
    CapturingAlready : VideoCaptureStartedResult # 2
    NoDeviceSupport : VideoCaptureStartedResult # 3
    NoSpaceOnDevice : VideoCaptureStartedResult # 4


class VideoDeviceCaptureQuality(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : VideoDeviceCaptureQuality # 0
    Low : VideoDeviceCaptureQuality # 1
    Medium : VideoDeviceCaptureQuality # 2
    High : VideoDeviceCaptureQuality # 3


class VideoError(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Ok : VideoError # 0
    Eof : VideoError # 1
    EAgain : VideoError # 2
    BadParameter : VideoError # 3
    AllocFailed : VideoError # 4
    CodecInitFailed : VideoError # 5
    CodecCloseFailed : VideoError # 6
    DecodeFailed : VideoError # 7
    ParsingFailed : VideoError # 8
    Unsupported : VideoError # 9
    Generic : VideoError # 10
    DownloadFailed : VideoError # 11
    StreamNotFound : VideoError # 12
    EncodeFailed : VideoError # 13
    CreateFailed : VideoError # 14
    NoPermission : VideoError # 15
    NoService : VideoError # 16
    ReleaseFailed : VideoError # 17
    Unknown : VideoError # 18


class ViewMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : ViewMode # 0
    GeometryComplexity : ViewMode # 1
    Transparent : ViewMode # 2
    Decal : ViewMode # 3


class VirtualCursorMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Default : VirtualCursorMode # 0
    Disabled : VirtualCursorMode # 1
    Enabled : VirtualCursorMode # 2


class VirtualInputMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : VirtualInputMode # 0
    Recording : VirtualInputMode # 1
    Playing : VirtualInputMode # 2


class VoiceChatDistanceAttenuationType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Inverse : VoiceChatDistanceAttenuationType # 0
    Legacy : VoiceChatDistanceAttenuationType # 1


class VoiceChatState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Idle : VoiceChatState # 0
    Joining : VoiceChatState # 1
    JoiningRetry : VoiceChatState # 2
    Joined : VoiceChatState # 3
    Leaving : VoiceChatState # 4
    Ended : VoiceChatState # 5
    Failed : VoiceChatState # 6


class VoiceControlPath(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Publish : VoiceControlPath # 0
    Subscribe : VoiceControlPath # 1
    Join : VoiceControlPath # 2


class VolumetricAudio(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Disabled : VolumetricAudio # 0
    Automatic : VolumetricAudio # 1
    Enabled : VolumetricAudio # 2


class VRComfortSetting(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Comfort : VRComfortSetting # 0
    Normal : VRComfortSetting # 1
    Expert : VRComfortSetting # 2
    Custom : VRComfortSetting # 3


class VRControllerModelMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Disabled : VRControllerModelMode # 0
    Transparent : VRControllerModelMode # 1


class VRDeviceType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Unknown : VRDeviceType # 0
    OculusRift : VRDeviceType # 1
    HTCVive : VRDeviceType # 2
    ValveIndex : VRDeviceType # 3
    OculusQuest : VRDeviceType # 4


class VRLaserPointerMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Disabled : VRLaserPointerMode # 0
    Pointer : VRLaserPointerMode # 1
    DualPointer : VRLaserPointerMode # 2


class VRSafetyBubbleMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    NoOne : VRSafetyBubbleMode # 0
    OnlyFriends : VRSafetyBubbleMode # 1
    Anyone : VRSafetyBubbleMode # 2


class VRScaling(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    World : VRScaling # 0
    Off : VRScaling # 1


class VRSessionState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Undefined : VRSessionState # 0
    Idle : VRSessionState # 1
    Visible : VRSessionState # 2
    Focused : VRSessionState # 3
    Stopping : VRSessionState # 4


class VRTouchpad(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Left : VRTouchpad # 0
    Right : VRTouchpad # 1


class VRTouchpadMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Touch : VRTouchpadMode # 0
    VirtualThumbstick : VRTouchpadMode # 1
    ABXY : VRTouchpadMode # 2


class WaterDirection(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    NegX : WaterDirection # 0
    X : WaterDirection # 1
    NegY : WaterDirection # 2
    Y : WaterDirection # 3
    NegZ : WaterDirection # 4
    Z : WaterDirection # 5


class WaterForce(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : WaterForce # 0
    Small : WaterForce # 1
    Medium : WaterForce # 2
    Strong : WaterForce # 3
    Max : WaterForce # 4


class WebSocketState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Connecting : WebSocketState # 0
    Open : WebSocketState # 1
    Closing : WebSocketState # 2
    Closed : WebSocketState # 3


class WeldConstraintPreserve(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    All : WeldConstraintPreserve # 0
    None_ : WeldConstraintPreserve # 1
    Touching : WeldConstraintPreserve # 2


class WhisperChatPrivacyMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    AllUsers : WhisperChatPrivacyMode # 0
    NoOne : WhisperChatPrivacyMode # 1


class WrapLayerAutoSkin(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Disabled : WrapLayerAutoSkin # 0
    EnabledPreserve : WrapLayerAutoSkin # 1
    EnabledOverride : WrapLayerAutoSkin # 2


class WrapLayerDebugMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : WrapLayerDebugMode # 0
    BoundCage : WrapLayerDebugMode # 1
    LayerCage : WrapLayerDebugMode # 2
    BoundCageAndLinks : WrapLayerDebugMode # 3
    Reference : WrapLayerDebugMode # 4
    Rbf : WrapLayerDebugMode # 5
    OuterCage : WrapLayerDebugMode # 6
    ReferenceMeshAfterMorph : WrapLayerDebugMode # 7
    HSROuterDetail : WrapLayerDebugMode # 8
    HSROuter : WrapLayerDebugMode # 9
    HSRInner : WrapLayerDebugMode # 10
    HSRInnerReverse : WrapLayerDebugMode # 11
    LayerCageFittedToBase : WrapLayerDebugMode # 12
    LayerCageFittedToPrev : WrapLayerDebugMode # 13
    PreWrapDeformerOuterCage : WrapLayerDebugMode # 14


class WrapTargetDebugMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : WrapTargetDebugMode # 0
    TargetCageOriginal : WrapTargetDebugMode # 1
    TargetCageCompressed : WrapTargetDebugMode # 2
    TargetCageInterface : WrapTargetDebugMode # 3
    TargetLayerCageOriginal : WrapTargetDebugMode # 4
    TargetLayerCageCompressed : WrapTargetDebugMode # 5
    TargetLayerInterface : WrapTargetDebugMode # 6
    Rbf : WrapTargetDebugMode # 7
    OuterCageDetail : WrapTargetDebugMode # 8
    PreWrapDeformerCage : WrapTargetDebugMode # 9


class ZIndexBehavior(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Global : ZIndexBehavior # 0
    Sibling : ZIndexBehavior # 1

