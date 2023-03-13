from django.core import exceptions

VARIABLE_INT = 1
MAX_IMAGE_SIZE = VARIABLE_INT * 1024 * 1024    # if we want to use limitation in MB
# MAX_IMAGE_SIZE = VARIABLE_INT * 1024    #if we want to use limitation in KB or change limit_size to 0.99-0.01

def user_directory_path(instance, filename):
    # file will be uploaded to media / user_<id>/<filename>
    return 'owner_{0}/{1}'.format(instance.owner.id, filename)


def validate_image_size(image):
    size = image.size
    if size > MAX_IMAGE_SIZE:
        raise exceptions.ValidationError('Max file size is %s MB' % str(MAX_IMAGE_SIZE))
        # raise exceptions.ValidationError('Max file size is %s KB' % str(MAX_IMAGE_SIZE))
