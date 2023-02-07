import cv2

# Create a VideoCapture object
cap = cv2.VideoCapture(0)
# Capture a frame
ret, frame = cap.read()
# Convert the frame to grayscale
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Apply a threshold to the frame
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Find the contours of the arrow
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Load the two Haar cascades
right_cascade = cv2.CascadeClassifier('/home/devanshu/Downloads/rpi-car-arrow-detection-using-cascade-classifier-master/haar_trained_xml/right/cascade.xml')
left_cascade = cv2.CascadeClassifier('/home/devanshu/Downloads/rpi-car-arrow-detection-using-cascade-classifier-master/haar_trained_xml/left/cascade.xml')

# Iterate over the contours and use the detectMultiScale function to detect the right and left arrows using the two Haar cascades.
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    right_arrows = right_cascade.detectMultiScale(gray[y:y+h, x:x+w])
    left_arrows = left_cascade.detectMultiScale(gray[y:y+h, x:x+w])

# Draw bounding boxes around the arrows
for (x, y, w, h) in right_arrows:
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
for (x, y, w, h) in left_arrows:
    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

# Display the frame
cv2.imshow("Arrow Detection", frame)
cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()
