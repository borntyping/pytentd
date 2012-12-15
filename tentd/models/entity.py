"""
Data model for tent entities
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey

from tentd.models import db
from tentd.models.profiles import Profile, Core, Basic

class Entity(db.Model):
    """A tent entity"""
    
    #: The local identifier and primary key
    id = Column(Integer, primary_key=True)
    
    #: The url identifier
    name = Column(String(20), unique=True)

    profiles = db.relationship('Profile', lazy='dynamic')

    @property
    def core (self):
        return self.profiles.filter(Profile.schema==Core.__schema__).one()

    def __init__ (self, core={}, **kwargs):
        """Creates an Entity and a Core profile"""
        super(Entity, self).__init__(**kwargs)
        if not core is None:
            db.session.add(Core(entity=self, **core))
            db.session.add(Basic(entity=self))
    
    def __repr__ (self):
        return "<{} '{}' [{}]>".format(self.__class__.__name__, self.name, self.id)
    
    def __str__ (self):
        """	Used in urls, so don't change! """
        return self.name
