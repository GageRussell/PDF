from xhtml2pdf import pisa             # import python module
import urllib.request
from bs4 import BeautifulSoup
# Define your data

src_url = "https://support.apple.com/en-gb/guide/iphone/toc"
# Utility function
def convert_html_to_pdf(source_html, output_filename):
    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
            source_html,                # the HTML to convert
            dest=result_file)           # file handle to recieve result

    # close output file
    result_file.close()   

    # return False on success and True on errors
    return pisa_status.err

def get_html(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()
    return mystr

def get_urls(src_url):
    parser = 'html.parser' # or 'lxml' (preferred) or 'html5lib', if installed
    resp = urllib.request.urlopen(src_url)
    soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))
    links = soup.find_all('a')
    urls = []
    for tag in links:
        link = tag.get('href',None)
        if link is not None:
            if link.startswith('http'):
                urls.append(link)
    return urls

# Main program
if __name__ == "__main__":
    pisa.showLogging()
    urls = get_urls(src_url)
    pdf_list = []
    pdf_cnt = 0
    for url in urls:
        source_html = get_html(url)
        output_filename = 'pdf_{}.pdf'.format(pdf_cnt)
        convert_html_to_pdf(source_html, output_filename)
        pdf_cnt+=1
    