import cv2


def test():
    cv2.destroyAllWindows()
    for i in range(0, 10):
        cap = cv2.VideoCapture(i)
        ret, frame = cap.read()
        cap.release()
        print(ret)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    test()
