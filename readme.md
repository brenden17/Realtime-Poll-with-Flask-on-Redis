# Real Poll with redis on Flask

This is Flask extension which implements Poll on page with Redis bitmap.


## Reqirements

* Redis server
* Python library
~~~
pip install flask-session
pip install redis
~~~
* Bootsrap
* Javascript library for graph
* http://dimplejs.org/

## How to use
Just put snippet on html page.

* Poll

~~~

{{ poll(title='What is your favorite OS?',
      description='Please select your OS for new modules.',
      items=[('windows', 'Windows'),
              ('linux', 'Linux'),
              ('os-x', 'OS X')],
      poll_name='OS') }}


~~~

* Poll Result

It supports different 3 type graphs like bar, pie and total pie

~~~

  {{ poll_analytics(items=[('windows', 'Windows'),
                            ('linux', 'Linux'),
                            ('os-x', 'OS X')],
                    poll_name='OS',
                    graph='pie') }}


  {{ poll_analytics(items=[('windows', 'Windows'),
                          ('linux', 'Linux'),
                          ('os-x', 'OS X')],
                    poll_name='OS',
                    graph='bar') }}

  {{ poll_analytics(items=[('windows', 'Windows'),
                              ('linux', 'Linux'),
                              ('os-x', 'OS X')],
                    poll_name='OS',
                    width='590',
                    height='400',
                    graph='total-pie') }}

~~~

* Poll

![alt text](https://github.com/brenden17/Realtime-Poll-with-Flask-on-Redis/blob/master/img/poll.png "image")

* Result
![alt text](https://github.com/brenden17/Realtime-Poll-with-Flask-on-Redis/blob/master/img/result.png "image")



That's all.