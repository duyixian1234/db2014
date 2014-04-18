"""A simple library manage system using webpy 0.3,mysql and bootstrap."""
import web
import model

### Url mappings
urls=(
    '^/$','index',
    '^/login', 'login',
    '^/logout', 'logout',
     '^/(.*?)','index'
    )

###Application settings
app=web.application(urls,globals())

###Session settings
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={
        'login':0,
        'id':'',
    })
    web.config._session = session
else:
    session = web.config._session

#variables defination

titles={'book':['bno','category','title','press','year','price','total','stock'],
        'card':['cno','name','department','type'],
        'borrow':['cno','bno','id','borrow_date','return_date'],
        'manager':['id','name','tel']
        }


###Functions defination

def logged():
    """If login in or not"""
    if session.login==1:
        return True
    else:
        return False

def check(user,passwd):
    """Check whether the user name and password is effective."""
    myvars=dict(id=user)
    try:
        table=model.db.select('manager',myvars,where=web.db.sqlwhere(myvars))
        real_passwd=table[0]['passwd']
        if real_passwd==passwd:
            session.login=1
            session.id=user
        else:
            pass
    except:
        pass



###Templates

render = web.template.render('templates',base='base',globals=globals())
blank= web.template.render('templates',base='blank',globals=globals())

###Main
class login:
    """Log in"""
    def GET(self):
        if logged():
            return web.seeother('/')
        return blank.login()
    def POST(self):
        user=web.input().user
        passwd=web.input().passwd
        check(user,passwd)
        if logged():
            return web.seeother('/')
        else:
            return blank.login()

class logout:
    """Log out"""
    def GET(self):
        session.login=0
        return web.seeother('/login')

class index:
    """index page"""
    def GET(self):
        if logged():
            data=web.input()
            try:
                posts=model.show(data.table)
                return render.view(posts,data.table,titles[data.table],session.id)
            except:
                return web.seeother('/?table=manager')
        else:
            return web.seeother('/login')

    def POST(self):
        """Deal with the input."""
        data=web.input(booklists={})
        posts=model.operate(data)
        return render.view(posts,data.table,titles[data.table],session.id)

if __name__=='__main__':
    app.run()
