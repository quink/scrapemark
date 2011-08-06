#!/usr/bin/env python

from bottle import route, run, request

@route('/')
def index():
    return '<em>hello</em>'

@route('/testget/', method='GET')
def testget():
    test = request.GET.get('test')
    if test=='yay': return '<em>passed</em>'
    else: return '<em>failed</em>'

@route('/testpost/', method='POST')
def testpost():
    test = request.POST.get('test')
    if test=='yay': return '<em>passed</em>'
    else: return '<em>failed</em>'

if __name__=='__main__':
    run(host='localhost', port=8081, reloader=True)
