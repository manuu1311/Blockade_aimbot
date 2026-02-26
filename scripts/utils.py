from PIL import Image,ImageEnhance,ImageFilter
import numpy as np


#class that procedurally generates new images starting from base backgrounds, chars, objects
class ImageGenerator:
    def __init__(self,backgrounds, characters, objects,ui):
        self.backgrounds=backgrounds
        self.chars=characters
        self.objects=objects
        self.ui=ui
    
    #merge background with another image (char/ui/object)
    def merger(self,background,masked,topaste,x,y,block=False):
        background.paste(topaste, (x, y), mask=topaste.getchannel(3)) 
        #mask
        masked_paste=topaste.getchannel(3)
        if block:
            masked.paste(0, (x, y), mask=masked_paste)
        else:
            masked_paste = masked_paste.point([0] + [255]*255)
            masked.paste(masked_paste,(x,y),mask=masked_paste)
    
    #char_p: probability of character not appearing
    def new_image(self,char_p=0.1,object_p=0.6,bg_p=0.7,augmentation=True):
        #get random background
        idxbg=np.random.randint(0,len(self.backgrounds))
        background=self.backgrounds[idxbg].copy()
        img=background.convert('RGBA')

        #masked image
        masked=Image.new('L',img.size)

        #with probability 1-p, insert character
        if np.random.uniform()>char_p:
            idxchar=np.random.randint(0,len(self.chars))
            char=self.chars[idxchar].copy()
            offx=np.random.randint(-30,460)
            offy=np.random.randint(-30,160)
            #augmentation
            #scaling factor
            factor=np.random.uniform(0.3,1.5)
            h,w=char.size
            char=char.resize((int(h*factor),int(w*factor)))
            if augmentation:
                char=self.transform(char)
            self.merger(img,masked,char,offx,offy)
            
        
        #insert object with probability 1-p
        if np.random.uniform()>object_p:
            offx=np.random.randint(-30,460)
            offy=np.random.randint(-30,160)
            factor=np.random.uniform(0.2,0.4)
            idobj=np.random.randint(low=0,high=len(self.objects))
            obj=self.objects[idobj]
            h,w=obj.size
            obj=obj.resize((int(h*factor),int(w*factor)))
            self.merger(img,masked,obj,offx,offy,True)

        if augmentation:
            #flip entire image with probability 1-p
            if np.random.uniform()>bg_p:
                img=img.transpose(Image.FLIP_LEFT_RIGHT)
                masked=masked.transpose(Image.FLIP_LEFT_RIGHT)
            elif np.random.uniform()>bg_p:
                img=img.transpose(Image.FLIP_TOP_BOTTOM)
                masked=masked.transpose(Image.FLIP_TOP_BOTTOM)
    
        return img,masked
    
    def transform(self,img,p=0.4):
        #quad
        if np.random.uniform()>p:
            quad = [0, 0, 0, 256,256, 512, 128, -256]
            img=img.transform((256, 256), Image.Transform.QUAD, data=quad)

        #rotate
        if np.random.uniform()>p:
            angle = np.random.randint(20, 46) if np.random.rand() < 0.5 else np.random.randint(-45, -19)
            img = img.rotate(angle,center=(75, 75),expand=True)

        #color jitter
        if np.random.uniform()>p:
            brightness=0.4
            img = ImageEnhance.Brightness(img).enhance(1.0 + np.random.uniform(-brightness, brightness))
            contrast=0.4
            img = ImageEnhance.Contrast(img).enhance(1 + np.random.uniform(-contrast, contrast))
            saturation=0.4
            img = ImageEnhance.Color(img).enhance(1 + np.random.uniform(-saturation, saturation))
        
        #blur
        if np.random.uniform()>p:
            r = np.random.uniform(0, 1)
            img=img.filter(ImageFilter.GaussianBlur(r))

        #opacity 
        if np.random.uniform()>p:
            alpha = img.split()[-1]
            factor = np.random.uniform(0.7, 0.9)
            alpha = alpha.point(lambda p: int(p * factor))
            img.putalpha(alpha)
        return img