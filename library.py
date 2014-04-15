"""A simple library manage system using webpy 0.3 and mysql"""
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

if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={
        'login':0,
        'id':'',
    })
    web.config._session = session
else:
    session = web.config._session

#variables

titles={'book':['bno','category','title','press','year','price','total','stock'],
        'card':['cno','name','department','type'],
        'borrow':['cno','bno','id','borrow_date','return_date'],
        'manager':['id','name','tel']
        }

db=web.database(dbn='mysql',db='library',user='root',passwd='0800')
current_table=''

###Functions

def logged():
    if session.login==1:
        return True
    else:
        return False

def check(user,passwd):
    myvars=dict(id=user)
    try:
        table=db.select('manager',myvars,where=web.db.sqlwhere(myvars))
        real_passwd=table[0]['passwd']
        if real_passwd==passwd:
            session.login=1
            session.id=user
        else:
            pass
    except:
        pass

def query(execs='select 0'):
    return db.query(execs)

def show(table='manager'):
    return db.select(table,_test=False)

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
                current_table=data.table
                print current_table
                posts=show(data.table)
                return render.view(posts,data.table,titles[data.table],session.id)
            except:
                return web.seeother('/?table=manager')
        else:
            return web.seeother('/login')

    def POST(self):
        data=web.input()
        current_table=data.table
        lists=titles[data.table]
        unique=lists[0]
        vars={}
        for each_title in lists:
            try:
                if data[each_title]!='':
                     vars[each_title]=data[each_title]
            except:
                pass

        posts=show(data.table)


        try:
            if data.operate=='select':
                posts=db.select(data.table,where=web.db.sqlwhere(vars))
            elif data.operate=='insert':
                query='insert into '+data.table+' set '
                query=query+unique+' = "'+vars[unique]+'"'
                for i in vars:
                    if i!=unique:
                        query=query+','+i+' = "'+vars[i]+'"'
                db.query(query)
                print query
                print data.table
                if data.table=='borrow':
                    print 'begin to borrow'
                    borrow='update  book set stock=stock-1 where bno = "'
                    borrow=borrow+vars['bno']+'"'
                    print borrow
                    db.query(borrow)
                posts=show(data.table)
            elif data.operate=='delete':
                try:
                    vars[unique]=data.unique
                except:
                    pass
                db.delete(data.table,where=web.db.sqlwhere(vars))
                posts=show(data.table)
            else:
                pass
        except:
            pass
        return render.view(posts,data.table,titles[data.table],session.id)

if __name__=='__main__':
    app.run()
