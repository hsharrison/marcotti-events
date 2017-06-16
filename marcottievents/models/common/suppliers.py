from sqlalchemy import Column, Integer, String, Unicode, ForeignKey, Sequence
from sqlalchemy.orm import relationship, backref

from marcottievents.models import GUID
from marcottievents.models.common import BaseSchema
from marcottievents.models.common import enums


class Suppliers(BaseSchema):
    __tablename__ = "suppliers"

    id = Column(Integer, Sequence('supplier_id_seq', start=1000), primary_key=True)
    name = Column(Unicode(40), nullable=False)

    def __repr__(self):
        return "<Supplier(id={0}, name={1})>".format(self.id, self.name).encode('utf-8')


class CountryMap(BaseSchema):
    __tablename__ = "country_mapper"

    id = Column(GUID, ForeignKey('countries.id'), primary_key=True)
    remote_id = Column(String, nullable=False, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), primary_key=True)

    supplier = relationship('Suppliers', backref=backref('countries'))

    def __repr__(self):
        return "<CountryMap(local={}, remote={}, supplier={})>".format(
            self.id, self.remote_id, self.supplier.name)


class CompetitionMap(BaseSchema):
    __tablename__ = "competition_mapper"

    id = Column(GUID, ForeignKey('competitions.id'), primary_key=True)
    remote_id = Column(String, nullable=False, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), primary_key=True)

    supplier = relationship('Suppliers', backref=backref('competitions'))

    def __repr__(self):
        return "<CompetitionMap(local={}, remote={}, supplier={})>".format(
            self.id, self.remote_id, self.supplier.name)


class SeasonMap(BaseSchema):
    __tablename__ = "season_mapper"

    id = Column(Integer, ForeignKey('seasons.id'), primary_key=True)
    remote_id = Column(String, nullable=False, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), primary_key=True)

    supplier = relationship('Suppliers', backref=backref('seasons'))

    def __repr__(self):
        return "<SeasonMap(local={}, remote={}, supplier={})>".format(
            self.id, self.remote_id, self.supplier.name)


class VenueMap(BaseSchema):
    __tablename__ = "venue_mapper"

    id = Column(GUID, ForeignKey('venues.id'), primary_key=True)
    remote_id = Column(String, nullable=False, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), primary_key=True)

    supplier = relationship('Suppliers', backref=backref('venues'))

    def __repr__(self):
        return "<VenueMap(local={}, remote={}, supplier={})>".format(
            self.id, self.remote_id, self.supplier.name)


class PlayerMap(BaseSchema):
    __tablename__ = "player_mapper"

    id = Column(GUID, ForeignKey('players.id'), primary_key=True)
    remote_id = Column(String, nullable=False, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), primary_key=True)

    supplier = relationship('Suppliers', backref=backref('players'))

    def __repr__(self):
        return "<PlayerMap(local={}, remote={}, supplier={})>".format(
            self.id, self.remote_id, self.supplier.name)


class ManagerMap(BaseSchema):
    __tablename__ = "manager_mapper"

    id = Column(GUID, ForeignKey('managers.id'), primary_key=True)
    remote_id = Column(String, nullable=False, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), primary_key=True)

    supplier = relationship('Suppliers', backref=backref('managers'))

    def __repr__(self):
        return "<ManagerMap(local={}, remote={}, supplier={})>".format(
            self.id, self.remote_id, self.supplier.name)


class RefereeMap(BaseSchema):
    __tablename__ = "referee_mapper"

    id = Column(GUID, ForeignKey('referees.id'), primary_key=True)
    remote_id = Column(String, nullable=False, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), primary_key=True)

    supplier = relationship('Suppliers', backref=backref('referees'))

    def __repr__(self):
        return "<RefereeMap(local={}, remote={}, supplier={})>".format(
            self.id, self.remote_id, self.supplier.name)


class PositionMap(BaseSchema):
    __tablename__ = "position_mapper"

    id = Column(Integer, ForeignKey('positions.id'), primary_key=True)
    remote_id = Column(String, nullable=False, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), primary_key=True)

    supplier = relationship('Suppliers', backref=backref('positions'))

    def __repr__(self):
        return "<PositionMap(local={}, remote={}, supplier={})>".format(
            self.id, self.remote_id, self.supplier.name)


class MatchMap(BaseSchema):
    __tablename__ = "match_mapper"

    id = Column(GUID, ForeignKey('matches.id'), primary_key=True)
    remote_id = Column(String, nullable=False, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), primary_key=True)

    supplier = relationship('Suppliers', backref=backref('matches'))

    def __repr__(self):
        return "<MatchMap(local={}, remote={}, supplier={})>".format(
            self.id, self.remote_id, self.supplier.name)


class MatchEventMap(BaseSchema):
    __tablename__ = "event_mapper"

    id = Column(GUID, ForeignKey('match_events.id'), primary_key=True)
    remote_id = Column(String, nullable=False, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), primary_key=True)

    supplier = relationship('Suppliers', backref=backref('match_events'))

    def __repr__(self):
        return "<MatchEventMap(local={}, remote={}, supplier={})>".format(
            self.id, self.remote_id, self.supplier.name)


class ActionMap(BaseSchema):
    __tablename__ = "action_type_mapper"

    id = Column(enums.ActionType.db_type(), primary_key=True)
    remote_id = Column(String, nullable=False, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), primary_key=True)

    supplier = relationship('Suppliers', backref=backref('actions'))

    def __repr__(self):
        return "<MatchActionMap(local={}, remote={}, supplier={})>".format(
            self.id, self.remote_id, self.supplier.name)


class ModifierMap(BaseSchema):
    __tablename__ = "modifier_type_mapper"

    id = Column(Integer, ForeignKey('modifiers.id'), primary_key=True)
    remote_id = Column(String, nullable=False, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), primary_key=True)

    supplier = relationship('Suppliers', backref=backref('modifiers'))

    def __repr__(self):
        return "<ModifierMap(local={}, remote={}, supplier={})>".format(
            self.id, self.remote_id, self.supplier.name)
