import pygame
import sys
import os
from tkinter import Tk, filedialog, simpledialog, Button, Label, Frame, Checkbutton, IntVar, Scale, HORIZONTAL, Toplevel
from PIL import Image, ImageTk
import io


class SpriteSheetTester:
    def __init__(self):
        # Maximum dimensions for the sprite sliders
        self.MAX_SPRITE_WIDTH = 100
        self.MAX_SPRITE_HEIGHT = 100

        # Initialize pygame
        pygame.init()

        # Initialize tkinter for file dialogs and controls
        self.root = Tk()
        self.root.title("Cizzle's Sprite Sheet Tester")
        self.root.geometry("400x300")
        self.root.withdraw()  # Hide the main window initially

        # Sprite sheet properties
        self.sprite_sheet = None
        self.sprite_sheet_path = None
        self.sprite_width = 0
        self.sprite_height = 0
        self.cols = 0
        self.rows = 0
        self.total_frames = 0
        self.selected_frames = []

        # Animation properties
        self.current_frame = 0
        self.animation_speed = 10  # frames per second
        self.clock = pygame.time.Clock()

        # Display properties
        self.display_width = 800
        self.display_height = 600
        self.display = None
        self.zoom = 1

        # Create UI
        self.setup_ui()

    def setup_ui(self):
        self.root.deiconify()  # Show the main window

        # Create main frame
        main_frame = Frame(self.root)
        main_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Create buttons
        load_button = Button(
            main_frame, text="Load Sprite Sheet", command=self.load_sprite_sheet)
        load_button.pack(pady=5)

        # Sprite dimensions frame
        dim_frame = Frame(main_frame, bd=2, relief="groove")
        dim_frame.pack(pady=5, fill='x')

        Label(dim_frame, text="Sprite Dimensions").pack(pady=(5, 0))

        # Width input
        width_frame = Frame(dim_frame)
        width_frame.pack(fill='x', padx=5, pady=2)
        Label(width_frame, text="Width:").pack(side='left')
        self.width_var = IntVar(value=32)
        self.width_slider = Scale(
            width_frame, from_=1, to=self.MAX_SPRITE_WIDTH, orient=HORIZONTAL, variable=self.width_var)
        self.width_slider.pack(side='left', fill='x', expand=True, padx=5)

        # Height input
        height_frame = Frame(dim_frame)
        height_frame.pack(fill='x', padx=5, pady=2)
        Label(height_frame, text="Height:").pack(side='left')
        self.height_var = IntVar(value=32)
        self.height_slider = Scale(
            height_frame, from_=1, to=self.MAX_SPRITE_HEIGHT, orient=HORIZONTAL, variable=self.height_var)
        self.height_slider.pack(side='left', fill='x', expand=True, padx=5)

        # Apply dimensions button
        apply_dim_button = Button(
            dim_frame, text="Apply Dimensions", command=self.apply_sprite_dimensions)
        apply_dim_button.pack(pady=5)

        select_frames_button = Button(
            main_frame, text="Select Animation Frames", command=self.select_frames)
        select_frames_button.pack(pady=5)

        run_button = Button(main_frame, text="Run Animation",
                            command=self.run_animation)
        run_button.pack(pady=5)

        # Animation speed slider
        speed_frame = Frame(main_frame)
        speed_frame.pack(pady=5)

        speed_label = Label(speed_frame, text="Animation Speed (FPS):")
        speed_label.pack(side='left')

        self.speed_slider = Scale(
            speed_frame, from_=1, to=60, orient=HORIZONTAL)
        self.speed_slider.set(self.animation_speed)
        self.speed_slider.pack(side='left')

        # Zoom slider
        zoom_frame = Frame(main_frame)
        zoom_frame.pack(pady=5)

        zoom_label = Label(zoom_frame, text="Zoom Level:")
        zoom_label.pack(side='left')

        self.zoom_slider = Scale(zoom_frame, from_=1, to=10, orient=HORIZONTAL)
        self.zoom_slider.set(self.zoom)
        self.zoom_slider.pack(side='left')

        # Add a separator before status area
        separator = Frame(main_frame, height=2, bd=1, relief="sunken")
        separator.pack(fill='x', pady=10)

        # Create a styled status frame
        self.status_frame = Frame(
            main_frame, bd=2, relief="ridge", bg="#f0f0f0")
        self.status_frame.pack(fill='x', pady=5)

        # Add a title for the status area
        Label(self.status_frame, text="STATUS INFORMATION", font=("Arial", 10, "bold"),
              bg="#f0f0f0").pack(pady=(5, 0))

        # Create individual status fields with labels
        status_grid = Frame(self.status_frame, bg="#f0f0f0")
        status_grid.pack(padx=10, pady=5, fill='x')

        # File info
        Label(status_grid, text="Sprite Sheet:", bg="#f0f0f0", anchor='w', font=(
            "Arial", 9, "bold")).grid(row=0, column=0, sticky='w', padx=5)
        self.sprite_path_label = Label(
            status_grid, text="None", bg="#f0f0f0", anchor='w')
        self.sprite_path_label.grid(row=0, column=1, sticky='w')

        # Dimensions info
        Label(status_grid, text="Sheet Size:", bg="#f0f0f0", anchor='w', font=(
            "Arial", 9, "bold")).grid(row=1, column=0, sticky='w', padx=5)
        self.sheet_size_label = Label(
            status_grid, text="N/A", bg="#f0f0f0", anchor='w')
        self.sheet_size_label.grid(row=1, column=1, sticky='w')

        # Grid info
        Label(status_grid, text="Sprite Size:", bg="#f0f0f0", anchor='w', font=(
            "Arial", 9, "bold")).grid(row=2, column=0, sticky='w', padx=5)
        self.sprite_size_label = Label(
            status_grid, text="N/A", bg="#f0f0f0", anchor='w')
        self.sprite_size_label.grid(row=2, column=1, sticky='w')

        # Second column
        Label(status_grid, text="Grid:", bg="#f0f0f0", anchor='w', font=(
            "Arial", 9, "bold")).grid(row=0, column=2, sticky='w', padx=(20, 5))
        self.grid_label = Label(status_grid, text="N/A",
                                bg="#f0f0f0", anchor='w')
        self.grid_label.grid(row=0, column=3, sticky='w')

        # Frames info
        Label(status_grid, text="Total Frames:", bg="#f0f0f0", anchor='w', font=(
            "Arial", 9, "bold")).grid(row=1, column=2, sticky='w', padx=(20, 5))
        self.total_frames_label = Label(
            status_grid, text="0", bg="#f0f0f0", anchor='w')
        self.total_frames_label.grid(row=1, column=3, sticky='w')

        # Selected frames
        Label(status_grid, text="Selected:", bg="#f0f0f0", anchor='w', font=(
            "Arial", 9, "bold")).grid(row=2, column=2, sticky='w', padx=(20, 5))
        self.selected_frames_label = Label(
            status_grid, text="0", bg="#f0f0f0", anchor='w')
        self.selected_frames_label.grid(row=2, column=3, sticky='w')

        # General status message at the bottom
        self.status_message = Label(self.status_frame, text="Ready to load sprite sheet",
                                    bg="#f0f0f0", fg="#0066cc", font=("Arial", 9, "italic"))
        self.status_message.pack(pady=(0, 5))

        # Create empty row/column to make the grid expandable
        status_grid.grid_columnconfigure(1, weight=1)
        status_grid.grid_columnconfigure(3, weight=1)

        # Adjust window size to fit new controls
        self.root.geometry("500x500")

        self.root.mainloop()

    def update_status_display(self):
        """Update all status display fields with current information"""
        # Sprite sheet info
        if self.sprite_sheet_path:
            filename = os.path.basename(self.sprite_sheet_path)
            self.sprite_path_label.config(text=filename)

            if self.sprite_sheet:
                sheet_width, sheet_height = self.sprite_sheet.get_size()
                self.sheet_size_label.config(
                    text=f"{sheet_width} × {sheet_height} px")
            else:
                self.sheet_size_label.config(text="Error loading")
        else:
            self.sprite_path_label.config(text="None")
            self.sheet_size_label.config(text="N/A")

        # Sprite dimensions
        if self.sprite_width > 0 and self.sprite_height > 0:
            self.sprite_size_label.config(
                text=f"{self.sprite_width} × {self.sprite_height} px")
            self.grid_label.config(text=f"{self.cols} × {self.rows} cells")
            self.total_frames_label.config(text=str(self.total_frames))
        else:
            self.sprite_size_label.config(text="N/A")
            self.grid_label.config(text="N/A")
            self.total_frames_label.config(text="0")

        # Selected frames
        if self.selected_frames:
            self.selected_frames_label.config(
                text=f"{len(self.selected_frames)} frames")

            # Show first few frames and total count if many are selected
            if len(self.selected_frames) > 5:
                frame_str = f"{self.selected_frames[:5]}... ({len(self.selected_frames)} total)"
            else:
                frame_str = str(self.selected_frames)
        else:
            self.selected_frames_label.config(text="None")

    def load_sprite_sheet(self):
        """Open a file dialog to select a sprite sheet image"""
        self.sprite_sheet_path = filedialog.askopenfilename(
            title="Select Sprite Sheet Image",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")]
        )

        if self.sprite_sheet_path:
            try:
                # Initialize a temporary display if none exists
                temp_display = None
                if pygame.display.get_surface() is None:
                    temp_display = pygame.display.set_mode((1, 1))

                # Load the sprite sheet with Pygame
                self.sprite_sheet = pygame.image.load(
                    self.sprite_sheet_path).convert_alpha()
                sheet_width, sheet_height = self.sprite_sheet.get_size()

                # Close the temporary display if we created one
                if temp_display is not None and self.display is None:
                    pygame.display.quit()

                # Update slider max values based on sprite sheet dimensions, but respect maximum limits
                max_width = min(sheet_width, self.MAX_SPRITE_WIDTH)
                max_height = min(sheet_height, self.MAX_SPRITE_HEIGHT)

                self.width_slider.config(to=max_width)
                self.height_slider.config(to=max_height)

                # Set default dimensions to reasonable values based on the loaded image
                default_width = min(sheet_width // 4, 32)
                default_height = min(sheet_height // 4, 32)
                self.width_var.set(default_width)
                self.height_var.set(default_height)

                # Update status message
                self.status_message.config(
                    text=f"Loaded sprite sheet successfully"
                )

                # Update full status display
                self.update_status_display()

            except Exception as e:
                self.status_message.config(
                    text=f"Error loading sprite sheet: {str(e)}")
                self.sprite_sheet = None
                self.update_status_display()

    def apply_sprite_dimensions(self):
        """Apply the sprite dimensions from the sliders"""
        if not self.sprite_sheet:
            self.status_message.config(text="Please load a sprite sheet first")
            return

        # Update slider max values based on sprite sheet dimensions, but respect maximum limits
        max_width = min(self.sprite_sheet.get_width(), self.MAX_SPRITE_WIDTH)
        max_height = min(self.sprite_sheet.get_height(),
                         self.MAX_SPRITE_HEIGHT)

        self.width_slider.config(to=max_width)
        self.height_slider.config(to=max_height)

        # Get dimensions from sliders
        self.sprite_width = self.width_var.get()
        self.sprite_height = self.height_var.get()

        # Calculate number of rows and columns in the sprite sheet
        sheet_width, sheet_height = self.sprite_sheet.get_size()
        self.cols = sheet_width // self.sprite_width
        self.rows = sheet_height // self.sprite_height
        self.total_frames = self.cols * self.rows

        # By default, select all frames
        self.selected_frames = list(range(self.total_frames))

        # Update status message
        self.status_message.config(
            text=f"Dimensions applied: {self.sprite_width}×{self.sprite_height}, {self.total_frames} frames"
        )

        # Update full status display
        self.update_status_display()

    def select_frames(self):
        """Open a dialog to select frames for animation"""
        if not self.sprite_sheet or not self.sprite_width or not self.sprite_height:
            self.status_message.config(
                text="Please load a sprite sheet and set dimensions first")
            return

        # Create a new dialog window using Toplevel instead of Tk for better parent-child relationship
        frame_selector = Toplevel(self.root)
        frame_selector.title("Select Animation Frames")
        frame_selector.resizable(True, True)

        # Make dialog modal
        frame_selector.grab_set()

        # Create a label with instructions
        Label(frame_selector, text="Select frames for animation:").pack(
            pady=(10, 5))

        # Create frame for the checkbuttons
        frame_container = Frame(frame_selector)
        frame_container.pack(padx=10, pady=5)

        # Create a variable to track each frame's selection state
        frame_vars = []

        # Create a frame for displaying the sprite sheet
        sprite_frame = Frame(frame_selector, bd=2, relief="groove")
        sprite_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Add a label for the sprite sheet
        Label(sprite_frame, text="Sprite Sheet Reference:").pack(pady=(5, 0))

        # Image display label - create it once and update its image later
        image_label = Label(sprite_frame)
        image_label.pack(pady=10)

        # Function to create and update the sprite sheet image with selection overlay
        def update_sprite_sheet_image():
            # Initialize a temporary display if none exists
            temp_display = None
            if pygame.display.get_surface() is None:
                temp_display = pygame.display.set_mode((1, 1))

            try:
                # Get the sprite sheet as a surface
                surface = self.sprite_sheet

                # Create a new surface with grid lines and selection highlights
                width, height = surface.get_size()
                grid_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                grid_surface.blit(surface, (0, 0))

                # Get currently selected frames
                selected_indices = [i for i, var in enumerate(
                    frame_vars) if var.get() == 1]

                # Draw selection overlays for selected frames (semi-transparent blue)
                highlight_color = (0, 100, 255, 100)  # Semi-transparent blue
                for frame_idx in selected_indices:
                    col = frame_idx % self.cols
                    row = frame_idx // self.cols
                    x = col * self.sprite_width
                    y = row * self.sprite_height

                    # Create a selection rectangle
                    selection_surface = pygame.Surface(
                        (self.sprite_width, self.sprite_height), pygame.SRCALPHA)
                    selection_surface.fill(highlight_color)
                    grid_surface.blit(selection_surface, (x, y))

                # Draw grid lines
                grid_color = (255, 0, 0, 128)  # Semi-transparent red
                for i in range(self.cols + 1):
                    x = i * self.sprite_width
                    pygame.draw.line(grid_surface, grid_color,
                                     (x, 0), (x, height), 1)

                for i in range(self.rows + 1):
                    y = i * self.sprite_height
                    pygame.draw.line(grid_surface, grid_color,
                                     (0, y), (width, y), 1)

                # Convert pygame surface to PIL Image
                raw_str = pygame.image.tostring(grid_surface, "RGBA", False)
                image = Image.frombytes(
                    "RGBA", grid_surface.get_size(), raw_str)

                # Fixed reasonable dimensions for the displayed image
                available_width = 700
                available_height = 400

                scale_factor = min(available_width / width,
                                   available_height / height)
                if scale_factor < 1:
                    new_width = int(width * scale_factor)
                    new_height = int(height * scale_factor)
                    image = image.resize(
                        (new_width, new_height), Image.BICUBIC)

                # Convert to PhotoImage and update the display
                photo_image = ImageTk.PhotoImage(image)
                image_label.config(image=photo_image)
                image_label.image = photo_image  # Keep a reference to prevent garbage collection

                # Also store the reference at the class level
                frame_selector.sprite_sheet_img = photo_image

                # Close the temporary display if we created one
                if temp_display is not None and self.display is None:
                    pygame.display.quit()

                return True

            except Exception as e:
                import traceback
                traceback.print_exc()

                # Close the temporary display if we created one
                if temp_display is not None and self.display is None:
                    pygame.display.quit()

                return False

        # Function to create a checkbox with update functionality
        def create_checkbox(parent, row, col, frame_index):
            var = IntVar(value=1 if frame_index in self.selected_frames else 0)
            frame_vars.append(var)

            # When checkbox state changes, update the sprite sheet image
            def on_checkbox_change():
                update_sprite_sheet_image()

            cb = Checkbutton(parent, text=str(frame_index),
                             variable=var, command=on_checkbox_change)
            cb.grid(row=row, column=col, padx=5, pady=5, sticky='w')

        # Create a grid of checkbuttons representing each frame
        for i in range(self.rows):
            for j in range(self.cols):
                frame_index = i * self.cols + j
                create_checkbox(frame_container, i, j, frame_index)

        # Initial update of the sprite sheet image
        if not update_sprite_sheet_image():
            Label(sprite_frame, text="Could not display sprite sheet. Check console for details.").pack(
                pady=10)

        # Function to save the selection
        def save_selection():
            # Save the selected frames
            self.selected_frames = [
                i for i, var in enumerate(frame_vars) if var.get() == 1]

            # Update the status message
            self.status_message.config(
                text=f"Selected {len(self.selected_frames)} frames for animation")

            # Update the full status display
            self.update_status_display()

            # Destroy the dialog
            frame_selector.destroy()

        # Button to select all frames
        def select_all():
            for var in frame_vars:
                var.set(1)
            update_sprite_sheet_image()

        # Button to deselect all frames
        def deselect_all():
            for var in frame_vars:
                var.set(0)
            update_sprite_sheet_image()

        # Buttons for actions
        button_frame = Frame(frame_selector)
        button_frame.pack(pady=10)

        Button(button_frame, text="Select All",
               command=select_all).pack(side='left', padx=5)
        Button(button_frame, text="Deselect All",
               command=deselect_all).pack(side='left', padx=5)
        Button(button_frame, text="Save Selection",
               command=save_selection).pack(side='left', padx=5)

        # Set a reasonable default size
        frame_selector.geometry("800x600")

        # Center the dialog
        frame_selector.update_idletasks()
        width = frame_selector.winfo_width()
        height = frame_selector.winfo_height()
        x = (frame_selector.winfo_screenwidth() // 2) - (width // 2)
        y = (frame_selector.winfo_screenheight() // 2) - (height // 2)
        frame_selector.geometry(f"{width}x{height}+{x}+{y}")

        # Wait for the dialog to be closed
        frame_selector.wait_window()

    def get_frame_rect(self, frame_index):
        """Get the rectangle coordinates for a specific frame"""
        col = frame_index % self.cols
        row = frame_index // self.cols

        return pygame.Rect(
            col * self.sprite_width,
            row * self.sprite_height,
            self.sprite_width,
            self.sprite_height
        )

    def run_animation(self):
        """Run the animation with the selected frames"""
        if not self.sprite_sheet or not self.sprite_width or not self.sprite_height:
            self.status_message.config(
                text="Please load a sprite sheet and set dimensions first")
            return

        if not self.selected_frames:
            self.status_message.config(text="No frames selected for animation")
            return

        # Hide Tkinter window temporarily
        self.root.withdraw()

        # Create a pygame display window
        pygame.display.set_caption("Sprite Animation")
        self.display = pygame.display.set_mode(
            (self.display_width, self.display_height))

        # Get current animation speed and zoom from sliders
        self.animation_speed = self.speed_slider.get()
        self.zoom = self.zoom_slider.get()

        running = True
        frame_index = 0

        # Main animation loop
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_LEFT:
                        # Previous frame
                        frame_index = (
                            frame_index - 1) % len(self.selected_frames)
                    elif event.key == pygame.K_RIGHT:
                        # Next frame
                        frame_index = (
                            frame_index + 1) % len(self.selected_frames)
                    elif event.key == pygame.K_UP:
                        # Increase zoom
                        self.zoom = min(10, self.zoom + 1)
                    elif event.key == pygame.K_DOWN:
                        # Decrease zoom
                        self.zoom = max(1, self.zoom - 1)
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                        # Increase speed
                        self.animation_speed = min(
                            60, self.animation_speed + 1)
                    elif event.key == pygame.K_MINUS:
                        # Decrease speed
                        self.animation_speed = max(1, self.animation_speed - 1)

            # Clear screen
            self.display.fill((50, 50, 50))

            # Get the current frame to display
            current_frame_index = self.selected_frames[frame_index]
            frame_rect = self.get_frame_rect(current_frame_index)

            # Extract the current sprite from the sprite sheet
            sprite = self.sprite_sheet.subsurface(frame_rect)

            # Scale the sprite according to zoom level
            if self.zoom > 1:
                sprite = pygame.transform.scale(
                    sprite,
                    (self.sprite_width * self.zoom, self.sprite_height * self.zoom)
                )

            # Center the sprite on screen
            sprite_rect = sprite.get_rect(
                center=(self.display_width // 2, self.display_height // 2))

            # Draw the sprite
            self.display.blit(sprite, sprite_rect)

            # Draw frame information
            font = pygame.font.SysFont(None, 24)
            info_text = f"Frame: {current_frame_index} | Speed: {self.animation_speed} FPS | Zoom: {self.zoom}x"
            info_surface = font.render(info_text, True, (255, 255, 255))
            self.display.blit(info_surface, (10, 10))

            controls_text = "Controls: Arrow keys (Left/Right: change frame, Up/Down: zoom), +/- (speed), ESC (quit)"
            controls_surface = font.render(
                controls_text, True, (200, 200, 200))
            self.display.blit(controls_surface, (10, self.display_height - 30))

            # Update the display
            pygame.display.flip()

            # Move to the next frame for the next iteration
            frame_index = (frame_index + 1) % len(self.selected_frames)

            # Control the animation speed
            self.clock.tick(self.animation_speed)

        # Clean up pygame display
        pygame.display.quit()

        # Show Tkinter window again
        self.root.deiconify()

        # Update status
        self.status_message.config(text="Animation closed")


if __name__ == "__main__":
    app = SpriteSheetTester()
    pygame.quit()
    sys.exit()
