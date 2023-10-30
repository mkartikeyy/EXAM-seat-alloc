import random
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import Entry, Button, Label, Frame, Scrollbar, Canvas, Text, VERTICAL

# Function to create and display an image for a room's seating arrangement with a grid (max 5 columns)
def create_room_image(room_name, seats):
    # Calculate the image size based on the number of seats
    seat_count = len(seats)
    max_columns = min(5, seat_count)
    cell_size = 100
    image_width = max_columns * cell_size
    rows = (seat_count + max_columns - 1) // max_columns
    cell_height = 100
    image_height = rows * cell_height

    # Create a blank image with a white background
    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()  # Use the default font

    for i in range(1, max_columns):
        x = i * cell_size
        draw.line([(x, 0), (x, image_height)], fill="black", width=2)
    for i in range(1, rows):
        y = i * cell_height
        draw.line([(0, y), (image_width, y)], fill="black", width=2)

    # Draw seats and student
    for i, (seat, student) in enumerate(seats.items()):
        col = i % max_columns
        row = i // max_columns
        x = (col * cell_size) + (cell_size / 2)
        y = (row * cell_height) + (cell_height / 2)

        seat_text, student_text = seat, student

        # position
        seat_bbox = draw.textbbox((x, y), seat_text, font=font)
        student_bbox = draw.textbbox((x, y), student_text, font=font)
        seat_x_pos = x - (seat_bbox[2] - seat_bbox[0]) / 2
        seat_y_pos = y - (seat_bbox[3] - seat_bbox[1] + student_bbox[3] - student_bbox[1]) / 2
        student_x_pos = x - (student_bbox[2] - student_bbox[0]) / 2
        student_y_pos = y + (seat_bbox[3] - seat_bbox[1] + student_bbox[3] - student_bbox[1]) / 2

        # Create a rectangle behind the student number for highlighting
        padding = 5  # Adjust this value to control the padding around the student number
        rect_x1 = student_bbox[0] - padding
        rect_y1 = student_bbox[1] - padding
        rect_x2 = student_bbox[2] + padding
        rect_y2 = student_bbox[3] + padding
        draw.rectangle([(rect_x1, rect_y1), (rect_x2, rect_y2)], fill="yellow")

        draw.text((seat_x_pos, seat_y_pos), seat_text, fill="black", font=font, anchor="mm")
        draw.text((student_x_pos, student_y_pos), student_text, fill="black", font=font, anchor="mm")

    return image

# Function to generate seating arrangement
def generate_seating_arrangement():
    # Read the number of exam rooms
    num_exam_rooms = int(num_rooms_entry.get())
    room_capacities = []

    # Read capacities for each room
    for i in range(num_exam_rooms):
        capacity = int(capacity_entries[i].get())
        room_capacities.append(capacity)

    num_students = sum(room_capacities)
    students = [f"{i+1}" for i in range(num_students)]
    random.shuffle(students)

    images = []

    for i, room_capacity in enumerate(room_capacities):
        room = f"Room {i+1}"
        seat_allocation = {}
        for j in range(room_capacity):
            seat = f"Seat {j+1}"
            if students:
                student = students.pop()
                seat_allocation[seat] = student

        # Create an image for the room's seating arrangement
        room_image = create_room_image(room, seat_allocation)
        
        # Add room numbers to the image
        font = ImageFont.load_default()
        draw = ImageDraw.Draw(room_image)
        draw.text((10, 10), room, fill="black", font=font)
        
        images.append(room_image)

    # Calculate the total width and height for the result image
    total_width = max(image.width for image in images) + 20  # Add some space for room numbers
    total_height = sum(image.height for image in images) + 20 * (len(images) - 1)  # Add space between images

    result_image = Image.new("RGB", (total_width, total_height), "white")
    y_offset = 10  # Initial offset for room numbers
    for image in images:
        result_image.paste(image, (10, y_offset))
        y_offset += image.height + 20  # Update the offset for the next room

    # Display the result image
    result_image.show()
    
# Create a Tkinter window
app = tk.Tk()
app.title("Seating Arrangement Generator")

# Input fields and labels for the number of rooms
num_rooms_label = Label(app, text="Enter the number of exam rooms:")
num_rooms_label.pack()
num_rooms_entry = Entry(app)
num_rooms_entry.pack()

# Function to dynamically add capacity input fields based on the number of rooms
def add_capacity_fields():
    num_rooms = int(num_rooms_entry.get())
    for i in range(num_rooms):
        label = Label(app, text=f"Capacity for Room {i + 1} (max 20):")
        label.pack()
        entry = Entry(app)
        entry.pack()
        capacity_entries.append(entry)

add_capacity_button = Button(app, text="Add Capacity Fields", command=add_capacity_fields)
add_capacity_button.pack()

# List to store the capacity input fields
capacity_entries = []

# Generate button to create seating arrangement
generate_button = Button(app, text="Generate Seating Arrangement", command=generate_seating_arrangement)
generate_button.pack()

# Start the Tkinter main loop
app.mainloop()
