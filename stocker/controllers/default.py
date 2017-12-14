# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
def index():
    tickers = db().select(db.stock_w_fi.ticker, distinct=db.stock_w_fi.ticker)
    return dict(tickers=tickers)

def show():
    ticker = request.args[0]
    c_prices_row = db(db.stock_w_fi.ticker == ticker).select(db.stock_w_fi.close)
    close_prices = []

    for c_price in c_prices_row:
        close_prices.append(c_price.close)

    response.files.append(URL('default','static/js/pygal-tooltips.min.js'))
    response.headers['Content-Type']='image/svg+xml'
    import pygal
    from pygal.style import CleanStyle
    chart = pygal.Line(style=CleanStyle)
    chart.add(ticker, close_prices)
    return chart.render()

def show_old():
    ticker = request.args[0]
                           #or redirect(URL('index')))
    #db.stock_w_fi.ticker.default = ticker
    #ticker=db().select(db.stock_w_fi.ticker, distinct=db.stock_w_fi.ticker)
    #if form.process().accepted:
    #    response.flash = 'your comment is posted'
    #comments = db(db.post.image_id == image.id).select()
    ticker = db(db.stock_w_fi.ticker == ticker).select()
    #ticker = request.args[0]
    return dict(ticker=ticker)

# <trainings
def displayTickers():
    #query=db().select(db.stock_w_fi.ticker, distinct=db.stock_w_fi.ticker)
    #return grid(SQLFORM.grid(query))
    tuples=db().select(db.stock_w_fi.ticker, distinct=db.stock_w_fi.ticker)
    return dict(grid=tuples)

def displayTickersG():
    #query=((db.stock_w_fi.ticker))
    #fields = (db.stock_w_fi.ticker)
    #default_sort_order=[db.stock_w_fi.ticker]
    #form = SQLFORM.grid(query=query,fields=fields,orderby=default_sort_order)
    #return dict(form=form)
    grid = SQLFORM.grid(db.stock_w_fi)
    return locals()

def TickerSelector():
    tickers = db().select(db.stock_w_fi.ticker, distinct=db.stock_w_fi.ticker)
    form = FORM(TR(tickers))
# /trainings>

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
