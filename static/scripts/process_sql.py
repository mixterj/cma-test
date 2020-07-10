# Script to extract transform and load data from SQL datafile into JSON document
# author: Jeff Mixter
# email: jeffmixter@gmail.com

# import libraries
import sqlite3, json

# set variables
global artwork_dic
artwork_dic = {}


# connect to the SQL file
conn = sqlite3.connect('../database/cma-artworks.db')
cursor = conn.cursor()


def main():
    global artwork_dic
    cursor.execute("""SELECT DISTINCT artwork.id, artwork.accession_number, artwork.title, artwork.tombstone
    FROM artwork
    """)
    rows = cursor.fetchall()

    ## build artwork dictionary
    for row in rows:
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
    # process the departments table
    process_departments()
    # process the creators table
    process_creators()
    with open('../data/image-data.json', 'w') as outfile:
        json.dump(artwork_dic, outfile)
    outfile.close()

def process_departments():
    # build department objects to connect to the artwork records
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
    # build creator objects to connect to the artwork records
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
    main()
