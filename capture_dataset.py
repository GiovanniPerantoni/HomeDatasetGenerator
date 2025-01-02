import csv
import time
import pyzed.sl as sl
import config as cfg


def main():
    # Create a camera object
    zed = sl.Camera()


    # Open the camera
    err = zed.open(cfg.init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print("Camera Open : " + repr(err) + ". Exit Program")
        exit()

    # Enable positional tracking
    if cfg.body_params.enable_tracking:
        zed.enable_positional_tracking(cfg.positional_tracking_param)

    # Load body tracking module
    print("Body tracking: loading module...")
    err = zed.enable_body_tracking(cfg.body_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print("Enable Body Tracking : " + repr(err) + ". Exit program.")
        zed.close()
        exit()

    current_time = 0
    with open('dataset.csv', 'w', newline='') as f:
        f_writer = csv.writer(f, delimiter=',')
        labels = ['timestep', 'ID', 'pos.x', 'pos.y', 'pos.z']
        for key in cfg.JOINT_DICT:
            if cfg.JOINT_DICT[key][1]:
               labels.append(cfg.JOINT_DICT[key][0]) 
        f_writer.writerow(labels)
        f.flush()

        print("Starting record in:")
        print(" 3")
        time.sleep(1)
        print(" 2")
        time.sleep(1)
        print(" 1")
        time.sleep(1)
        print("Recording...")

        start = time.time()
        # TODO: test timestep fraction
        while (cfg.TOTAL_TIME-current_time) > (cfg.TIMESTEP/1000):
            # TODO: move to standalone function
            if zed.grab() == sl.ERROR_CODE.SUCCESS:
                err = zed.retrieve_bodies(bodies, body_runtime_param)
                if cfg.bodies.is_new:
                    body_array = bodies.body_list
                    if len(body_array) > 0:
                        first_body = body_array[0]
                        data = []
                        data.append(current_time)
                        data.append(first_body.id)
                        data.extend(first_body.position)
                        for key in cfg.JOINT_DICT:
                            if cfg.JOINT_DICT[key][1]:
                                data.append(first_body.keypoint[key])
                        f_writer.writerow(data)
                        f.flush()
            print(current_time)
            current_time += cfg.TIMESTEP
            while (time.time()-start < current_time):
                pass
        end = time.time()
        f.close()

    # Close the camera
    zed.disable_body_tracking()
    zed.close()

    print("Elapsed: ", end-start)



if __name__ == "__main__":
    main()


