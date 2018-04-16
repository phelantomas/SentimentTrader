import ttk
import Tkinter as tk

win = tk.Tk()
win.resizable(width=0, height=0)

tree = ttk.Treeview(win, selectmode='browse')
tree.pack(side='left')

vsb = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
vsb.pack(side='right', fill='y')

tree.configure(yscrollcommand=vsb.set)

tree["columns"] = ("1", "2", "3")
tree['show'] = 'headings'
tree.column("1", width=100, anchor='c')
tree.column("2", width=110, anchor='c')
tree.column("3", width=100, anchor='c')
tree.heading("1", text="Time")
tree.heading("2", text="Tweet")
tree.heading("3", text="Sentiment")
tree.insert("",'end',text="L1",values=("4am","Best in the world", ".4"))
tree.insert("",'end',text="L1",values=("5am","Best in the world", ".4"))
tree.insert("",'end',text="L1",values=("6am","Best in the world", ".4"))
tree.insert("",'end',text="L1",values=("7am","Best in the world", ".4"))
tree.insert("",'end',text="L1",values=("8am","Best in the world", ".4"))
tree.insert("",'end',text="L1",values=("9am","Best in the world", ".4"))
tree.insert("",'end',text="L1",values=("10am","Best in the world", ".4"))
tree.insert("",'end',text="L1",values=("11am","Best in the world", ".4"))
tree.insert("",'end',text="L1",values=("12am","Best in the world", ".4"))
tree.insert("",'end',text="L1",values=("13pm","Best in the world", ".4"))
tree.insert("",'end',text="L1",values=("14pm","Best in the world", ".4"))

win.mainloop()