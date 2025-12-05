import tkinter as tk
from tkinter import messagebox
import random
import time

class RingSortGame:
    def __init__(self, root, difficulty):
        self.root = root
        self.difficulty = difficulty
        self.root.title(f"Ring Sort Game - {difficulty} Mode")
        
        window_width = 1000
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        
        self.root.configure(bg='#f4f4f4')
        self.poles = [[] for _ in range(7)]
        self.max_capacity = 9
        self.move_count = 0
        self.selected_ring = None
        self.colors = ["green", "red", "pink", "blue", "yellow"]
        self.init_rings()
        
        self.canvas = tk.Canvas(root, width=1000, height=450, bg='#eaeaea', bd=0)
        self.canvas.grid(row=0, column=0, columnspan=7, padx=20, pady=10)
        
        self.buttons = []
        for i in range(7):
            btn = tk.Button(root, text=f"Pole {i+1}", width=12, height=2, font=("Arial", 12, "bold"), 
                            bg="#ff8c00", activebackground="#e08e00", command=lambda i=i: self.select_pole(i))
            self.buttons.append(btn)
            self.buttons[i].grid(row=1, column=i, padx=5, pady=5)
        
        self.move_label = tk.Label(root, text=f"Moves: {self.move_count}", font=("Arial", 14, "bold"), fg="#333")
        self.move_label.grid(row=2, columnspan=7, pady=10)
        
        self.update_display()
        
    def init_rings(self):
        rings = ["green"] * 8 + ["red"] * 8 + ["pink"] * 8 + ["blue"] * 8 + ["yellow"] * 8
        random.shuffle(rings)
        for i in range(5):
            self.poles[i] = rings[i*8:(i+1)*8]

    def select_pole(self, index):
        if self.selected_ring is None:
            if self.poles[index]:
                self.selected_ring = (index, self.poles[index][-1])
        else:
            if self.move_ring(self.selected_ring[0], index, self.selected_ring[1]):
                self.move_count += 1
                self.move_label.config(text=f"Moves: {self.move_count}")
                self.check_win_condition()
            self.selected_ring = None
        self.update_display()

    def move_ring(self, from_pole, to_pole, ring):
        if not self.poles[from_pole]:
            return False
        if not self.poles[to_pole] or self.poles[to_pole][-1] == ring:
            if len(self.poles[to_pole]) < self.max_capacity:
                self.poles[to_pole].append(self.poles[from_pole].pop())
                return True
        return False
    
    def update_display(self):
        self.canvas.delete("all")
        for i in range(7):
            x = (i * 140) + 80
            self.canvas.create_line(x, 300, x, 120, width=4, fill="gray")
            for j, ring_color in enumerate(self.poles[i]):
                y_position = 300 - (j * 36)
                self.canvas.create_oval(x-18, y_position-18, x+18, y_position+18, fill=ring_color, outline="black", width=2)
    
    def check_win_condition(self):
        sorted_poles = 0
        for pole in self.poles:
            if len(pole) == 8 and all(color == pole[0] for color in pole):
                sorted_poles += 1
        
        if sorted_poles == 5:  # Check if all 5 colors are fully sorted
            self.display_congratulations()
    
    def display_congratulations(self):
        self.canvas.create_text(500, 200, text="Congratulations! 🎉", font=("Arial", 24, "bold"), fill="gold")
        self.canvas.create_text(500, 250, text="Level Completed! ✨", font=("Arial", 20, "bold"), fill="orange")
        self.show_spark_effects()
        messagebox.showinfo("Game Over", "Congratulations! You have completed the level!")

    def show_spark_effects(self):
        for _ in range(20):
            x, y = random.randint(200, 800), random.randint(150, 300)
            size = random.randint(5, 15)
            self.canvas.create_oval(x-size, y-size, x+size, y+size, fill="yellow", outline="gold")
            self.root.update()
            time.sleep(0.05)


def start_game(difficulty):
    root = tk.Tk()
    game = RingSortGame(root, difficulty)
    root.mainloop()

def show_difficulty_menu():
    menu = tk.Tk()
    menu.title("Select Difficulty")
    menu.geometry("400x300")
    menu.configure(bg='#f4f4f4')
    
    label = tk.Label(menu, text="Select Difficulty", font=("Arial", 16, "bold"), fg="#444")
    label.pack(pady=20)
    
    for text in ["Easy", "Medium", "Hard", "Conqueror"]:
        button = tk.Button(menu, text=text, font=("Arial", 14, "bold"), width=20, height=2, 
                           bg="#ff8c00", activebackground="#e08e00", 
                           command=lambda d=text: [menu.destroy(), start_game(d)])
        button.pack(pady=10)
    
    menu.mainloop()

show_difficulty_menu()
