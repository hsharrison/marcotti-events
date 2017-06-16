import uuid

from sqlalchemy import Column, Integer, Numeric, String, Sequence, Date, ForeignKey, Unicode, Index
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.sql.expression import cast, case

from marcottievents.models import GUID
from marcottievents.models.common import BaseSchema
import marcottievents.models.common.enums as enums


class Positions(BaseSchema):
    """
    Football player position data model.
    """
    __tablename__ = 'positions'

    id = Column(Integer, Sequence('position_id_seq', start=10), primary_key=True)
    name = Column(Unicode(20), nullable=False)
    type = Column(enums.PositionType.db_type())

    def __repr__(self):
        return "<Position(name={0}, type={1})>".format(self.name, self.type.value)


class Persons(BaseSchema):
    """
    Persons common data model.   This model is subclassed by other Personnel data marcottievents.models.
    """
    __tablename__ = 'persons'

    person_id = Column(GUID, primary_key=True, default=uuid.uuid4)
    first_name = Column(Unicode(40), nullable=False)
    known_first_name = Column(Unicode(40))
    middle_name = Column(Unicode(40))
    last_name = Column(Unicode(40), nullable=False)
    second_last_name = Column(Unicode(40))
    nick_name = Column(Unicode(40))
    birth_date = Column(Date)
    order = Column(enums.NameOrderType.db_type(), default=enums.NameOrderType.western)
    type = Column(String)

    country_id = Column(GUID, ForeignKey('countries.id'))
    country = relationship('Countries', backref=backref('persons'))

    Index('persons_indx', 'first_name', 'middle_name', 'last_name', 'nick_name')

    __mapper_args__ = {
        'polymorphic_identity': 'persons',
        'polymorphic_on': type
    }

    @hybrid_property
    def full_name(self):
        """
        The person's commonly known full name, following naming order conventions.

        If a person has a nickname, that name becomes the person's full name.

        If a person has an alternate first name by which he/she is otherwise known, that name
        becomes part of the full name.

        :return: Person's full name.
        """
        if all([self.nick_name is not None, self.nick_name != '']):
            return self.nick_name
        else:
            if self.order == enums.NameOrderType.western:
                return "{} {}".format(self.known_first_name or self.first_name, self.last_name)
            elif self.order == enums.NameOrderType.middle:
                return "{} {} {}".format(self.known_first_name or self.first_name,
                                          self.middle_name, self.last_name)
            elif self.order == enums.NameOrderType.eastern:
                return "{} {}".format(self.last_name, self.first_name)

    @full_name.expression
    def full_name(cls):
        """
        The person's commonly known full name, following naming order conventions.

        If a person has a nickname, that name becomes the person's full name.

        If a person has an alternate first name by which he/she is otherwise known, that name
        becomes part of the full name.

        :return: Person's full name.
        """
        return case(
            [(cls.nick_name != None, cls.nick_name)],
            else_=case(
                [
                    (cls.order == enums.NameOrderType.middle,
                     case([(cls.known_first_name != None, cls.known_first_name)], else_=cls.first_name) +
                     ' ' + cls.middle_name + ' ' + cls.last_name),
                    (cls.order == enums.NameOrderType.eastern, cls.last_name + ' ' + cls.first_name)
                ],
                else_=case(
                    [(cls.known_first_name != None, cls.known_first_name)],
                    else_=cls.first_name) + ' ' + cls.last_name))

    @hybrid_property
    def official_name(self):
        """
        The person's legal name, following naming order conventions and with middle names included.

        :return: Person's legal name.
        """
        if self.order == enums.NameOrderType.eastern:
            return "{} {}".format(self.last_name, self.first_name)
        else:
            return " ".join([getattr(self, field) for field in
                              ['first_name', 'middle_name', 'last_name', 'second_last_name']
                              if getattr(self, field) is not None])

    @official_name.expression
    def official_name(cls):
        """
        The person's legal name, following naming order conventions and with middle names included.

        :return: Person's legal name.
        """
        return case(
            [(cls.order == enums.NameOrderType.eastern, cls.last_name + ' ' + cls.first_name)],
            else_=(
                case([cls.first_name != None, cls.first_name + ' '], else_='') +
                case([cls.middle_name != None, cls.middle_name + ' '], else_='') +
                case([cls.last_name != None, cls.last_name + ' '], else_='') +
                case([cls.second_last_name != None, cls.second_last_name], else_=''))
        )

    @hybrid_method
    def exact_age(self, reference):
        """
        Player's exact age (years + days) relative to a reference date.

        :param reference: Date object of reference date.
        :return: Player's age expressed as a (Year, day) tuple
        """
        delta = reference - self.birth_date
        years = int(delta.days/365.25)
        days = int(delta.days - years*365.25 + 0.5)
        return years, days

    @hybrid_method
    def age(self, reference):
        """
        Player's age relative to a reference date.

        :param reference: Date object of reference date.
        :return: Integer value of player's age.
        """
        delta = reference - self.birth_date
        return int(delta.days/365.25)

    @age.expression
    def age(cls, reference):
        """
        Person's age relative to a reference date.

        :param reference: Date object of reference date.
        :return: Integer value of person's age.
        """
        return cast((reference - cls.birth_date)/365.25 - 0.5, Integer)

    def __repr__(self):
        return "<Person(name={}, country={}, DOB={})>".format(
            self.full_name, self.country.name, self.birth_date.isoformat()).encode('utf-8')


class Players(Persons):
    """
    Players data model.

    Inherits Persons model.
    """
    __tablename__ = 'players'
    __mapper_args__ = {'polymorphic_identity': 'players'}

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    person_id = Column(GUID, ForeignKey('persons.person_id'))

    position_id = Column(Integer, ForeignKey('positions.id'))
    position = relationship('Positions', backref=backref('players'))

    def __repr__(self):
        return "<Player(name={}, DOB={}, country={}, position={})>".format(
            self.full_name, self.birth_date.isoformat(), self.country.name, self.position.name).encode('utf-8')

    def __unicode__(self):
        return "<Player(name={}, DOB={}, country={}, position={})>".format(
            self.full_name, self.birth_date.isoformat(), self.country.name, self.position.name)


class PlayerHistory(BaseSchema):
    """
    Player physical history data model.
    """
    __tablename__ = 'player_histories'

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    player_id = Column(GUID, ForeignKey('players.id'))
    date = Column(Date, doc="Effective date of player physical record")
    height = Column(Numeric(3, 2), CheckConstraint('height >= 0 AND height <= 2.50'), nullable=False,
                    doc="Height of player in meters")
    weight = Column(Numeric(3, 0), CheckConstraint('weight >= 0 AND weight <= 150'), nullable=False,
                    doc="Weight of player in kilograms")

    player = relationship('Players', backref=backref('history'))

    def __repr__(self):
        return "<PlayerHistory(name={}, date={}, height={:.2f}, weight={:d})>".format(
            self.player.full_name, self.date.isoformat(), self.height, self.weight).encode('utf-8')

    def __unicode__(self):
        return "<PlayerHistory(name={}, date={}, height={:.2f}, weight={:d})>".format(
            self.player.full_name, self.date.isoformat(), self.height, self.weight)


class Managers(Persons):
    """
    Managers data model.

    Inherits Persons model.
    """
    __tablename__ = 'managers'
    __mapper_args__ = {'polymorphic_identity': 'managers'}

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    person_id = Column(GUID, ForeignKey('persons.person_id'))

    def __repr__(self):
        return "<Manager(name={}, DOB={}, country={})>".format(
            self.full_name, self.birth_date.isoformat(), self.country.name).decode('utf-8')

    def __unicode__(self):
        return "<Manager(name={}, DOB={}, country={})>".format(
            self.full_name, self.birth_date.isoformat(), self.country.name)


class Referees(Persons):
    """
    Referees data model.

    Inherits Persons model.
    """
    __tablename__ = 'referees'
    __mapper_args__ = {'polymorphic_identity': 'referees'}

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    person_id = Column(GUID, ForeignKey('persons.person_id'))

    def __repr__(self):
        return "<Referee(name={}, DOB={}, country={})>".format(
            self.full_name, self.birth_date.isoformat(), self.country.name).encode('utf-8')

    def __unicode__(self):
        return "<Referee(name={}, DOB={}, country={})>".format(
            self.full_name, self.birth_date.isoformat(), self.country.name)
