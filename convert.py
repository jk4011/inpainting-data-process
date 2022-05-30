from PIL import Image
import glob
import os

path_celebA = "/Users/jh/Downloads/celebA/"
path_ffhq = "/Users/jh/Downloads/ffhq/"

path_save_celebA = "/Users/jh/Downloads/celebA_converted/"
path_save_ffhq = "/Users/jh/Downloads/ffhq_converted/"

# celebA : 178×218 jpg -> 224×224 png

print(1111, "celebA converting start")
for file_path in glob.glob(path_celebA + '*.jpg'):
    file_name = file_path.split('/')[-1].split('.')[0] + '.png'
    if os.path.exists(path_save_celebA + file_name):
        continue

    im=Image.open(file_path)

    (left, upper, right, lower) = (0, 20, 178, 198)

    # Here the image "im" is cropped and assigned to new variable im_crop
    im_crop = im.crop((left, upper, right, lower))
    im_resized = im_crop.resize((224, 224), Image.ANTIALIAS)

    im_resized.save(fp = path_save_celebA + file_name)

    # print(1111, path_save_celebA + file_name, "done")



print(2222, "ffhq converting start")
# ffhq : 128×128 png -> 224×224 png
for file_path in glob.glob(path_ffhq + '*.png'):
    file_name = file_path.split('/')[-1]
    if os.path.exists(path_save_ffhq + file_name):
        continue

    im=Image.open(file_path)

    im = im.resize((224, 224), Image.ANTIALIAS)
    im.save(fp = path_save_ffhq + file_name)
