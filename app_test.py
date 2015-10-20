import Tkinter

import run_lda



class Counter:
    def __init__(self, init=0):
        self.counter = init

    def get(self):
        n = self.counter
        self.counter +=1
        return n

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

class Param:
    def __init__(self,parent,name,
                 init=None, lbound=None, ubound=None,
                 width=4, row=0, column=0,
                 callback=None):
        self.parent = parent
        self.name = name
        self.lbound = lbound
        self.ubound = ubound

        self.label = Tkinter.Label(parent, text=name, anchor='w')
        self.label.grid(row=row,column=column, sticky='w')

        self.var = Tkinter.StringVar()
        if init is not None:
            self.var.set(init)
        self.entry = Tkinter.Entry(parent, textvariable=self.var, width=width,
                                   justify='right')
        if callback is not None:
            self.entry.bind("<Return>", callback)
        self.entry.grid(row=row,column=column+1)

    def get_int(self):
        n = get_int_from_StringVar(self.var,
                                   name=self.name, entry=self.entry,
                                   lbound=self.lbound, ubound=self.ubound)
        return n




class LDA_App:
    def __init__(self, parent=None):
        self.root = Tkinter.Tk(parent)
        self.root.title('LDA on masters')

        self.lda_frame = Tkinter.Frame(self.root)
        self.lda_frame.grid()

        self.lda_label = Tkinter.Label(self.lda_frame, text="LDA parameters")
        self.lda_label.grid(row=0,column=0,sticky='EW')

        self.lda_params_frame = Tkinter.Frame(self.lda_frame)
        self.lda_params_frame.grid(row=1,column=0,sticky='EW')

        param_row = Counter(init=0)

        self.n_topics_param = Param(self.lda_params_frame, 'number of topics',
                                    row=param_row.get(),
                                    init=10, lbound=2, ubound=100,
                                    callback=self.run_lda_callback)

        self.n_iter_param = Param(self.lda_params_frame, 'number of iterations',
                                  row=param_row.get(),
                                  init=100, lbound=10, ubound=9999,
                                  callback=self.run_lda_callback)

        self.n_topic_words_param = Param(self.lda_params_frame, 'number of words displayed per topic',
                                         row=param_row.get(),
                                         init=20, lbound=1, ubound=100,
                                         callback=self.run_lda_callback)


        lda_button = Tkinter.Button(self.lda_frame, text="Run LDA",
                                    command=self.run_lda)
        lda_button.grid(column=0, row=3)
        self.lda_run_label_var = Tkinter.StringVar()
        self.lda_run_label = Tkinter.Label(self.lda_frame, textvariable=self.lda_run_label_var)
        self.lda_run_label.grid(column=0, row=4,sticky='EW')



    def run_lda_callback(self,event):
        self.run_lda()

    def run_lda(self):
        try:
            n_topics = self.n_topics_param.get_int()
            n_iter = self.n_iter_param.get_int()
            n_topic_words = self.n_topic_words_param.get_int()
            self.run_lda_with_args(n_topics, n_iter, n_topic_words)
        except InvalidValueException as e:
            self.lda_run_label_var.set(e.message)
            self.lda_run_label.config(fg="red")
            e.entry.focus_set()
            e.entry.selection_range(0, tkinter.END)

    def run_lda_with_args(self, n_topics, n_iter, n_topic_words):
        msg = 'LDA on masters with {} topics, {} iterations, and {} words displayed per topic.'.format(n_topics, n_iter, n_topic_words)
        self.lda_run_label_var.set(msg+'\nRunning...')
        self.lda_run_label.config(fg="black")
        self.root.update()
        f = run_lda.run_lda_masters(n_topics=n_topics, n_iter=n_iter, n_topic_words=n_topic_words)
        msg = msg + '\nResults stored in file {}'.format(f)
        self.lda_run_label_var.set(msg)

    def mainloop(self):
        self.root.mainloop()



def launch_app():
    app = LDA_App()
    app.mainloop()




if __name__ == "__main__":
    launch_app()