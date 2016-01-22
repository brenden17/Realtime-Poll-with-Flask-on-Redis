import json
from random import getrandbits
from datetime import datetime, timedelta

from redis import Redis

from flask import session
from flask import request
from flask import Blueprint
from flask import render_template
from flask import Markup
from flask.views import View

redis = Redis()

class PollSession(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.add_url_rule('/poll', view_func=PollAjax.as_view('poll'))


class PollAjax(View):
    methods = ['POST']
    def dispatch_request(self):
        if request.method == 'POST':
            item = request.form.get('item')
            poll_name = request.form.get('name')

            session_id = session.sid
            user_id = redis.get(session_id)
            if not user_id:
                user_id = getrandbits(24) # random number of 24bit
                redis.set(session_id, user_id)
            # vote
            poll_item(user_id, item, poll_name)

            return '{"result":"ok"}'


def poll_item(user_id, item='none', poll_name='poll'):
    key = create_key(item, poll_name)
    try:
        redis.setbit(key, user_id, 1)
    except Exception, e:
        print(e)


def create_key(item='none', poll_name='poll', target_time=None):
    if not target_time:
        target_time = datetime.now()
    
    created_time = target_time.strftime('%Y-%m-%d')
    return '{0}:{1}:{2}'.format(poll_name, item, created_time)


class PollAnalytics(object):
    def __init__(self, items, poll_name='poll'):
        self.items = [item for item, caption in items]
        self.item_captions = {item:caption for item, caption in items}
        self.poll_name = poll_name

    def fetch_daily(self, last=30):
        items = ','.join([self.get_item(item, day) for item in self.items for day in range(last)])
        return '[{}]'.format(items)

    def get_item(self, item, last=30):
        d = datetime.today() - timedelta(days=last)
        key = create_key(item, self.poll_name, d)
        count = redis.bitcount(key)
        return '{"date":"%s", "item":"%s", "count":"%s"}' % \
                    (key.split(':')[2], self.item_captions[item], count)

    def delete_all_events(self, action):
        events = redis.keys('{}:*:*'.format(self.poll_name))
        if events:
            try:
                redis.delete(*events)
            except Exception, e:
                print(e)


class PollRender(object):
    def __init__(self, 
                title='',
                description='',
                items=[],
                poll_name='poll-name',
                poll_type='radio'):
        self.title = title
        self.description = description
        self.items = items
        self.poll_name = poll_name
        self.poll_type = poll_type

    def render(self, *args, **kwargs):
        return render_template(*args, **kwargs)

    @property
    def html(self):
        if self.poll_type == 'button':
            return Markup(self.render('PollRedis/inline_button.html', pb=self))
        else:
            return Markup(self.render('PollRedis/inline.html', pb=self))


def poll(*args, **kwargs):
    poll_render = PollRender(*args, **kwargs)
    return poll_render.html


class PollResultRender(object):
    def __init__(self, 
                    items=[],
                    poll_name='Poll',
                    graph='bar',
                    width='600',
                    height='350',
                    last=7,
                    x='date', 
                    y='count'):
        self.items = items
        self.poll_name = poll_name
        self.graph = graph
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.PA = PollAnalytics(self.items, self.poll_name)
        self.data = self.PA.fetch_daily(last)

    def render(self, *args, **kwargs):
        return render_template(*args, **kwargs)

    @property
    def html(self):
        base_html = 'PollRedis/{}.html'.format(self.graph)
        return Markup(self.render(base_html, pr=self))


def poll_analytics(*args, **kwargs):
    pollresult_render = PollResultRender(*args, **kwargs)
    return pollresult_render.html


class Poll(object):
    def __init__(self, app):
        self.init_app(app)

    def init_app(self, app):
        self.register_blueprint(app)
        app.add_template_global(poll_analytics)
        app.add_template_global(poll)

    def register_blueprint(self, app):
        module = Blueprint(
            'PollRedis',
            __name__,
            template_folder='templates'
        )
        app.register_blueprint(module)
        return module
        
class PollRedis(object):
    def __init__(self, app):
        PollSession(app)
        Poll(app)