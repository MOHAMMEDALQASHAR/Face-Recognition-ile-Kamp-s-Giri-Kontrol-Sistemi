import cv2

def list_ports():
    is_working = True
    dev_port = 0
    working_ports = []
    while is_working:
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            is_working = False
            print(f"Port {dev_port} is not working.")
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if is_reading:
                print(f"Port {dev_port} is working and reads images ({w}x{h})")
                working_ports.append(dev_port)
            else:
                print(f"Port {dev_port} is present but not reading.")
            camera.release()
        dev_port += 1
        if dev_port > 5: # Limit search
            break
    return working_ports

print("Checking camera ports...")
ports = list_ports()
print(f"Available ports: {ports}")
