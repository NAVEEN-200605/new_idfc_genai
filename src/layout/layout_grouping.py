def get_y_center(bbox):
    try:
        ys = [p[1] for p in bbox]
        return sum(ys) / len(ys)
    except:
        return None

def group_by_layout(ocr_outputs, image_height):
    header, body, footer = [], [], []

    for item in ocr_outputs:
        y = get_y_center(item["bbox"])
        if y is None:
            continue

        if y < 0.33 * image_height:
            header.append(item)
        elif y > 0.70 * image_height:
            footer.append(item)
        else:
            body.append(item)

    return {
        "header": header,
        "body": body,
        "footer": footer
    }
