import tkinter as tk
from tkinter import *
from automata.fa.dfa import DFA
from PIL import ImageTk, Image
from tkinter import *
from tkinter import filedialog
import os

"""
This module scanns the code of TINY language from an input file, and produces an output filte
"""
root = tk.Tk()
root.title("Compile your code!")
label1 = tk.Label(root)
label3 = tk.Label(root)
label5 = tk.Label(root)
class Scanner:

    def __init__(self):
        """Initialize paramaeters for the scanner."""
        self.special_symbols = ["||", "&&", ">", "<", "=", "<=", "!", ">="]
        self.digits = "0123456789"
        self.letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.current_state = 1
        self.set_value = ""
        self.set_type = ""
        self.tokens = []
        self.sequence = []

    def process_line(self, line):
        """iterate over each char in line applying DFA."""
        for char in line:
            if self.current_state == 1:

                if char == "{":
                    self.current_state = 2  # Comment
                elif (char == ">" or char == "<"):
                    self.set_type = "COMPARATOR"
                    self.set_value = char
                    self.current_state = 3  # not eguality comparison
                elif char in self.letters:
                    self.set_type = "ID"
                    self.set_value = char
                    self.current_state = 4  # Identifier
                elif char in self.digits:
                    self.set_type = "NUM"
                    self.set_value = char
                    self.current_state = 5  # Number
                elif char == "&":
                    self.set_type = "AND"
                    self.set_value = char
                    self.current_state = 6  # and
                elif char == "|":
                    self.set_type = "OR"
                    self.set_value = char
                    self.current_state = 7  # or
                elif char == "!":
                    self.set_type = "NOT"
                    self.set_value = char
                    self.current_state = 1  # not
                    self.tokens.append(self.set_value + ", " + self.set_type)  # Done
                    self.sequence.append(self.set_type)  # Done


                elif char == "=":
                    self.set_type = "COMPARATOR"
                    self.set_value = char
                    self.tokens.append(self.set_value + ", " + self.set_type)  # Done
                    self.sequence.append(self.set_type)  # Done
                    self.current_state = 1
                elif char != " " and char != "\n":
                    self.current_state = -1


            elif self.current_state == 2:

                if char == "}":  # ending the comment
                    self.current_state = 1
                    self.set_value = ""



            elif self.current_state == 3:

                if char == "=":
                    self.set_type = "COMPARATOR"
                    self.set_value += char
                    self.tokens.append(self.set_value + ", " + self.set_type)  # Done
                    self.sequence.append(self.set_type)  # Done
                    self.current_state = 1
                else:
                    self.tokens.append(self.set_value + ", " + self.set_type)
                    self.sequence.append(self.set_type)  # Done
                    self.current_state = 1
                    self.process_line(line)


            elif self.current_state == 4:

                if char in self.letters:
                    self.set_value += char
                elif char in self.digits:
                    self.set_value += char
                else:  # Done
                    self.tokens.append(self.set_value + ", " + self.set_type)  # Done
                    self.sequence.append(self.set_type)  # Done
                    self.current_state = 1
                    self.process_line(line)



            elif self.current_state == 5:

                if char in self.digits:
                    self.set_value += char
                else:  # Done
                    self.tokens.append(self.set_value + ", " + self.set_type)
                    self.sequence.append(self.set_type)  # Done
                    self.current_state = 1
                    self.process_line(line)
            # elif self.current_state == 6:
            #
            #
            #     self.tokens.append(self.set_value + self.set_type)
            #     self.current_state = 1
            elif self.current_state == 6:
                if char == "&":
                    self.set_value += char
                    self.tokens.append(self.set_value + ", " + self.set_type)  # Done
                    self.sequence.append(self.set_type)  # Done
                    self.current_state = 1
                else:
                    self.current_state = -1

            elif self.current_state == 7:
                if char == "|":
                    self.set_value += char
                    self.tokens.append(self.set_value + ", " + self.set_type)  # Done
                    self.sequence.append(self.set_type)  # Done
                    self.current_state = 1
                else:
                    self.current_state = -1

    # def file_process(self, in_file="tiny_in.txt", out_file="tiny_out.txt"):
    #     in_file = open(in_file)
    #     count = 0
    #     for line in in_file:
    #         count += 1
    #         self.process_line(line)
    #         if self.current_state < 0:
    #             break
    #
    #     if self.current_state < 0:
    #         print("Error in line ", count)
    #         return
    #     else:
    #         out_file = open(out_file, 'w')
    #         for token in self.tokens:
    #             out_file.write(token+"\n")
    #         out_file.close()
    #         print("Scanning run successfully!")


    def buttonCmd(self):
        global label1
        label1.destroy()

    def text_process(self):

        global label1, label3, label5
        ListOfTokens = ""
        x1 = my_text.get(1.0, END)
        count = 0
        for line in x1:
            count += 1
            self.process_line(line)
            if self.current_state < 0:
                break
        if self.current_state < 0:
            print("Error in line ", count)
            return

        else:
            ListOfTokens = ""
            for token in self.tokens:
                ListOfTokens = ListOfTokens + token + "\n"
            print("Scanning run successfully!")
        label1 = tk.Label(text=ListOfTokens)
        canvas1.create_window(0, 600, window=label1)
        print(ListOfTokens)
        for token in self.sequence:
            print(token)
            print("\n")
            # DFA which matches all binary strings ending in an odd number of '1's
            dfa = DFA(
                states={'q0', 'q1', 'q2', 'q3', 'DEAD'},
                input_symbols={'NUM', 'ID', 'AND', 'OR', 'NOT', 'COMPARATOR'},
                transitions={
                    'q0': {'NUM': 'q1', 'ID': 'q1', 'AND': 'DEAD', 'OR': 'DEAD', 'COMPARATOR': 'DEAD', 'NOT': 'q0'},
                    'q1': {'AND': 'q2', 'OR': 'q2', 'COMPARATOR': 'q2', 'NUM': 'DEAD', 'ID': 'DEAD', 'NOT': 'DEAD', },
                    'q2': {'AND': 'DEAD', 'OR': 'DEAD', 'COMPARATOR': 'DEAD', 'NOT': 'q2', 'NUM': 'q3', 'ID': 'q3'},
                    'q3': {'ID': 'DEAD', 'NUM': 'DEAD', 'NOT': 'DEAD', 'AND': 'q0', 'OR': 'q0', 'COMPARATOR': 'q0'},
                    'DEAD': {'ID': 'DEAD', 'NUM': 'DEAD', 'NOT': 'DEAD', 'AND': 'DEAD', 'OR': 'DEAD',
                             'COMPARATOR': 'DEAD'}
                },
                initial_state='q0',
                final_states={'q1', 'q3', 'q2' ,'DEAD'}
            )
            stringTokens = scanner.sequence
            Printing = " "
            acceptedString= ''
            if dfa.accepts_input(stringTokens):
                statesSequence = list(dfa.read_input_stepwise(stringTokens))
                if  (dfa.read_input(stringTokens) == 'q1'or (dfa.read_input(stringTokens) == 'q3')  ) :
                    acceptedString = "String is Accepted!!"
                else :
                    acceptedString ="String is not Accepted!!"


                for x, y in zip(stringTokens,statesSequence[1:]):  # for loop to print each token and its arrived state
                    print(x + " -----> " + y)
                # Printing = ("final state is :" + str(dfa.read_input(stringTokens)))
                # print(Printing)
            for state in statesSequence [1:] :
                Printing = Printing + state + "\n"
            states = []

            try:
                a = dfa.read_input_stepwise(stringTokens)
            except:
                print("not valid")
                count = 0
                try:
                    for i in a:
                        states.append(str(i))
                        count += 1
                except:
                    print("last state is not valid")
            label3 = tk.Label(text=Printing)
            canvas1.create_window(100, 600, window=label3)
            label5 = tk.Label(text=acceptedString , )
            label5.configure(font=("Arial", 18, "bold"))
            canvas1.create_window(1000, 250, window=label5)
def openWindow():
    new = Toplevel(root)
    new.geometry("1000x1000")
    new.title("DFA")


    # Show image using label
    bg = PhotoImage(file="DFA.jpeg")
    label1 = Label(new, image=bg, text="ss")

    canvas1.create_window(200, 200, window=label1)
    #img = ImageTk.PhotoImage(Image.open("DFA.jpeg"))
    #canvas.create_image(20, 20, anchor=NW, image=img)
if __name__ == '__main__':
    scanner = Scanner()

    canvas1 = tk.Canvas(root, width=1000, height=800)
    canvas1.pack()

    my_text = Text(root, width=40, height=10, font=("Helvetica", 16))
    my_text.pack(pady=200)
    canvas1.create_window(70, 140, window=my_text)

    button1 = tk.Button(text='Get list of tokens', command=scanner.text_process)
    canvas1.create_window(200, 300, window=button1)
    button2 = tk.Button(text='clear', command=scanner.buttonCmd)
    canvas1.create_window(200, 350, window=button2)
    button3 = tk.Button(text='Show DFA', command=openWindow)
    canvas1.create_window(200, 400, window=button3)

    img = PhotoImage(file="DFA_New.png")
    canvas1.create_image(600, 600,image=img)
    label4 = tk.Label(root ,font= "Arial"  ,text="Regular Expression = [!* [chars+ nums*chars* | nums+]] (oper !*[chars+nums*chars*|chars])*       \n")
    label4.configure(font=("Arial",18,"bold"))
    canvas1.create_window(900, 200, window=label4)
    label5 = tk.Label(root, font="Arial",text= "String State: ")
    label5.configure(font=("Arial", 18, "bold"))
    canvas1.create_window(780, 250, window=label5)



    root.mainloop()



    # while True:
    #     fname = input("Enter the file name (or click enter for \"tiny_in.txt\"): ")
    #     if len(fname) < 1:
    #         scanner.file_process()
    #         cmd = input("click y to continue or any key to exit: ")
    #         if cmd == 'y' or cmd == "Y":
    #             continue
    #         else:
    #             break
    #     else:
    #         try:
    #             scanner.file_process(fname)
    #         except Exception:
    #             print('File cannot be opened:', fname)







