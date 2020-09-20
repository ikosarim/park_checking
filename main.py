import cv2
import Camera as camera
import Contours as cont

if __name__ == '__main__':
    cam = camera.Camera("rtsp://admin:admin@185.76.82.115:9853/0")
    main_contour = cont.Contours()

    while (True):
        frame = cam.read()
        frame = main_contour.print_main_contour(frame)
        cv2.imshow("Src", frame)
        main_contour.create_main_contour()

        if main_contour.get_ready_to_crop:
            print("Hello!")

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
