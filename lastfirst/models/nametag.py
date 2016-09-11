# -*- coding: utf-8 -*-

from coaster.utils import LabeledEnum
from . import db, BaseMixin

__all__ = ['GENDER', 'TAG_TYPE', 'Name', 'Tag']


class GENDER(LabeledEnum):
    UNDEFINED = (None, "Undefined")
    UNISEX = (0, "Unisex")
    MALE = (1, "Male")
    FEMALE = (2, "Female")


class TAG_TYPE(LabeledEnum):
    UNDEFINED = (None, "Undefined")
    COMMUNITY = (1, "Community")  # Indian, Hindu, Muslim, etc
    NAMETYPE = (2, "Name type")   # Given, Surname, etc


name_tag = db.Table('name_tag', db.Model.metadata,
    db.Column('name_id', None, db.ForeignKey('name.id'), primary_key=True),
    db.Column('tag_id', None, db.ForeignKey('tag.id'), primary_key=True, index=True),
    db.Column('created_at', db.DateTime, default=db.func.utcnow()),
    )


class Name(BaseMixin, db.Model):
    __tablename__ = 'name'

    # Naming convention:
    # 'title' is the human-readable version of the name.
    # A URL-friendly version would be called 'name'
    title = db.Column(db.Unicode(250), nullable=False, index=True)
    gender = db.Column(db.SmallInteger, nullable=True, default=GENDER.UNDEFINED, index=True)
    description = db.Column(db.UnicodeText, nullable=True)

    def __repr__(self):
        return '<Name %s %s>' % (self.title, GENDER[self.gender])


class Tag(BaseMixin, db.Model):
    __tablename__ = 'tag'

    title = db.Column(db.Unicode(250), nullable=False, index=True)
    type = db.Column(db.SmallInteger, nullable=True, default=TAG_TYPE.UNDEFINED, index=True)
    description = db.Column(db.UnicodeText, nullable=True)
    names = db.relationship(Name, lazy='dynamic', backref=db.backref('tags', order_by=title),
        secondary=name_tag, order_by=Name.title)

    def __repr__(self):
        return '<Tag %s %s>' % (self.title, TAG_TYPE[self.type])
