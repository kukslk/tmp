from pathlib import Path
from PyPDF2 import PdfReader,PdfWriter
import os,time,json,threading,concurrent.futures,argparse,sys

class Scaner():
    file_path = os.path.abspath(Path.cwd().joinpath('files'))
    json_path =  os.path.abspath(Path.cwd().joinpath('json'))
    result_path =  os.path.abspath(Path.cwd().joinpath('result'))

    def _init_(self):
        pass
    # convert and replace pdf to json
    def update(self,files=os.listdir(file_path),verbose=False):
        count=len(files)
        if verbose:
            print(count,'files')
        index=1
        for file in files:
            pages = self.read_pdf(os.path.join(self.file_path, file))
            # print(file, 'has', len(pages), 'pages')
            with open(os.path.join(self.json_path,'.'.join([file.split('.')[0], 'json'])), 'w', encoding='utf8') as fd:
                # fd.write(text.encode('utf8'))
                json.dump(pages, fd, ensure_ascii=False)
            if verbose:
                print(index,'of',count)
            index+=1
        pass

    # search
    def scan(self, text, verbose=False):
        if verbose:
            print('Searching for',text)
        files=os.listdir(self.json_path)
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            values = {executor.submit(self.search_text, os.path.join(self.json_path, file), text): file for file in files}
            result = []
            for future in concurrent.futures.as_completed(values):
                if len(future.result()[1]):
                    print(future.result())
                    result.append(future.result())
            pages = {executor.submit(self.get_pages, pdf_pages): pdf_pages for pdf_pages in result}
            wr = PdfWriter()
            for future in concurrent.futures.as_completed(pages):
                for page in future.result():
                    wr.add_page(page)
            if len(wr.pages)>0:
                wr.write(open(os.path.join(self.result_path, text.replace(' ','_') + '.pdf'), 'wb'))
        pass

    #get pages from pdf file
    def read_pdf(self,pdf_path):
        pdf = PdfReader(pdf_path)
        pages = []
        text = ''
        for i in range(0, len(pdf.pages)):
            extr = pdf.pages[i].extract_text()
            pages.append(extr.lower())
        return pages

    # verify all words are on the page
    def search_all_text(self,page, text):
        # page=' '.join([liter for liter in page.replace(' ','').replace('\t','')])
        for word in text.split(' '):
            if word not in page:
                return False
        return True

    #extract pages from pdf file
    def get_pages(self,pdf_pages):
        try:
            source = PdfReader(os.path.join(self.file_path, os.path.basename(pdf_pages[0])).replace('json', 'pdf'))
            pages = []
            for page_index in pdf_pages[1]:
                pages.append(source.pages[page_index])
        except:
            return []
        return pages

    #search text on pages in json files
    def search_text(self,path, text):
        with open(path, 'r', encoding='utf8') as fd:
            pages = json.load(fd)
        indexies = []
        for page in pages:
            if self.search_all_text(page.lower(), text.lower()):
                indexies.append(pages.index(page))
        return (path, indexies)

if __name__ == "__main__":
    scan=Scaner()
    # parser = argparse.ArgumentParser()
    # parser.add_argument('words', metavar='W', type=str, nargs='?',
    #                     help='words to search')
    # args = parser.parse_args()
    # scan.scan(' '.join(sys.argv[1:]),True)
    scan.scan('ldap brute')
