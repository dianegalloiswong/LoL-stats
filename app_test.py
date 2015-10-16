import tkinter
# import tkinter.messagebox
# tkinter.messagebox.showerror("Error","Invalid number of topics")


# http://sebsauvage.net/python/gui/
class simpleapp_tk(tkinter.Tk):
    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        self.entryVariable = tkinter.StringVar()
        self.entry = tkinter.Entry(self, textvariable=self.entryVariable)
        self.entry.grid(column=0, row=0, sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter text here.")

        button = tkinter.Button(self, text=u"Click me !",
                                command=self.OnButtonClick)
        button.grid(column=1, row=0)

        self.labelVariable = tkinter.StringVar()
        label = tkinter.Label(self, textvariable=self.labelVariable,
                              anchor="w", fg="white", bg="blue")
        label.grid(column=0, row=1, columnspan=2, sticky='EW')
        self.labelVariable.set(u"Hello !")

        self.grid_columnconfigure(0, weight=1)
        self.resizable(True, False)
        self.update()
        self.geometry(self.geometry())
        self.entry.focus_set()
        self.entry.selection_range(0, tkinter.END)

    def OnButtonClick(self):
        self.labelVariable.set(self.entryVariable.get() + " (You clicked the button)")
        self.entry.focus_set()
        self.entry.selection_range(0, tkinter.END)

    def OnPressEnter(self, event):
        self.labelVariable.set(self.entryVariable.get() + " (You pressed ENTER)")
        self.entry.focus_set()
        self.entry.selection_range(0, tkinter.END)


"""
app = simpleapp_tk(None)
app.title('my application')
app.mainloop()
"""




b_app = True

class InvalidValueException(Exception):
    def __init__(self, name, entry, lbound=None, ubound=None):
        if lbound is not None:
            msg_end = 'should be at least {}'.format(lbound)
        elif ubound is not None:
            msg_end = 'should be at most {}'.format(ubound)
        else:
            msg_end = "should be an integer"
        self.message = "Invalid {}: {}.".format(name,msg_end)
        self.entry = entry

def get_int_from_StringVar(stringvar,name=None,entry=None,lbound=None,ubound=None):
    try:
        n = int(stringvar.get())
        if lbound is not None and n < lbound:
            raise InvalidValueException(name, entry, lbound=lbound)
        if ubound is not None and n > ubound:
            raise InvalidValueException(name, entry, ubound=ubound)
        return n
    except ValueError:
        raise InvalidValueException(name,entry)


class App(tkinter.Tk):
    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent

        self.lda_frame = tkinter.Frame(self)
        self.lda_frame.grid()

        self.lda_label = tkinter.Label(self.lda_frame, text="LDA parameters")
        self.lda_label.grid(row=0,column=0,sticky='EW')

        self.lda_params_frame = tkinter.Frame(self.lda_frame)
        self.lda_params_frame.grid(row=1,column=0,sticky='EW')

        self.lda_n_topics_var = tkinter.StringVar()
        self.lda_n_topics_var.set("10")
        lda_n_topics_label = tkinter.Label(self.lda_params_frame, text="number of topics")
        lda_n_topics_label.grid(row=0,column=0)
        self.lda_n_topics_entry = tkinter.Entry(self.lda_params_frame,
                                                textvariable=self.lda_n_topics_var,
                                                width=3)
        self.lda_n_topics_entry.bind("<Return>", self.run_lda_callback)
        self.lda_n_topics_entry.grid(row=0,column=1)

        lda_button = tkinter.Button(self.lda_frame, text="Run LDA",
                                    command=self.run_lda)
        lda_button.grid(column=0, row=3)
        self.lda_run_label_var = tkinter.StringVar()
        self.lda_run_label = tkinter.Label(self.lda_frame, textvariable=self.lda_run_label_var)
        self.lda_run_label.grid(column=0, row=4,sticky='EW')

    def run_lda_callback(self,event):
        self.run_lda()

    def run_lda(self):
        try:
            n_topics = get_int_from_StringVar(self.lda_n_topics_var,
                                              name="number of topics",
                                              entry=self.lda_n_topics_entry,
                                              lbound=2, ubound=100)
            self.run_lda_with_args(n_topics)
        except InvalidValueException as e:
            self.lda_run_label_var.set(e.message)
            self.lda_run_label.config(fg="red")
            e.entry.focus_set()
            e.entry.selection_range(0, tkinter.END)
        # try:
        #     n_topics = int(self.lda_n_topics_var.get())
        #     self.lda_run_label_var.set('Running LDA with {} topics.'.format(n_topics))
        # except ValueError:
        #     self.lda_run_label_var.set("Invalid number of topics")
        #     self.lda_n_topics_entry.focus_set()
        #     self.lda_n_topics_entry.selection_range(0, tkinter.END)

    def run_lda_with_args(self,n_topics):
        self.lda_run_label_var.set('Running LDA with {} topics.'.format(n_topics))
        self.lda_run_label.config(fg="black")




def launch_app():
    app = App(None)
    app.title('App')
    app.mainloop()



class TestApp(tkinter.Tk):
    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        self.entryVariable = tkinter.StringVar()
        self.entry = tkinter.Entry(self, textvariable=self.entryVariable)
        self.entry.grid(column=0, row=0, sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter text here.")

        button = tkinter.Button(self, text=u"Click me !",
                                command=self.OnButtonClick)
        button.grid(column=1, row=0)

        self.labelVariable = tkinter.StringVar()
        label = tkinter.Label(self, textvariable=self.labelVariable,
                              anchor="w", fg="white", bg="blue")
        label.grid(column=0, row=1, columnspan=2, sticky='EW')
        self.labelVariable.set(u"Hello !")




        rbuttons = tkinter.Frame(self)
        rbuttons.grid(column=0,row=2)
        self.rvar = tkinter.IntVar()
        self.rlabelvar = tkinter.StringVar()
        r1 = tkinter.Radiobutton(rbuttons, text="Option1",
                                 variable=self.rvar, value=1,
                                 command=self.rselect)
        r1.grid(column=0,row=0)
        r2 = tkinter.Radiobutton(rbuttons, text="Option2",
                                 variable=self.rvar, value=2,
                                 command=self.rselect)
        r2.grid(column=0,row=1)
        r3 = tkinter.Radiobutton(rbuttons, text="Option3",
                                 variable=self.rvar, value=3,
                                 command=self.rselect)
        r3.grid(column=0,row=2)
        self.rlabel = tkinter.Label(rbuttons, textvariable=self.rlabelvar)
        self.rlabel.grid(column=0,row=3)

        self.grid_columnconfigure(0, weight=1)
        self.resizable(True, False)
        #self.update()
        #self.geometry(self.geometry())
        self.entry.focus_set()
        self.entry.selection_range(0, tkinter.END)

    def rselect(self):
        selection = "You selected the option " + str(self.rvar.get())
        #self.rlabel.config(text=selection)
        self.rlabelvar.set(selection)

    def OnButtonClick(self):
        self.labelVariable.set(self.entryVariable.get() + " (You clicked the button)")
        self.entry.focus_set()
        self.entry.selection_range(0, tkinter.END)

    def OnPressEnter(self, event):
        self.labelVariable.set(self.entryVariable.get() + " (You pressed ENTER)")
        self.entry.focus_set()
        self.entry.selection_range(0, tkinter.END)

def launch_TestApp():
    tapp = TestApp(None)
    tapp.title('TestApp')
    tapp.mainloop()


if __name__ == "__main__":
    if b_app:
        launch_app()
    else:
        launch_TestApp()

"""
top = tkinter.Tk()
CheckVar1 = tkinter.IntVar()
CheckVar2 = tkinter.IntVar()
C1 = tkinter.Checkbutton(top, text = "Music", variable = CheckVar1, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20)
C2 = tkinter.Checkbutton(top, text = "Video", variable = CheckVar2, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20)
C1.pack()
C2.pack()
Lb1 = tkinter.Listbox(top)
Lb1.insert(1, "Python")
Lb1.insert(2, "Perl")
Lb1.insert(3, "C")
Lb1.insert(4, "PHP")
Lb1.insert(5, "JSP")
Lb1.insert(6, "Ruby")

Lb1.pack()
top.mainloop()
"""
