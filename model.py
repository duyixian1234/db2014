import web

###Variables




###Functions
def query(execs='select 0'):
    return db.query(execs)

def show(table='book'):
    return db.select(table,_test=False)


