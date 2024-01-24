import gradio as gr
from extractor import extract

# Define the Gradio Interface
iface = gr.Interface(fn=extract,
                     title="ChatParser",
                     description="Easier, faster, and more efficient way to extract text from Chat Screenshot.",
                     inputs=["text", "checkbox"],
                     outputs="json",
                     live=True)

# Launch the Gradio Interface
iface.launch(share=True, show_error=True)
