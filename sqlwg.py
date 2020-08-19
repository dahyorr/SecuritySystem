def sqget(command):
  import MySQLdb
  db =MySQLdb.connect("localhost", "dahyor", "aaaazzzz", "secsys")
  curs= db.cursor()
  curs.execute (command)
  info=[]
  for reading in curs.fetchall():
    info.append((str(reading).strip("('")).strip("',)"))
  db.close()
  return info

def sqget1(command):
  import MySQLdb
  db =MySQLdb.connect("localhost", "dahyor", "aaaazzzz", "secsys")
  curs= db.cursor()
  curs.execute (command)
  info=""
  for reading in curs.fetchall():
    info= (str(reading).strip("('")).strip("',)")
  db.close()
  return info
    

def sqwrite(command):
  import MySQLdb
  doordb =MySQLdb.connect("localhost", "dahyor", "aaaazzzz", "secsys")
  curs= doordb.cursor()
  curs.execute(command)
  doordb.commit()
  doordb.close()
#UPDATE pincode set code ='222444'
#UPDATE lockstate set state ='1'