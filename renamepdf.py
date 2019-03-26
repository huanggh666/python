import os
from glob import glob
from PyPDF4 import PdfFileReader


def rename():
    path = r'E:\yan\papers\ECCV\ECCV-2018'   #pdf files' parent directory
    filenames = glob(f'{path}/*.pdf')
    filenames = sorted(filenames)
    for filename in filenames:
        with open(filename, 'rb') as file:
            pdf_reader = PdfFileReader(file)
            pdf_title = pdf_reader.getDocumentInfo().title
        if ':' in pdf_title:
            pdf_title = pdf_title.replace(':', '：')
        if '?' in pdf_title:
            pdf_title = pdf_title.replace('?', '？')
        file_path, filename_l = os.path.split(filename)
        try:
            if file_path == f'{pdf_title}.pdf':
                continue
            os.rename(filename, os.path.join(file_path, f'{pdf_title}.pdf'))
            print(pdf_title)
        except:     #--- filename includes unexpected char
            with open(f'{file_path}/Nold.txt', 'a') as file:
                file.write(f'{filename_l}\n')
            with open(f'{file_path}/Nnew.txt', 'a') as file:
                file.write(f'{pdf_title}\n')
        
if __name__ == '__main__':
    rename()
    
