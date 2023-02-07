from rmn import RMN
import cv2
m=RMN()
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    results = m.detect_emotion_for_single_frame(frame)
#    print(results[emo_label])
    frame = m.draw(frame,results)
    cv2.imshow("imh",frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

#intellisense