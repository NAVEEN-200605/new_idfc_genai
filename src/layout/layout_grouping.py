from extraction.field_extraction import get_y_center

def group_by_layout(ocr_outputs, image_height):
    header, body, footer = [], [], []

    for item in ocr_outputs:
        y_center = get_y_center(item["bbox"])
        if y_center is None:
            continue

        if y_center < 0.33 * image_height:
            header.append(item)
        elif y_center > 0.70 * image_height:
            footer.append(item)
        else:
            body.append(item)

    return {
        "header": header,
        "body": body,
        "footer": footer
    }
