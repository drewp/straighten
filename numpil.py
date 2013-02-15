import Numeric
import FFT
import Tkinter
import Image
import ImageTk
import sys

w = 256
h = 256

if __name__ == '__main__':
    data = Numeric.arrayrange(w*h)
    data = data.astype('l')

    im = Image.new("RGBA", (w, h))
    print len(data.tostring())
    print len(im.tostring())
    im.fromstring(data.tostring())

    root = Tkinter.Tk()
    image = ImageTk.PhotoImage(im)
    x = Tkinter.Label(root, image=image)
    x.pack()

    root.mainloop()
