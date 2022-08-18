import tkinter as tk

def tick_box_window():
    def change_bool():
        global show_steps
        if var.get() == 1:
            show_steps = True
        else:
            show_steps = False
    def close_window():
        global show_steps_choosed
        show_steps_choosed = True
        root.destroy()
    root = tk.Tk()
    root.title('A* path finder')
    root.geometry('230x100')
    text = tk.Label(text='Would you like to see the steps?',width=30,height=3)
    text.grid(row=0,column=0,sticky='nsew')
    var = tk.IntVar()
    checkbutton = tk.Checkbutton(root,text='Show steps',variable=var,onvalue=1,offvalue=0,command=change_bool)
    checkbutton.grid(row=1,column=0,sticky='nsew')
    button = tk.Button(text='Done',command=close_window,width=25)
    button.grid(row=2,column=0)
    root.mainloop()


