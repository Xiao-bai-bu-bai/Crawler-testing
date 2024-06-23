import scrapy
from scrapy_redis.spiders import RedisSpider
from tuxingren.items import TuxingrenItem
from redis import Redis


class YuansuSpider(RedisSpider):
    name = "yuansu"
    allowed_domains = ["txrpic.com"]
    # start_urls = ["https://www.txrpic.com/"]
    redis_key = 'tuxingren:yuansu:start_urls'
    def __init__(self, name=None, **kwargs):
        super(YuansuSpider, self).__init__(name, **kwargs)
        try:
            self.redis = Redis(host='localhost', port=6379, db=1, password='666666', decode_responses=True)
            self.redis.ping()
            self.logger.warning("已成功连接到 Redis。")
        except Exception as e:
            self.logger.error(f"无法连接到 Redis: {e}")

    def parse(self, response, **kwargs):
        # 提取所有分类的url和名称
        url_kinds = response.xpath('//div[@class="left-side"]/ul/li//a/@href').extract()
        kind_names = response.xpath('//div[@class="left-side"]/ul/li//a/text()').extract()

        for url, kind_name in zip(url_kinds, kind_names):
            url = response.urljoin(url)
            yield scrapy.Request(url=url, method='get', callback=self.parse_kind, meta={'kind_name': kind_name})

    def parse_kind(self, response, **kwargs):
        # 提取分类下的所有图片的url
        a_hrefs = response.xpath('//div[@class="box data-info"]/div[1]/a/@href').extract()
        kind_name = response.meta.get('kind_name', 'unknown')
        for a_href in a_hrefs:
            yield scrapy.Request(url=a_href, method='get', callback=self.parse_detail, meta={'kind_name': kind_name})
        

        # 获取下一页的url，判断是否为下一页
        next_page = response.xpath('//div[@class="main-page-box"]/a[contains(text(), "下一页")]/@href').extract_first()
        if next_page:
            next_page = response.urljoin(next_page)
            self.logger.warning(f"下一页网址: {next_page}")
            yield scrapy.Request(next_page, callback=self.parse_kind, meta={'kind_name': kind_name})

    def parse_detail(self, response, **kwargs):
        # 提取图片的url和名称
        img_url = response.xpath('//div[@class="work-img-box"]/img/@src').extract_first()
        img_name = response.xpath('//div[@class="work-img-box"]/img/@title').extract_first()
        kind_name = response.meta.get('kind_name', 'unknown')

        # 判断是否爬取过
        # if self.redis.sismember('tuxingren:ty:detail:url', img_url):
        #     self.logger.warning(f'已经爬取过 {img_name} 了')
        # else:

        # 不用判断是否爬取，scrapy_redis会自动去重
        item = TuxingrenItem()
        item['img_url'] = img_url
        item['img_name'] = img_name
        item['kind_name'] = kind_name
        # 将爬取过的url存入redis
        # self.redis.sadd('tuxingren:ty:detail:url', img_url)
        yield item