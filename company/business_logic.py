from django.core import exceptions

VARIABLE_INT = 2
MAX_IMAGE_SIZE = VARIABLE_INT * 1024 * 1024  # if we want to use limitation in MB


def validate_image_size(image):
    size = image.size
    if size > MAX_IMAGE_SIZE:
        raise exceptions.ValidationError('Max file size is %s KB' % str(MAX_IMAGE_SIZE))
