
import argparse
import glob
import json
import os
import re

import bs4
import jinja2



def get_args():

    parser = argparse.ArgumentParser(description='Script that uses json files downloaded by TumblThree to generate HTML files')

    parser.add_argument('BLOG_DIR',
                        help='Directory to where TumblThree has downloaded a blog (this directory must ' \
                             'contain images from the blog, the HTML files will be generated to this directory)')

    args = parser.parse_args()

    return args



def get_posts():

    posts = glob.glob('[0-9]*.json')

    return posts



def make_soup(html_source):

    soup = bs4.BeautifulSoup(html_source, 'html.parser')

    return soup



def read_json_file(filepath):

    with open(filepath, encoding='utf8') as fid:  
        data = json.load(fid)

    return data



def get_template(name):

    # http://jinja.pocoo.org/docs/2.10/api/#jinja2.FileSystemLoader
    # http://jinja.pocoo.org/docs/2.10/templates/

    print

    template_dir = os.path.dirname(os.path.realpath(__file__))
    template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
    template = template_env.get_template(name)

    return template



def fix_images(soup):

    # redirect network images to local images (if found)

    imgs = soup.find_all('img')

    for img in imgs:

        rslt = re.search(r'(\w+?)(?:_\d+)?\.(jpg|png|gif|mp4)', img['src'])

        if rslt:
            possible_matches = glob.glob(rslt.group(1) + '*' + rslt.group(2))
            if possible_matches:
                link = soup.new_tag('a', href=possible_matches[0])
                img['src'] = possible_matches[0]
                img.wrap(link)
                continue

        print('Unable to replace network image with local copy:')
        print('\t', img['src'])


def parse_post(post_json):

    # generate a soup object for a post
    # three types: text, question/answer, link

    if post_json['type'] == 'regular':
        soup = make_soup(post_json['regular-body'])

    elif post_json['type'] == 'answer':
        soup = make_soup('')

        label = soup.new_tag('h2')
        label.string = 'Question'
        soup.append(label)
        soup.append(make_soup(post_json['question']))

        label = soup.new_tag('h2')
        label.string = 'Answer'
        soup.append(label)
        soup.append(make_soup(post_json['answer']))

    elif post_json['type'] == 'link':        
        soup = make_soup(post_json['link-description'])

        link_text = soup.new_tag('h2')
        link_text.string = post_json['link-text']
        soup.insert(0, link_text)

        source_link = '<h4>Source: <a href="' + post_json['link-url'] + '">' + post_json['link-url'] + '</a></h4>'
        source_link_soup = make_soup(source_link)

        soup.append(source_link_soup)

    elif post_json['type'] == 'photo':

        soup = make_soup(post_json['photo-caption'])

        if post_json['photos']:
            for photo in reversed(post_json['photos']):
                img = soup.new_tag('img', src=photo['photo-url-1280'])
                soup.insert(0, img)

        else:
            img = soup.new_tag('img', src=post_json['photo-url-1280'])
            soup.insert(0, img)

    elif post_json['type'] == 'video':
        soup = make_soup('<h2>Unable to parse video items at this time</h2>')

    else:
        soup = make_soup('<h2>Unable to parse the page</h2>')

    return soup


def main():

    BLOG_DIR = get_args().BLOG_DIR

    # set our working dir

    post_template = get_template(name='post.htm.j2')
    index_template = get_template(name='index.htm.j2')

    os.chdir(BLOG_DIR)

    # find all the posts in the tumblr directory
    posts = [{'filename': x} for x in get_posts()]

    if not posts:
        print('Unable to find any posts. Please make sure:')
        print('\t1) To specifiy the path to where the downloaded image/json files are located')
        print('\t2) The "Dump crawler data" option is checked in TumblThree')
        return

    for post in posts:

        # obtain the json object for the post and get some metadata off it
        post_json = read_json_file(post['filename'])
        post['id'] = post_json['id']
        post['timestamp'] = post_json['unix-timestamp']
        post['title'] = post_json['slug'].replace('-', ' ').title() if post_json['slug'] else 'Posted on ' + post_json['date']
        post['title'] += ' ({})'.format(post_json['type'].title())

        # generate an html file for the post
        soup = parse_post(post_json)
        fix_images(soup)
        post_template.stream(post=post_json, body=soup.prettify(formatter='html')).dump(post['id'] + '.html')

    # generate an index page
    index_template.stream(posts=posts).dump('_index.html')

    print('All done! The generated HTML file can be found at:\n\t', os.path.join(BLOG_DIR, '_index.html'))

main()
