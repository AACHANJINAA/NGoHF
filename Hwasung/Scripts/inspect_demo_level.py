import unreal

MAP_PATH = "/Game/HwaseongForteressGate/Level/Demo.Demo"

level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
if not level_subsystem.load_level(MAP_PATH):
    raise RuntimeError(f"Failed to load map: {MAP_PATH}")

actors = unreal.EditorLevelLibrary.get_all_level_actors()
unreal.log(f"Loaded {MAP_PATH} with {len(actors)} actors")

for actor in actors:
    label = actor.get_actor_label()
    cls = actor.get_class().get_name()
    loc = actor.get_actor_location()
    unreal.log(f"ACTOR | {label} | {cls} | {loc.x:.2f}, {loc.y:.2f}, {loc.z:.2f}")
