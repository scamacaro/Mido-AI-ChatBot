"""
Sanyerlis Camacaro - CSC235 - Sancamac@uat.edu Assignment:
Assignment 3.1: Your Third Assignment

"Mido Chat Bot"

Requirements and Expectations:

Create a new Python application.
Give your program the ability to do new things and have new features using 3rd party libraries. 
Give your program the ability to do new things and have new features using Python packages.
Your application must do something innovative and interesting, not just demo libraries and objects.
Make a great User experience.
Over comment your code showing your intent and your understanding of what your code does. 

Reminder, this code works, but does not open in my computer. Professor Hinton tested it successfully 
on his computer.
"""
# Import our libraries
import os
# Import our libraries for the GUI tkinter
import tkinter as tk
# Import our libraries to create a text area with a scrollbar
from tkinter import scrolledtext
# Import our libraries to load our language model and generate responses
from llama_cpp import Llama
# Import our random libraries to generate random numbers
import random
# Import a library to get the current date
import datetime

# Create a global variable for the pathto our model
# If you  use different model later, you need to change this path
############## This is where you change the path to your model ############
model_path = "llama-2-7b-chat.Q5_K_M.gguf"

# Create a global variable to set the version of your application
version = "1.00"

# Get the current date and stuff into a variable
todays_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Create function to load our model
def load_model():
    # check if the model path is valid
    if not os.path.isfile(model_path):
        print("ERROR: The model path is not valid, please check the path in the main.py file")
        print("and make sure the model is in the same folder as the main.py file")
        # If the model path is not valid, exist the program
        exit()

    # If not the model path is valid, load the model
    global model
    model = Llama(
        model_path=model_path,
        seed=random.randint(1, 2**31)
    )

# Create function to generate a response
def generate_response(model, input_tokens, prompt_input_text):
    # Display the input text in the text area response on top
    text_area_display.insert(tk.INSERT, '\n\nUser: ' + prompt_input_text + '\n')

    output_response_text = b""
    count = 0
    output_response_text = b"\n\nHAL9000:"
    text_area_display.insert(tk.INSERT, output_response_text)
    #Generate a response
    for token in model.generate(input_tokens, top_k=40, top_p=0.95, temp=0.72, repeat_penalty=1.1):
        # Extract the response text from the output of the model which is in token 
        # format and convert it to a string
        response_text = model.detokenize([token])
        output_response_text = response_text.decode()
        # Display the respone text in the textarea response on top
        text_area_display.insert(tk.INSERT, output_response_text)
        root.update_idletasks()
        count += 1
        # Now that we have a response, we can break out of the loop
        if count > 2000 or (token == model.token_eos()):
            break
        # And we can clear in the input to let the user know the response 
        # from the model is complete
        text_area_main_user_input.delete('1.0', 'end')

# Create a function to send a message to the model and display a response
def send_message():
    # Get the text from the textarea input that the user typed in.
    user_prompt_input_text = text_area_main_user_input.get('1.0', 'end-1c')
    # Delete any leading or tralling spaces from the user input.
    user_prompt_input_text = user_prompt_input_text.strip()
    # ecode the message with uft-8
    byte_message = user_prompt_input_text.encode('utf-8')

    # Here is where you can change the prompt formart for the LLM.
    # This is something you will need to experiment to get the best result.
    input_tokens = model.tokenize(b"### Human: " + byte_message + b"\n### Assistant: ")

    # print out the inpt tokens to the console for debugging and information on how this works.
    print("Input tokens:", input_tokens)
    # Call the generate_response function to generate a response
    generate_response(model, input_tokens, user_prompt_input_text)

# Our main function to build to GUI
def main():
    # Load our model when our app starts!
    load_model()
    # Create our GUI
    # Remember root is in this case our main window
    global root
    root =tk.Tk()
   
    # Set the title of our app
    root.title("Hal900 -v" + version + " - " + todays_date)    
    # Create a frame to add a scrollbar to our textarea
    frame_display = tk.Frame(root)
    scrollbar_frame_display = tk.Scrollbar(frame_display)
    # The text area where we will display the response from the model plus the user input together
    # This will allow to see the conversation between the user and the model in one place
    global text_area_display
    text_area_display = scrolledtext.ScrolledText(frame_display, height=25, width=128, yscrollcommand=scrollbar_frame_display.set)
    # Create our color here. You can change these to whatever you want.
    my_light_yellow = "#ffff33"
    my_dark_grey = "#202020"
    # Set the background and foreground colors of the textarea, and font. change these to whatever you want.
    text_area_display.config(background=my_dark_grey, foreground=my_light_yellow, font=("Courier", 12))
    scrollbar_frame_display.config(command=text_area_display.yview)
    text_area_display.pack(side=tk.RIGHT, fill=tk.BOTH)
    scrollbar_frame_display.pack(side=tk.RIGHT, fill=tk.Y)
    # Fill our root window with the frame
    frame_display.pack()

    frame_controls = tk.Frame(root)
    # Create a label to let the user knwo what LLM model and path to the model we are currently using
    model_path_label = tk.Label(frame_controls, text="Model Path: " + model_path, font=("Courier", 12))
    model_path_label.pack(side=tk. LEFT, padx=10)
    frame_controls.pack(fill=tk.BOTH, padx=5, pady=5)

    # Create our frame for the user input, remember this at tthe bottom of out app
    frame_user_input = tk.Frame(root)
    frame_user_input.pack(fill=tk.BOTH)

    frame_main_user_input = tk.Frame(root)
    scrollbar_main_user_input = tk.Scrollbar(frame_main_user_input)

    global text_area_main_user_input
    text_area_main_user_input = scrolledtext.ScrolledText(frame_main_user_input, height=5, width=128, yscrollcommand=scrollbar_main_user_input.set)
    # Set the background and foregroybd colors of tge textarea, abd font. Change these to whatever you want.
    text_area_main_user_input.config(background=my_dark_grey, foreground=my_light_yellow, font=("Courier",12))
    scrollbar_main_user_input.config(command=text_area_main_user_input.yview)
    # Fill our roort window with the frame
    text_area_main_user_input.pack(side=tk.LEFT, fill=tk.BOTH)
    scrollbar_main_user_input.pack(side=tk.RIGHT,fill=tk.Y)
    frame_main_user_input.pack()

    # Create a button to send the user input to the model
    # Remember the enter key will NOT send the user input to the model. You must press the button! Howeever, you can change the
    send_button = tk.Button(root, text="Send", command=send_message)
    # Fill our roort window with the button
    send_button.pack()
    # Must have this run our app
    root.mainloop()

# App start here
if __name__ == "__main__":
    # Call our main function to start the app!
    main()