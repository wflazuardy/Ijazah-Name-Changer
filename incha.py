from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar, Style
import os
from os import  listdir
from os.path import isfile, join
from shutil import copyfile
from ocr_function import format_img, read_nrp

class IjazahNameChanger:
    def __init__(self, master):

        # Variables
        self.version = 'version 0.5'
        self.extensions = [".jpg", ".jpeg", "JPG", "JPEG",
                           ".png", ".PNG",
                           ".bmp", ".BMP"]

        self.master = master
        master.title("Ijazah Name Changer")
        # master.geometry('400x200')

        # *** Style ***
        self.s = Style()
        self.s.theme_use("default")
        self.s.configure("TProgressbar", thickness=8, background='green')

        frameTitle = Frame(master)
        frameTitle.pack()
        frameMain = Frame(master)
        frameMain.pack()

        self.process = False

        # *** Title Frame ***
        self.labelJudul = Label(frameTitle, text='Ijazah Name Changer', font=('times', 14, 'bold'), pady=8)
        self.labelJudul.pack(side=TOP,padx=7,pady=4)

        # *** Main Frame ***
        self.labelSource = Label(frameMain, text="Source Folder")
        self.labelDestination = Label(frameMain, text="Destination Folder")

        self.entrySource = Entry(frameMain, width=25)
        self.entryDestination = Entry(frameMain, width=25)

        self.buttonSource = Button(frameMain, text="Search", command=self.get_source)
        self.buttonDestination = Button(frameMain, text="Search", command=self.get_dest)
        self.buttonStart = Button(frameMain, text="START",font=('Helvetica', 9, 'bold'), width=5, fg='green', command=self.directory_ocr)
        self.buttonCancel = Button(frameMain, text="CANCEL",font=('Helvetica', 9, 'bold'), width=7, fg='red', command=self.stop_process)

        self.labelPercent = Label(frameMain, text="")
        self.progressBar = Progressbar(frameMain, orient="horizontal", mode="determinate", style="TProgressbar")

        # *** Main Frame Widgets Pack ***
        self.labelSource.grid(row=0, sticky=E)
        self.entrySource.grid(row=0, column=1, padx=3)
        self.buttonSource.grid(row=0, column=2, padx=3)
        self.labelDestination.grid(row=1, sticky=E)
        self.entryDestination.grid(row=1, column=1, padx=7)
        self.buttonDestination.grid(row=1, column=2, padx=7)
        self.buttonStart.grid(columnspan=3, pady=9)
        self.labelPercent.grid(columnspan=3)
        self.progressBar.grid(columnspan=3, sticky=EW)

        # *** Root Frame ***
        self.statusText = StringVar()
        self.status = Label(master, textvariable=self.statusText, font=('Helvetica', 8, 'normal'), anchor=W,
                            relief=SUNKEN, bd=1)
        self.statusText.set('Plese select source and destination folder')
        self.labelVersion = Label(master, text=self.version, font=('Helvetica', 7, 'normal'), anchor=E)

        self.status.pack(side=TOP, fill=X)
        self.labelVersion.pack(side=RIGHT,padx=7)

    def get_source(self):
        self.sourcedir = filedialog.askdirectory(initialdir = "C:/")
        self.entrySource.delete(0, END)
        self.entrySource.insert(0, self.sourcedir)

    def get_dest(self):
        self.destdir = filedialog.askdirectory(initialdir = "C:/")
        self.entryDestination.delete(0, END)
        self.entryDestination.insert(0, self.destdir)

    def make_cancel_button(self):
        self.buttonStart.grid_forget()
        self.buttonCancel.grid(row=2, columnspan=3, pady=9)

    def stop_process(self):
        ask_cancel = messagebox.askquestion("Cancel Message", "Are you sure?")
        if ask_cancel=='yes':
            self.process = False
            self.progressBar.stop()
            messagebox.showinfo("Warning", "Proses canceled\nOnly %i/%i Files Have Been Renamed"%(self.count,self.countfiles))
            self.statusText.set("Process canceled")

    def normalize_entry(self):
        self.entrySource.config({"background": "white"})
        self.entryDestination.config({"background": "white"})


    # Function When the START Button Clicked  --> Main Function
    def directory_ocr(self):
        source_dir = self.entrySource.get()
        dest_dir = self.entryDestination.get()

        # Responses when entries are empty
        if source_dir == '':
            messagebox.showwarning('Warning', 'Please select source folder!')
            self.entrySource.config({"background": "#ffc0b2"})
            return

        if dest_dir == '':
            messagebox.showwarning('Warning', 'Please select destination folder!')
            self.entryDestination.config({"background": "#ffc0b2"})
            return

        # Response if the selected folders are not exist
        if os.path.isdir(source_dir) != True:
            messagebox.showerror('Error', 'The source folder must be exist!')
            self.entrySource.config({"background": "#ffc0b2"})
            return

        if os.path.isdir(dest_dir) != True:
            dest_dialog = messagebox.askquestion("Warning!", "Destination folder is not exist! Do you want to create the folder?")
            if dest_dialog == 'yes':
                os.mkdir(dest_dir)
            else:
                messagebox.showwarning('Warning', 'Please make the destination folder first!')
                self.entryDestination.config({"background": "#ffc0b2"})
                return

        # Responses if the source directory is empty
        if len(listdir(source_dir)) == 0:
            messagebox.showerror('Error', 'The source folder is empty!')
            self.entrySource.config({"background": "#ffc0b2"})
            return

        self.process = True

        if source_dir[:1] != '/':
            source_dir = source_dir + '/'

        if dest_dir[:1] != '/':
            dest_dir = dest_dir + '/'

        # A list to store 'only files' location data
        onlyfiles = [f for f in listdir(source_dir) if isfile(join(source_dir, f)) & f.endswith(tuple(self.extensions))]

        # Main Process Start
        while self.process == True:
            self.make_cancel_button()
            self.normalize_entry()

            self.countfiles = len(onlyfiles)
            self.progressBar["value"] = 0
            self.progressBar["maximum"] = self.countfiles

            self.labelPercent['text'] = "0%"
            self.statusText.set("Read source and destination folders...")


            for i,img_file in enumerate(onlyfiles):

                if self.process == True:
                    self.statusText.set("Detect NRP in %s...\t\t\t\t%i/%i"%(img_file, i+1,self.countfiles))
                    location = source_dir + img_file
                    cropped = format_img(location)

                    try:
                        nrp = read_nrp(cropped)
                        copyfile(location, (dest_dir + nrp + '.jpg'))
                    except IndexError:
                        nrp = "_ERROR_ " + img_file
                        copyfile(location, (dest_dir + nrp))
                    self.count = i+1
                    self.progressBar["value"] = i + 1
                    percent = ((i+1) / self.progressBar["maximum"]) * 100
                    self.labelPercent['text'] = "{}%".format(int(percent))
                    self.master.update()

                else:
                    break

            if percent==100:
                messagebox.showinfo("Process Report","Process Complete!")
                self.statusText.set("Process complete!")

            self.process=False
            # break

        self.progressBar["value"] = 0
        self.labelPercent['text'] = ""

        self.buttonCancel.grid_forget()
        self.buttonStart.grid(row=2,columnspan=3, pady=9)


if __name__ == '__main__':
    root = Tk()
    app = IjazahNameChanger(root)
    root.mainloop()