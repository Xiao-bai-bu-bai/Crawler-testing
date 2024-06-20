import scrapy
from baiduwenku.items import BaiduwenkuItem


class BaiqiSpider(scrapy.Spider):
    name = "baiqi"
    allowed_domains = ["baidu.com"]
    start_urls = ["https://baike.baidu.com/item/%E7%99%BD%E8%B5%B7/131407?fr=ge_ala"]

    def parse(self, response, **kwargs):
        # 提取标题
        title = response.xpath('//*[@id="J-lemma-main-wrapper"]/div[1]/div/div/div[1]/div[1]/div[1]/h1/text()').extract_first()
        # 提取标签
        posts = response.xpath('//*[@id="lemmaDesc"]/div[1]/text()').extract_first()
        # 提取所有文本中div元素

        divs = response.xpath('//*[@id="J-lemma-main-wrapper"]/div[2]/div/div[1]/div/div[2]/div')

        # 初始化一个空列表来存储处理后的文本
        substances = []

        for div in divs:
            # 提取当前div中的所有文本
            texts = div.xpath('.//span//text()').extract()
            # 将文本内容连接成一个字符串，并添加换行符
            substances.append(''.join(texts) + '\n')

        # 将所有文本内容连接成一个最终的字符串
        substance = ''.join(substances)

        item = BaiduwenkuItem()
        item['title'] = title
        item['posts'] = posts
        item['substance'] = substance
        yield item

