from dataclasses import dataclass, field

import numpy as np
from cv2.cv2 import KeyPoint, drawKeypoints

from Mask_R_CNN_COCO import get_class_name_for_id
from ORB import get_keypoints_and_descriptors_for_object, average_descriptor_distance
from model.Box import Box
from utils.image_utils import show
from utils.timer import timing

LOCATION_VARIANCE_THRESHOLD = 0.1  # how far an object can move between two frames before it is recognized as a new obj


@dataclass
class ObjectInstance:
    class_name: str
    roi: Box
    confidence_score: float
    mask: [[]]
    keypoints: [KeyPoint] = field(default_factory=list)
    descriptors: np.ndarray = None

    def similarity_to(self, obj_instance) -> float:
        # Check if same class
        if not self.class_name == obj_instance.class_name:
            return 0
        # Check if both have descriptors
        if self.descriptors is None or obj_instance.descriptors is None:
            return 0
        # Check if instances are in similar location
        this_position_x, this_position_y = self.roi.get_position_in_image()
        other_position_x, other_position_y = obj_instance.roi.get_position_in_image()
        if abs(this_position_x - other_position_x) > LOCATION_VARIANCE_THRESHOLD or \
                abs(this_position_y - other_position_y) > LOCATION_VARIANCE_THRESHOLD:
            return 0
        # Check if descriptors match
        average_distance = average_descriptor_distance(self.descriptors, obj_instance.descriptors)
        normalized_distance = average_distance / 100  # normalize?
        return max(0.0, 1 - normalized_distance)


@timing
def create_objects(result, frame) -> [ObjectInstance]:
    objects = []
    number_of_results = result["class_ids"].shape[0]
    for i in range(number_of_results):
        class_name = get_class_name_for_id(result["class_ids"][i])

        roi = result["rois"][i]
        y1, x1, y2, x2 = roi
        box = Box(x1, y1, x2, y2)

        confidence_score = result["scores"][i]

        mask = result["masks"][:, :, i]

        keypoints, descriptors = get_keypoints_and_descriptors_for_object(frame, mask)
        # show(drawKeypoints(frame, keypoints, None))
        detected_object = ObjectInstance(class_name, box, confidence_score, mask, keypoints, descriptors)
        objects.append(detected_object)
    return objects
