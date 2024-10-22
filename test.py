import pygame
import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import numpy as np
import math

# Initialize Pygame
pygame.init()

# Create Tkinter window
root = tk.Tk()
root.title("Pygame in Tkinter")

# Create Canvas in Tkinter
canvas = Canvas(root, width=500, height=400)
canvas.pack()

# Create a Pygame surface
pygame_surface = pygame.Surface((500, 400))

# Load the ant image
ant_image = pygame.image.load('ant.png')  # Replace with the correct path to your image
ant_image = pygame.transform.scale(ant_image, (60, 60))  # Resize if needed

# Ball (ant) properties
ball_x = 250  # Initial X position
ball_y = 200  # Initial Y position
ball_dx = 5  # Speed in X direction
ball_dy = 3  # Speed in Y direction
ant_width, ant_height = ant_image.get_size()  # Get the dimensions of the image


# Function to convert Pygame surface to a format Tkinter can display
def pygame_to_tk_image(surface):
    # Convert Pygame surface to a string of pixels
    image_data = pygame.surfarray.array3d(surface)
    # Convert the data to an Image using PIL
    image = Image.fromarray(np.transpose(image_data, (1, 0, 2)))
    # Convert the image to a format that Tkinter can use
    return ImageTk.PhotoImage(image)


# Update function to redraw Pygame surface in Tkinter
def update_canvas():
    global ball_x, ball_y, ball_dx, ball_dy

    # Fill Pygame surface with a background color
    pygame_surface.fill((0, 128, 255))

    # Move the ball (ant)
    ball_x += ball_dx
    ball_y += ball_dy

    # Bounce off the edges (left, right)
    if ball_x - ant_width // 2 <= 0 or ball_x + ant_width // 2 >= pygame_surface.get_width():
        ball_dx = -ball_dx  # Reverse direction

    # Bounce off the edges (top, bottom)
    if ball_y - ant_height // 2 <= 0 or ball_y + ant_height // 2 >= pygame_surface.get_height():
        ball_dy = -ball_dy  # Reverse direction

    # Calculate the angle of movement
    angle = math.degrees(math.atan2(-ball_dy, ball_dx))  # Inverse Y-axis for Pygame

    # Rotate the ant image based on the angle
    rotated_ant = pygame.transform.rotate(ant_image, angle)

    # Get the new dimensions of the rotated image
    rotated_width, rotated_height = rotated_ant.get_size()

    # Draw the rotated ant image, centered at (ball_x, ball_y)
    pygame_surface.blit(rotated_ant, (ball_x - rotated_width // 2, ball_y - rotated_height // 2))

    # Convert Pygame surface to Tkinter-compatible image
    img = pygame_to_tk_image(pygame_surface)

    # Add image to the canvas
    canvas.create_image(0, 0, anchor=tk.NW, image=img)

    # Keep a reference to avoid garbage collection
    canvas.image = img

    # Call this function again after 30ms
    root.after(30, update_canvas)


# Start the update loop
update_canvas()

# Run Tkinter event loop
root.mainloop()

# Quit Pygame when done
pygame.quit()
