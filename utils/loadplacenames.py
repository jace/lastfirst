# -*- coding: utf-8 -*-
import sys
from collections import namedtuple
import unicodecsv
from progressbar import ProgressBar
import progressbar.widgets
from lastfirst import init_for, db, models

NAME_TYPES = {
    u'Place': None,
    }

GeoNameRecord = namedtuple('GeoNameRecord', ['geonameid', 'title', 'ascii_title', 'alternatenames',
    'latitude', 'longitude', 'fclass', 'fcode', 'country_id', 'cc2', 'admin1', 'admin2',
    'admin3', 'admin4', 'population', 'elevation', 'dem', 'timezone', 'moddate'])

features = {
    ('L', 'CONT'),
    ('A', 'PCL'),
    ('A', 'PCLD'),
    ('A', 'PCLF'),
    ('A', 'PCLI'),
    ('A', 'PCLS'),
    ('A', 'ADM1'),
    ('P', 'PPLC'),
    ('P', 'PPLA'),
    ('P', 'PPLA2'),
    ('P', 'PPLA3'),
    ('P', 'PPLA4'),
    ('P', 'PPLG'),
    ('P', 'PPL'),
    ('P', 'PPLR'),
    ('P', 'PPLS'),
    ('P', 'PPLX'),
    ('S', 'TRIG'),
    ('P', 'PPLL'),
    ('P', 'PPLF'),
    ('A', 'ADM2'),
    ('A', 'ADM3'),
    }

admin1_community = {
    ('IN', '28'): [u'Indian', u'Bengali'],  # West Bengal West Bengal 1252881
    ('IN', '36'): [u'Indian'],  # Uttar Pradesh   Uttar Pradesh   1253626
    ('IN', '26'): [u'Indian'],  # Tripura Tripura 1254169
    ('IN', '40'): [u'Indian', u'Telugu'],  # Telangana   Telangana   1254788
    ('IN', '25'): [u'Indian', u'Tamil'],  # Tamil Nadu  Tamil Nadu  1255053
    ('IN', '29'): [u'Indian'],  # Sikkim  Sikkim  1256312
    ('IN', '24'): [u'Indian'],  # Rajasthan   Rajasthan   1258899
    ('IN', '23'): [u'Indian', u'Punjabi'],  # Punjab  Punjab  1259223
    ('IN', '22'): [u'Indian'],  # Pondicherry Pondicherry 1259424
    ('IN', '21'): [u'Indian', u'Oriya'],  # Odisha  Odisha  1261029
    ('IN', '20'): [u'Indian'],  # Nagaland    Nagaland    1262271
    ('IN', '31'): [u'Indian'],  # Mizoram Mizoram 1262963
    ('IN', '18'): [u'Indian'],  # Meghalaya   Meghalaya   1263207
    ('IN', '17'): [u'Indian'],  # Manipur Manipur 1263706
    ('IN', '16'): [u'Indian', u'Marathi'],  # Maharashtra Maharashtra 1264418
    ('IN', '35'): [u'Indian'],  # Madhya Pradesh  Madhya Pradesh  1264542
    ('IN', '14'): [u'Indian'],  # Laccadives  Laccadives  1265206
    ('IN', '13'): [u'Indian', u'Malayalam'],  # Kerala  Kerala  1267254
    ('IN', '19'): [u'Indian', u'Kannada'],  # Karnataka   Karnataka   1267701
    ('IN', '12'): [u'Indian', u'Kashmiri'],  # Kashmir Kashmir 1269320
    ('IN', '11'): [u'Indian'],  # Himachal Pradesh    Himachal Pradesh    1270101
    ('IN', '10'): [u'Indian', u'Haryanvi'],  # Haryana Haryana 1270260
    ('IN', '09'): [u'Indian', u'Gujarati'],  # Gujarat Gujarat 1270770
    ('IN', '32'): [u'Indian'],  # Daman and Diu   Daman and Diu   1271155
    ('IN', '33'): [u'Indian'],  # Goa Goa 1271157
    ('IN', '07'): [u'Indian'],  # NCT NCT 1273293
    ('IN', '06'): [u'Indian'],  # Dadra and Nagar Haveli  Dadra and Nagar Haveli  1273726
    ('IN', '05'): [u'Indian'],  # Chandigarh  Chandigarh  1274744
    ('IN', '34'): [u'Indian', u'Bihari'],  # Bihar   Bihar   1275715
    ('IN', '03'): [u'Indian', u'Assamese'],  # Assam   Assam   1278253
    ('IN', '30'): [u'Indian'],  # Arunachal Pradesh   Arunachal Pradesh   1278341
    ('IN', '02'): [u'Indian', u'Telugu'],  # Andhra Pradesh  Andhra Pradesh  1278629
    ('IN', '01'): [u'Indian'],  # Andaman and Nicobar Islands Andaman and Nicobar Islands 1278647
    ('IN', '37'): [u'Indian'],  # Chhattisgarh    Chhattisgarh    1444364
    ('IN', '38'): [u'Indian'],  # Jharkhand   Jharkhand   1444365
    ('IN', '39'): [u'Indian'],  # Uttarakhand Uttarakhand 1444366
    }

community_tags = {}


def loadnametypes():
    for nametype in list(NAME_TYPES.keys()):
        nt = models.Tag.query.filter_by(title=nametype, type=models.TAG_TYPE.NAMETYPE).first()
        if not nt:
            nt = models.Tag(title=nametype, type=models.TAG_TYPE.NAMETYPE)
            db.session.add(nt)
        NAME_TYPES[nametype] = nt


def loadfile(fileob):
    gender = models.GENDER.UNDEFINED
    size = sum(1 for line in fileob)
    fileob.seek(0)  # Return to start
    progress = ProgressBar(maxval=size,
        widgets=[progressbar.widgets.Percentage(), ' ', progressbar.widgets.Bar(), ' ', progressbar.widgets.ETA(), ' ']).start()

    for counter, line in enumerate(fileob):
        progress.update(counter)
        line = unicode(line, 'utf-8')

        if line.startswith('#'):
            continue

        rec = GeoNameRecord(*line.strip().split('\t'))
        if (rec.fclass, rec.fcode) not in features:
            continue

        name1 = models.Name.query.filter_by(title=rec.title, gender=gender).first()
        if not name1:
            name1 = models.Name(title=rec.title, gender=gender)
            db.session.add(name1)
        if rec.ascii_title == rec.title:
            name2 = name1
        else:
            name2 = models.Name.query.filter_by(title=rec.ascii_title, gender=gender).first()
            if not name2:
                name2 = models.Name(title=rec.ascii_title, gender=gender)
                db.session.add(name2)
        for name in (name1, name2):
            if NAME_TYPES['Place'] not in name.tags:
                name.tags.append(NAME_TYPES['Place'])
            if (rec.cc2, rec.admin1) in admin1_community:
                for community_name in admin1_community[(rec.cc2, rec.admin1)]:
                    tagob = community_tags.get(community_name)
                    if not tagob:
                        tagob = models.Tag.query.filter_by(title=community_name, type=models.TAG_TYPE.COMMUNITY).first()
                        if not tagob:
                            tagob = models.Tag(title=community_name, type=models.TAG_TYPE.COMMUNITY)
                            db.session.add(tagob)
                        community_tags[community_name] = tagob
                    if tagob not in name.tags:
                        name.tags.append(tagob)
    progress.finish()


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
