import os
import cv2
from PIL import Image


def detect(filename, size=(128, 128), cascade_file="lbpcascade_animeface.xml"):
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)

    try:
        cascade = cv2.CascadeClassifier(cascade_file)
        image = cv2.imread(filename, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        faces = cascade.detectMultiScale(gray,
                                         # detector options
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(16, 16))

        faces_windows = []
        for (x, y, w, h) in faces:
            face = image[y: y + h + 1, x: x + w + 1]
            print('size: {},{}'.format(w, h))
            # cv2.imshow('face', face)
            # a:97, b:98
            # key = cv2.waitKey(0)
            reshaped = cv2.resize(face, dsize=size, interpolation=cv2.INTER_CUBIC)
            faces_windows.append(reshaped)

            # if key == 97:
            #     reshaped = cv2.resize(face, dsize=size, interpolation=cv2.INTER_CUBIC)
            #     faces_windows.append(reshaped)
            #     print('stacked this window')
            # else:
            #     print('not like as a face')
    except:
        print('{} unloaded.'.format(filename))
        return None

    return faces_windows


def test():
    key = cv2.waitKey(0)
    print(key)


if __name__ == '__main__':
    SAVE_DIR = 'million_faces/'
    CARD_DIR = '_card/'
    dirs = os.listdir(CARD_DIR)
    count = len(os.listdir(SAVE_DIR)) + 1
    for dir in dirs:
        imgs = os.listdir(CARD_DIR + dir)
        for img_name in imgs:
            faces = detect(CARD_DIR + dir + '/' + img_name, size=(64, 64))

            if faces is None:
                continue

            for face in faces:
                cv2.imwrite(SAVE_DIR + 'face_{}.png'.format(count), face)
                print('saved face_{}.png'.format(count))
                count += 1
