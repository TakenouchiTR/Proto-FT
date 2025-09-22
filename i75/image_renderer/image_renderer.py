import settings

class ImageRenderer():
    def render_pixels(self, pixels: list[list[tuple[int,int,int]]]):
        pass

    def render_bytes(self, data: bytes):
        pixels: list[list[tuple[int,int,int]]] = []
        for i in range(settings.MATRIX_HEIGHT):
            row = []
            for j in range(settings.MATRIX_WIDTH):
                r = data[i * settings.MATRIX_WIDTH * 3 + j * 3]
                g = data[i * settings.MATRIX_WIDTH * 3 + j * 3 + 1]
                b = data[i * settings.MATRIX_WIDTH * 3 + j * 3 + 2]
                row.append((r, g, b))
            pixels.append(row)
        self.render_pixels(pixels)