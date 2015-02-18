# travel_hamster

Usage:

    python travel_hamster.py example.json

When I consider vacation destinations, I want to consider multiple cities and modes of transportation.  I wrote TravelHamster to examine all these options for me.  TravelHamster is inspired and made possible by Rome2rio, an excellent service that provides cost estimates for different travel modes.  Numbeo, another excellent excellent service, also provides estimates of cost per day for travellers. TravelHamster combines both these services and outputs its comparison as CSV.  In short, TravelHamster turns this:

```javascript
{
	"home": "Knoxville",
	"to": [
		"New-Orleans",
		"Denver",
		"Miami",
		"New-York",
		"Seattle",
		"Chicago",
		"San-Diego",
		"Phoenix",
		"Las-Vegas"
	],
	"leave_date": "2015-3-14",
	"return_date": "2015-3-22"
}
```

into this:

![ScreenShot](https://raw.githubusercontent.com/cmwslw/travel_hamster/master/output_example.png)

TravelHamster outputs multiple columns that are often a consideration when choosing a destination, such as transportation cost and living cost for travellers.

In order to get Numbeo data, be sure to modify the "mapping" dictionary to map Rome2rio city names to Numbeo city names. JSON input files use Rome2rio city names. Both of these name formats can be found in the URLs of both Rome2rio and Numbeo when looking up the cities.

Price quotes are provided through Rome2rio and Numbeo and should be taken with a grain of salt.

Bon voyage!
