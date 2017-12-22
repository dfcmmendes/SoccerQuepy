# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Domain specific language for DBpedia quepy.
"""

from quepy.dsl import FixedType, HasKeyword, FixedRelation, FixedDataRelation
from quepy.expression import Expression
from quepy.encodingpolicy import encoding_flexible_conversion

# Setup the Keywords for this application
HasKeyword.relation = "rdfs:label"
HasKeyword.language = "en"

class IsPerson(FixedType):
    fixedtype = "foaf:Person"


class IsPlace(FixedType):
    fixedtype = "dbpedia:Place"


class IsCountry(FixedType):
    fixedtype = "dbo:Country"


class IsPopulatedPlace(FixedType):
    fixedtype = "dbpedia-owl:PopulatedPlace"


class IsBand(FixedType):
    fixedtype = "dbpedia-owl:Band"


class IsAlbum(FixedType):
    fixedtype = "dbpedia-owl:Album"


class IsTvShow(FixedType):
    fixedtype = "dbpedia-owl:TelevisionShow"


class IsMovie(FixedType):
    fixedtype = "dbpedia-owl:Film"


class HasShowName(FixedDataRelation):
    relation = "dbpprop:showName"
    language = "en"


class HasName(FixedDataRelation):
    relation = "foaf:name"
    language = "en"

class HasShortName(FixedDataRelation):
    relation = "dbp:shortName"

class DefinitionOf(FixedRelation):
    relation = "rdfs:comment"
    reverse = True


class LabelOf(FixedRelation):
    relation = "rdfs:label"
    reverse = True


class UTCof(FixedRelation):
    relation = "dbpprop:utcOffset"
    reverse = True


class PresidentOf(FixedRelation):
    relation = "dbpprop:leaderTitle"
    reverse = True


class IncumbentOf(FixedRelation):
    relation = "dbpprop:incumbent"
    reverse = True


class CapitalOf(FixedRelation):
    relation = "dbpedia-owl:capital"
    reverse = True


class LanguageOf(FixedRelation):
    relation = "dbpprop:officialLanguages"
    reverse = True


class PopulationOf(FixedRelation):
    relation = "dbpprop:populationCensus"
    reverse = True


class IsMemberOf(FixedRelation):
    relation = "dbpedia-owl:bandMember"
    reverse = True


class ActiveYears(FixedRelation):
    relation = "dbpprop:yearsActive"
    reverse = True


class MusicGenreOf(FixedRelation):
    relation = "dbpedia-owl:genre"
    reverse = True


class ProducedBy(FixedRelation):
    relation = "dbpedia-owl:producer"


class BirthDateOf(FixedRelation):
    relation = "dbpprop:birthDate"
    reverse = True


class BirthPlaceOf(FixedRelation):
    relation = "dbpedia-owl:birthPlace"
    reverse = True


class ReleaseDateOf(FixedRelation):
    relation = "dbpedia-owl:releaseDate"
    reverse = True


class StarsIn(FixedRelation):
    relation = "dbpprop:starring"
    reverse = True


class NumberOfEpisodesIn(FixedRelation):
    relation = "dbpedia-owl:numberOfEpisodes"
    reverse = True


class ShowNameOf(FixedRelation):
    relation = "dbpprop:showName"
    reverse = True


class HasActor(FixedRelation):
    relation = "dbpprop:starring"


class CreatorOf(FixedRelation):
    relation = "dbpprop:creator"
    reverse = True


class NameOf(FixedRelation):
    relation = "foaf:name"
    # relation = "dbpprop:name"
    reverse = True


class DirectedBy(FixedRelation):
    relation = "dbpedia-owl:director"


class DirectorOf(FixedRelation):
    relation = "dbpedia-owl:director"
    reverse = True


class DurationOf(FixedRelation):
    # DBpedia throws an error if the relation it's
    # dbpedia-owl:Work/runtime so we expand the prefix
    # by giving the whole URL.
    relation = "<http://dbpedia.org/ontology/Work/runtime>"
    reverse = True


class HasAuthor(FixedRelation):
    relation = "dbpedia-owl:author"


class AuthorOf(FixedRelation):
    relation = "dbpedia-owl:author"
    reverse = True


class IsBook(FixedType):
    fixedtype = "dbpedia-owl:Book"


class LocationOf(FixedRelation):
    relation = "dbpedia-owl:location"
    reverse = True

#SOCCER
class ManagerOf(FixedRelation):
    relation = "dbo:manager"
    reverse = True

class ManagerBy(FixedRelation):
    relation = "dbo:manager"

class MostSuccessfulOf(FixedRelation):
    relation = "dbp:mostSuccessfulClub"
    reverse = True

class ChairmanOf(FixedRelation):
    relation = "dbo:chairman"
    reverse = True

class GroundOf(FixedRelation):
    relation = "dbo:ground"
    reverse = True

class IsCareerStation(FixedType):
    fixedtype ="dbo:CareerStation"

class IsTeamOf(FixedRelation):
    relation = "dbo:team"


class IsStadium(FixedType):
    fixedtype = "dbo:Stadium"

class IsTeam(FixedType):
    fixedtype = "dbo:SoccerClub"

class IsManager(FixedType):
    fixedtype = "dbo:SportsManager"

class IsLeague(FixedType):
    fixedtype = "dbo:SoccerLeague"


class IsCountryLeagueOf(FixedRelation):
    relation = "dbo:country"

class IsCareerStationOf(FixedRelation):
    relation = "dbo:careerStation"


class FixedYearRelation(Expression):
    """
    Expression for a fixed relation. This is
    "A is related to Data" through the relation defined in `relation`.
    """

    relation = "dbo:years"
    type = "http://www.w3.org/2001/XMLSchema#gYear"

    def __init__(self, data):
        super(FixedYearRelation, self).__init__()
        if self.relation is None:
            raise ValueError("You *must* define the `relation` "
                             "class attribute to use this class.")
        self.relation2 = encoding_flexible_conversion(self.relation)
        if self.type is not None:
            self.type = encoding_flexible_conversion(self.type)
            data = u"\"{0}\"^^<{1}>".format(data, self.type)
        self.add_data(self.relation, data)


class HasYear(FixedYearRelation):
    """
    Abstraction of an information retrieval key, something standarized used
    to look up things in the database.
    """
    relation = u"dbo:years"

    def __init__(self, data):
        data = self.sanitize(data)
        super(HasYear, self).__init__(data)

    @staticmethod
    def sanitize(text):
        # User can redefine this method if needed
        return text