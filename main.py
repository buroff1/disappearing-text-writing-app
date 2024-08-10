# Import the necessary modules and classes from the customtkinter package
from customtkinter import *


def center_window_to_display(screen: CTk, width: int, height: int, scale_factor: float = 1.0):
    """Centers the window to the main display/monitor"""
    screen_width = screen.winfo_screenwidth()  # Get the width of the screen
    screen_height = screen.winfo_screenheight()  # Get the height of the screen
    x = int(((screen_width / 2) - (width / 2)) * scale_factor)  # Calculate x-coordinate for centering
    y = int(((screen_height / 2) - (height / 1.5)) * scale_factor)  # Calculate y-coordinate for centering
    return f"{width}x{height}+{x}+{y}"  # Return the geometry string for the window


def update_label(value):
    """Updates the label to show the selected number of seconds"""
    sec_label.configure(text=f"{int(value)} seconds")  # Update the label with the slider value


def fade_out(window):
    """Gradually fades out a window by reducing its opacity"""
    alpha = window.attributes("-alpha")  # Get current opacity of the window
    if alpha > 0:  # If the window is not fully transparent
        alpha -= 0.1  # Decrease the opacity
        window.attributes("-alpha", alpha)  # Apply new opacity
        window.after(30, fade_out, window)  # Schedule the next step in the fade out process
    else:
        window.withdraw()  # Hide the window when it becomes fully transparent


def fade_in(window):
    """Gradually fades in a window by increasing its opacity"""
    alpha = window.attributes("-alpha")  # Get current opacity of the window
    if alpha < 1:  # If the window is not fully opaque
        alpha += 0.1  # Increase the opacity
        window.attributes("-alpha", alpha)  # Apply new opacity
        window.after(30, fade_in, window)  # Schedule the next step in the fade in process


def start_typing():
    """Starts the typing window with fade-in effect and sets up the text disappear functionality"""
    fade_out(app)  # Fade out the main application window
    typing_window = CTkToplevel(app)  # Create a new top-level window for typing
    typing_window.title("Typing Window")  # Set the title of the typing window
    typing_window.iconbitmap("clock.ico")  # Set the icon for the typing window
    typing_window.configure(bg="#333333")  # Set background color for typing window
    typing_window.resizable(False, False)  # Make the typing window non-resizable
    typing_window.attributes("-alpha", 0)  # Start with full transparency

    # Create a label with instructions
    typing_label = CTkLabel(typing_window, text="Start typing below. The text will disappear after the set time.",
                            font=("Roboto", 20), text_color="white")
    typing_label.pack(pady=20)  # Add padding around the label

    # Create a text widget for typing
    text_widget = CTkTextbox(typing_window, height=400, width=600, font=("Roboto", 15), fg_color="#fff",
                             text_color="black", )
    text_widget.pack(pady=20)  # Add padding around the text widget

    # Create an exit button
    exit_button = CTkButton(typing_window, text="Exit", corner_radius=32, font=("Roboto", 20), command=app.destroy,
                            fg_color="#225AC7", hover_color="#3335AF")
    exit_button.pack(pady=20)  # Add padding around the button

    def disappear_text():
        """Clears the text in the text widget"""
        text_widget.delete("1.0", END)  # Delete all text from the widget

    def reset_timer(event=None):
        """Resets the timer to clear text after a set time when a key is pressed"""
        if hasattr(reset_timer, 'timer_id'):  # Check if the timer_id attribute exists
            typing_window.after_cancel(reset_timer.timer_id)  # Cancel the previous timer
        reset_timer.timer_id = typing_window.after(var.get() * 1000, disappear_text)  # Start a new timer

    text_widget.bind("<Key>", reset_timer)  # Bind key press event to reset the timer

    # Center the typing window on the screen
    typing_window.geometry(center_window_to_display(app, 650, 600, app._get_window_scaling()))
    fade_in(typing_window)  # Fade in the typing window


# Create the main application window
app = CTk()  # Create an instance of CTk
app.title("Disappearing Text Writing App")  # Set the title of the main window
app.iconbitmap("clock.ico")  # Set the icon for the main window
app.resizable(False, False)  # Make the main window non-resizable
app.attributes("-alpha", 1)  # Ensure the app starts with full opacity

# Set app background color
app_bg_color = "#333333"

var = IntVar(value=5)  # Create an IntVar to store the slider value, default is 5 seconds

# Create a frame to hold the widgets and center it in the main window
frame = CTkFrame(app, fg_color="transparent")  # Set frame background color
frame.pack(expand=True)  # Expand the frame to fill available space

# Create a label for the app title
label = CTkLabel(frame, text="Disappearing Text Writing App", font=("Roboto", 35), text_color="white")
label.pack(pady=10)  # Add padding around the label

# Create a label for the time choice
choice_label = CTkLabel(frame, text="Time for text to disappear", font=("Roboto", 30), text_color="white")
choice_label.pack(pady=10)  # Add padding around the label

# Create a label to display the selected time
sec_label = CTkLabel(frame, text='', font=("Roboto", 40), text_color="#FFD700")
sec_label.pack(pady=10)  # Add padding around the label

# Create a slider to select time
slider = CTkSlider(frame, from_=5, to=100, number_of_steps=95, orientation="horizontal", height=16, variable=var,
                   command=update_label, fg_color="#FFD700", progress_color="#FFD700", button_color="#FFD700",
                   button_hover_color="#d1b000")
slider.pack(pady=10)  # Add padding around the slider

# Initialize the label with the default slider value
update_label(var.get())  # Set initial label value to match the slider's default

# Create a button to start the typing activity
button = CTkButton(frame, text="Start Typing", corner_radius=32, font=("Roboto", 20), command=start_typing,
                   fg_color="#225AC7", hover_color="#3335AF")
button.pack(pady=20)  # Add padding around the button

# Center the main application window on the screen
app.geometry(center_window_to_display(app, 650, 600, app._get_window_scaling()))

app.mainloop()  # Start the main loop to run the application
