import cv2
import numpy as np
import math

ASSUMED_FLOOR_HEIGHT_M = 3.048  # 10 ft

def _line_point_dist(px, py, x1, y1, x2, y2):
    # distance from point P to segment AB
    A = np.array([x1, y1], dtype=float)
    B = np.array([x2, y2], dtype=float)
    P = np.array([px, py], dtype=float)
    AB = B - A
    t = np.dot(P - A, AB) / (np.dot(AB, AB) + 1e-9)
    t = np.clip(t, 0.0, 1.0)
    proj = A + t * AB
    return float(np.linalg.norm(P - proj)), proj

def _extend_within_mask(mask, p1, p2, max_steps=5000):
    """
    Extend the line through p1->p2 in both directions while staying inside mask.
    Returns two endpoints inside mask (approx boundary intersection).
    """
    h, w = mask.shape[:2]
    p1 = np.array(p1, dtype=float)
    p2 = np.array(p2, dtype=float)
    v = p2 - p1
    norm = np.linalg.norm(v)
    if norm < 1e-6:
        return tuple(map(int, p1)), tuple(map(int, p2))
    v = v / norm

    # start from mid
    mid = 0.5 * (p1 + p2)

    def step_until_exit(start, direction):
        last_in = start.copy()
        for _ in range(max_steps):
            nxt = last_in + direction
            x, y = int(round(nxt[0])), int(round(nxt[1]))
            if x < 0 or y < 0 or x >= w or y >= h or mask[y, x] == 0:
                break
            last_in = nxt
        return tuple(map(int, np.clip(last_in, [0, 0], [w - 1, h - 1])))

    end1 = step_until_exit(mid, v)     # forward
    end2 = step_until_exit(mid, -v)    # backward
    return end1, end2

def _vertical_fallback(mask, click_xy, neighborhood=20):
    """
    If Hough lines fail, scan vertically near the click to find top/bottom inside mask.
    """
    h, w = mask.shape[:2]
    cx = int(round(click_xy[0]))
    x0 = max(0, cx - neighborhood)
    x1 = min(w - 1, cx + neighborhood)

    best_span = 0
    best_top = None
    best_bottom = None

    for x in range(x0, x1 + 1):
        ys = np.where(mask[:, x] > 0)[0]
        if ys.size == 0:
            continue
        top = int(ys.min())
        bottom = int(ys.max())
        span = bottom - top
        if span > best_span:
            best_span = span
            best_top = (x, top)
            best_bottom = (x, bottom)

    if best_top is None:
        return None, None
    return best_top, best_bottom

def auto_height_from_mask(image_bgr, mask_uint8, click_xy, ppm):
    """
    Returns:
      endpoints: (pt_top, pt_bottom) as (x,y)
      measures: dict with 'slanted_m', 'vertical_m', 'floors'
    """
    h, w = mask_uint8.shape[:2]
    # Crop ROI to mask bounding box for speed
    x, y, bw, bh = cv2.boundingRect(mask_uint8)
    roi_img = image_bgr[y:y+bh, x:x+bw]
    roi_mask = mask_uint8[y:y+bh, x:x+bw]
    cx, cy = click_xy
    rcx, rcy = cx - x, cy - y

    # Edges in ROI (masked)
    gray = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(gray, 50, 150)
    edges[roi_mask == 0] = 0

    # Hough lines (prefer near-vertical)
    lines = cv2.HoughLinesP(
        edges, 1, np.pi / 180,
        threshold=max(60, int(0.05 * (bw + bh))),
        minLineLength=max(20, int(0.25 * bh)),
        maxLineGap=10
    )

    chosen = None
    best_metric = (1e9, 0)  # (distance to click, vertical_span)

    if lines is not None:
        for L in lines:
            x1, y1, x2, y2 = L[0]
            # angle to horizontal
            angle = abs(math.degrees(math.atan2(y2 - y1, x2 - x1)))
            # keep moderately vertical lines
            if angle < 45:  # too horizontal
                continue

            dist, _ = _line_point_dist(rcx, rcy, x1, y1, x2, y2)
            vertical_span = abs((y2 - y1))
            metric = (dist, -vertical_span)  # prefer closer, then longer
            if metric < best_metric:
                best_metric = metric
                chosen = (x1, y1, x2, y2)

    if chosen is None:
        # fallback: vertical scan near click
        top, bottom = _vertical_fallback(roi_mask, (rcx, rcy))
        if top is None:
            return None, {"slanted_m": None, "vertical_m": None, "floors": None}
        p1 = (top[0] + x, top[1] + y)
        p2 = (bottom[0] + x, bottom[1] + y)
    else:
        x1, y1, x2, y2 = chosen
        # extend within mask to boundary for cleaner endpoints
        (ex1, ey1), (ex2, ey2) = _extend_within_mask(roi_mask, (x1, y1), (x2, y2))
        p1 = (ex1 + x, ey1 + y)
        p2 = (ex2 + x, ey2 + y)

        # order by y so p_top has smaller y
        if p1[1] > p2[1]:
            p1, p2 = p2, p1

    # Measurements
    slanted_px = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
    vertical_px = abs(p2[1] - p1[1])

    slanted_m = slanted_px / ppm
    vertical_m = vertical_px / ppm
    floors = max(1, int(round(vertical_m / ASSUMED_FLOOR_HEIGHT_M)))

    return (p1, p2), {"slanted_m": slanted_m, "vertical_m": vertical_m, "floors": floors}
