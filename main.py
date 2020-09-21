import cv2
import Camera as camera
import Contours as cont
import ParkingRois as park_roi

if __name__ == '__main__':
    cam = camera.Camera("rtsp://admin:admin@185.76.82.115:9853/0")
    main_contour = cont.Contours()
    parking_rois = park_roi.ParkingRois()

    while (True):
        frame = cam.read()
        frame = main_contour.print_main_contour(frame)
        cv2.imshow("Src", frame)
        main_contour.create_main_contour()

        if main_contour.get_ready_to_crop:
            main_roi = main_contour.crop_and_mask_main_contour(frame)

            main_roi = parking_rois.print_parking_rois(main_roi)
            cv2.imshow("Main_roi", main_roi)
            parking_rois.create_parking_rois()

            if parking_rois.get_ready:
                parking_rois.get_final_frame(main_roi)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break