"""Enroll a dog: build its reference fingerprints from photos, a video, or the ESP32-CAM itself.

  From a folder of photos:   .venv\\Scripts\\python.exe tools\\enroll.py --dog biscuit --photos D:\\photos\\biscuit
  From a phone video:        .venv\\Scripts\\python.exe tools\\enroll.py --dog biscuit --video D:\\videos\\biscuit.mp4
  From the camera:           .venv\\Scripts\\python.exe tools\\enroll.py --dog biscuit --camera 192.168.43.120 --count 15

Other options: --gallery FOLDER (default D:\\kibbly_data\\galleries\\demo), --list, --remove DOG.
Enrolling a dog again replaces its references.
"""

import argparse
import pathlib
import time

from PIL import Image

from common import DEFAULT_GALLERY, fetch_photo, load_gallery, load_models, save_gallery, session_folder

PHOTO_TYPES = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def from_folder(folder):
    paths = sorted(p for p in pathlib.Path(folder).iterdir() if p.suffix.lower() in PHOTO_TYPES)
    return [Image.open(p).convert("RGB") for p in paths]


def from_camera(ip, count):
    folder = session_folder("enroll")
    images = []
    print(f"Taking {count} photos, one every 0.7 s. Move the dog or the camera a little between photos.")
    for i in range(count):
        image, data, _ = fetch_photo(ip)
        (folder / f"enroll_{i + 1:02d}.jpg").write_bytes(data)
        images.append(image)
        print(f"   photo {i + 1}/{count}", flush=True)
        time.sleep(0.7)
    print(f"Saved in {folder}")
    return images


def main():
    parser = argparse.ArgumentParser(description="Enroll a dog for recognition tests.")
    parser.add_argument("--dog", help="short id, for example biscuit")
    parser.add_argument("--name", help="display name (default: the id with a capital letter)")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--photos", help="folder of photos of this dog")
    source.add_argument("--video", help="short video of this dog")
    source.add_argument("--camera", help="ESP32-CAM IP address")
    parser.add_argument("--count", type=int, default=15, help="photos to take with --camera")
    parser.add_argument("--keep", type=int, default=12, help="references kept per dog")
    parser.add_argument("--gallery", default=str(DEFAULT_GALLERY))
    parser.add_argument("--list", action="store_true", help="show the enrolled dogs")
    parser.add_argument("--remove", help="remove a dog from the gallery")
    args = parser.parse_args()

    folder = pathlib.Path(args.gallery)
    gallery, names = load_gallery(folder)
    if args.list or args.remove:
        if args.remove:
            gallery.remove(args.remove)
            names.pop(args.remove, None)
            save_gallery(gallery, names, folder)
            print(f"Removed {args.remove}")
        for dog_id in gallery.dog_ids:
            print(f"   {dog_id}: {names.get(dog_id, dog_id)}, {gallery.reference_count(dog_id)} references")
        if not gallery.dog_ids:
            print("   No dog enrolled yet.")
        return
    if not args.dog or not (args.photos or args.video or args.camera):
        parser.error("give --dog and one of --photos, --video or --camera")

    if args.photos:
        images = from_folder(args.photos)
    elif args.video:
        from kibbly_ai.perception.enrollment import sample_video_frames
        images = sample_video_frames(args.video)
    else:
        images = from_camera(args.camera, args.count)
    print(f"{len(images)} image(s) to check. Loading the models (about 20 s the first time)")

    from kibbly_ai.perception.enrollment import build_references
    detector, scene, embedder = load_models()
    vectors, report = build_references(images, detector, embedder, k=args.keep, scene=scene,
                                       min_dog_confidence=0.35)
    print(f"Usable photos: {report['usable']}, kept as references: {report['kept']}, dropped: {report['dropped']}")
    if report["kept"] < 3:
        print("Not enough usable photos (at least 3). Use sharper photos with one dog clearly visible.")
        return
    folder.mkdir(parents=True, exist_ok=True)
    gallery.enroll(args.dog, vectors)
    names[args.dog] = args.name or args.dog.capitalize()
    save_gallery(gallery, names, folder)
    print(f"Enrolled {names[args.dog]} ({args.dog}) in {folder}. Dogs now: {', '.join(gallery.dog_ids)}")


if __name__ == "__main__":
    main()
