import scrapy
import json
import os

class BooksSpider(scrapy.Spider):
    name = 'books'
    start_urls = ['https://books.toscrape.com/']
    
    def parse(self, response):
        # Extract book links from the current page
        book_links = response.css('article.product_pod h3 a::attr(href)').getall()
        
        for link in book_links:
            book_url = response.urljoin(link)
            yield scrapy.Request(book_url, callback=self.parse_book)
        
        # Follow pagination
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
    
    def parse_book(self, response):
        # Extract book details
        title = response.css('h1::text').get()
        price = response.css('p.price_color::text').get()
        availability = response.css('p.instock.availability::text').getall()
        availability = ''.join(availability).strip() if availability else 'Not available'
        
        # Extract rating
        rating_class = response.css('p.star-rating::attr(class)').get()
        rating = rating_class.split()[-1] if rating_class else 'No rating'
        
        # Extract description
        description = response.css('#product_description + p::text').get()
        if not description:
            description = "No description available"
        
        # Extract image URL
        image_url = response.css('div.item.active img::attr(src)').get()
        if image_url:
            image_url = response.urljoin(image_url)
        
        # Extract category
        category = response.css('ul.breadcrumb li:nth-child(3) a::text').get()
        
        yield {
            'title': title,
            'price': price,
            'availability': availability,
            'rating': rating,
            'image_url': image_url,
            'category': category,
            'url': response.url
        }
