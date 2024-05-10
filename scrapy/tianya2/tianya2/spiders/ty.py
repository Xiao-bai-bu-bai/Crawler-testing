import scrapy
from scrapy_redis.spiders import RedisSpider
from tianya2.items import Tianya2Item
from redis import Redis
from scrapy.utils.project import get_project_settings

# 分布式爬虫
class TySpider(RedisSpider):  # 修改继承类
    name = "ty"
    allowed_domains = ["tianya.im"]
    # start_urls = ["https://tianya.im"]  # 删除start_urls
    redis_key = 'tianya:ty:start_urls'  # 修改redis_key

    settings = get_project_settings()
    redis = Redis(host=settings.get('REDIS_HOST'),
                  port=settings.get('REDIS_PORT'),
                  db=settings.get('REDIS_DB'),
                  password=settings.get('REDIS_PASSWORD'))

    def parse(self, response, **kwargs):
        # print(response.text)
        li_list = response.xpath("//ol[@class='user-items']/li/div/div/a[@title='打开帖子']/@href").extract()
        for li in li_list:
            li = response.urljoin(li)
            yield scrapy.Request(li, callback=self.parse_detail)

        # 提取最后一个a标签的href属性值
        next_href = response.xpath("//div[@class='stream-footer']/div/a[last()]/@href").extract_first()
        yield scrapy.Request(response.urljoin(next_href), callback=self.parse)

    def parse_detail(self, response):
        item = Tianya2Item()
        author = response.xpath("//div[@class='topic-user']/a/strong/text()").extract_first()
        content = response.xpath("//div[@class='topic-content']/p/text()").extract()
        item['author'] = author.strip()
        if content:  # 判断是否为空
            if isinstance(content, list):  # 判断是否为列表类型
                item['content'] = ' '.join([c.strip() for c in content])  # 如果是列表，移除每个元素周围的空白并用空格连接它们
            elif isinstance(content, str):  # 检查content是否为字符串
                item['content'] = content.strip()  # 如果是字符串，直接移除两边的空白
        else:
            item['content'] = ""  # 如果content为空，为避免报错，我们可以赋值为空字符串
        yield item
