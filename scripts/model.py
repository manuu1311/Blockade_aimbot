from tensorflow import keras
import numpy as np
from scipy import ndimage


class detector:
    def __init__(self,model_name='model_v2.keras'):
        self.model=keras.saving.load_model('model/'+model_name,compile=False)
    
    #process image
    def predict(self,img):
        pass
    #given the prediction, return x and y coordinates to shoot
    def get_centroid(self,prediction):
        pass



class segment_detector(detector):
    def __init__(self, model_name='model_v2.keras'):
        super().__init__(model_name)
        self.size=(576,288)

    def predict(self, img,thresh=0.8,scale=255,cleanup=False):
        predicted=self.model.predict(np.array(img)[None,...]/scale)[0,...,0]
        argpred=(predicted>thresh).astype(np.uint8)
        if cleanup:
            argpred=self.clean_segmentation_mask(argpred)
        return argpred
    
    def get_centroid(self, prediction):
        mask=np.array(prediction)
        mask=np.column_stack(np.where(mask==1))
        if mask.size==0:
            return 0,0
        maxy,miny=np.max(mask[:,0]),np.min(mask[:,0])
        h=miny+(maxy-miny)/3
        mask=mask[mask[:,0]<h]
        centroid=mask.mean(axis=0).astype(int)
        return centroid
    
    #clean image,optional
    def clean_segmentation_mask(self,mask: np.ndarray,keep_mode: str = "largest",
                                min_relative_size: float = 0.2,
                                apply_opening: bool = True,
                                ) -> np.ndarray:
        """
        Clean a binary segmentation mask by removing small spurious regions.

        Parameters
        ----------
        mask : np.ndarray
            2D binary array (0/1 or bool).
        keep_mode : str
            "largest" → keep only the largest component (default, safest)
            "relative" → keep components larger than min_relative_size * largest
        min_relative_size : float
            Used only when keep_mode="relative".
        apply_opening : bool
            If True, performs a small morphological opening to remove speckle noise.

        Returns
        -------
        np.ndarray
            Cleaned binary mask (uint8).
        """

        if mask.ndim != 2:
            raise ValueError("Mask must be 2D")

        # ensure binary uint8
        mask = (mask > 0).astype(np.uint8)

        # --- optional morphological cleanup ---
        if apply_opening:
            mask = ndimage.binary_opening(mask, structure=np.ones((3, 3))).astype(np.uint8)

        # --- connected components ---
        labeled, num_features = ndimage.label(mask)

        if num_features == 0:
            return mask  # nothing detected

        sizes = ndimage.sum(mask, labeled, range(1, num_features + 1))
        sizes = np.array(sizes)

        if keep_mode == "largest":
            largest_label = np.argmax(sizes) + 1
            cleaned = (labeled == largest_label)

        elif keep_mode == "relative":
            max_size = sizes.max()
            keep_labels = np.where(sizes >= max_size * min_relative_size)[0] + 1
            cleaned = np.isin(labeled, keep_labels)

        else:
            raise ValueError('keep_mode must be "largest" or "relative"')

        return cleaned.astype(np.uint8)