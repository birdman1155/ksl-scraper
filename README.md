# ksl-scraper
A scraper that sends you an email everytime a new listing has been put up.

###Setup Instructions for Raspberry Pi

sudo apt-get install postfix

sudo apt-get install sqlite3

sudo apt-get install python-pip

sudo pip install requests beautifulsoup4

chmod +x /home/pi/Desktop/ksl-scraper/scraper.py


crontab -e

*/1 * * * * /home/pi/Desktop/ksl-scraper/./scraper.py


