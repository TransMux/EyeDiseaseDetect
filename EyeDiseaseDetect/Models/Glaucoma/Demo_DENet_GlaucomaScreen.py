#
import os
from pathlib import Path
from time import time
from typing import List

import cv2
import numpy as np
from keras.preprocessing import image
# from scipy.misc import imsave
from skimage.measure import regionprops, label
from skimage.transform import rotate, resize

from EyeDiseaseDetect.Models.ModelConstructor import BaseModel
from EyeDiseaseDetect.Models.utils import change_status, update_meta, predict_result_template
from .utils import BW_img, Deep_Screening, Disc_Crop

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

from . import Model_Disc_Seg as DiscSegModel
from . import Model_resNet50 as ScreenModel
from . import Model_UNet_Side as DiscModel

Img_Seg_size = 640
Img_Scr_size = 400
ROI_Scr_size = 224

pre_model_DiscSeg = './Models/Glaucoma/pre_model/pre_model_DiscSeg.h5'
pre_model_img = './Models/Glaucoma/pre_model/pre_model_img.h5'
pre_model_ROI = './Models/Glaucoma/pre_model/pre_model_ROI.h5'
pre_model_flat = './Models/Glaucoma/pre_model/pre_model_flat.h5'
pre_model_disc = './Models/Glaucoma/pre_model/pre_model_disc.h5'

data_type = '.jpg'

seg_model = DiscSegModel.DeepModel(Img_Seg_size)
seg_model.load_weights(pre_model_DiscSeg, by_name=True)

img_model = ScreenModel.DeepModel(Img_Scr_size)
img_model.load_weights(pre_model_img, by_name=True)

ROI_model = ScreenModel.DeepModel(ROI_Scr_size)
ROI_model.load_weights(pre_model_ROI, by_name=True)

ROIpt_model = ScreenModel.DeepModel(ROI_Scr_size)
ROIpt_model.load_weights(pre_model_flat, by_name=True)

Disc_model = DiscModel.DeepModel(Img_Seg_size)
Disc_model.load_weights(pre_model_disc, by_name=True)


class Glaucoma(BaseModel):
    def predict(self, data_paths: List[Path]) -> List:
        change_status(data_paths, self.__class__.__name__, "Predict")

        for pic in data_paths:
            org_img = np.asarray(image.load_img(pic))  # + temp_txt[0]

            img_scale = 2048.0 / org_img.shape[0]
            org_img = resize(org_img, (2048, int(org_img.shape[1] * img_scale), 3))

            start_time = time()

            # disc segmentation
            temp_img = resize(org_img, (Img_Seg_size, Img_Seg_size, 3))
            temp_img = np.reshape(temp_img, (1,) + temp_img.shape)
            [prob_6, prob_7, prob_8, prob_9, prob_10] = seg_model.predict([temp_img])
            disc_map = np.reshape(prob_10, (Img_Seg_size, Img_Seg_size))

            disc_map[0:round(disc_map.shape[0] / 5), :] = 0
            disc_map[-round(disc_map.shape[0] / 5):, :] = 0
            disc_map = BW_img(disc_map, 0.5)

            regions = regionprops(label(disc_map))
            C_x = regions[0].centroid[0] * org_img.shape[0] / Img_Seg_size
            C_y = regions[0].centroid[1] * org_img.shape[1] / Img_Seg_size
            disc_region = Disc_Crop(org_img, Img_Scr_size * 2, C_x, C_y)

            Disc_flat = rotate(
                cv2.linearPolar(disc_region, (Img_Scr_size, Img_Scr_size), Img_Scr_size, cv2.WARP_FILL_OUTLIERS),
                -90)

            # global screening
            Img_pred = Deep_Screening(img_model, org_img, Img_Scr_size)
            Disc_pred = Deep_Screening(ROI_model, disc_region, ROI_Scr_size)
            Polar_pred = Deep_Screening(ROIpt_model, Disc_flat, ROI_Scr_size)
            Seg_pred = Deep_Screening(Disc_model, org_img, Img_Seg_size)

            DENet_pred = np.mean([Img_pred[0][1], Disc_pred[0][1], Polar_pred[0][1], Seg_pred[0][1]])
            run_time = time() - start_time

            print('Run time: ' + str(run_time))

            # sio.savemat(tmp_name[:-4] + '.mat', {'Img_pred': Img_pred,
            #                                      'Disc_pred': Disc_pred, 'Polar_pred': Polar_pred, 'Seg_pred': Seg_pred,
            #                                      'DENet_pred': DENet_pred})
            # imsave(tmp_name[:-4] + '.png', Disc_flat)

            update_meta(
                pic,
                self.__class__.__name__,
                predict_result_template(
                    status="Finish",
                    results={'Img_pred': Img_pred.tolist(),
                             'Disc_pred': Disc_pred.tolist(), 'Polar_pred': Polar_pred.tolist(),
                             'Seg_pred': Seg_pred.tolist(),
                             'DENet_pred': DENet_pred.tolist()},
                    overall_confident=DENet_pred.item()
                )
            )
        return [{}]
