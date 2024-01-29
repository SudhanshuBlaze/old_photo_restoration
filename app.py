import gradio as gr
import os
import cv2
from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import PIL
import numpy as np
from gradio_imageslider import ImageSlider

# Specify the output directory
output_dir = 'output'

# Check if the output directory exists, create it if not
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created '{output_dir}' directory.")

img_colorization = pipeline(Tasks.image_colorization, model='iic/cv_ddcolor_image-colorization')

def color(image, filename):
    # Run colorization model
    output = img_colorization(image[...,::-1])
    result = output[OutputKeys.OUTPUT_IMG].astype(np.uint8)

    # Generate a meaningful filename based on the original file name
    base_name = os.path.splitext(os.path.basename(filename))[0]
    output_filename = os.path.join(output_dir, f"{base_name}_colorized.png")
    
    cv2.imwrite(output_filename, result)
    print('Inference finished!')
    
    # Return the input image and the path to the output image
    return (image, output_filename)

title = "old_photo_restoration"
description = "Upload old photo, ddcolor image colorization"
examples = [[os.path.join('assets', 'tajmahal.jpeg'),os.path.join('assets', 'oldhouse.jpeg'),],]

# Set up Gradio interface
demo = gr.Interface(
    fn=color,
    inputs=["image", "text"],
    outputs=ImageSlider(position=0.5, label='Colored image with slider-view'),
    examples=examples,
    title=title,
    description=description
)

if __name__ == "__main__":
    # Launch the Gradio app on port 8000
    demo.launch(share=False, server_port=8000)
