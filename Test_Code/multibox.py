import ttk
import Tkinter as tk

win = tk.Tk()
win.resizable(width=0, height=0)

tree = ttk.Treeview(win, selectmode='browse')
tree.pack(side='left')

vsb = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
vsb.pack(side='right', fill='y')

tree.configure(yscrollcommand=vsb.set)

tree["columns"] = ("1", "2")
tree['show'] = 'headings'
tree.column("1", width=100, anchor='c')
tree.column("2", width=100, anchor='c')
tree.heading("1", text="Account")
tree.heading("2", text="Type")
tree.insert("",'end',text="L1",values=("Big1","Best"))
tree.insert("",'end',text="L2",values=("Big2","Best"))
tree.insert("",'end',text="L3",values=("Big3","Best"))
tree.insert("",'end',text="L4",values=("Big4","Best"))
tree.insert("",'end',text="L5",values=("Big5","Best"))
tree.insert("",'end',text="L6",values=("Big6","Best"))
tree.insert("",'end',text="L7",values=("Big7","Best"))
tree.insert("",'end',text="L8",values=("Big8","Best"))
tree.insert("",'end',text="L9",values=("Big9","Best"))
tree.insert("",'end',text="L10",values=("Big10","Best"))
tree.insert("",'end',text="L11",values=("Big11","Best"))
tree.insert("",'end',text="L12",values=("Big12","Best"))

win.mainloop()