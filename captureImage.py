import time
import cv2

if __name__ == "__main__":
    # Camera configuration
    cap = cv2.VideoCapture(1)
    count = 0
    
    while True:
        ret, image = cap.read()
        cv2.imshow("Capture", image)
        key =  cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            cv2.imwrite('image/{}.png'.format(count), image)
            count+=1
    
    cap.release()
    cv2.destroyAllWindows()