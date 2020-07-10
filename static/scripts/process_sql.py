import sqlite3, json
conn = sqlite3.connect('../database/cma-artworks.db')
cursor = conn.cursor()
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# print(cursor.fetchall())

#[('artwork__department',), ('artwork',), ('creator',), ('department',), ('artwork__creator',)]

# [(0, 'id', '', 0, None, 0), (1, 'accession_number', '', 0, None, 0), (2, 'title', '', 0, None, 0), (3, 'tombstone', '', 0, None, 0)]
global artwork_dic
artwork_dic = {}

def main():
    # cursor.execute("PRAGMA table_info(artwork__creator)")
    # print (cursor.fetchall())
    global artwork_dic
    #get artwork ID
    cursor.execute("""SELECT DISTINCT artwork.id, artwork.accession_number, artwork.title, artwork.tombstone
    FROM artwork
    """)
    rows = cursor.fetchall()

    ## build artwork diction
    for row in rows:
        #print(row)
        id = row[0]
        accession_number = row[1]
        title = row[2]
        tombstone = row[3]
        artwork_dic[id] = {}
        artwork_dic[id]['accession_number'] = accession_number
        artwork_dic[id]['image'] = '/static/images/'+accession_number + '_reduced.jpg'
        artwork_dic[id]['title'] = title
        artwork_dic[id]['tombstone'] = tombstone
        artwork_dic[id]['department'] = {}
        artwork_dic[id]['creator'] = []
    process_departments()
    process_creators()
    with open('../data/image-data.json', 'w') as outfile:
        json.dump(artwork_dic, outfile)
    outfile.close()

def process_departments():
    global artwork_dic
    for id in artwork_dic.keys():
        cursor.execute("""SELECT artwork__department.department_id
        FROM artwork__department
        WHERE artwork__department.artwork_id = '%s'
        """ % (id))
        rows = cursor.fetchall()
        for row in rows:
            department_id = row[0]
            department_dic = {}
            department_dic['id'] = department_id
            cursor.execute("""SELECT DISTINCT department.name
            FROM department
            WHERE department.id = '%s'
            """ % (department_id))
            rows = cursor.fetchall()
            for row in rows:
                name = row[0]
                department_dic['name'] = name
            artwork_dic[id]['department'].update(department_dic)

def process_creators():
    global artwork_dic
    for id in artwork_dic.keys():
        cursor.execute("""SELECT artwork__creator.creator_id
        FROM artwork__creator
        WHERE artwork__creator.artwork_id = '%s'
        """ % (id))
        rows = cursor.fetchall()
        for row in rows:
            creator_id = row[0]
            creator_dic = {}
            creator_dic['id'] = creator_id
            creator_dic['role'] = []
            creator_dic['description'] = 'UNKNOWN'
            cursor.execute("""SELECT DISTINCT creator.role, creator.description
            FROM creator
            WHERE creator.id = '%s'
            """ % (creator_id))
            rows = cursor.fetchall()
            for row in rows:
                role = row[0]
                description = row[1]
                if description == 'NULL' or len(description) == 0:
                    description = 'UNKNOWN'
                if role not in creator_dic['role']:
                    creator_dic['role'].append(role)
                creator_dic['description'] = description
            artwork_dic[id]['creator'].append(creator_dic)


if __name__ == "__main__":

    # call the main function, passing along arguments
    main()
