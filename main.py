from src.image import Image
from src.camera import Camera
from src.triangle import Triangle
from src.vector3d import Vector3d
from src.color import Color
from src.imageio import export_image

def generate_image(cam: Camera, tri: Triangle):
    t = [None]
    barycentric_coord = [None]
    result = Image(cam.width(), cam.height())

    for y in range(result.height()):
        for x in range(result.width()):
            r = cam(x, y)

            hit = tri.intersect(r, barycentric_coord, t)

            if hit:
                result[(x, y)] = Color(barycentric_coord[0][0], barycentric_coord[0][1], barycentric_coord[0][2])
            else:
                result[(x, y)] = Color(0.0, 0.0, 0.0)
    
    return result

def main():
    cam = Camera(Vector3d(0.0, 0.0, 0.0), Vector3d(0.0, 0.0, -1.0), Vector3d(0.0, 1.0, 0.0), 60.0, 512, 512)

    print("Generating image 1")
    t1 = Triangle(Vector3d(1.0, -1.0, -2.0), Vector3d(0.0, 1.0, -2.0), Vector3d(-1.0, -1.0, -2.0))
    result1 = generate_image(cam, t1)
    export_image("result1.ppm", result1)

    print("Generating image 2")
    t2 = Triangle(Vector3d(1.0, -1.0, 2.0), Vector3d(0.0, 1.0, 2.0), Vector3d(-1.0, -1.0, 2.0))
    result2 = generate_image(cam, t2)
    export_image("result2.ppm", result2)

    print("Generating image 3")
    t3 = Triangle(Vector3d(-1.0, -1.0, -2.0), Vector3d(1.0, -1.0, -2.0), Vector3d(0.0, 1.0, -2.0))
    result3 = generate_image(cam, t3)
    export_image("result3.ppm", result3)

    print("Generating image 4")
    t4 = Triangle(Vector3d(-1.0, -1.0, 2.0), Vector3d(0.0, 1.0, 2.0), Vector3d(1.0, -1.0, 2.0))
    result4 = generate_image(cam, t4)
    export_image("result4.ppm", result4)

    print("Generating image 5")
    t5 = Triangle(Vector3d(-1.0, -1.0, -1.0), Vector3d(1.0, -1.0, -1.0), Vector3d(1.0, 1.0, -1.0))
    result5 = generate_image(cam, t5)
    export_image("result5.ppm", result5)

    print("Generating image 6")
    t6 = Triangle(Vector3d(-1.0, 2.0, -1.0), Vector3d(0.0, 2.0, 1.0), Vector3d(1.0, 2.0, -1.0))
    result6 = generate_image(cam, t6)
    export_image("result6.ppm", result6)

    print("Finished")

if __name__ == "__main__":
    main()