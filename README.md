# travel_hamster

Usage:

    python travel_hamster.py example.json

Often when I consider vacation destinations, I usually have multiple cities that I consider and I also usually consider multiple modes of transportation. I wanted a tool that could output a CSV that compared the travel expenses of multiple cities. I recently came across a fantastic service called Rome2rio that checks multiple travel modes. I also know that Numbeo provides estimates of cost per day for travellers. Travel_hamster combines both these services and outputs the results into a CSV file. Travel_hamster turns this:

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

Travel_hamster outputs multiple columns that are often a consideration when choosing a destination, such as transportation cost and living cost for travellers.

In order to get Numbeo data, be sure to modify the "mapping" dictionary to map Rome2rio city names to Numbeo city names. JSON input files use Rome2rio city names. Both of these name formats can be found in the URLs of both Rome2rio and Numbeo when looking up the cities.
