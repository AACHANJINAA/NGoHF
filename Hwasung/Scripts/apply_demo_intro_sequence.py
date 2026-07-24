import unreal

MAP_PATH = "/Game/HwaseongForteressGate/Level/Demo.Demo"
SEQ_DIR = "/Game/HwaseongForteressGate/Cinematics"
SEQ_PATH = f"{SEQ_DIR}/LS_DEMO_Intro_Janganmun"
SEQ_NAME = "LS_DEMO_Intro_Janganmun"

INTRO_TEXT = "환영합니다! 이곳은 수원화성의 정문, 장안문입니다!"


def load_map():
    level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    if not level_subsystem.load_level(MAP_PATH):
        raise RuntimeError(f"Failed to load map: {MAP_PATH}")


def get_all_actors():
    return unreal.EditorLevelLibrary.get_all_level_actors()


def find_by_label(label):
    for actor in get_all_actors():
        if actor.get_actor_label() == label:
            return actor
    return None


def delete_if_exists(label):
    actor = find_by_label(label)
    if actor:
        unreal.EditorLevelLibrary.destroy_actor(actor)


def ensure_directory(path):
    if not unreal.EditorAssetLibrary.does_directory_exist(path):
        unreal.EditorAssetLibrary.make_directory(path)


def create_sequence():
    if unreal.EditorAssetLibrary.does_asset_exist(SEQ_PATH):
        unreal.EditorAssetLibrary.delete_asset(SEQ_PATH)

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    seq = asset_tools.create_asset(
        asset_name=SEQ_NAME,
        package_path=SEQ_DIR,
        asset_class=unreal.LevelSequence,
        factory=unreal.LevelSequenceFactoryNew(),
    )
    seq.set_display_rate(unreal.FrameRate(30, 1))
    seq.set_playback_start(0)
    seq.set_playback_end(120)
    return seq


def key_transform_section(section, start_frame, end_frame, start_values, end_values):
    channels = section.get_all_channels()
    if len(channels) < 9:
        raise RuntimeError(f"Expected at least 9 transform channels, got {len(channels)}")
    for idx in range(9):
        channels[idx].add_key(unreal.FrameNumber(start_frame), start_values[idx])
        channels[idx].add_key(unreal.FrameNumber(end_frame), end_values[idx])


def add_transform_track(binding, start_frame, end_frame, start_values, end_values):
    track = binding.add_track(unreal.MovieScene3DTransformTrack)
    section = track.add_section()
    section.set_range(start_frame, end_frame)
    key_transform_section(section, start_frame, end_frame, start_values, end_values)
    return track


def assign_basic_sphere(actor):
    sphere_mesh = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Sphere.Sphere")
    sm_component = actor.get_component_by_class(unreal.StaticMeshComponent)
    if sm_component and sphere_mesh:
        sm_component.set_static_mesh(sphere_mesh)
        actor.set_actor_scale3d(unreal.Vector(0.35, 0.35, 0.35))


def configure_text_actor(actor, text):
    component = actor.get_component_by_class(unreal.TextRenderComponent)
    if not component:
        return
    component.set_text(text)
    component.set_horizontal_alignment(unreal.HorizTextAligment.EHTA_CENTER)
    component.set_world_size(45.0)
    component.set_text_render_color(unreal.Color(255, 220, 220, 255))


load_map()
ensure_directory(SEQ_DIR)

for label in [
    "LSA_DEMO_Intro_Janganmun",
    "TXT_DEMO_IntroWelcome",
    "CHR_DEMO_IntroMascot",
    "CINE_DEMO_Intro_Janganmun",
]:
    delete_if_exists(label)

seq = create_sequence()
camera_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
    unreal.CineCameraActor,
    unreal.Vector(4200.0, -120.0, 2550.0),
    unreal.Rotator(-12.0, 178.0, 0.0),
)
camera_actor.set_actor_label("CINE_DEMO_Intro_Janganmun")
camera_binding = unreal.MovieSceneSequenceExtensions.add_possessable(seq, camera_actor)

start_cam = [4200.0, -120.0, 2550.0, -12.0, 178.0, 0.0, 1.0, 1.0, 1.0]
end_cam = [1150.0, -90.0, 980.0, -6.0, 182.0, 0.0, 1.0, 1.0, 1.0]
add_transform_track(camera_binding, 0, 120, start_cam, end_cam)

camera_actor.set_actor_location(unreal.Vector(start_cam[0], start_cam[1], start_cam[2]), False, False)
camera_actor.set_actor_rotation(unreal.Rotator(start_cam[3], start_cam[4], start_cam[5]), False)

camera_cut_track = unreal.MovieSceneSequenceExtensions.add_track(seq, unreal.MovieSceneCameraCutTrack)
camera_cut_section = camera_cut_track.add_section()
camera_cut_section.set_range(0, 120)
camera_binding_id = seq.get_portable_binding_id(seq, camera_binding)
camera_cut_section.set_camera_binding_id(camera_binding_id)

mascot_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
    unreal.StaticMeshActor,
    unreal.Vector(980.0, 180.0, 1320.0),
    unreal.Rotator(0.0, 0.0, 0.0),
)
mascot_actor.set_actor_label("CHR_DEMO_IntroMascot")
assign_basic_sphere(mascot_actor)
mascot_binding = unreal.MovieSceneSequenceExtensions.add_possessable(seq, mascot_actor)
start_mascot = [980.0, 180.0, 1320.0, 0.0, 0.0, 0.0, 0.35, 0.35, 0.35]
end_mascot = [930.0, 120.0, 760.0, 0.0, 0.0, 0.0, 0.35, 0.35, 0.35]
add_transform_track(mascot_binding, 40, 90, start_mascot, end_mascot)

text_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
    unreal.TextRenderActor,
    unreal.Vector(860.0, 520.0, 860.0),
    unreal.Rotator(0.0, 180.0, 0.0),
)
text_actor.set_actor_label("TXT_DEMO_IntroWelcome")
configure_text_actor(text_actor, INTRO_TEXT)

seq_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
    unreal.LevelSequenceActor,
    unreal.Vector(0.0, 0.0, 0.0),
    unreal.Rotator(0.0, 0.0, 0.0),
)
seq_actor.set_actor_label("LSA_DEMO_Intro_Janganmun")
try:
    seq_actor.set_sequence(seq)
except Exception:
    seq_actor.set_editor_property("level_sequence_asset", seq)

unreal.LevelSequenceEditorBlueprintLibrary.refresh_current_level_sequence()
unreal.EditorAssetLibrary.save_loaded_asset(seq)
unreal.EditorLevelLibrary.save_current_level()
unreal.log("DEMO intro sequence applied successfully")
