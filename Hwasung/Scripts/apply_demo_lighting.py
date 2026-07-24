import unreal

MAP_PATH = "/Game/HwaseongForteressGate/Level/Demo.Demo"


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


def ensure_actor(actor_class, label, location, rotation=None, folder=None):
    actor = find_by_label(label)
    if actor is None:
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(actor_class, location, rotation or unreal.Rotator(0, 0, 0))
        actor.set_actor_label(label)
    else:
        actor.set_actor_location(location, False, False)
        if rotation is not None:
            actor.set_actor_rotation(rotation, False)
    if folder:
        actor.set_folder_path(folder)
    return actor


def get_component(actor, component_class):
    component = actor.get_component_by_class(component_class)
    if component is None:
        raise RuntimeError(f"Missing component {component_class} on {actor.get_actor_label()}")
    return component


def safe_set(component, prop_name, value):
    try:
        component.set_editor_property(prop_name, value)
    except Exception as exc:
        unreal.log_warning(f"Skipped property {prop_name} on {component.get_name()}: {exc}")


def set_common_light(component, intensity, color, mobility=unreal.ComponentMobility.MOVABLE):
    safe_set(component, "mobility", mobility)
    safe_set(component, "intensity", intensity)
    component.set_light_color(color, True)
    safe_set(component, "cast_shadows", True)
    safe_set(component, "affects_world", True)


load_map()

# Morning base rig
sun_actor = ensure_actor(
    unreal.DirectionalLight,
    "LGT_DEMO_MorningSun",
    unreal.Vector(0.0, 0.0, 400.0),
    unreal.Rotator(-32.0, -38.0, 0.0),
    "Lighting/DEMO/Morning",
)
sun_component = get_component(sun_actor, unreal.DirectionalLightComponent)
set_common_light(sun_component, 10.0, unreal.LinearColor(1.0, 0.956, 0.87, 1.0))
safe_set(sun_component, "atmosphere_sun_light", True)
safe_set(sun_component, "indirect_lighting_intensity", 1.2)
safe_set(sun_component, "volumetric_scattering_intensity", 1.0)

sky_atmosphere_actor = ensure_actor(
    unreal.SkyAtmosphere,
    "LGT_DEMO_SkyAtmosphere",
    unreal.Vector(0.0, 0.0, 500.0),
    folder="Lighting/DEMO/Morning",
)
sky_atmosphere_component = get_component(sky_atmosphere_actor, unreal.SkyAtmosphereComponent)
safe_set(sky_atmosphere_component, "trace_sample_count_scale", 2.0)

sky_light_actor = ensure_actor(
    unreal.SkyLight,
    "LGT_DEMO_SkyLight",
    unreal.Vector(0.0, 0.0, 600.0),
    folder="Lighting/DEMO/Morning",
)
sky_light_component = get_component(sky_light_actor, unreal.SkyLightComponent)
safe_set(sky_light_component, "mobility", unreal.ComponentMobility.MOVABLE)
safe_set(sky_light_component, "intensity", 1.0)
safe_set(sky_light_component, "real_time_capture", True)
safe_set(sky_light_component, "lower_hemisphere_is_black", False)

fog_actor = ensure_actor(
    unreal.ExponentialHeightFog,
    "LGT_DEMO_HeightFog",
    unreal.Vector(-5600.0, -50.0, -6850.0),
    folder="Lighting/DEMO/Morning",
)
fog_component = get_component(fog_actor, unreal.ExponentialHeightFogComponent)
safe_set(fog_component, "fog_density", 0.01)
safe_set(fog_component, "fog_height_falloff", 0.2)
safe_set(fog_component, "volumetric_fog", True)
safe_set(fog_component, "volumetric_fog_scattering_distribution", 0.6)
safe_set(fog_component, "fog_inscattering_color", unreal.LinearColor(0.82, 0.88, 1.0, 1.0))

# Hongyemun interior highlight
hongyemun_spot = ensure_actor(
    unreal.SpotLight,
    "LGT_DEMO_HongyemunSpot",
    unreal.Vector(-1310.0, -100.0, 900.0),
    unreal.Rotator(90.0, 0.0, 0.0),
    "Lighting/DEMO/Interior",
)
hongyemun_spot_component = get_component(hongyemun_spot, unreal.SpotLightComponent)
set_common_light(hongyemun_spot_component, 18000.0, unreal.LinearColor(1.0, 0.93, 0.80, 1.0))
safe_set(hongyemun_spot_component, "inner_cone_angle", 24.0)
safe_set(hongyemun_spot_component, "outer_cone_angle", 48.0)
safe_set(hongyemun_spot_component, "attenuation_radius", 1800.0)
safe_set(hongyemun_spot_component, "indirect_lighting_intensity", 1.5)
safe_set(hongyemun_spot_component, "volumetric_scattering_intensity", 1.2)

# Night lighting along eaves and walls
night_specs = [
    ("LGT_DEMO_NightPoint_01", unreal.Vector(-1300.0, -900.0, 1700.0)),
    ("LGT_DEMO_NightPoint_02", unreal.Vector(-1300.0, 900.0, 1700.0)),
    ("LGT_DEMO_NightPoint_03", unreal.Vector(-950.0, -120.0, 1850.0)),
    ("LGT_DEMO_NightPoint_04", unreal.Vector(-1650.0, -120.0, 1850.0)),
    ("LGT_DEMO_NightPoint_05", unreal.Vector(-1100.0, -120.0, 1350.0)),
    ("LGT_DEMO_NightPoint_06", unreal.Vector(-1500.0, -120.0, 1350.0)),
]

for label, location in night_specs:
    actor = ensure_actor(
        unreal.PointLight,
        label,
        location,
        folder="Lighting/DEMO/Night",
    )
    component = get_component(actor, unreal.PointLightComponent)
    set_common_light(component, 3500.0, unreal.LinearColor(1.0, 0.78, 0.52, 1.0))
    safe_set(component, "attenuation_radius", 2200.0)
    safe_set(component, "source_radius", 35.0)
    safe_set(component, "soft_source_radius", 75.0)
    safe_set(component, "indirect_lighting_intensity", 1.0)
    safe_set(component, "volumetric_scattering_intensity", 0.8)

# Save level
unreal.EditorLevelLibrary.save_current_level()
unreal.log("DEMO lighting rig applied successfully")
