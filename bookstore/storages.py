from cloudinary_storage.storage import StaticHashedCloudinaryStorage
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage

class CustomStaticHashedCloudinaryStorage(StaticHashedCloudinaryStorage):
    """
    A custom storage class for Cloudinary that ignores missing source map files
    and other file-not-found errors during the collectstatic process.
    """
    def url_converter(self, name):
        # Get the default converter from the parent class.
        base_converter = super().url_converter(name)

        def converter(matchobj):
            try:
                # Try to process the URL as usual.
                return base_converter(matchobj)
            except (ValueError, TypeError):
                # If a ValueError is raised (e.g., file not found for a source map),
                # or a TypeError (e.g., path is None due to jazzmin conflicts),
                # just return the original, unprocessed URL.
                return matchobj.group(0)

        return converter

class CustomManifestStaticFilesStorage(ManifestStaticFilesStorage):
    """
    A custom storage class for local development that ignores missing source map files
    and other file-not-found errors during the collectstatic process.
    """
    def url_converter(self, name):
        # Get the default converter from the parent class.
        base_converter = super().url_converter(name)

        def converter(matchobj):
            try:
                # Try to process the URL as usual.
                return base_converter(matchobj)
            except (ValueError, TypeError):
                # If a ValueError is raised (e.g., file not found for a source map),
                # or a TypeError (e.g., path is None due to jazzmin conflicts),
                # just return the original, unprocessed URL.
                return matchobj.group(0)

        return converter 