import tkinter as tk
import requests
import json
import pyttsx3

# Function to handle chat interaction
def get_chat_response(query):
    url = 'http://localhost:11434/api/chat'
    payload = {
        "model": "dolphin-llama3:8b",
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ]
    }

    response = requests.post(url, json=payload, stream=True)

    accumulated_content = ''  # Variable to accumulate content from streamed responses

    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, f"\nYou: {query}\nAssistant: ")

    for line in response.iter_lines():
        if line:
            json_response = json.loads(line.decode('utf-8'))  # Decode bytes to string and parse JSON
            # Extract content from the message part of the response
            message_content = json_response.get('message', {}).get('content', '')
            text_area.insert(tk.END, f"{message_content} ")
            # Accumulate content from each response
            accumulated_content += ' ' + message_content.strip()

    # After the loop, json_response should contain the last streamed object
    final_response = json_response  # Assuming json_response contains the last streamed object
    
    text_area.insert(tk.END, "\n\n")   
    text_area.config(state=tk.DISABLED)
    
    return accumulated_content.strip()

# Function to speak the accumulated response with a delay
def speak_response_with_delay(response, delay=500):
    def speak_with_delay():
        engine = pyttsx3.init()
        engine.say(response)
        engine.runAndWait()
    
    # Schedule the speech function after the delay
    text_area.after(delay, speak_with_delay)

# Function to handle button click event
def on_submit():
    query = entry.get()  # Get user input from entry field
    if query:
        response = get_chat_response(query)
        speak_response_with_delay(response)
        entry.delete(0, tk.END)  # Clear the entry field

# Create the main window
def create_gui():
    root = tk.Tk()
    root.title("Text-to-Speech Assistant")

    # Create text area to display conversation
    global text_area
    text_area = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Create entry field for user input
    global entry
    entry = tk.Entry(root)
    entry.pack(padx=10, pady=(0, 10), fill=tk.BOTH)

    # Create submit button
    submit_btn = tk.Button(root, text="Submit", command=on_submit)
    submit_btn.pack(padx=10, pady=(0, 10), fill=tk.BOTH)

    # Start the Tkinter main loop
    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    create_gui()
