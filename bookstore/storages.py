from cloudinary_storage.storage import StaticHashedCloudinaryStorage
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage

class CustomStaticHashedCloudinaryStorage(StaticHashedCloudinaryStorage):
    """
    A custom storage class for Cloudinary that ignores missing source map files
    during the collectstatic process.
    """
    def url_converter(self, name, MAPPING_URL_REGEXP):
        # Get the default converter from the parent class.
        base_converter = super().url_converter(name, MAPPING_URL_REGEXP)

        def converter(matchobj):
            try:
                # Try to process the URL as usual.
                return base_converter(matchobj)
            except ValueError:
                # If a ValueError is raised (e.g., file not found for a source map),
                # just return the original, unprocessed URL.
                return matchobj.group(0)

        return converter

class CustomManifestStaticFilesStorage(ManifestStaticFilesStorage):
    """
    A custom storage class for local development that ignores missing source map files
    during the collectstatic process.
    """
    def url_converter(self, name, MAPPING_URL_REGEXP):
        # Get the default converter from the parent class.
        base_converter = super().url_converter(name, MAPPING_URL_REGEXP)

        def converter(matchobj):
            try:
                # Try to process the URL as usual.
                return base_converter(matchobj)
            except ValueError:
                # If a ValueError is raised (e.g., file not found for a source map),
                # just return the original, unprocessed URL.
                return matchobj.group(0)

        return converter 