import os
import urllib
from fpdf import FPDF

##############################################################################
TITLE = input('Enter title: ')
SUBTITLE = input('Enter subtitle: ')
SEARCH_KEY = 'https://coursera-video-thumbnail-notes.s3.amazonaws.com/web/'
IMG_FILE_NAME_LENGTH = 44
SAVE_PATH = input('Enter path: ')
##############################################################################

while '\\' in SAVE_PATH:
    SAVE_PATH = SAVE_PATH.replace('\\', '/')

print('Reading source code...')
fo = open(SAVE_PATH + '/source_code.txt', 'r', encoding='utf-8')
source_code = fo.read()
fo.close()

imgs = []
index = 0
img_count = source_code.count(SEARCH_KEY)

print('Downloading images...')
for i in range(img_count):
    index = source_code.index(SEARCH_KEY, index + 1)
    start = index + len(SEARCH_KEY)
    stop = start + IMG_FILE_NAME_LENGTH
    file_name = source_code[start:stop]
    file_url = SEARCH_KEY + file_name
    urllib.request.urlretrieve(file_url, SAVE_PATH + file_name)
    new_file_name = file_name + '.jpg'
    os.rename(SAVE_PATH + file_name, SAVE_PATH + new_file_name)
    imgs.append(SAVE_PATH + new_file_name)
print('%i images downloaded' % img_count)

print('Generating pdf...')
pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 18)
pdf.cell(0, h=10, txt=TITLE, align = 'C')
pdf.ln()
pdf.set_font('Arial', 'B', 14)
pdf.cell(0, h=10, txt=SUBTITLE, align = 'C')

##############################################################################
IMG_X = 5
IMG_Y = 15
IMG_WIDTH = 200     # total width is 210
IMG_HEIGHT = 112.5  # total height is 297
IMGS_PER_PAGE = 2
IMG_GAP = 10
##############################################################################

i = 0
while i < len(imgs):
    pdf.add_page()
    pdf.image(imgs[i], IMG_X, IMG_Y,IMG_WIDTH, IMG_HEIGHT)
    i += 1
    while (i % IMGS_PER_PAGE) and (i < len(imgs)) :
        current_img_y = IMG_Y + (i % IMGS_PER_PAGE) * (IMG_HEIGHT + IMG_GAP)
        pdf.image(imgs[i], IMG_X, current_img_y, IMG_WIDTH, IMG_HEIGHT)
        i += 1
    
pdf.output(SAVE_PATH + '/Notes.pdf', 'F')

print('Deleting images...')
for img in imgs:
    os.remove(img)

print('Notes.pdf file is created successfully')
