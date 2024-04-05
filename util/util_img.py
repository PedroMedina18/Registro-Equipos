from PIL import ImageTk, Image


# funcion creada para manejar las imagenes se manda la imagen y el tamaño usando la libreria Pillow
def leer_imagen(path, size):
    return ImageTk.PhotoImage(Image.open(path).resize(size, Image.ADAPTIVE))
