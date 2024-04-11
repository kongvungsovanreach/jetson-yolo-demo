import cv2
import time
import os
import requests
import threading

def upload_video(filepath, api_url="http://localhost:9001/upload"):
  """
  Uploads a video file to the specified API endpoint.

  Args:
      filepath (str): Path to the video file.
      api_url (str, optional): URL of the upload API. Defaults to "http://localhost:5000/upload".

  Returns:
      bool: True if upload was successful, False otherwise.
  """
  def upload_worker():
    try:
      files = {'file': open(filepath, 'rb')}  # Open video file in binary mode
      response = requests.post(api_url, files=files)
      response.raise_for_status()  # Raise exception for non-2xx response codes
      print(response.text)
      print(f"Successfully uploaded video: {os.path.basename(filepath)}")
    except requests.exceptions.RequestException as e:
      print(f"Error uploading video {filepath}: {e}")

  # Create and start a thread for upload
  upload_thread = threading.Thread(target=upload_worker)
  upload_thread.daemon = True  # Set thread as daemon to avoid blocking program exit
  upload_thread.start()


def record_webcam(output_dir="webcam_recordings", fps=24):
  """
  Records video from webcam and saves it as a file every 10 minutes.

  Args:
      output_dir (str, optional): Directory to save the video files. 
          Defaults to "webcam_recordings".
      fps (int, optional): Frames per second for video recording. 
          Defaults to 24.
  """

  # Create output directory if it doesn't exist
  os.makedirs(output_dir, exist_ok=True)

  # Capture video from webcam
  cap = cv2.VideoCapture(0)

  # Get frame width and height
  width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

  # Define video codec
  fourcc = cv2.VideoWriter_fourcc(*"XVID")  # You can change the codec here (e.g., "MJPG")

  # Variable to store start time of each recording
  start_time = time.time()
  video_file_count = 1
  video_writer = None
  prev_saved_file = None
  while True:
    ret, frame = cap.read()

    if ret:
      # Display frame
      cv2.imshow("Video recording", frame)

      # Check for 10 minute interval and create new video writer
      current_hour = int(time.strftime('%H'))
      if (time.time() - start_time > 60  # 60 seconds * 10 minutes
          and 8 <= current_hour < 18):  # 60 seconds * 10 minutes
        start_time = time.time()
        video_file_count += 1

        # Generate video filename with timestamp
        filename = os.path.join(output_dir, f"recording_{time.strftime('%Y-%m-%d_%H-%M-%S')}.avi")

        # Create video writer object
        video_writer = cv2.VideoWriter(filename, fourcc, fps, (width, height))
        # filepath = os.path.join(output_dir, filename)
        if prev_saved_file is not None:
            print(prev_saved_file)
            #upload_video(prev_saved_file)
            print(f'[msg]: video file saved. Count: {video_file_count}')
        prev_saved_file = filename
      # Write frame to video
      if video_writer is not None:
        video_writer.write(frame)

      # Exit on 'q' press
      if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    else:
      break

  # Release resources
  cap.release()
  video_writer.release()
  cv2.destroyAllWindows()

#starting point of the application
if __name__ == "__main__":
    record_webcam()