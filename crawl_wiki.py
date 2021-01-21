import wikipediaapi
import random
import os

# import random.seed(datetime.datetime.now()) # https://wikidocs.net/15652

wikiApi = wikipediaapi.Wikipedia('ko')


def write_txtFile(src, data, no_sp=True):
    fw = open(src, 'w', encoding='utf-8')

    if no_sp:
        for x in data:
            fw.write(x)
    else:
        for x in data:
            fw.write(x + '\n')

    fw.close()


def crawl_wiki():
    link_list = ["홈쇼핑"]  # 메모리 문제 완화를 위해 title 만을 저장.
    visited_link_list = []
    while len(link_list) > 0:
        picked_link = link_list.pop(random.randint(0, len(link_list) - 1))
        pageData = wikiApi.page(picked_link)
        visited_link_list.append(pageData.title)

        if not pageData.exists():
            continue

        title = pageData.title
        links = pageData.links
        text = pageData.text

        # 이미 크롤링한 해당 문서 연관 링크는 link_list에 넣지 않는다
        for link_key in links.keys():
            if (link_key in visited_link_list) or '/' in link_key:
                continue  # '/'가 있는 title의 문서는 주로 주요 문서가 아니고, 폴더 경로로 인식되므로 제외시킴
            link_list.append(link_key)

        link_list = list(set(link_list))

        if not os.path.exists(title[0] + "/"):
            os.makedirs(title[0] + "/")
        write_txtFile(title[0] + "/" + title + '.txt', text, no_sp=True)



if __name__ == '__main__':
    crawl_wiki()
