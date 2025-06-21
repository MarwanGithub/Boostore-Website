from whitenoise.storage import CompressedManifestStaticFilesStorage

class WhiteNoiseSafeStaticFilesStorage(CompressedManifestStaticFilesStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manifest_strict = False

# comments wrriten by me not AI
# this file is created to fix the error of missing source map files from 3rd party libs.
# simply because we are using whitenoise to serve static files it is strict and now we created this file
# to make it less strict about finding the source map files whic hare not needed in our case
# we created this class and we are using it in the settings.py file
# we are not using the CompressedManifestStaticFilesStorage class because it is strict and we are not using it
# we are using the WhiteNoiseSafeStaticFilesStorage class instead, inherited it and set the manifest_strict to False
