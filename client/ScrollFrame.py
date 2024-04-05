import tkinter as tk
import tkinter.ttk as ttk


class VerticalScrolledFrame(ttk.Frame):
    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)

        # *Cree un objeto de lienzo y una barra de desplazamiento vertical para desplazarlo.
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        self.canvas = tk.Canvas(
            self, bd=0, highlightthickness=0, bg="red", yscrollcommand=vscrollbar.set
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=self.canvas.yview)

        # *Restablecer la vista
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # *Crea un marco dentro del lienzo que se desplazará con él.
        self.interior = tk.Frame(self.canvas, bg="black")
        self.interior.bind("<Configure>", self._configure_interior)
        self.canvas.bind("<Configure>", self._configure_canvas)
        self.interior_id = self.canvas.create_window(
            0, 0, window=self.interior, anchor=tk.NW
        )

    def _configure_interior(self, event):
        # *Actualice las barras de desplazamiento para que coincidan con el tamaño del marco interior.
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion=(0, 0, size[0], size[1]))
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # *Actualice el ancho del lienzo para que se ajuste al marco interior.
            self.canvas.config(width=self.interior.winfo_reqwidth())

    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # *Actualice el ancho del marco interior para llenar el lienzo.
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())
