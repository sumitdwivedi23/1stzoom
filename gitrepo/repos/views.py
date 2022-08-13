from distutils.filelist import findall
import requests
from bs4 import BeautifulSoup
from rest_framework import views,generics
from config.response import CustomResponse
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from django.views.generic import TemplateView
GITHUB = 'https://github.com'
TRENDING_URL = GITHUB + "/trending"
TRENDING_DEV_URL = TRENDING_URL + "/developers"

# from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = "home.html"

class Fetch(views.APIView,TemplateView):
    permission_classes = (IsAuthenticated,)
  
    def get(self,request):
        repos = []
        language = request.GET.get('language')
        since = request.GET.get('since')
        url = TRENDING_URL
        print(url)
        if language:
            url = url + '/' + language
        print(url)
        if since:
            url += '?since={}'.format(since)
        response = requests.get(url)
        print(response.status_code)
        if response.status_code == 200:
            repos = []
            soup = BeautifulSoup(response.text, "lxml")
            sd = soup.find_all('article', {'class': 'Box-row'})
            for li in sd:
                avatar_img_list = li.find_all('img', {'class': 'avatar mb-1 avatar-user'})
                if len(avatar_img_list)>0:
                    for authors in avatar_img_list:
                        avatar = authors['src']
                        owner = authors['alt']
                repo = li.find('span',{'class':'text-normal'})
                repo = repo.text.replace('\n', '').strip(' ')
                stars = li.find('a', {'class': 'Link--muted d-inline-block mr-3'})
                if stars:
                    star = stars.text.replace('\n', '').strip(' ')
                else:
                    star="0"
                link = li.find('h1', {'class': 'h3 lh-condensed'})
                if link:
                    links=link.find('a', href=True)['href']
                link1 = GITHUB + links
                desc=li.find('p', {'class': 'col-9 color-fg-muted my-1 pr-4'})
                if desc:
                    desc = desc.text.replace('\n', '').strip(' ')
                else:
                    desc= "None"
                repos.append({
                    'owner': owner,
                    'avatar': avatar,
                    'repo': repo,
                    'stars': star,
                    'desc': desc,
                    'link': link1
                })
        return CustomResponse(repos)
        # return render(request, "home.html",repos)


class devs(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):

        developers = []

        language = request.GET.get('language')
        since = request.GET.get('since')

        url = TRENDING_DEV_URL

        if language:
            url = url + '/' + language

        if since:
            url += '?since={}'.format(since)
        response = requests.get(url)
        if response.status_code==200:
            soup = BeautifulSoup(response.text, "lxml")
            sd = soup.find_all('article', {'class': 'Box-row d-flex'})
            for li in sd:
                avatar_image = li.find('img',{'class':'rounded avatar-user'})
                if avatar_image:
                    avatar_image = avatar_image['src']
                href = li.find('h1', {'class': 'h3 lh-condensed'})
                name=href.text
                link = li.find('h1', {'class': 'h3 lh-condensed'})
                if link:
                    links=link.find('a', href=True)['href']
                link1 = GITHUB + links
                developers.append({
                    'avatar': avatar_image,
                    'name': name,
                    'link': link1
                     })
         
        return CustomResponse(developers)

