import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
from doubly_linked_list import DoublyLinkedList

class Mp3Player(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mp3 Player")
        # tamaño de la ventana tkinter 1060x780: 700 para el reproductor y 350 para la playlist.
        self.geometry("1060x780")
        self.sound_on = True  # sonido on defecto
        
        self.left_bg = "#2C2C54"
        self.right_bg = "#1F1B24"
        self.highlight_bg = "#3C3C3C"  # color para resaltar el ítem reproducido
        
        self.configure(bg=self.right_bg)
        self.resizable(False, False)
        
        self.current_index = 0
        self.total_seconds = 0
        
        # Paneles
        self.left_frame = tk.Frame(self, bg=self.left_bg, bd=0, relief="flat")
        self.left_frame.place(x=0, y=0, width=700, height=780)
        self.right_frame = tk.Frame(self, bg=self.right_bg, bd=0, relief="flat")
        self.right_frame.place(x=700, y=0, width=350, height=780)
        
        # playlist:
        self.playlist = DoublyLinkedList()
        dummy_songs = [
            {"title": "Stairway to Heaven", "artist": "Led Zeppelin", "duration": "08:02", "cover": "led_zeppelin1.jpg", "album": "Led Zeppelin IV"},
            {"title": "Bohemian Rhapsody", "artist": "Queen", "duration": "05:55", "cover": "queen_bohemian.jpg", "album": "A Night at the Opera"},
            {"title": "Paranoid Android", "artist": "Radiohead", "duration": "06:23", "cover": "radiohead_paranoid.jpg", "album": "OK Computer"},
            {"title": "Hotel California", "artist": "Eagles", "duration": "06:30", "cover": "eagles_hotel.jpg", "album": "Hotel California"},
            {"title": "Comfortably Numb", "artist": "Pink Floyd", "duration": "06:22", "cover": "pink_floyd_comfortably.jpg", "album": "The Wall"},
            {"title": "Imagine", "artist": "John Lennon", "duration": "03:04", "cover": "lennon_imagine.jpg", "album": "Imagine"},
            {"title": "Smells Like Teen Spirit", "artist": "Nirvana", "duration": "05:01", "cover": "nirvana_smells.jpg", "album": "Nevermind"}
        ]
        for song in dummy_songs:
            self.playlist.insert_at_end(song)
        self.song_thumbs = []
        
        # tamaños de íconos
        self.icon_size = (30, 30)
        self.play_icon_size = (60, 60)
        self.trash_icon_size = (20, 20)
        self.add_icon_size = (30, 30)
        self.arrow_icon_size = (10, 10)
        
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.img_dir = os.path.join(self.base_dir, "img")
        
        self.vol_icon = self.load_icon("vol.png", self.icon_size)
        self.mute_icon = self.load_icon("mute.png", self.icon_size)
        self.add_icon = self.load_icon("add.png", self.add_icon_size)
        self.up_icon = self.load_icon("up.png", self.arrow_icon_size)
        self.down_icon = self.load_icon("down.png", self.arrow_icon_size)
        
        self.create_player_ui()
        self.create_playlist_ui()
        self.populate_playlist()
        
        if self.playlist.size > 0:
            self.after(100, lambda: self.on_select_song(0))
    
    def create_player_ui(self):
        # Area de Portada
        cover_frame = tk.Frame(self.left_frame, width=400, height=400, bg=self.left_bg, bd=0, relief="flat")
        cover_frame.pack(pady=(30,10))
        cover_frame.pack_propagate(False)
        self.cover_img = None
        self.cover_label = tk.Label(cover_frame, bg=self.left_bg)
        self.cover_label.pack(expand=True, fill="both")
        
        # Detalles de la Canción
        details_frame = tk.Frame(self.left_frame, bg=self.left_bg, bd=0)
        details_frame.pack(pady=10)
        self.song_title = tk.StringVar(value="Song Title")
        tk.Label(details_frame, textvariable=self.song_title, font=("Helvetica",22,"bold"),
                 fg="white", bg=self.left_bg).pack()
        self.artist = tk.StringVar(value="Artist Name")
        tk.Label(details_frame, textvariable=self.artist, font=("Helvetica",16),
                 fg="#CCCCCC", bg=self.left_bg).pack()
        self.album = tk.StringVar(value="Album Name")
        tk.Label(details_frame, textvariable=self.album, font=("Helvetica",14),
                 fg="#AAAAAA", bg=self.left_bg).pack()
        
        # Barra de Progreso y Temporizadores
        progress_frame = tk.Frame(self.left_frame, bg=self.left_bg, bd=0)
        progress_frame.pack(pady=10)
        self.current_time_label = tk.Label(progress_frame, text="0:00", font=("Helvetica",12),
                                           fg="white", bg=self.left_bg, width=6)
        self.current_time_label.pack(side="left", padx=5)
        self.progress_bar_width = 300
        self.progress_bar_height = 6
        self.progress_margin = 20
        self.thumb_radius = 6
        canvas_height = self.progress_bar_height + 20
        self.progress_canvas = tk.Canvas(progress_frame, width=self.progress_bar_width, height=canvas_height,
                                          bg=self.left_bg, highlightthickness=0, bd=0)
        self.progress_canvas.pack(side="left", padx=5)
        self.track_y = (canvas_height - self.progress_bar_height) / 2
        self.thumb_center_y = canvas_height / 2
        self.track = self.progress_canvas.create_rectangle(
            self.progress_margin, self.track_y,
            self.progress_bar_width - self.progress_margin, self.track_y + self.progress_bar_height,
            fill="#3C3C3C", outline="")
        self.progress_bar_fill = self.progress_canvas.create_rectangle(
            self.progress_margin, self.track_y,
            self.progress_margin, self.track_y + self.progress_bar_height,
            fill="#9c27b0", outline="")
        self.thumb = self.progress_canvas.create_oval(
            self.progress_margin - self.thumb_radius, self.thumb_center_y - self.thumb_radius,
            self.progress_margin + self.thumb_radius, self.thumb_center_y + self.thumb_radius,
            fill="#ffffff", outline="")
        self.progress_canvas.bind("<Button-1>", self.progress_click)
        self.progress_canvas.bind("<B1-Motion>", self.progress_click)
        self.total_time_label = tk.Label(progress_frame, text="3:45", font=("Helvetica",12),
                                         fg="white", bg=self.left_bg, width=6)
        self.total_time_label.pack(side="left", padx=5)
        
        # Controles de navegacion
        controls_frame = tk.Frame(self.left_frame, bg=self.left_bg, bd=0)
        controls_frame.pack(pady=20)
        self.btn_sound = tk.Button(controls_frame, image=self.vol_icon, bd=0, relief="flat",
                                   bg=self.left_bg, command=self.sound_action)
        self.btn_sound.pack(side="left", padx=10)
        self.prev_icon = self.load_icon("prev.png", self.icon_size)
        btn_prev = tk.Button(controls_frame, image=self.prev_icon, bd=0, relief="flat",
                             bg=self.left_bg, command=self.prev_song)
        btn_prev.pack(side="left", padx=10)
        self.play_icon = self.load_icon("play.png", self.play_icon_size)
        self.pause_icon = self.load_icon("pause.png", self.play_icon_size)
        self.play_pause_state = True
        self.btn_play = tk.Button(controls_frame, image=self.play_icon, bd=0, relief="flat",
                                  bg=self.left_bg, command=self.toggle_play)
        self.btn_play.pack(side="left", padx=10)
        self.next_icon = self.load_icon("next.png", self.icon_size)
        btn_next = tk.Button(controls_frame, image=self.next_icon, bd=0, relief="flat",
                             bg=self.left_bg, command=self.next_song)
        btn_next.pack(side="left", padx=10)
        self.like_icon = self.load_icon("like.png", self.icon_size)
        btn_like = tk.Button(controls_frame, image=self.like_icon, bd=0, relief="flat",
                             bg=self.left_bg, command=self.like)
        btn_like.pack(side="left", padx=10)
        self.share_icon = self.load_icon("share.png", self.icon_size)
        btn_share = tk.Button(controls_frame, image=self.share_icon, bd=0, relief="flat",
                              bg=self.left_bg, command=self.share)
        btn_share.pack(side="left", padx=10)
    
    def create_playlist_ui(self):
        playlist_header = tk.Frame(self.right_frame, bg=self.right_bg, bd=0)
        playlist_header.pack(fill="x", pady=(10,5))
        self.playlist_label = tk.Label(playlist_header, text="PlayList", font=("Helvetica",18,"bold"),
                                       fg="white", bg=self.right_bg)
        self.playlist_label.pack(side="left", padx=10)
        add_song_btn = tk.Button(playlist_header, image=self.add_icon, bd=0,
                                 bg=self.right_bg, command=self.add_song)
        add_song_btn.pack(side="right", padx=10)
        self.playlist_canvas = tk.Canvas(self.right_frame, bg=self.right_bg, highlightthickness=0, bd=0)
        self.playlist_canvas.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(self.right_frame, orient="vertical", command=self.playlist_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.playlist_canvas.configure(yscrollcommand=scrollbar.set)
        self.playlist_container = tk.Frame(self.playlist_canvas, bg=self.right_bg, bd=0)
        self.playlist_canvas.create_window((0,0), window=self.playlist_container, anchor="nw")
        self.playlist_container.bind("<Configure>", lambda event: self.playlist_canvas.configure(
            scrollregion=self.playlist_canvas.bbox("all")))
    
    def populate_playlist(self):
        for widget in self.playlist_container.winfo_children():
            widget.destroy()
        self.song_thumbs.clear()
        self.trash_icon = self.load_icon("trash.png", self.trash_icon_size)
        for idx in range(self.playlist.size):
            node = self.playlist.get_node(idx)
            self.create_playlist_item(idx, node.data)
        self.playlist_label.config(text=f"Up Next ({self.playlist.size})")
    
    def create_playlist_item(self, idx, song):
        # destacar cancion reproduciendo
        bg_color = self.highlight_bg if idx == self.current_index else self.right_bg
        item_frame = tk.Frame(self.playlist_container, bg=bg_color, bd=0)
        item_frame.pack(fill="x", pady=5, padx=5)
        item_frame.bind("<Button-1>", lambda e, index=idx: self.on_select_song(index))
        
        thumb_size = (50,50)
        try:
            thumb_path = os.path.join(self.img_dir, song["cover"])
            im = Image.open(thumb_path)
            im = im.resize(thumb_size, Image.LANCZOS)
            photo = ImageTk.PhotoImage(im)
        except Exception as e:
            print(f"Error loading thumbnail for {song['title']}: {e}")
            photo = None
        self.song_thumbs.append(photo)
        if photo:
            thumb_label = tk.Label(item_frame, image=photo, bg=bg_color)
        else:
            thumb_label = tk.Label(item_frame, text="No Img", bg=bg_color, fg="white", width=5, height=3)
        thumb_label.pack(side="left", padx=10, pady=5)
        thumb_label.bind("<Button-1>", lambda e, index=idx: self.on_select_song(index))
        
        info_frame = tk.Frame(item_frame, bg=bg_color, bd=0)
        info_frame.pack(side="left", fill="both", expand=True)
        display_title = song["title"] if len(song["title"]) <= 20 else song["title"][:20] + "..."
        title_label = tk.Label(info_frame, text=display_title, font=("Helvetica",14,"bold"), fg="white", bg=bg_color)
        title_label.pack(anchor="w")
        title_label.bind("<Button-1>", lambda e, index=idx: self.on_select_song(index))
        artist_label = tk.Label(info_frame, text=song["artist"], font=("Helvetica",12), fg="#CCCCCC", bg=bg_color)
        artist_label.pack(anchor="w")
        artist_label.bind("<Button-1>", lambda e, index=idx: self.on_select_song(index))
        
        controls_frame = tk.Frame(item_frame, bg=bg_color, bd=0)
        controls_frame.pack(side="right", padx=2)
        btn_up = tk.Button(controls_frame, image=self.up_icon, bd=0, relief="flat", bg=bg_color,
                           command=lambda idx=idx: self.move_song_up(idx))
        btn_up.pack(side="left", padx=1)
        btn_down = tk.Button(controls_frame, image=self.down_icon, bd=0, relief="flat", bg=bg_color,
                             command=lambda idx=idx: self.move_song_down(idx))
        btn_down.pack(side="left", padx=1)
        if self.trash_icon:
            btn_trash = tk.Button(controls_frame, image=self.trash_icon, bd=0, relief="flat", bg=bg_color,
                                  command=lambda idx=idx: self.delete_song_item(idx))
            btn_trash.pack(side="left", padx=1)
    
    def move_song_up(self, index):
        if index <= 0:
            return
        self.playlist.move_up(index)
        self.populate_playlist()
        print(f"Movida canción a la posición superior (índice {index})")
        if index - 1 == 0:
            self.current_index = 0
            self.on_select_song(0)
    
    def move_song_down(self, index):
        if index >= self.playlist.size - 1:
            return
        self.playlist.move_down(index)
        self.populate_playlist()
        print(f"Movida canción a la posición inferior (índice {index})")
        if index == 0:
            self.current_index = 0
            self.on_select_song(0)
    
    def delete_song_item(self, index):
        if index < 0 or index >= self.playlist.size:
            return
        self.playlist.delete_at_position(index)
        self.populate_playlist()
        print(f"Canción en índice {index} eliminada.")
        if self.playlist.size > 0:
            if self.current_index >= self.playlist.size:
                self.current_index = 0
            self.on_select_song(self.current_index)
        else:
            self.song_title.set("")
            self.artist.set("")
            self.album.set("")
            self.cover_label.config(image="", text="No Song", bg=self.left_bg)
            self.total_time_label.config(text="0:00")
            self.current_time_label.config(text="0:00")
    
    def add_song(self):
        filepath = filedialog.askopenfilename(title="Select a song",
                                              filetypes=(("MP3 files", "*.mp3"), ("All files", "*.*")))
        if filepath:
            song_name = os.path.basename(filepath)
            new_song = {"title": song_name, "artist": "Unknown Artist",
                        "duration": "00:00", "cover": "cover.jpg", "album": "Unknown Album"}
            self.playlist.insert_at_end(new_song)
            self.populate_playlist()
            print(f"Added song: {song_name}")
    
    def update_player_with_song(self, song):
        self.song_title.set(song["title"])
        self.artist.set(song["artist"])
        self.album.set(song["album"])
        try:
            cover_path = os.path.join(self.img_dir, song["cover"])
            cover_image = Image.open(cover_path)
            cover_image = cover_image.resize((400,400), Image.LANCZOS)
            self.cover_img = ImageTk.PhotoImage(cover_image)
            self.cover_label.config(image=self.cover_img, bg=self.left_bg, text="")
        except Exception as e:
            self.cover_label.config(text="No Cover", image="", bg="#333333", fg="white", font=("Helvetica",20))
        total_duration = song["duration"]
        self.total_seconds = self.convert_duration(total_duration)
        self.update_progress_bar(0)
        self.total_time_label.config(text=total_duration)
        self.current_time_label.config(text="0:00")
        print("Selected song:", song["title"])
    
    def on_select_song(self, index):
        self.current_index = index
        song = self.playlist.get_node(index).data
        self.update_player_with_song(song)
        self.populate_playlist()
    
    def update_progress_bar(self, pos):
        fraction = pos / self.total_seconds if self.total_seconds else 0
        effective_width = self.progress_bar_width - 2 * self.progress_margin
        new_fill_width = self.progress_margin + (fraction * effective_width)
        self.progress_canvas.coords(self.progress_bar_fill,
                                      self.progress_margin, self.track_y,
                                      new_fill_width, self.track_y + self.progress_bar_height)
        new_center_x = new_fill_width
        self.progress_canvas.coords(self.thumb,
                                      new_center_x - self.thumb_radius, self.thumb_center_y - self.thumb_radius,
                                      new_center_x + self.thumb_radius, self.thumb_center_y + self.thumb_radius)
        self.current_time_label.config(text=self.format_time(int(pos)))
    
    def progress_click(self, event):
        x = max(self.progress_margin, min(event.x, self.progress_bar_width - self.progress_margin))
        fraction = (x - self.progress_margin) / (self.progress_bar_width - 2 * self.progress_margin)
        new_pos = fraction * self.total_seconds if self.total_seconds else 0
        self.update_progress_bar(new_pos)
        print(f"Track position set to: {int(new_pos)} seconds")
    
    def update_volume(self, value):
        volume = int(value)
        print(f"Volume set to: {volume} %")
    
    def convert_duration(self, duration_str):
        try:
            minutes, seconds = duration_str.split(":")
            return int(minutes) * 60 + int(seconds)
        except Exception as e:
            print(f"Error converting duration '{duration_str}': {e}")
            return 0
    
    def format_time(self, seconds):
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}:{secs:02d}"
    
    def load_icon(self, filename, size=None):
        try:
            if size is None:
                size = self.icon_size
            icon_path = os.path.join(self.img_dir, filename)
            icon = Image.open(icon_path)
            icon = icon.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(icon)
        except Exception as e:
            print(f"Error loading icon {filename}: {e}")
            return None
    
    def next_song(self):
        if self.playlist.size == 0:
            return
        self.current_index = (self.current_index + 1) % self.playlist.size
        song = self.playlist.get_node(self.current_index).data
        self.update_player_with_song(song)
        self.populate_playlist()
        print("Next song selected")
    
    def prev_song(self):
        if self.playlist.size == 0:
            return
        self.current_index = (self.current_index - 1) % self.playlist.size
        song = self.playlist.get_node(self.current_index).data
        self.update_player_with_song(song)
        self.populate_playlist()
        print("Previous song selected")
    
    def toggle_play(self):
        if self.play_pause_state:
            self.btn_play.config(image=self.pause_icon if self.pause_icon else self.play_icon)
            print("Playing song")
        else:
            self.btn_play.config(image=self.play_icon)
            print("Pausing song")
        self.play_pause_state = not self.play_pause_state
    
    def like(self):
        print("Liked song")
    
    def share(self):
        print("Shared song")
    
    def sound_action(self):
        self.sound_on = not self.sound_on
        new_icon = self.vol_icon if self.sound_on else self.mute_icon
        self.btn_sound.config(image=new_icon)
        self.btn_sound.image = new_icon
        print("Sound on" if self.sound_on else "Mute on")

if __name__ == "__main__":
    app = Mp3Player()
    app.mainloop()
