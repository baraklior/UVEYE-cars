# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved.
import argparse
import cv2
import torch

from maskrcnn_benchmark.config import cfg
from shameless_predictor import COCODemo
from PIL import Image
import os
from pathlib import Path


INPUT_FOLDER_PATH = "/mnt/input/"
OUTPUT_FOLDER_PATH = "/mnt/output/"

class CarFinder:
    def __init__(self):
        config_file = "../maskrcnn-benchmark/configs/caffe2/e2e_mask_rcnn_R_50_FPN_1x_caffe2.yaml"
        confidence_threshold = 0.7
        min_image_size = 224
        show_mask_heatmaps = False
        masks_per_dim = 2

        cfg.merge_from_file(config_file)
        cfg.merge_from_list(["MODEL.DEVICE", "cpu"]) # hard coded to run on cpu at the moment
        cfg.freeze()

        # prepare object that handles inference plus adds predictions on top of image
        self.coco_demo = COCODemo(
            cfg,
            confidence_threshold=confidence_threshold,
            show_mask_heatmaps=show_mask_heatmaps,
            masks_per_dim=masks_per_dim,
            min_image_size=min_image_size,
        )

    def process_one_photo(self, image_path, save_to_disk):
        full_image_path = os.path.join(INPUT_FOLDER_PATH,image_path)
        img = cv2.imread(full_image_path)
        top_predictions, composite = self.coco_demo.run_on_opencv_image(
            img, only_cars=True)

        xy_coordinate_list = self.get_xy_coordinates(top_predictions)
        confidence_list = self.get_confidence_level(top_predictions)
        detected_cars = [
            {"Confidence": a, "BoundingBox": b} for a, b in zip(confidence_list, xy_coordinate_list)
        ]

        if save_to_disk:
            out_file_name = image_path.replace(".", "-output.")
            output_full_path = os.path.join(OUTPUT_FOLDER_PATH,out_file_name)
            Path(output_full_path).parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(output_full_path, composite)

        else:
            output_full_path = None

        return detected_cars, output_full_path

    @staticmethod
    def get_xy_coordinates(predictions):
        boxes = predictions.bbox
        return [box.to(torch.int64).tolist() for box in boxes]

    @staticmethod
    def get_confidence_level(predictions):
        return predictions.get_field("scores").tolist()
