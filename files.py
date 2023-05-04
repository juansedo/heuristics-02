from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_PARAGRAPH_ALIGNMENT
from utils import summary_plot

def get_test_file(id):
    with open(f"data/mtVRP{id}.txt") as f:
        lines = [line.rstrip() for line in f]
        lines = [line.split() for line in lines]
        lines = [[int(x) for x in line] for line in lines]
    return [lines[0], lines[1:]]

class Slides:
    output_path = './outputs/'
    
    def __init__(self, title, subtitle, total_pages = 10):
        self.prs = Presentation()
        self.title_slide_layout = self.prs.slide_layouts[0]
        self.image_slide_layout = self.prs.slide_layouts[5]
        self.page = 1
        self.total_pages = total_pages
        self.data = {}
        
        slide = self.prs.slides.add_slide(self.title_slide_layout)
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = RGBColor(179, 229, 252)

        slide.shapes.title.text = title
        slide.shapes.title.text_frame.paragraphs[0].font.color.rgb = RGBColor(0, 0, 0)
        slide.shapes.title.text_frame.paragraphs[0].font.bold = True

        slide.placeholders[1].text = subtitle
        slide.placeholders[1].text_frame.paragraphs[0].font.color.rgb = RGBColor(0, 0, 0)
        slide.placeholders[1].text_frame.paragraphs[0].font.size = Pt(16)
    
    def add_method_slide(self, method, filename, description = ''):
        slide = self.prs.slides.add_slide(self.image_slide_layout)
        
        slide.shapes.title.text = method + " results"
        slide.shapes.title.bold = True
        slide.shapes.add_picture(Slides.output_path + filename, left=Inches(1), top=Inches(1.5), width=Inches(8), height=Inches(5.25))

        txBox = slide.shapes.add_textbox(left=Inches(0), top=Inches(6.4), width=Inches(5), height=Inches(1))
        p = txBox.text_frame.add_paragraph()
        p.text = description
        p.font.size = Pt(14)
        p.alignment = PP_PARAGRAPH_ALIGNMENT.LEFT
        
        txBox = slide.shapes.add_textbox(left=Inches(9), top=Inches(6.75), width=Inches(1), height=Inches(1))
        p = txBox.text_frame.add_paragraph()
        p.text = str('{}/{}'.format(self.page, self.total_pages))
        p.font.size = Pt(10)
        
        self.page += 1
    
    def add_method_value(self, method, filename, value):
        if (not method in self.data): self.data[method] = []
        self.data[method].append([filename, value])

    def generate_summary(self):
        summary_plot("summary", self.data)
        slide = self.prs.slides.add_slide(self.image_slide_layout)
        
        slide.shapes.title.text = "General comparison"
        slide.shapes.title.bold = True
        slide.shapes.add_picture(Slides.output_path + "summary.png", left=Inches(0.25), top=Inches(1.5), width=Inches(9.5), height=Inches(5.5))
        
        txBox = slide.shapes.add_textbox(left=Inches(9), top=Inches(6.75), width=Inches(1), height=Inches(1))
        p = txBox.text_frame.add_paragraph()
        p.text = str('{}/{}'.format(self.page, self.total_pages))
        p.font.size = Pt(10)
        
        self.page += 1

    def save(self, filename):
        self.prs.save(filename)

