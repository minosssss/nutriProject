import os
from uuid import uuid4
from django.utils import timezone

from upload.detection.imageDetection import imageDetection


def upload_to_func(instance, filename):
    prefix = timezone.now().strftime("%Y/%m")
    file_name = uuid4().hex
    user_id = instance.user.user_id
    extension = os.path.splitext(filename)[-1].lower() # 확장자 추출
    return "/".join(
        [user_id, prefix, file_name+extension]
    )
    #구분을 하자면 일은 의미가 없고,, 년월만 ....
