from PIL import Image

from app.tiler import ImageTiler


def test_tiler_covers_image_bounds():
    image = Image.new("RGB", (2000, 4000))
    tiles = ImageTiler(rows=4, columns=1, overlap=0.1).create_tiles(
        image, worker_count=4
    )

    assert tiles
    assert tiles[0].left == 0
    assert tiles[0].top == 0
    assert tiles[-1].right == 2000
    assert tiles[-1].bottom == 4000
