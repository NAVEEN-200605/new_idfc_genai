def group_by_layout(ocr_outputs, image_height):
    """
    Groups OCR outputs into header, body, footer based on y-position.
    """
    header, body, footer = [], [], []

    for item in ocr_outputs:
        bbox = item["bbox"]
        y_coords = [pt[1] for pt in bbox]
        y_center = sum(y_coords) / len(y_coords)

        if y_center < 0.25 * image_height:
            header.append(item)
        elif y_center > 0.75 * image_height:
            footer.append(item)
        else:
            body.append(item)

    return {
        "header": header,
        "body": body,
        "footer": footer
    }
