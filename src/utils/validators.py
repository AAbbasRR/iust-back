from django.core.exceptions import ValidationError

from Abrat.settings import MAX_DOCUMENTS_SIZE

from utils.base_errors import BaseErrors


def validate_image_file(value):
    if not value:
        return

    allowed_formats = ["JPEG", "PNG", "JPG", "PDF", "DOC", "DOCX", "BMP"]
    file_extension = value.name.split(".")[-1].upper()
    if file_extension not in allowed_formats:
        raise ValidationError(
            BaseErrors._change_error_variable(
                "invalid_file_formats", formats=", ".join(allowed_formats)
            )
        )

    if value.size > MAX_DOCUMENTS_SIZE:
        raise ValidationError(BaseErrors._change_error_variable("invalid_file_size"))
