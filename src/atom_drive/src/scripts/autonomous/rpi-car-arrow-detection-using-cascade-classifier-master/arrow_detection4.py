import cv2

# Load the trained AI model
model = load_model('arrow_detection_model.h5')

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()

    # Pre-process the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    # Use the trained AI model to detect the arrow
    arrow = model.predict(thresh)

    # Draw a bounding box around the detected arrow
    x, y, w, h = arrow
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the arrow's direction on the frame
    if arrow_direction == 'left':
        cv2.putText(frame, 'Left', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    else:
        cv2.putText(frame, 'Right', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Arrow Detection', frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()
