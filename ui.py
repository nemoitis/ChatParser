import gradio as gr
from extractor import extract

# Define input fields
urlText = gr.Text(placeholder='URL of the image', label='URL', autofocus=True, show_copy_button=True)
switchFormatCheckBox = gr.Checkbox(value=False, label='Switch Format')

# Define the output field
jsonOutput = gr.Json(label="Parsed Text")

# Define the Gradio Interface
iface = gr.Interface(fn=extract,
                     title="ChatParser",
                     description="Easier, faster, and more efficient way to extract text from Chat Screenshot.",
                     inputs=[urlText, switchFormatCheckBox],
                     outputs=jsonOutput,
                     live=True)

# Launch the Gradio Interface
iface.launch(share=False, show_error=True)
