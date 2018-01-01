# This contains our frontend; since it is a bit messy to use the @app.route
# decorator style when using application factories, all of our routes are
# inside blueprints. This is the front-facing blueprint.
#
# You can find out more about blueprints at
# http://flask.pocoo.org/docs/blueprints/

import datetime

from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from flask_googlecharts import GoogleCharts, LineChart, AnnotationChart
from markupsafe import escape

from .forms import SignupForm
from .nav import nav
from .milestone import connect, get_latest_index, get_milestone, get_milestones_hr
from .node import get_node_info

MILESTONE_PAGE_ITEM = 50


frontend = Blueprint('frontend', __name__)
charts = GoogleCharts()

# We're adding a navbar as well through flask-navbar. In our example, the
# navbar has an usual amount of Link-Elements, more commonly you will have a
# lot more View instances.
nav.register_element('frontend_top', Navbar(
    View('IOTA COO Milestone Monitor', '.index'),
    View('Home', '.index'),
    View('Milestones', '.milestones'),
    View('Stats', '.stats'),
    View('About', '.about')))


# Our index-page just shows a quick explanation. Check out the template
# "templates/index.html" documentation for more details.
@frontend.route('/')
def index():
    nodeinfo = get_node_info()
    mindex = get_latest_index()
    milestones = get_milestone({'mindex >': mindex - 5})
    return render_template('index.html', milestones=milestones, nodeinfo=nodeinfo)


def get_maxp(mindex):
    return (mindex - 243000) // MILESTONE_PAGE_ITEM + 1

def get_page(page, mindex):
    max_page = get_maxp(mindex) + 1
    start = 1 if page - 5 < 1 else page - 5
    end = max_page if page + 5 > max_page else page + 5
    if end - start < 10 and end != max_page:
        end = start + 9
    return start, end


@frontend.route('/milestones')
def milestones():
    page = int(request.args.get('p', 1))
    mindex = get_latest_index()
    maxp = get_maxp(mindex)

    if page > maxp or page < 1:
        return "milestone page error"
    
    milestones = get_milestone(
        {'mindex >': mindex - MILESTONE_PAGE_ITEM * page,
         'mindex <=': mindex - (MILESTONE_PAGE_ITEM * (page - 1))})
    start, end = get_page(page, mindex)
    return render_template('milestones.html', milestones=milestones,
                           page=page, start=start, end=end, maxp=maxp)


@frontend.route('/stats')
def stats():
    # Get all milestone hours from 243001
    d = datetime.datetime.now() - datetime.datetime.fromtimestamp(1508788869)
    days_all = get_milestones_hr(d.days + 1)
    chart = AnnotationChart("milestones_hr", options={"title": "test", "width": "80%", "height": "50%"})
    chart.add_column("datetime", "Days")
    chart.add_column("number", "Milestones")
    chart.add_rows(days_all)
    charts.register(chart)
    return render_template('stats.html')


@frontend.route('/about')
def about():
    return render_template('about.html')
