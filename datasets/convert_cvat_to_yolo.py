import os
import xml.etree.ElementTree as ET

# Define your paths
xml_file = "datasets/annotations.xml"  # change this path if needed
output_dir = "datasets/labels"
os.makedirs(output_dir, exist_ok=True)

# Define the class names
classes = ["free_parking_space", "not_free_parking_space", "partially_free_parking_space"]

def convert_polygon_to_bbox(points):
    xs = [float(p.split(",")[0]) for p in points.split(";")]
    ys = [float(p.split(",")[1]) for p in points.split(";")]
    return min(xs), min(ys), max(xs), max(ys)

def convert_bbox_to_yolo(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[2]) / 2.0
    y = (box[1] + box[3]) / 2.0
    w = box[2] - box[0]
    h = box[3] - box[1]
    return (x * dw, y * dh, w * dw, h * dh)

tree = ET.parse(xml_file)
root = tree.getroot()

for image in root.findall("image"):
    img_name = os.path.basename(image.attrib["name"])
    img_w = int(image.attrib["width"])
    img_h = int(image.attrib["height"])
    label_path = os.path.join(output_dir, os.path.splitext(img_name)[0] + ".txt")

    with open(label_path, "w") as out_file:
        for poly in image.findall("polygon"):
            label = poly.attrib["label"]
            if label not in classes:
                continue
            cls_id = classes.index(label)
            points = poly.attrib["points"]
            bbox = convert_polygon_to_bbox(points)
            bb = convert_bbox_to_yolo((img_w, img_h), bbox)
            out_file.write(f"{cls_id} {' '.join([str(round(a, 6)) for a in bb])}\n")

print("✅ Conversion complete! YOLO labels saved in:", output_dir)
