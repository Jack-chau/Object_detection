# Intersection over Union

import torch

def intersetion_over_union(boxes_preds, boxes_labels, box_format = 'midpoint'):
    """
    Calculate intersection over union

    Parameters:
        boxes_preds (tensor): Predictions of Boundung Boxes (Batch_size, 4)
        boxes_labels  (tensor): Correct labels of Bounding Boxes (Batch_size, 4)
        box_format (str):   midpoint/corners. if boxes (x,y,w,h) or (x1,y1,x2,y2)

    Returns: IoU
    """
    # label after CNN (N,4) where N is the number of bboxes
    # boxes_preds.shape (N,4) x1,y1,width, height
    if box_format == 'midpoint':
        box1_x1 = boxes_preds[..., 0:1] - boxes_preds[...,2:3]/2
        box1_y1 = boxes_preds[..., 1:2] - boxes_preds[...,3:4]/2
        box1_x2 = boxes_preds[..., 0:1] + boxes_preds[...,2:3]/2
        box1_y2 = boxes_preds[..., 1:2] + boxes_preds[...,3:4]/2
        # boxes_labels.shape (N,4) x1,y1,x2,y2
        box2_x1 = boxes_labels[..., 0:1] - boxes_labels[..., 2:3]/2
        box2_y1 = boxes_labels[..., 1:2] - boxes_labels[..., 3:4]/2
        box2_x2 = boxes_labels[..., 0:1] + boxes_labels[..., 2:3]/2
        box2_y2 = boxes_labels[..., 1:2] + boxes_labels[..., 3:4]/2

    elif box_format == 'corner':
        # label after CNN (N,4) where N is the number of bboxes
        # boxes_preds.shape (N,4) x1,y1,x2,y2
        box1_x1 = boxes_preds[...,0:1]
        box1_y1 = boxes_preds[...,1:2]
        box1_x2 = boxes_preds[...,2:3]
        box1_y2 = boxes_preds[...,3:4]
        # boxes_labels.shape (N,4) x1,y1,x2,y2
        box2_x1 = boxes_labels[...,0:1]
        box2_y1 = boxes_labels[...,1:2]
        box2_x2 = boxes_labels[...,2:3]
        box2_y2 = boxes_labels[...,3:4]

    x1 = torch.max(box1_x1, box2_x1)
    y1 = torch.max(box1_y1, box2_y1)
    x2 = torch.min(box1_x2, box2_x2)
    y2 = torch.min(box1_y2, box2_y2)
    # .clamp(0) is for the case when they do not intersect
    intersetion = (x2-x1).clamp(0) * (y2-y1).clamp(0)

    box1_area = abs((box1_x2-box1_x1) * (box1_y2-box1_y1))
    box2_area = abs((box2_x2-box2_x1) * (box2_y2-box2_y1))
    union = (box1_area + box2_area - intersetion + 1e-6)
    IoU = intersetion/union
    return IoU
