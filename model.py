import web

#variables defination

titles={'book':['bno','category','title','press','year','price','total','stock'],
        'card':['cno','name','department','type'],
        'borrow':['cno','bno','id','borrow_date','return_date'],
        'manager':['id','name','tel']
        }

###Connencting the database
db=web.database(dbn='mysql',db='library',user='root',passwd='0800')


###Functions defination


def show(table='manager'):
    """Show tables"""
    return db.select(table,limit=50,_test=False)



def operate(data):
    """Deal with the post and send it to Mysql"""
    lists=titles[data.table]
    unique=lists[0]
    vars={}
    for each_title in lists:
        try:
            if data[each_title]!='':
                vars[each_title]=data[each_title]
        except:
            pass
    try:
        for line in data.booklists.file:
            try:
                query='insert into book values'
                line=line[3:-4]
                words=line.split(', ')
                query+='("'+words[0]+'"'
                for i in range(1,len(words)):
                    if i in [1,2,3,5]:
                        query+=',"'+words[i]+'"'
                    else:
                        query+=','+words[i]
                query+=','+words[len(words)-1]
                query+=')'
                db.query(query)
            except:
                pass
    except:
        pass
    posts=show(data.table)
    try:
        if data.operate=='select':
            if data.table!='book':
                posts=db.select(data.table,where=web.db.sqlwhere(vars))
            else:
                fr='1000'
                to='3999'
                small='0.00'
                large='99999.99'
                try:
                    fr,to=vars['year'].split(':')
                    del vars['year']
                except:
                    pass
                try:
                    small,large=vars['price'].split(':')
                    del vars['price']
                except:
                    pass
                wheres='select * from book where '
                for each in vars:
                    wheres+=each+' = "'+vars[each]+'" and '
                wheres+='year >= '+fr+' and year <= '+to+' and price >= '+small+' and price <= '+large
                posts=db.query(wheres)
        elif data.operate=='insert':
            query='insert into '+data.table+' set '
            query=query+unique+' = "'+vars[unique]+'"'
            for i in vars:
                if i!=unique:
                    query=query+','+i+' = "'+vars[i]+'"'
            if data.table=='borrow' :
                if data.borrow_date!='':
                    borrow='update  book set stock=stock-1 where bno = "'
                    borrow=borrow+vars['bno']+'"'
                    with db.transaction():
                        db.query(borrow)
                        db.query(query)
                elif data.return_date!='':
                    borrow='update  book set stock=stock+1 where bno = "'
                    borrow=borrow+vars['bno']+'"'
                    query='update borrow set return_date = "'
                    query+=vars['return_date']+'" where cno = "'+vars['cno']+'" and bno = "'+vars['bno']+'" and return_date is NULL  order by borrow_date  limit 1'
                    wheres=' cno = "'+vars['cno']+'" and bno = "'+vars['bno']+'" and return_date is NULL  order by borrow_date  limit 1'
                    a=len(db.select('borrow',where=wheres))
                    if a==1:
                        with db.transaction():
                            db.query(borrow)
                            db.query(query)
            else:
                with db.transaction():
                    db.query(query)
            posts=show(data.table)
        elif data.operate=='delete':
            try:
                vars[unique]=data.unique
            except:
                pass
            with db.transaction():
                db.delete(data.table,where=web.db.sqlwhere(vars))
            posts=show(data.table)
        else:
            pass
    except:
        pass
    return posts
