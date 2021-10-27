#import modules
import pygame
from tkinter import *
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

#initialize tkinter window
root = Tk()
root.title("Dotify Music Player")
root.geometry("400x445")
root.configure(bg="grey")

dotifyimg = PhotoImage(file="C:/Users/omara/Desktop/Coding/Python/gui/dotify.png")
root.iconphoto(True, dotifyimg)

heading = Label(root, text="Dotify", font=("Helvetica", 14), bg="black", fg="white", width=300, height=3)
heading.pack()

dotify = Label(image=dotifyimg, bg="black")
dotify.place(x=115, y=10)

#Intitialize pygame mixer
pygame.mixer.init()

#functions

#how to know if pause, variable
global paused
paused = False

#add one song
def add_song():
    song = filedialog.askopenfilename(initialdir="C:/Users/omara/Desktop/Coding/Python/gui/music", title="Open a file", filetypes=(("mp3 Files", "*.mp3"),("m4a Files", "*.m4a")))

    #get rid of extra text for listbox
    song = song.replace("C:/Users/omara/Desktop/Coding/Python/gui/music/", "")
    song = song.replace(".mp3", "")
    song = song.replace(".m4a", " *")

    song_box.insert(END, song)

def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir="C:/Users/omara/Desktop/Coding/Python/gui/music", title="Open a file", filetypes=(("mp3 Files", "*.mp3"), ("m4a Files", "*.m4a")))

    for song in songs:
        song = song.replace("C:/Users/omara/Desktop/Coding/Python/gui/music/", "")
        song = song.replace(".mp3", "")
        song = song.replace(".m4a", " *")

        song_box.insert(END, song)

#play song
def play():
    song = song_box.get(ACTIVE)
    song = f"C:/Users/omara/Desktop/Coding/Python/gui/music/{song}.mp3"

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #get song play time info
    play_time()

    """update slider
    slider_pos = int(song_length)
    my_slider.set(0)
    my_slider.config(to=slider_pos)"""

#pause music
def pause(is_paused):
    global paused
    paused = is_paused

    #paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    #unpause
    else:
        pygame.mixer.music.pause()
        paused = True

#stop music
def stop():
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

    #clear status bar
    status_bar.config(test="No music currently playing")

#next song
def next_song():
    curr = song_box.curselection()
    next_song = curr[0] + 1

    song = song_box.get(next_song)

    song = f"C:/Users/omara/Desktop/Coding/Python/gui/music/{song}.mp3"

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_box.selection_clear(0, END)
    song_box.activate(next_song)
    song_box.selection_set(next_song, last=None)

    # update slider
    my_slider.set(0)

#prev song
def prev_song():
    curr = song_box.curselection()
    next_song = curr[0] - 1

    song = song_box.get(next_song)

    song = f"C:/Users/omara/Desktop/Coding/Python/gui/music/{song}.mp3"

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_box.selection_clear(0, END)
    song_box.activate(next_song)
    song_box.selection_set(next_song, last=None)

    # update slider
    my_slider.set(0)

#remove one song
def remove_song():
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()

#remove many songs
def remove_many_songs():
    song_box.delete(0, END)
    pygame.mixer.music.stop()

#get song length info
def play_time():
    #get curr position in song
    currtime = pygame.mixer.music.get_pos() / 1000
    converted_time = time.strftime("%M:%S", time.gmtime(currtime))

    #get curr song
    curr_song = song_box.curselection()
    song = song_box.get(ACTIVE)
    song = f"C:/Users/omara/Desktop/Coding/Python/gui/music/{song}.mp3"

    #get curr song length
    song_mut = MP3(song)

    global song_length
    song_length = song_mut.info.length

    converted_song_length = time.strftime("%M:%S", time.gmtime(song_length))

    currtime += 1

    if int(my_slider.get()) == int(currtime):
        slider_pos = int(song_length)
        my_slider.set(int(currtime))
        my_slider.config(to=slider_pos)

    else:
        slider_pos = int(song_length)
        my_slider.set(0)
        my_slider.config(to=slider_pos)

        converted_time = time.strftime("%M:%S", time.gmtime(int(my_slider.get())))
        status_bar.config(text=f"Time Elapsed:   {converted_time}  of  {converted_song_length}   ")

    #output time
    #my_slider.set(int(currtime))

    #CHANGING SLIDER
    #slider_pos = int(song_length)
    #my_slider.set(int(currtime))
    #my_slider.config(to=slider_pos)

    #update time
    status_bar.after(100, play_time)

#change volume
def change_vol(_=None):
    pygame.mixer.music.set_volume(vol.get())

#music slider
def slide_music(x):
    song = song_box.get(ACTIVE)
    song = f"C:/Users/omara/Desktop/Coding/Python/gui/music/{song}.mp3"

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(x))

    #comment this later
    slider_label.config(text=f"{(x)} of {int(song_length)}")

#textbox
song_box = Listbox(root, bg="black", fg="white", width=60, selectbackground="grey", selectforeground="black")
song_box.pack(pady=20)

#control frame
controls_frame = Frame(root)
controls_frame.pack()

#buttons
play_btn_img = PhotoImage(file="C:/Users/omara/Desktop/Coding/Python/gui/play.png")
pause_btn_img = PhotoImage(file="C:/Users/omara/Desktop/Coding/Python/gui/pause.png")
stop_btn_img = PhotoImage(file="C:/Users/omara/Desktop/Coding/Python/gui/stop.png")
next_btn_img = PhotoImage(file="C:/Users/omara/Desktop/Coding/Python/gui/next.png")
back_btn_img = PhotoImage(file="C:/Users/omara/Desktop/Coding/Python/gui/prev.png")

play_button = Button(controls_frame, image=play_btn_img, borderwidth=0, bg="grey", command=play)
pause_button = Button(controls_frame, image=pause_btn_img, borderwidth=0, bg="grey", command=lambda: pause(paused))
stop_button = Button(controls_frame, image=stop_btn_img, borderwidth=0, bg="grey", command=stop)
next_button = Button(controls_frame, image=next_btn_img, borderwidth=0, bg="grey", command=next_song)
back_button = Button(controls_frame, image=back_btn_img, borderwidth=0, bg="grey", command=prev_song)

play_button.grid(row=0, column=3)
pause_button.grid(row=0, column=2)
stop_button.grid(row=0, column=1)
next_button.grid(row=0, column=4)
back_button.grid(row=0, column=0)

#menu
my_menu = Menu(root)
root.config(menu=my_menu)

manage_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Options", menu=manage_menu)
manage_menu.add_command(label="Configure", command=None)
manage_menu.add_command(label="Exit", command=root.destroy)

add_song_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Add Music", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song to Playlist", command=add_song)
add_song_menu.add_command(label="Add Multiple Songs to Playlist", command=add_many_songs)

remove_song_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Remove Music", menu=remove_song_menu)
remove_song_menu.add_command(label="Remove Highlighted Song from Playlist", command=remove_song)
remove_song_menu.add_command(label="Remove All Songs from Playlist", command=remove_many_songs)

#create status bar
status_bar = Label(root, text="No music currently playing", bd=2, relief=GROOVE, anchor=E, bg="black", fg="white")
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

#sliders frame
slider_Frame = Frame(root, borderwidth=2, relief=GROOVE, width=400, height=60, bg="black")
slider_Frame.grid_propagate(0)
slider_Frame.pack(side=BOTTOM)

#volume scale
vol = Scale(slider_Frame, bd=0, from_=0, showvalue=0, to=1, orient=HORIZONTAL, resolution=.1, command=change_vol, relief=GROOVE, sliderrelief=GROOVE,
            bg="black", fg="white", label="Volume", troughcolor="grey", activebackground="black", highlightthickness=0)
vol.set(100)
vol.grid(row=0, column=1, padx=5, pady=7)

#music slider
my_slider = Scale(slider_Frame, showvalue=0, bd=0, from_=0, to=100, orient=HORIZONTAL, command=slide_music, relief=GROOVE, sliderrelief=GROOVE,
            bg="black", fg="white", label="Song position", troughcolor="grey", activebackground="black", highlightthickness=0, length=275)
my_slider.set(0)
my_slider.grid(row=0, column=0, padx=5, pady=7)

#temp slider lavel
slider_label = Label(root, text="0")
slider_label.pack(pady=10)

#mainloop
root.mainloop()

