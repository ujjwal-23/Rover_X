import cv2
# Load the Haar cascade classifiers for arrow detection
right_cascade = cv2.CascadeClassifier("/home/devanshu/Downloads/rpi-car-arrow-detection-using-cascade-classifier-master/haar_trained_xml/right/cascade.xml")
left_cascade = cv2.CascadeClassifier("/home/devanshu/Downloads/rpi-car-arrow-detection-using-cascade-classifier-master/haar_trained_xml/left/cascade.xml")

# Create a VideoCapture object to access the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_gauss = cv2.GaussianBlur(gray, (9,9), cv2.BORDER_DEFAULT)
    #test = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 255, 0)
    test1 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    edged = cv2.Canny(gray_gauss, 50, 150)
    # Detect right arrows in the frame
    right_arrows = right_cascade.detectMultiScale(edged)

    # Detect left arrows in the frame
    left_arrows = left_cascade.detectMultiScale(edged)

    # Draw rectangles around the detected right arrows
    for (x, y, w, h) in right_arrows:
        cv2.rectangle(edged, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(edged, "Right", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    # Draw rectangles around the detected left arrows
    for (x, y, w, h) in left_arrows:
        cv2.rectangle(edged, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(edged, "Left", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Show the frame with the arrow detection
    cv2.imshow("Edge Detection", edged)
    cv2.imshow("Arrow Detection", frame)
    cv2.imshow("Gaussian Blur", gray_gauss)


    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object
cap.release()
cv2.destroyAllWindows()
