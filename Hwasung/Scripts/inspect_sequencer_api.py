import unreal

unreal.log("SEQAPI LevelSequenceFactoryNew exists: {}".format(hasattr(unreal, "LevelSequenceFactoryNew")))
unreal.log("SEQAPI MovieScene3DTransformTrack exists: {}".format(hasattr(unreal, "MovieScene3DTransformTrack")))
unreal.log("SEQAPI MovieSceneScriptingDoubleChannel exists: {}".format(hasattr(unreal, "MovieSceneScriptingDoubleChannel")))

if hasattr(unreal, "MovieSceneScriptingDoubleChannel"):
    methods = [m for m in dir(unreal.MovieSceneScriptingDoubleChannel) if "key" in m.lower()]
    unreal.log("SEQAPI DoubleChannel key methods: {}".format(", ".join(methods)))

if hasattr(unreal, "MovieSceneScriptingFloatChannel"):
    methods = [m for m in dir(unreal.MovieSceneScriptingFloatChannel) if "key" in m.lower()]
    unreal.log("SEQAPI FloatChannel key methods: {}".format(", ".join(methods)))
