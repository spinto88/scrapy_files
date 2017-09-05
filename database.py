#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import os
import datetime
from datetime import timedelta
from lxml import etree

table_to_save = 'nytimes'
file_of_data = 'Databases/nytimes_01_2016-07_2017.xml'
description_of_the_text = 'Notas del diario NYTimes, tomadas de la edicion impresa de cada día'
#página web indexadas como http://www.pagina12.com.ar/id, donde id es el número de nota.'
# Las notas publicadas en la edición impresa tienen el atributo time = 00:00:00'

data = etree.parse(file_of_data)

con = sqlite3.connect('data_english.db')
cursor = con.cursor()

try:
    cursor.execute("create table {} \n /* {} */ \n(id int primary key, \ndate date /* Fecha */, \ntime time /* Hora de publicación */, \nprefix text /* Volanta */, \ntitle text /* Título de la nota */, \nsubtitle text /* Subtítulo o copete */, \nsection text /* Sección */, \nauthor text /* Autor de la nota */, \nnewspaper text /* Diario o portal de noticias */, \nbody text /* Cuerpo de la nota */, \ntag text /* Etiqueta propuesta por el periódico */, \nurl text /* Página web */);".format(table_to_save, description_of_the_text))
except:
    pass

try: 
    cursor.execute("select MAX(id) from {};".format(table_to_save))
    for i in cursor:
        id_note = i[0] + 1
except:
    id_note = 0

items = data.xpath('//item')
for item in items:

    order = 'insert into {} (id) values ({});'.format(table_to_save, id_note)
    cursor.execute(order)

    try:
        title = item.xpath('title/text()')[0]
        title = title.replace('"','\'')
        order = 'update {} set title  = "{}" where id = {};'\
              .format(table_to_save, title.encode("utf-8"), id_note)
        cursor.execute(order)
    except: 
        pass

    try:
        prefix = item.xpath('prefix/text()')[0]
        prefix = prefix.replace('"','\'')
        order = 'update {} set prefix  = "{}" where id = {};'\
              .format(table_to_save, prefix.encode("utf-8"), id_note)
        cursor.execute(order)
    except: 
        pass

    try:
        subtitle = item.xpath('subtitle/text()')[0]
        subtitle = subtitle.replace('"','\'')
        order = 'update {} set subtitle  = "{}" where id = {};'\
                 .format(table_to_save, subtitle.encode("utf-8"), id_note)
        cursor.execute(order)
    except: 
        pass

    try:
        body = item.xpath('body/text()')[0]
        body = body.replace('"','\'')
        order = 'update {} set body  = "{}" where id = {};'\
                 .format(table_to_save, body.encode("utf-8"), id_note)
        cursor.execute(order)
    except: 
        pass

    try:
        section = item.xpath('section/text()')[0]
        section = section.replace('"','\'')
        order = 'update {} set section  = "{}" where id = {};'\
                 .format(table_to_save, section.encode("utf-8"), id_note)
        cursor.execute(order)
    except: 
        pass

    try:
        author = item.xpath('author/text()')[0]
        author = author.replace('"','\'')
        order = 'update {} set author  = "{}" where id = {};'\
                 .format(table_to_save, author.encode("utf-8"), id_note)
        cursor.execute(order)
    except: 
        pass

    try:
        newspaper = item.xpath('newspaper/text()')[0]
        newspaper = newspaper.replace('"','\'')
        order = 'update {} set newspaper  = "{}" where id = {};'\
                 .format(table_to_save, newspaper.encode("utf-8"), id_note)
        cursor.execute(order)
    except: 
        pass

    try:
        url = item.xpath('url/text()')[0]
        url = url.replace('"','\'')
        order = 'update {} set url  = "{}" where id = {};'\
                 .format(table_to_save, url.encode("utf-8"), id_note)
        cursor.execute(order)
    except: 
        pass

    try:
        tag = item.xpath('tag/text()')[0]
        tag = tag.replace('"','\'')
        order = 'update {} set tag  = "{}" where id = {};'\
                 .format(table_to_save, tag.encode("utf-8"), id_note)
        cursor.execute(order)
    except: 
        pass

    try:
        date = item.xpath('date/text()')[0]
        order = 'update {} set date  = "{}" where id = {};'\
                 .format(table_to_save, date, id_note)
        cursor.execute(order)
    except: 
        pass

    try:
        time = item.xpath('time/text()')[0]
        order = 'update {} set time  = "{}" where id = {};'\
                 .format(table_to_save, time, id_note)
        cursor.execute(order)
    except: 
        pass
    
    con.commit()
    id_note += 1
    
con.close()
