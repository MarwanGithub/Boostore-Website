from whitenoise.storage import CompressedManifestStaticFilesStorage

class WhiteNoiseSafeStaticFilesStorage(CompressedManifestStaticFilesStorage):
    manifest_strict = False 