import requests
from bs4 import BeautifulSoup
import os
import shutil

# シンデレラガールズカードギャラリートップページ
CINDERELLA_CARD_MAIN = "http://imas.gamedbs.jp"
# ミリオンライブカードギャラリーページ detaill/の次に整数でアイドル指定
MILLION_LIVE_CARD_MAIN = "http://imas.gamedbs.jp/ml/character"

THEATER_CARD_MAIN = "http://imas.gamedbs.jp/mlth/"

DERESUTE_CARD_MAIN = "http://imas.gamedbs.jp/cgss/chara"


def get_all_idols_url(page=0):
    """

    :param page:
    :return:
    """
    if page == 0:
        # CINDERELLA
        pages = _get_all_idols_from_cinderella()
    elif page == 1:
        # MILLION LIVE
        pages = _get_all_idols_from_million()
    elif page == 2:
        pages = _get_all_idols_from_theater()
    else:
        print('Arguments Error.')
        exit()

    return pages


def _get_all_idols_from_cinderella():
    """
    シンデレラガールズのページから全アイドルのカードページを取得する
    :return:
    """
    r = requests.get(CINDERELLA_CARD_MAIN + '/cg')
    soup = BeautifulSoup(r.text, "lxml")
    divs = soup.find('div', id='result')
    idols = divs.find('ul', class_='lsbox flexbox flexwrap')
    idol_name = idols.find_all('div', class_='idol-name')
    idol_url = idols.find_all('a')
    pages = []

    if len(idol_name) == len(idol_url):
        print('length same')

    for name, url in zip(idol_name, idol_url):
        pages.append([name.text, url.attrs['href']])

    return pages


def _get_all_idols_from_million():
    """
    ミリオンライブのページから全アイドルのカードページを取得する
    :return:
    """
    r = requests.get(MILLION_LIVE_CARD_MAIN)
    soup = BeautifulSoup(r.text, "lxml")

    ul_box = soup.find('ul', class_='dblst flexbox flexwrap')
    idol_url_datas = ul_box.find_all('a')
    pages = []

    for data in idol_url_datas:
        pages.append([data['href'], data['title']])

    return pages


def _get_all_idols_from_theater():
    """
    ミリシタのページから全アイドルのカードページを取得する
    :return:
    """
    r = requests.get(THEATER_CARD_MAIN)
    soup = BeautifulSoup(r.text, "lxml")

    ul_box = soup.find('ul', class_='dblst flexbox flexwrap')
    idol_url_datas = ul_box.find_all('a')
    pages = []

    for data in idol_url_datas:
        pages.append([data['href'], data.text])

    return pages


def _get_all_idols_from_deresute():
    r = requests.get(DERESUTE_CARD_MAIN)
    soup = BeautifulSoup(r.text, "lxml")

    ul_box = soup.find('ul', class_='dblst flexbox flexwrap')
    idol_url_datas = ul_box.find_all('a')
    pages = []

    for data in idol_url_datas:
        pages.append([data['href'], data['title']])

    return pages


def _get_all_images_from_cinderella(data, dir_name, save_dir='cinderella_card/', org_name_flag=False):
    url = CINDERELLA_CARD_MAIN + data[1]
    r = requests.get(url)
    # r = requests.get('http://imas.gamedbs.jp/cg/idol/detail/71')
    soup = BeautifulSoup(r.text, "lxml")
    # モバマスの最初のカード
    # moba_top = soup.find('a', class_='swap-card-inf')
    moba_card = soup.find_all('a', class_='swap-card')

    # モバマスとデレステのカード全て
    # dere_card = soup.find_all('a', class_='imascg-card')

    #
    # singeki = soup.find_all('a', class_='lazy')

    if org_name_flag:
        dir_name = moba_card[0]['data-cn']

    dir_name = save_dir + dir_name

    if not os.path.isdir(dir_name):
        print('make directory {}'.format(dir_name))
        os.mkdir(dir_name)

    for num, card in enumerate(moba_card):
        link = card['href']
        card_name = str(num)

        if org_name_flag:
            card_name = card['data-cn']

        card_req = requests.get(CINDERELLA_CARD_MAIN + link)
        card_soup = BeautifulSoup(card_req.text, 'lxml')

        card_link = card_soup.find('img', class_='lazy')['data-original']
        src_link = requests.get(CINDERELLA_CARD_MAIN + card_link)

        with open(dir_name + '/' + card_name + '.png', 'wb') as file:
            file.write(src_link.content)
            print('save {} img, the card name of {}'.format(dir_name, card_name))


def _get_all_images_from_million(data, dir_name, save_dir='million_card/', org_name_flag=False):
    url = data[0]
    idol_name = data[1]
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    ul_box = soup.find('ul', class_='dblst flexbox flexwrap')
    card_href = ul_box.find_all('a')

    if org_name_flag:
        dir_name = idol_name

    dir_name = save_dir + dir_name
    if not os.path.isdir(dir_name):
        print('make directory {}'.format(dir_name))
        os.mkdir(dir_name)

    for num, card in enumerate(card_href):
        link = card['href']
        card_name = str(num)

        if org_name_flag:
            card_name = card['title'].replace('?', '_')

        src_link = requests.get(link)

        with open(dir_name + '/' + card_name + '.png', 'wb') as file:
            file.write(src_link.content)
            print('save {} img, the card name of {}'.format(dir_name, card_name))


def _get_all_images_from_theater(data, dir_name, save_dir='theater_card/', org_name_flag=False):
    url = data[0]
    idol_name = data[1]
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    ul_box = soup.find('ul', class_='dblst flexbox flexwrap')
    card_href = ul_box.find_all('a')

    if org_name_flag:
        dir_name = idol_name

    dir_name = save_dir + dir_name
    if not os.path.isdir(dir_name):
        print('make directory {}'.format(dir_name))
        os.mkdir(dir_name)

    for num, card in enumerate(card_href):
        link = card['href']
        before_name = str(num) + '_1'
        after_name = str(num) + '_2'

        img_link = requests.get(link)
        img_link_soup = BeautifulSoup(img_link.text, 'lxml')
        current_img_box = img_link_soup.find('section', class_='imgbox flexbox flexwrap')
        card_name = current_img_box.find('h2')
        current_img_box = current_img_box.find('section', class_='imgbox flexbox flexwrap')

        imgs_box = current_img_box.find_all('a')
        if len(imgs_box) > 5:
            before_href = imgs_box[4]['href']
            after_href = imgs_box[5]['href']

            before_src = requests.get(before_href)
            after_src = requests.get(after_href)
        else:
            before_href = imgs_box[0]['href']
            after_href = imgs_box[3]['href']

            before_src = requests.get(before_href)
            after_src = requests.get(after_href)

        if org_name_flag:
            if len(imgs_box) > 5:
                before_name = imgs_box[4]['title']
                after_name = imgs_box[5]['title']
            else:
                before_name = imgs_box[0]['title']
                after_name = imgs_box[3]['title']

        try:
            with open(dir_name + '/' + before_name + '.png', 'wb') as file:
                file.write(before_src.content)
                print('save {} img, the card name of {}'.format(dir_name, before_name))

            with open(dir_name + '/' + after_name + '.png', 'wb') as file:
                file.write(after_src.content)
                print('save {} img, the card name of {}'.format(dir_name, after_name))
        except:
            print('{} and {} could not be saved'.format(before_name, after_name))


def _get_all_images_from_deresute(data, dir_name, save_dir='deresute_card/', org_name_flag=False):
    url = data[0]
    idol_name = data[1]
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    ul_box = soup.find('ul', class_='dblst flexbox flexwrap')
    card_href = ul_box.find_all('a')

    if org_name_flag:
        dir_name = idol_name

    dir_name = save_dir + dir_name
    if not os.path.isdir(dir_name):
        print('make directory {}'.format(dir_name))
        os.mkdir(dir_name)

    for num, card in enumerate(card_href):
        link = card['href']
        card_name = str(num)

        if org_name_flag:
            card_name = card['title']

        src_link = requests.get(link)

        with open(dir_name + '/' + card_name + '.png', 'wb') as file:
            file.write(src_link.content)
            print('save {} img, the card name of {}'.format(dir_name, card_name))


def get_all_images(page):
    """
    各アイドルのページから，全カード画像を取得する
    :param page:
    :return:
    """
    if page == 0:
        pass


def integrate_files(dirs, output):
    count = 0
    for dir in dirs:
        # dir/0/0.img
        # みたいな感じになってるはず
        char_dirs = os.listdir(dir)
        for char_dir in char_dirs:
            char_dir = os.path.join(dir, char_dir)
            img_names = os.listdir(char_dir)
            for img_name in img_names:
                img_path = os.path.join(char_dir, img_name)
                output_path = os.path.join(output, "{:0=5}.png".format(count))
                shutil.copy(img_path, output_path)
                print('copy {} to {}'.format(img_path, output_path))


def reshape_as_trainset(trainA_dirs, trainB_dirs, train_dir):
    if not os.path.isdir(train_dir):
        os.mkdir(train_dir)
        print('mkdir {}'.format(train_dir))
    trainA_dir = os.path.join(train_dir, 'trainA')
    trainB_dir = os.path.join(train_dir, 'trainB')

    if not os.path.isdir(trainA_dir):
        os.mkdir(trainA_dir)
        print('mkdir {}'.format(trainA_dir))

    if not os.path.isdir(trainB_dir):
        os.mkdir(trainB_dir)
        print('mkdir {}'.format(trainB_dir))

    integrate_files(trainA_dirs, trainA_dir)
    integrate_files(trainB_dirs, trainB_dir)


if __name__ == '__main__':
    CH = [0]
    FLAG = True
    for ch in CH:
        pages = get_all_idols_url(ch)
        for num, page in enumerate(pages[44:]):
            if ch == 0:
                _get_all_images_from_cinderella(page, str(num), org_name_flag=FLAG)
            elif ch == 1:
                _get_all_images_from_million(page, str(num), org_name_flag=FLAG)
            elif ch == 2:
                _get_all_images_from_theater(page, str(num), org_name_flag=FLAG)
