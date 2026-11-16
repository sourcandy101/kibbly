# ESP32-CAM camera test program

A test tool for the AI, not the feeder firmware. The ESP32-CAM joins WiFi and serves photos, so the AI scripts in `ai_v2/tools/` can test recognition with the real camera.

| Address | Answer |
|---|---|
| `http://<ip>/` | Short help |
| `http://<ip>/status` | JSON: IP, WiFi signal, frame size, free memory, uptime |
| `http://<ip>/capture` | A fresh 640 x 480 JPEG. `?flash=1` lights the white LED for the photo |

Compiled and checked on 16 November 2026 (RAM 15%, flash 27%).

## Steps

1. **WiFi:** turn on your phone hotspot in **2.4 GHz** (the ESP32 cannot join 5 GHz). Connect the laptop to the same hotspot. Campus WiFi often blocks devices from talking to each other, so use the hotspot.
2. **Secrets:** copy `include/secrets.example.h` to `include/secrets.h` and write the hotspot name and password. `secrets.h` is never pushed to GitHub.
3. **Wire** circuit 6: `hardware/circuits_by_part/06_esp32_cam_flashing/README.md` (DevKit and ESP32-CAM, USB unplugged while wiring).
4. **Open this folder** in VS Code with PlatformIO (File, Open Folder, `firmware/esp32_camera_test`).
5. **Upload:** IO0 on GND, press RST on the ESP32-CAM, click Upload (arrow in the bottom bar).
6. **Run:** remove the IO0 wire, press RST, open the Serial Monitor (plug icon, 115200). You should see:

```
Kibbly camera test starting
Camera ready (640 x 480 JPEG)
Joining WiFi "your_hotspot"....
WiFi connected, signal -48 dBm
Ready. On the laptop: python tools\camera_check.py --ip 192.168.43.120
```

7. **Check in a browser:** open `http://<ip>/capture`. You should see a photo. Then go to `ai_v2/tools/README.md`.

## If it fails

| Sign | Fix |
|---|---|
| `Camera start failed, error 0x...` | Ribbon cable of the camera not fully in: open the small latch, push the cable in, close the latch |
| `WiFi failed` | Name or password in `secrets.h`, hotspot set to 2.4 GHz, phone close to the board |
| `Brownout detector was triggered` | Weak 5 V: another USB port or a shorter cable (see circuit 6) |
| Browser cannot open the IP | Laptop not on the same hotspot |
| Dark photos | Use `?flash=1`, or add light: the feeder bowl area should be lit |
