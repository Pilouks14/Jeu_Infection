import tkinter as tk


class DragDropMixin:
	"""https://stackoverflow.com/questions/37280004/drag-and-drop-widgets-tkinter"""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.drag_start_x = 0
		self.drag_start_y = 0
		self.drag_stop_x = 0
		self.drag_stop_y = 0
		self.bind("<Button-1>", self.drag_start)
		self.bind("<B1-Motion>", self.drag_motion)
		self.bind("<ButtonRelease-1>", self.drag_stop)

	def drag_start(self, event):
		self.drag_start_x = event.x
		self.drag_start_y = event.y

	def drag_motion(self, event):
		x = self.winfo_x() - self.drag_start_x + event.x
		y = self.winfo_y() - self.drag_start_y + event.y
		self.place(x=x, y=y)

	def drag_stop(self, event):
		x = self.winfo_x() - self.drag_start_x + event.x
		y = self.winfo_y() - self.drag_start_y + event.y
		self.drag_stop_x = event.x
		self.drag_stop_y = event.y
		self.place(x=x, y=y)


class DnDFrame(DragDropMixin, tk.Frame):
    pass


main = tk.Tk()
main.attr
main.attributes("-transparentcolor", "blue")
notesFrame = DnDFrame(main, bd=4, bg="grey")
notesFrame.place(x=10, y=10)
canvas = tk.Canvas(notesFrame)
canvas.configure(bg="blue")
canvas.pack()

canvas.create_line(4, 4, 90, 160, fill="red", width=8)
main.mainloop()
