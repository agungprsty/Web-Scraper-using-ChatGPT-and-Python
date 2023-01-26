#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
from bs4 import BeautifulSoup
from utils import save_img_to_local

for page in range(1, 13):
    url = f'https://saprotan-utama.com/product-category/semua-produk/page/{page}/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    products = []
    for product_div in soup.find_all('div', class_='product-list'):
        product = {}
        product['link'] = product_div.find('footer').find('a')['href']
        product_response = requests.get(product['link'])
        product_soup = BeautifulSoup(product_response.text, 'html.parser')

        # ambil gambar produk
        img_div = product_soup.find('div', class_='col-lg-5')
        product['img'] = img_div.find('img')['src'] if img_div else ''
        
        # cek apakah gambarnya ada, jika ada simpan
        if product.get("img"):
            img = product.get("img")
            save_img_to_local(img)

            # replace value img, dengan nama filenya saja.
            filename = img.split("/")
            product['img'] = filename.pop()
        
        # ambil nama, deskripsi, keunggulan, spesifikasi, dan penggunaan produk
        detail_div = product_soup.find('div', class_='col-lg-7')
        product['name'] = detail_div.find('h1').text
        product['description'] = detail_div.find('p').text

        keunggulan_div = product_soup.find('div', id='keunggulan-tab')
        if keunggulan_div:
            product['keunggulan'] = [p.text for p in keunggulan_div.find_all('p')]

        spesifikasi_div = product_soup.find('div', id='spesifikasi-tab')
        if spesifikasi_div:
            product['spesifikasi'] = [p.text for p in spesifikasi_div.find_all('p')]

        penggunaan_div = product_soup.find('div', id='penggunaan-tab')
        if penggunaan_div:
            product['penggunaan'] = [p.text for p in penggunaan_div.find_all('p')]

        products.append(product)

    # simpan hasil scraping ke file json
    with open(f'data/produk/page-{page}.json', 'w') as f:
        json.dump(products, f)
