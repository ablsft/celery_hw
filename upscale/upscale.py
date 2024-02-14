import os
from io import BytesIO
from typing import Union

import cv2
from cv2 import dnn_superres
import numpy as np
from gridfs.grid_file import GridOut


FILE = Union[str, BytesIO, GridOut]

FILE_URL = 'http://127.0.0.1:5000/processed/'


class Upscaler:

    instance = None

    def __init__(self, scaler):
        self.scaler = scaler
        self.__class__.instance = self

    @classmethod
    def get_instance(cls, model_path: str = os.path.join('upscale', 'EDSR_x2.pb')):
        if not cls.instance:
            scaler = dnn_superres.DnnSuperResImpl_create()
            scaler.readModel(model_path)
            scaler.setModel("edsr", 2)
            cls.instance = cls(scaler)
        return cls.instance

    def upscale(self, input_file: FILE) -> None:
        image = np.frombuffer(input_file.read(), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        result = self.scaler.upsample(image)

        output_filename = f'upscaled_{input_file.filename}'
        output_path = os.path.join('images', output_filename)
        cv2.imwrite(output_path, result)
        return f'{FILE_URL}{output_filename}'
    
def upscale_input_photo(input_file: FILE):
    return Upscaler.get_instance().upscale(input_file)
