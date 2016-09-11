# -*- coding: utf-8 -*-
import sys
import unicodecsv
from lastfirst import init_for, db, models


NAME_TYPES = {
    u'Given': None,
    u'Surname': None,
    u'Profession': None,
    u'Title': None,
    u'Prefix': None,
    u'Suffix': None,
    u'Community': None,
    u'Place': None,
    u'Preposition': None,
    u'Initial': None,
    }


def loadnametypes():
    for nametype in list(NAME_TYPES.keys()):
        nt = models.Tag.query.filter_by(title=nametype, type=models.TAG_TYPE.NAMETYPE).first()
        if not nt:
            nt = models.Tag(title=nametype, type=models.TAG_TYPE.NAMETYPE)
            db.session.add(nt)
        NAME_TYPES[nametype] = nt


def loadfile(fileob):
    input = unicodecsv.reader(fileob)
    for row in input:
        if row[0].startswith('#'):
            # Comment. Ignore this row
            continue
        title = row[0]
        gender = {'m': models.GENDER.MALE, 'f': models.GENDER.FEMALE}.get(row[1])
        description = row[2]
        tags = row[3:]

        name = models.Name.query.filter_by(title=title, gender=gender).first()
        if not name:
            name = models.Name(title=title, gender=gender, description=description)
            db.session.add(name)
        for tag in tags:
            tagob = models.Tag.query.filter_by(title=tag, type=models.TAG_TYPE.COMMUNITY).first()
            if not tagob:
                tagob = models.Tag(title=tag, type=models.TAG_TYPE.COMMUNITY)
                db.session.add(tagob)
            if tagob not in name.tags:
                name.tags.append(tagob)
        if NAME_TYPES['Given'] not in name.tags:
            name.tags.append(NAME_TYPES['Given'])


def main(argv):
    if len(argv) < 3:
        print sys.stderr, "Syntax: %s <env> <file>…" % argv[0]
    env = argv[1]
    filenames = argv[2:]
    init_for(env)
    loadnametypes()
    for fname in filenames:
        loadfile(open(fname))
    db.session.commit()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
