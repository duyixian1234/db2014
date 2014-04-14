"""A simple library manage system using webpy 0.3 and mysql"""
import web

### Url mappings
urls=(
    '^/$','Exec',
    '^/login', 'login',
    '^/logout', 'logout',
     '^/(.*?)','Exec'
    )

###Application settings
app=web.application(urls,globals())


###Variables

titles={'book':['bno','category','title','press','year','price','total','stock'],
        'card':['cno','name','department','type'],
        'borrow':['cno','bno','id','borrow_date','return_date'],
        'manager':['id','name','tel']
        }

db=web.database(dbn='mysql',db='library',user='root',passwd='0800')


if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={
        'login':0,
        'privilege':0
    })
    web.config._session = session
else:
    session = web.config._session


###Functions
def query(execs='select 0'):
    return db.query(execs)

def show(table='book'):
    return db.select(table,_test=False)



###Templates
render = web.template.render('templates',base='base')
blank= web.template.render('templates',base='blank')

class Exec:

    def GET(self):
        if session.login==0:
            return web.seeother('/login')
        data=web.input(table='book')
        posts=show(data.table)
        return render.view(posts,data.table,titles[data.table])

    def POST(self):
        data=web.input(execs='select 0')
        if data.execs!='':
            query(data.execs)
        return web.seeother(web.ctx.fullpath)

class login:
    def GET(self):
        return blank.login()

    def POST(self):
        user=web.input().user
        passwd=web.input().passwd
        myvars=dict(id=user)
        if db.select('manager',myvars,where='id=$id') is not None:
            table=db.select('manager',myvars,where='id=$id')
            correct=table[0]
            if correct['passwd']==passwd:
                session.login=1
        return web.seeother('/')

class logout:
    def GET(self):
        session.login=0
        return web.seeother('/login')





if __name__=='__main__':
    app.run()
