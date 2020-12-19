
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: N10067680
#    Student name: Ayden Beggs
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  Submitted files will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Assignment Description-----------------------------------------#
#
#  Stay at Home Shopping
#
#  In this assignment you will combine your knowledge of HTMl/XML
#  mark-up languages with your skills in Python scripting, pattern
#  matching, and Graphical User Interface design to produce a useful
#  application for simulating an online shopping experience.  See
#  the instruction sheet accompanying this file for full details.
#
#--------------------------------------------------------------------#



#-----Imported Functions---------------------------------------------#
#
# Below are various import statements for helpful functions.  You
# should be able to complete this assignment using these functions
# only.  You can import other functions provided they are standard
# ones that come with the default Python/IDLE implementation and NOT
# functions from modules that need to be downloaded and installed
# separately.  Note that not all of the imported functions below are
# needed to successfully complete this assignment.

# The function for opening a web document given its URL.
# (You WILL need to use this function in your solution,
# either directly or via our "download" function.)
from urllib.request import urlopen
import webbrowser

# Import some standard Tkinter functions. (You WILL need to use
# some of these functions in your solution.)  You may also
# import other widgets from the "tkinter" module, provided they
# are standard ones and don't need to be downloaded and installed
# separately.
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

# Functions for finding all occurrences of a pattern
# defined via a regular expression, as well as
# the "multiline" and "dotall" flags.  (You do NOT need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.)
from re import findall, finditer, MULTILINE, DOTALL

# Import the standard SQLite functions (just in case they're
# needed).
from sqlite3 import *

#
#--------------------------------------------------------------------#



#--------------------------------------------------------------------#
#
# A function to download and save a web document. If the
# attempted download fails, an error message is written to
# the shell window and the special value None is returned.
#
# Parameters:
# * url - The address of the web page you want to download.
# * target_filename - Name of the file to be saved (if any).
# * filename_extension - Extension for the target file, usually
#      "html" for an HTML document or "xhtml" for an XML
#      document.
# * save_file - A file is saved only if this is True. WARNING:
#      The function will silently overwrite the target file
#      if it already exists!
# * char_set - The character set used by the web page, which is
#      usually Unicode UTF-8, although some web pages use other
#      character sets.
# * lying - If True the Python function will try to hide its
#      identity from the web server. This can sometimes be used
#      to prevent the server from blocking access to Python
#      programs. However we do NOT encourage using this option
#      as it is both unreliable and unethical!
# * got_the_message - Set this to True once you've absorbed the
#      message above about Internet ethics.
#
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'download',
             filename_extension = 'html',
             save_file = True,
             char_set = 'UTF-8',
             lying = False,
             got_the_message = False):

    # Import the function for opening online documents and
    # the class for creating requests
    from urllib.request import urlopen, Request

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        if lying:
            # Pretend to be something other than a Python
            # script (NOT RELIABLE OR RECOMMENDED!)
            request = Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0')
            if not got_the_message:
                print("Warning - Request does not reveal client's true identity.")
                print("          This is both unreliable and unethical!")
                print("          Proceed at your own risk!\n")
        else:
            # Behave ethically
            request = url
        web_page = urlopen(request)
    except ValueError:
        print("Download error - Cannot find document at URL '" + url + "'\n")
        return None
    except HTTPError:
        print("Download error - Access denied to document at URL '" + url + "'\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to download " + \
              "the document at URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Read the contents as a character string
    try:
        web_page_contents = web_page.read().decode(char_set)
    except UnicodeDecodeError:
        print("Download error - Unable to decode document from URL '" + \
              url + "' as '" + char_set + "' characters\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to decode " + \
              "the document from URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Optionally write the contents to a local text file
    # (overwriting the file if it already exists!)
    if save_file:
        try:
            text_file = open(target_filename + '.' + filename_extension,
                             'w', encoding = char_set)
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as message:
            print("Download error - Unable to write to file '" + \
                  target_filename + "'")
            print("Error message was:", message, "\n")

    # Return the downloaded document to the caller
    return web_page_contents

#
#--------------------------------------------------------------------#



#--------------------------------------------------------------------#
#
# A function to open a local HTML document in your operating
# system's default web browser.  (Note that Python's "webbrowser"
# module does not guarantee to open local files, even if you use a
# 'file://..." URL). The file to be opened must be in the same folder
# as this module.
#
# Since this code is platform-dependent we do NOT guarantee that it
# will work on all systems.
#
def open_html_file(file_name):
    
    # Import operating system functions
    from os import system
    from os.path import isfile
    
    # Remove any platform-specific path prefixes from the
    # filename
    local_file = file_name[file_name.rfind('/') + 1:] # Unix
    local_file = local_file[local_file.rfind('\\') + 1:] # DOS
    
    # Confirm that the file name has an HTML extension
    if not local_file.endswith('.html'):
        raise Exception("Unable to open file " + local_file + \
                        " in web browser - Only '.html' files allowed")
    
    # Confirm that the file is in the same directory (folder) as
    # this program
    if not isfile(local_file):
        raise Exception("Cannot find file " + local_file + \
                        " in the same folder as this program")
    
    # Collect all the exit codes for each attempt
    exit_codes = []
    
    # Microsoft Windows: Attempt to "start" the web browser
    code = system('start ' + local_file)
    if code != 0:
        exit_codes.append(code)
    else:
        return 0
    
    # Apple macOS: Attempt to "open" the web browser
    code = system("open './" + local_file + "'")
    if code != 0:
        exit_codes.append(code)       
    else:
        return 0
    
    # Linux: Attempt to "xdg-open" the local file in the
    # web browser
    code = system("xdg-open './" + local_file + "'")
    if code != 0:
        exit_codes.append(code)       
    else:
        return 0
    
    # Give up!
    raise Exception('Unable to open file ' + local_file + \
                    ' in web browser - Exit codes: ' + \
                    str(exit_codes))

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
# Put your solution at the end of this file.

 

app = Tk()
app.title(' Shopping At Home ')


class AllWidgets:
    import sqlite3
    
        
    def __init__(self, master):

        new = 2
        bg = 'powderblue' 
        fg = 'darkslateblue' 
        
        def showimagebutton():
            tkMessageBox.showinfo("")

        #copy file location and paste in url ----


        

            
            
#----------------------- Frame 1 ------------------------------------
        l1 = Label (app, text="Pandemic Products: Shop at Home", font=("Arial", 20, "bold"), fg='midnightblue')
        l1.pack()
                    
        frame = Frame(master, width=500, height=400)
        frame.pack()

        iframe1 = LabelFrame(frame, bd=2,fg=fg,font=('Arial',8, "bold"),
                             relief=GROOVE, text='In Store Today')



        iframe1.pack()
        iframe1.config(padx=20, pady=0)
        iframe1.place(x=320, y=0)

#----------------------- Frame 2 ------------------------------------
        frame2 = Frame(master, width=500, height=400)
        frame2.pack() 

        iframe2 = LabelFrame(app, bd=2, fg=fg,font=('Arial',8, "bold"),
                             relief=GROOVE, text='Old Stock on order',)


        def clicked(value):
            myLabel = Label(app, text=value)
            myLabel.pack()
#------------------------------------------------functions ^ ------------------
        Modes = None
#---------------------------------------------------------------------------------

        
        v = StringVar(app)
        v.set(Modes)
        
        strings = ['Medical Items', 'Vitamins']
        strings_2 = ['Supplements', 'Blenders']
        Pro = ['Please Select Product Category']
        Pro2 = ['Your Cart Items :']
        Med_items = ['We Apologise, ','only one of each','product per customer','', 'Medical Items:','1. Type 1 Medical Sticker ($4.50)','2. 3-Ply Protective Masks ($39.99)',
                     '3. Dettol Hand Sanitizer 50ml ($2.99)','4. Mediflex Latex Gloves ($32.99)',
                     '5. Medical Themometer ($16.40)','','','https://www.amazon.com.au/b?ie=UTF8&node=5148204051']
        
        Vitamins = ['Vitamins:','1. Sugarless C 500mg ($12.49)','2. Magnesium Tablets ($16.00) ',
                    '3. Calcium 600mg w VD3 ($16.00)','4. Vitamin D - 400 Capsules ($16.47)',
                    '5. Vanilla Whey Protein ($69.99)','','','https://www.amazon.com.au/s?k=Vitamins&i=hpc&ref=nb_sb_noss_2']
        
        Supplements = ['Supplements:','1.Gold Standard - Double Rich Choc ($90.20).','2. Pure Product Vanilla 1kg ($29.00)',
                       '3. Super Foods Greens Plus, 100g ($11.49)','4. Plant Protein - Cacao Hazlenut ($57.95)',
                       '5. Isopure Infusions fruit flavored ($42.24)','','','https://www.amazon.com.au/s?k=protein+powder&crid=3A9BI1572ZB16&sprefix=protein%2Caps%2C307&ref=nb_sb_ss_i_1_7']

        
        Blenders = ['Blenders:','1. TODO Heated Blender ($79.00)','2. Breville twist Blender ($129.00)','3. Kambrook Power Blender ($70.00)',
                    '4. Portable Blender ($33.99)', '5. Classic Blender Bottle 590ml ($12.95)','','','https://www.amazon.com.au/s?k=blender&ref=nb_sb_noss_2']
        

        def sel():
            
           
                
            listbox.delete(0, END)

            print("You selected the option " + str(v.get()))

            if v.get() == 'Medical Items':
                for item in Med_items:
                    listbox.insert(END, item)
                
            elif v.get() == 'Vitamins':
                for item in Vitamins:
                    listbox.insert(END, item)
                    
            elif v.get() == 'Supplements':
                for item in Supplements:
                    listbox.insert(END, item)

            else:
                for item in Blenders:
                        listbox.insert(END, item)
           
        
        def Onclick():
            
            if v.get() == 'Medical Items' :
                fname = 'product_images.html'
                html_file = open(fname, 'r')
                source_code = html_file.read()
                webbrowser.open(fname,new=2)  
            
            elif v.get() == 'Vitamins' :
                fname = 'product_images_2.html'
                html_file = open(fname, 'r')
                source_code = html_file.read()
                webbrowser.open(fname,new=2)
                
            elif v.get() == 'Supplements' :
                fname = 'product_images_3.html'
                html_file = open(fname, 'r')
                source_code = html_file.read()
                webbrowser.open(fname,new=2)                 
            else:
                fname = 'product_images_4.html'
                html_file = open(fname, 'r')
                source_code = html_file.read()
                webbrowser.open(fname,new=2)

        def Selection(Event = None):
            
            index = listbox.curselection()
            if index != ():
                selected_item = listbox.get(index)
                listbox2.insert(END, selected_item)

        def Delete(Event = None):
            index = listbox.curselection()
            if index != ():
                selected_item = listbox.get(index)
                

        def SavingOrder():
            c_nect= sqlite3.connect('orders.db')
            con= c_nect.cursor()
            con.execute('INSERT INTO data (Product, Price) Values(?,?)',(Selection()))
            con.commit()
            print("Done")
            
                
#--------------------------------------Bttns and Radiobtnns---------------------------------------
         
               
        for item in strings:

            button = Radiobutton(iframe2, text=item, font=('Arial',10, "bold"),
                                 fg=fg, highlightcolor=fg
                                 ,variable=v, value=item,
                                 command=lambda: sel()).pack(anchor=NW)



        for items in strings_2:

            button = Radiobutton(iframe1, text=items, font=('Arial',10, "bold"),
                                 fg=fg, highlightcolor=fg,borderwidth=1,
                                 variable=v, value=items,
                                 command=lambda: sel()).pack(anchor=NW)


        

            
        iframe2.pack()
        iframe2.config(padx=20, pady=0)
        iframe2.place(x=320, y=120)
#------------------------- SHOW IMAGES -----------------------------------------
        btn = Button(app, text = ' View Images',
                     font=('Bold',10),
                     fg=fg, relief=GROOVE, highlightthickness=2,
                     command=lambda: Onclick())
        btn.place(x=0, y=0)
        btn.pack(side = 'top')
        btn.place(x=350, y=210)
#------------------------- LIST BOX ----------------------

        scrollbr = Scrollbar( orient="vertical", bg="aliceblue",
                              highlightcolor="aliceblue")
        
        listbox = Listbox( background="azure1",fg="blue4",
                           highlightcolor="aliceblue",width=30
                          , height=10, selectmode=BROWSE,
                           yscrollcommand=scrollbr, font=('Arial',9, "bold"))
        #listbox allocations
        listbox.pack(side=LEFT, anchor=W)
        listbox.insert(END, Pro)
        listbox.place(x=10, y=270)
        listbox.get(ANCHOR)
        
        #scrollbar positioning & commands
        scrollbr.config(command=listbox.yview)
      
        
        scrollbr.pack(side="left", fill=BOTH )
        scrollbr.place(x=225, y=300)

      

#---------------------------------------------------------

#-------------------- Add products-----------------------------

#--------------------------------------------------------
        listbox2 = Listbox(app, background="azure1", fg="blue4",
                           highlightcolor="aliceblue", width=30, 
                          height=10, selectmode=BROWSE, font=('Arial',9, "bold"))

        listbox2.pack(side=LEFT, anchor=W)
        listbox2.insert(0, 'Your Shopping Cart Items:')
        
        scrollbar2 = Scrollbar( orient="vertical", bg="aliceblue", relief=GROOVE
                                ,highlightcolor="aliceblue")
        
        scrollbar2.config(command=listbox2.yview)
        
      
        
        scrollbar2.pack(side="left", fill=BOTH )
        scrollbar2.place(x=465, y=300)
#----------------Scrollbar^^^

        #creating listbox
        
        listbox2.place(x=250, y=270)
        listbox2.config(yscrollcommand=scrollbar2.set)
        listbox2.bind('<<ListboxSelect>>', Selection())
        
       #creating the buttons
        btn2 = Button(app, text = 'Add Products To Cart',
                        font=('Bold',9, "bold"),
                        fg=fg, relief=GROOVE, 
                      command=lambda: Selection())
        
        btn2.place(x=0, y=0)
        btn2.pack(side = 'top')
        btn2.place(x=30, y=450)

        btn2 = Button(app, text = 'Delete Items in Cart',
                        font=('Bold',9, "bold"),
                        fg=fg, relief=GROOVE, 
                      command=lambda: Delete())
        
        btn2.place(x=0, y=0)
        btn2.pack(side = 'top')
        btn2.place(x=195, y=450)

        btn3 = Button(app, text = 'Submit Order',
                font=('Bold',9, "bold"),
                fg=fg, relief=GROOVE, 
              command=lambda: SavingOrder())
        
        btn3.place(x=0, y=0)
        btn3.pack(side = 'top')
        btn3.place(x=350, y=450)
#---------------------------------------------------------


#----------------------------
        #creating the logo position
        def image():
            photo = PhotoImage(file="logo.png")
            L1 = Label(app, image=photo, anchor=W)
            L1.photo = photo
            L1.place(x=60, y=50)
            

        image()



app.geometry("500x500")
all = AllWidgets(app)
app.mainloop()


# Name of the product images file.  To assist marking, your
# program should export your product images using this file name.
image_file = 'product_images.html'

pass
