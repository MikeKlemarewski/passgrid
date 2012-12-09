import cv2 as cv


def template_match(_img, _template):
    img = cv.imread(_img, 1)
    template = cv.imread(_template, 1)

    # Flip template, because pic from webcam will be backwards
    template = cv.flip(template,1)

    result = cv.matchTemplate(img,template, cv.TM_CCORR_NORMED)
    result8 = cv.normalize(result,None,0,255,cv.NORM_MINMAX,cv.CV_8U)

    minVal,maxVal,minLoc,maxLoc = cv.minMaxLoc(result)

    return maxVal > 0.73
