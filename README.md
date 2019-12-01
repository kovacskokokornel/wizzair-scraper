# Wizzair scraper
This folder contains python scripts to automatically scrape flight data (mainly prices) from <https://wizzair.com>. There are two types of codes with different level of details.

## Timetable approach

This approach uses data from <https://wizzair.com/en-gb/flights/timetable>. You can access multiple flight prices with one call, therefore, it is much faster than the other one. However, it only has the most important pieces of information of flights. In most of the cases, it is more than enough.

## Individual flight approach - __I am still working on this__

If you want to have a very detailed flight information, this is the way to go. It shows _basic_,  _wizz go_ and _wizz plus_ prices and services. Flight duration, arrival and departure time are, of course, included. The downside is that you can only make requests flight by flight which makes it quite slow. With the timetable approach, you could get around 80 records with one call, here you may only get 1 record.