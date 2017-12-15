# -*- coding:utf-8 -*-
__author__ = 'IanChen'

def makebold(f):
    def wrapped():
        return "<b>"+f()+"</b>"
    return wrapped

def makeitalic(f):
    def wrapped():
        return "<i>"+f()+"</i>"
    return wrapped()

@makeitalic
@makebold
def hello():
    return "hello world"

hello

# def log(func):
#     def wrapper(*args, **kw):
#         print('call %s():' % func.__name__)
#         return func(*args, **kw)
#     return wrapper
#
# @log
# def now():
#     print('2015-3-25')
#
# now()