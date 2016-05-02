import requests
import BeautifulSoup
import urlparse


def image_dem(url):
    result = requests.get(url, verify=False)
    soup = BeautifulSoup.BeautifulSoup(result.text)
    og_image = (soup.find('meta', property='og:image') or soup.find(
        'meta', attrs={'name': 'og:image'}))
    if og_image and og_image['content']:
        print og_image['content']
    thumbnail_spec = soup.find('link', rel='image_src')
    if thumbnail_spec and thumbnail_spec['href']:
        print thumbnail_spec['href']
    image = """<img src="%s"><br />"""
    imagelst = []
    for img in soup.findAll("img", src=True):
        if "sprite" not in img["src"]:
            imagelst.append(urlparse.urljoin(url, img["src"]))
    return imagelst
