import Tkinter
import csv

root = Tkinter.Tk()

# open file
with open("btcFeature.csv") as file:
   reader = csv.reader(file)

   # r and c tell us where to grid the labels
   r = 0
   for col in reader:
      c = 0
      for row in col:
         # i've added some styling
         label = Tkinter.Label(root, width = 10, height = 2, \
                               text = row, relief = Tkinter.RIDGE)
         label.grid(row = r, column = c)
         c += 1
      r += 1

root.mainloop()