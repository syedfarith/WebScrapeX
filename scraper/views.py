from django.shortcuts import render
from .forms import URLForm
import requests
from bs4 import BeautifulSoup

def scrape_site(request):
    scraped_content = ""  # Initialize the variable to hold scraped content
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Example: Extracting paragraphs. Adjust according to needs.
            tags_of_interest = ['h1', 'h2', 'h3', 'p', 'ul', 'ol', 'li']
            content_elements = soup.find_all(tags_of_interest)
            
            # Concatenate the text from all these elements
            scraped_content = '\n'.join([elem.text for elem in content_elements])

    else:
        form = URLForm()

    # The same template is used for GET and POST, but with additional content after POST
    return render(request, 'scrape_site.html', {
        'form': form,
        'scraped_content': scraped_content,
    })

from django.http import HttpResponse

def download_content_html(request):
    url = request.GET.get('url', '')  # Retrieve the URL from query parameters
    if url:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Specify tags of interest and regenerate the HTML content
        tags_of_interest = ['h1', 'h2', 'h3', 'p', 'ul', 'ol']
        content_elements = soup.find_all(tags_of_interest)
        html_content = ''.join(str(element) for element in content_elements)

        # Create an HttpResponse with HTML content, set appropriate headers for download
        response = HttpResponse(html_content, content_type='text/html')
        response['Content-Disposition'] = 'attachment; filename="scraped_content.html"'
        return response
    else:
        return HttpResponse("No URL provided", status=400)

def download_content_txt(request):
    url = request.GET.get('url', '')  # Retrieve the URL from query parameters
    if url:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Specify tags of interest
        tags_of_interest = ['h1', 'h2', 'h3', 'p', 'ul', 'ol']
        content_elements = soup.find_all(tags_of_interest)

        # Extracting text and combining it into one string
        text_content = '\n\n'.join(element.get_text(separator="\n", strip=True) for element in content_elements)

        # Create an HttpResponse with text content, set headers for download
        response = HttpResponse(text_content, content_type='text/plain; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="scraped_content.txt"'
        return response
    else:
        return HttpResponse("No URL provided", status=400)