# -*- coding: utf-8 -*-

def index():
    return dict(message=T('Welcome to web2py!'))

def tickers():
    # temporary set to constatnt. to be replaced with  last date.
    tickers = db(db.stock_w_fi.dt == '5-12-2017').select(db.stock_w_fi.volume,db.stock_w_fi.ticker,db.stock_w_fi.close,db.stock_w_fi.dt)
    #tickers = db().select(db.stock_w_fi.ticker,distinct=db.stock_w_fi.ticker)
    return dict(tickers=tickers)

def main_chart():
    ticker = request.args[0]
    db_data = db(db.stock_w_fi.ticker == ticker).select(db.stock_w_fi.close,db.stock_w_fi.dt,db.stock_w_fi.ema10,db.stock_w_fi.ema20)

    close_prices = []
    close_dates = []
    ema10=[]
    ema20=[]

    for row in db_data:
        close_prices.append(row.close)
        close_dates.append(row.dt)
        ema20.append(row.ema20)
        ema10.append(row.ema10)

    response.files.append(URL('default','static/js/pygal-tooltips.min.js'))
    response.headers['Content-Type']='image/svg+xml'
    import pygal
    from pygal.style import CleanStyle
    chart = pygal.Line(style=CleanStyle)
    chart.x_labels = (map(lambda d: d.strftime('%Y-%m-%d'), close_dates))
    chart.add('close', close_prices)
    chart.add('ema10', ema10)
    chart.add('ema20', ema20)
    return chart.render()

def Elder_FI():
    ticker = request.args[0]
    db_data = db(db.stock_w_fi.ticker == ticker).select(db.stock_w_fi.dt,db.stock_w_fi.fi2,db.stock_w_fi.fi13)

    close_dates = []
    fi2=[]
    fi13=[]

    for row in db_data:
        close_dates.append(row.dt)
        fi2.append(row.fi2)
        fi13.append(row.fi13)

    response.files.append(URL('default','static/js/pygal-tooltips.min.js'))
    response.headers['Content-Type']='image/svg+xml'
    import pygal
    from pygal.style import CleanStyle
    chart = pygal.Line(style=CleanStyle)
    chart.x_labels = (map(lambda d: d.strftime('%Y-%m-%d'), close_dates))
    chart.add('fi2', fi2)
    chart.add('fi13', fi13)
    return chart.render()

def AO():
    ticker = request.args[0]
    db_data = db(db.stock_w_fi.ticker == ticker).select(db.stock_w_fi.dt,db.stock_w_fi.ao)

    close_dates = []
    ao=[]

    for row in db_data:
        close_dates.append(row.dt)
        ao.append(row.ao)

    response.files.append(URL('default','static/js/pygal-tooltips.min.js'))
    response.headers['Content-Type']='image/svg+xml'
    import pygal
    from pygal.style import CleanStyle
    chart = pygal.Bar(style=CleanStyle)
    chart.x_labels = (map(lambda d: d.strftime('%Y-%m-%d'), close_dates))
    chart.add('AO', ao)
    return chart.render()

def volume():
    ticker = request.args[0]
    db_data = db(db.stock_w_fi.ticker == ticker).select(db.stock_w_fi.dt,db.stock_w_fi.volume)

    close_dates = []
    vol=[]

    for row in db_data:
        close_dates.append(row.dt)
        vol.append(row.volume)

    response.files.append(URL('default','static/js/pygal-tooltips.min.js'))
    response.headers['Content-Type']='image/svg+xml'
    import pygal
    from pygal.style import CleanStyle
    chart = pygal.Bar(style=CleanStyle)
    chart.x_labels = (map(lambda d: d.strftime('%Y-%m-%d'), close_dates))
    chart.add('Volume', vol)
    return chart.render()

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
