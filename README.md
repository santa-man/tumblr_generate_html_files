
# tumblr_generate_html_files

tumblr_generate_html_files is a script which lets users generate HTML files for Tumblr posts. This script is a helper script for the [TumblThree](https://github.com/johanneszab/TumblThree) program.

## Installation

1. Clone the repository to your local machine
2. Make sure Python 3 is installed
3. Make sure jinja2 and BeautifulSoup are installed, if not:

   * `pip install Jinja2`
   * `pip install beautifulsoup4`
  
## Usage

Use [TumblThree](https://github.com/johanneszab/TumblThree) to download a blog of our choice. Make sure the option `Dump crawler data` is checked ([like so](https://i.imgur.com/5AIkxzN.png
)).

Then use the `generate_html_files.py` script to generate the HTML files.

```
usage: generate_html_files.py [-h] BLOG_DIR

Script that uses json files downloaded by the program TumblThree to generate HTML files

positional arguments:
  BLOG_DIR    Directory to where TumblThree has downloaded a blog (this
              directory must contain images from the blog, the HTML files will
              be generated to this directory)

```

BLOG_DIR is the download directory to which [TumblThree](https://github.com/johanneszab/TumblThree) downloaded a tumblr blog.

## Example

1. Download a blog with the correct settings using [TumblThree](https://github.com/johanneszab/TumblThree)

<img src="https://i.imgur.com/rYncGiI.png" width="850">

2. Run the script

<img src="https://i.imgur.com/ovkkVmH.png" width="850">

3. Here in the newly generated HTML index file

<img src="https://i.imgur.com/x0AirXT.png" width="850">

4. Here is one of the blog posts

<img src="https://i.imgur.com/dEVxYrM.png" width="850">

## License

[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)

## Contributions

Pull requests are welcome.

## Disclaimer

This is a simple helper script for [TumblThree](https://github.com/johanneszab/TumblThree). For any issues regarding TumblThree please visit that GitHub page.
