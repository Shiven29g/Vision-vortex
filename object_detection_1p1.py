import cv2, sys, os, object_detection_properties as odp
from werkzeug.utils import secure_filename
from PIL import Image

file = sys.argv[1]

ext = file.split(".")[1]

if (ext in odp.allowed_ext) == False:
    print(f"only {odp.allowed_ext} file extensions are allowed")
    sys.exit()

if (file == secure_filename(file)) == False:
    print("only filename without special characters is allowed")
    sys.exit()

size = os.path.getsize(file)
if (size in range(0, odp.allowed_file_size)) == False:
    print("only file with size less than 200kb is allowed")
    sys.exit()

try:
    Image.open(file)
    pass
except:
    print("only image file is allowed (to cross check, please try to open the file in a local image editor)")
    sys.exit()

img = cv2.imread(file)

net = cv2.dnn.readNet("dnn_model-220107-114215/dnn_model/yolov4-tiny.weights",
                      "dnn_model-220107-114215/dnn_model/yolov4-tiny.cfg")
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(320,320),scale=1/255)

classes=[]
with open("dnn_model-220107-114215/dnn_model/classes.txt","r") as f:
    for class_name in f.readlines():
        class_name=class_name.strip()
        classes.append(class_name)

(class_ids,scores,bboxes)=model.detect(img)
try:
	n=class_ids[0]
	print("this is an image of a",classes[n])
except:
	print("this is an unknown image")