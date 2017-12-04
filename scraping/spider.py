import scrapy
import re
	
class Spider(scrapy.Spider):
	name = 'ffb_proj'
	rotate_user_agent = True
	
	custom_settings = {
		"DOWNLOAD_DELAY": 1,
		"CONCURRENT_REQUESTS_PER_DOMAIN": 3,
		"RANDOMIZE_DOWNLOAD_DELAY":True
		#"HTTPCACHE_ENABLED": True
	}

	CURR_WEEK = 12
	
	proj_root_url = "http://games.espn.com/ffl/tools/projections?&scoringPeriodId={}&seasonId=2017"
	start_urls = []

	# populate start urls with all week urls
	for week in range(1,CURR_WEEK+1):
		start_urls.append(proj_root_url.format(week))
	
	# start_urls=["http://games.espn.com/ffl/tools/projections?&scoringPeriodId=1&seasonId=2017"]
	
	def parse(self, response):
		
		for startIndex in range(0, 1080, 40):

			next_url =response.url + "&startIndex={}".format(startIndex)

			yield scrapy.Request(
				url=next_url,
				callback=self.parse_week
			)

	def parse_week(self, response):
		
		print("\n", "SCRAPING FROM URL: ",response.url,"\n")

		players = response.xpath('//table[@id="playertable_0"]/tr[@class="pncPlayerRow playerTableBgRow0"]').extract()
		players +=response.xpath('//table[@id="playertable_0"]/tr[@class="pncPlayerRow playerTableBgRow1"]').extract()
		
		week_title = response.xpath('//div[@class="games-pageheader"]//div[2]/h1/text()').extract_first()

		for player in players:
			selector = scrapy.Selector(text=player, type="html")
			team = selector.xpath('//td[@class="playertablePlayerName"]/text()').extract_first()
			yield {
			'title' : week_title,
			'week' : re.sub('[^0-9]','', week_title),
			'name' : selector.xpath('//td[@class="playertablePlayerName"]/a//text()').extract_first(),
			'team' : team,
			'position' : team[len(team)-2:len(team)],
			'espn_playerid' : selector.xpath('//a[1]/@playerid').extract_first(),
			'proj_pts' : selector.xpath('//td[@class="playertableStat appliedPoints sortedCell"]//text()').extract_first()
			}