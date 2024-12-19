import csv
import pyzed.sl as sl

# times are expressed in seconds
TIMESTEP = 0.1
TOTAL_TIME = 60


def main2():
    # Create a camera object
    zed = sl.Camera()

    # Define initialization parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD720
    init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE
    init_params.coordinate_units = sl.UNIT.METER
    init_params.sdk_verbose = 1

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print("Camera Open : " + repr(err) + ". Exit Program")
        exit()

    # Define body tracking parameters
    body_params = sl.BodyTrackingParameters()
    body_params.body_format = sl.BODY_FORMAT.BODY_34
    body_params.detection_model = sl.BODY_TRACKING_MODEL.HUMAN_BODY_FAST
    body_params.enable_tracking = True
    body_params.enable_segmentation = False
    body_params.enable_body_fitting = True # WARNING: computationally heavier

    # Define positional tracking parameters if enabled
    if body_params.enable_tracking:
        positional_tracking_param = sl.PositionalTrackingParameters()
        positional_tracking_param.set_floor_as_origin = True
        zed.enable_positional_tracking(positional_tracking_param)

    # Load body tracking module
    print("Body tracking: loading module...")
    err = zed.enable_body_tracking(body_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print("Enable Body Tracking : " + repr(err) + ". Exit program.")
        zed.close()
        exit()

    # Define body tracking parameters
    bodies = sl.Bodies()
    body_runtime_param = sl.BodyTrackingRuntimeParameters()
    body_runtime_param.detection_confidence_threshold = 40

    current_time = 0
    with open('dataset.csv', 'a', newline='') as f:
        f.writerow(['timestep', 'ID', 'pos.x', 'pos.y', 'pos.z'])
        while current_time < TOTAL_TIME:
            if zed.grab() == sl.ERROR_CODE.SUCCESS:
                err = zed.retrieve_bodies(bodies, body_runtime_param)
                if bodies.is_new:
                    body_array = bodies.body_list
                    if len(body_array) > 0:
                        data = []
                        data.append(current_time)
                        data.append(body.id)
                        # data.append(body_array[0])
                        data.extend(first_body.position)
                        f.writerow(data)
            time.sleep(TIMESTEP)
            current_time += TIMESTEP
        f.close()

    # Close the camera
    zed.disable_body_tracking()
    zed.close()



if __name__ == "__main__":
    main()


