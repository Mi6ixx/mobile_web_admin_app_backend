from rest_framework.exceptions import ValidationError

def validate_image_size(value):
    max_size = 5 * 1024 * 1024  # 5MB in bytes
    if value.size > max_size:
        raise ValidationError('Image size must be less than 5 MB.')