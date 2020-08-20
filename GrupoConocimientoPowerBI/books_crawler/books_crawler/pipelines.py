# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

import json
import requests

# LIBRERIA PROPIA
from .SQL_CONECT_PANDAS import SQL_CONECT_PANDAS as P

def clean_data(data):
    data = data.replace(',',' ').replace('\t','').replace('\n','').replace('\u00a3','').replace('\u2014','')
    return data

class BooksCrawlerPipeline(object):
    def open_spider(self, spider):
        self.vat_factor = 4.67
        
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('upc'):
            adapter['page_url'] = clean_data(adapter['page_url'])
            adapter['title'] = clean_data(adapter['title'])
            adapter['price'] = clean_data(adapter['price'])
            adapter['image_url'] = clean_data(adapter['image_url'])
            adapter['rating'] = clean_data(adapter['rating'])
            # adapter['description'] = clean_data(adapter['description'])
            adapter['upc'] = clean_data(adapter['upc'])
            adapter['product_type'] = clean_data(adapter['product_type'])
            adapter['price_without_tax'] = clean_data(adapter['price_without_tax'])
            adapter['price_with_tax'] = clean_data(adapter['price_with_tax'])
            adapter['tax'] = clean_data(adapter['tax'])
            adapter['availability'] = clean_data(adapter['availability'])
            adapter['number_of_reviews'] = clean_data(adapter['number_of_reviews'])
            
            if adapter.get('price'):
                # convirtiendo a soles
                adapter['price'] = float(adapter['price']) * self.vat_factor
                adapter['price_without_tax'] = float(adapter['price_without_tax']) * self.vat_factor
                adapter['price_with_tax'] = float(adapter['price_with_tax']) * self.vat_factor
                adapter['tax'] = float(adapter['tax']) * self.vat_factor

            return item
            # return adapter
        else:
            raise DropItem("Missing upc in %s" % item)
    

class InsertInTableDatabase:
    
    input_credenciales_sql = input_credenciales_sql={'driver':'{SQL Server Native Client 11.0}',
                                            'server':r'server-pruebas.database.windows.net',
                                            'database':'db_pruebas',
                                            'username':'gdelgadr',
                                            'password':'Gonzalo1994!'
                                            }
    c = P(**input_credenciales_sql)
    query ="insert into books values('{upc}','{product_type}','{title}','{page_url}','{image_url}','{rating}','{availability}','{number_of_reviews}',{price},{price_without_tax},{price_with_tax},{tax})"


    def close_spider(self, spider):
        print('elementos subidos a la base de datos')

    def process_item(self, item, spider):
        valores ={
                'upc': item['upc'] , 
                'product_type': item['product_type'] , 
                'title': item['title'] , 
                'page_url': item['page_url'] ,
                'image_url': item['image_url'] ,
                'rating': item['rating'] ,
                'availability': item['availability'] , 
                'number_of_reviews': item['number_of_reviews'] , 
                'price': float(item['price']), 
                'price_without_tax': float(item['price_without_tax']),
                'price_with_tax': float(item['price_with_tax']), 
                'tax': float(item['tax']) 
        }
        try:
            sql_query = self.query.format(**valores)
            self.c.delete_sql(sql_query)
            return item
        except Exception as e:
            print(e)
