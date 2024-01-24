import gradio as gr
from extractor import extract as textract

# Define the function to be used by Gradio
def extract(url: str, list: bool = False):
    try:
        result = textract(url, list)
        return result
    except Exception as e:
        return {'error': str(e)}

# Define the Gradio Interface
iface = gr.Interface(fn=extract, 
                     inputs=["text", "checkbox"], 
                     outputs="text",
                     live=True)

# Launch the Gradio Interface
iface.launch(share=True)
