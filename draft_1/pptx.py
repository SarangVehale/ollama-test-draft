
m pptx import Presentation

def process_ppt(file_path):
    prs = Presentation(file_path)
    text = ''
    
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, 'text'):
                text += shape.text
    return text

