import tkinter as tk
from collections import deque
from PIL import Image, ImageTk 
import json
# assignment 8 
class TomAndJerryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tom and Jerry Game")
        self.grid_size = 10  
        self.tile_size = 50  

        self.canvas = tk.Canvas(self.root, width=self.grid_size * self.tile_size,
                                height=self.grid_size * self.tile_size)
        self.canvas.pack()

        self.tom_position = [0, 0]  
        self.jerry_position = [9, 9] 

        # Load and resize images for Tom and Jerry using Pillow
        self.tom_image_raw = Image.open("tom.png")  
        self.jerry_image_raw = Image.open("jerry.png")  

        # Resize the images to fit the tile size
        self.tom_image_raw = self.tom_image_raw.resize((self.tile_size, self.tile_size), Image.Resampling.LANCZOS)
        self.jerry_image_raw = self.jerry_image_raw.resize((self.tile_size, self.tile_size), Image.Resampling.LANCZOS)

        # Convert the images to a format that Tkinter can use
        self.tom_image = ImageTk.PhotoImage(self.tom_image_raw)
        self.jerry_image = ImageTk.PhotoImage(self.jerry_image_raw)

        self.create_grid()
        self.draw_characters()

        # Bind keys for Jerry's movement (Human player)
        self.root.bind("w", self.move_jerry_up)
        self.root.bind("s", self.move_jerry_down)
        self.root.bind("a", self.move_jerry_left)
        self.root.bind("d", self.move_jerry_right)

        self.ai_move_tom()

    def create_grid(self):
        """Draws the grid."""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.canvas.create_rectangle(i * self.tile_size, j * self.tile_size,
                                             (i + 1) * self.tile_size, (j + 1) * self.tile_size,
                                             fill="white", outline="black")

    def draw_characters(self):
        """Draws Tom and Jerry on the grid."""
        self.canvas.delete("tom")
        self.canvas.delete("jerry")
        
        # Draw Tom (AI) as an image
        self.canvas.create_image(self.tom_position[0] * self.tile_size + self.tile_size // 2, 
                                 self.tom_position[1] * self.tile_size + self.tile_size // 2,
                                 image=self.tom_image, tags="tom")

        # Draw Jerry (Human) as an image
        self.canvas.create_image(self.jerry_position[0] * self.tile_size + self.tile_size // 2,
                                 self.jerry_position[1] * self.tile_size + self.tile_size // 2,
                                 image=self.jerry_image, tags="jerry")

    def move_jerry(self, dx, dy):
        """Moves Jerry (human) and redraws the grid."""
        new_x = max(0, min(self.grid_size - 1, self.jerry_position[0] + dx))
        new_y = max(0, min(self.grid_size - 1, self.jerry_position[1] + dy))
        self.jerry_position = [new_x, new_y]
        self.draw_characters()
        self.check_for_catch()

    def move_jerry_up(self, event):
        self.move_jerry(0, -1)

    def move_jerry_down(self, event):
        self.move_jerry(0, 1)

    def move_jerry_left(self, event):
        self.move_jerry(-1, 0)

    def move_jerry_right(self, event):
        self.move_jerry(1, 0)

    def ai_move_tom(self):
        queue = deque([(self.tom_position, [])]) 
        visited = set()

        while queue:
            (x, y), path = queue.popleft()

            if (x, y) == tuple(self.jerry_position):
                if path:
                    next_move = path[0]
                    self.tom_position = [next_move[0], next_move[1]]
                break

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))

        self.draw_characters()
        self.check_for_catch()

        self.root.after(500, self.ai_move_tom)

    def check_for_catch(self):
        """Checks if Tom (AI) caught Jerry (Human)."""
        if self.tom_position == self.jerry_position:
            self.canvas.create_text(self.grid_size * self.tile_size // 2,
                                    self.grid_size * self.tile_size // 2,
                                    text="Tom Caught Jerry!", font=("Helvetica", 24), fill="green")
            self.root.unbind("w")
            self.root.unbind("s")
            self.root.unbind("a")
            self.root.unbind("d")


if __name__ == "__main__":
    root = tk.Tk()
    game = TomAndJerryGame(root, language='fr')  
    root.mainloop()
