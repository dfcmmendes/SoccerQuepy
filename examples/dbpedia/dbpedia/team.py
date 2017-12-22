#Web Semantics 2017/2018

#Soccer team related class
#University of Coimbra
#Authors:   Daniel  Mendes  <dfmendes@student.dei.uc.pt>
#           Pedro   Silva   <ptsilva@student.dei.uc.pt>

from refo import Plus, Question
from quepy.dsl import HasKeyword
from quepy.parsing import Lemma, Lemmas, Pos, QuestionTemplate, Particle, Token
from dsl import IsTeam, IsManager, ManagerOf, FormationDateOf, LeagueOf, IsPerson, NameOf, CapOf, IsLeague, IsCountry, IsCountryLeagueOf, HasName, MostSuccessfulOf, ChairmanOf, GroundOf, IsStadium, \
    LabelOf, IsCareerStation, IsTeamOf, HasYear, IsCareerStationOf



nouns = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))
numbers = Plus(Pos("CD"))

class Team(Particle):
    regex = Question(Pos("DT")) + nouns
    def interpret(self, match):
        name = match.words.tokens
        return IsTeam() + HasName(name)

class Year(Particle):
    regex = numbers
    def interpret(self, match):
        year = match.words.tokens
        return year

class Manager(Particle):
    regex = nouns

    def interpret(self, match):
        name = match.words.tokens
        return IsManager() + HasKeyword(name)


class League(Particle):
    regex = nouns

    def interpret(self, match):
        name = match.words.tokens
        return IsLeague() + HasKeyword(name)


class Country(Particle):
    regex = nouns

    def interpret(self, match):
        name = match.words.tokens
        return IsCountry() + HasKeyword(name)


class ChairmanOfQuestion(QuestionTemplate):
    """
        Regex for questions about club chairman.
        Ex: "Who is the chairman of Barcelona?"
            "Who is Porto chairman?"
            "Who is Porto boss?"
        """
    regex = ((Lemmas("who")+ Lemma("be") + Pos("DT") + Lemma("chairman") +
              Pos("of") + Team()) |
             (Lemma("who") + Lemma("be")  + Team())) + Lemma("chairman") + \
            Question(Pos(".")) | (Lemma("who") + Lemma("be")  + Team()) + Lemma("boss") + \
            Question(Pos("."))

    def interpret(self, match):
        chairman = IsPerson() + ChairmanOf(match.team)
        chairman_name = NameOf(chairman)
        return chairman_name, "literal"


class GroundOfQuestion(QuestionTemplate):
    """
        Regex for questions about club grounds.
        Ex: "Which is the ground of Barcelona?"
            "Which is the stadium of Porto?"
        """

    opening = Lemma("which") + Token("is")

    regex1 = opening + Pos("DT") + Lemma("ground") + Pos("IN") + \
        Question(Pos("DT")) + Team()

    regex2 = opening + Pos("DT") + Lemma("stadium") + Pos("IN") + \
        Question(Pos("DT")) + Team()

    regex = (regex1 | regex2) + Question(Pos("."))

    def interpret(self, match):
        ground = IsStadium() + GroundOf(match.team)
        ground_name = NameOf(ground)
        return ground_name, "literal"


class WhoPlayedIn(QuestionTemplate):
    """
        Regex for questions about players of a teamr.
        Ex: "Real Madrid players"
            "What are the players of Manchester United?"
        """

    #^^<http://www.w3.org/2001/XMLSchema#gYear>

    regex1 = Team() + Lemma("player")
    regex2 = Lemma("member") + Pos("IN") + Team()
    regex3 = Pos("WP") + Lemma("be") + Pos("DT") + Lemma("player") + \
             Pos("IN") + Team()

    regex = (regex1 | regex2 | regex3) + Question(Pos("."))

    def interpret(self, match):
        member = IsCareerStation() + IsTeamOf(match.team)
        label = LabelOf(member)
        return label, "enum"


class ManagerOfQuestion(QuestionTemplate):
    """
    Ex: "Who is the manager of Real Madrid?"
        "who manages Manchester United?"
        "Who is the coach of Porto"
        "who coach Porto?"
    """

    regex = ((Lemmas("who be") + Pos("DT") + Lemma("manager") + Pos("of") + Team()) |
             (Lemma("who") + Lemma("coach") + Team()) |
             (Lemma("who be") + Pos("DT") + Lemma("coach") + Lemma("of") + Team()) |
             (Lemma("who") + Lemma("manage") + Team())) + \
            Question(Pos("."))

    def interpret(self, match):
        manager = IsPerson() + ManagerOf(match.team)
        manager_name = NameOf(manager)
        return manager_name, "literal"


class MostWinsQuestion(QuestionTemplate):
    """
    Ex: "Who won more La Liga?"
    """

    regex = ((Lemmas("who win") + Lemma("more") + Pos("of") + League()) |
             (Lemma("who") + Lemma("win") + Lemma("more") + League() + Lemma("title"))) + \
            Question(Pos("."))

    def interpret(self, match):
        team = IsTeam() + MostSuccessfulOf(match.league)
        team_name = NameOf(team)
        return team_name, "literal"


class MostWinsQuestionCountry(QuestionTemplate):
    """
    Ex: "Who won more in Spain?"
        "Who won more Spain titles?"
    """

    regex = ((Lemmas("who win") + Lemma("more") + Lemma("in") + Country()) |
             (Lemmas("who win") + Lemma("more") + Country() + Lemma("title"))) + \
            Question(Pos("."))

    def interpret(self, match):
        league = IsLeague() + IsCountryLeagueOf(match.country)
        team = IsTeam() + MostSuccessfulOf(league)
        team_name = NameOf(team)
        return team_name, "literal"


class ClubGroundCapacity(QuestionTemplate):
    """
    Ex: "What is the ground capacity of Barcelona?"
        "What is Porto stadium capacity?"
    """

    regex = ((Pos("WP") + Lemma("be") + Pos("DT") + Lemma("ground") + Lemma("capacity") + Lemma("of") + Team()) |
              Pos("WP") + Lemma("be") + Team() + Lemma("stadium") + Lemma("capacity")) + \
            Question(Pos("."))

    def interpret(self, match):
        cap = CapOf(match.team)
        return cap, ("literal", "{} seats")


class ClubPlayingLeague(QuestionTemplate):
    """
    Ex: "What is the league of Barcelona?"
        "What is Porto league?"
    """

    regex = ((Pos("WP") + Lemma("be") + Pos("DT") + Lemma("league") + Lemma("of") + Team()) |
              Pos("WP") + Lemma("be") + Team() + Lemma("league")) + \
            Question(Pos("."))

    def interpret(self, match):
        cap = LeagueOf(match.team)
        return cap, "literal"


class ClubFormationDate(QuestionTemplate):
    """
    Ex: "What is the formation date of Barcelona?"
        "What is Porto foundation date?"
    """

    regex = ((Pos("WP") + Lemma("be") + Pos("DT") + Lemma("formation") + Lemma("date") + Lemma("of") + Team() |
              Pos("WP") + Lemma("be") + Team() + Lemma("foundation") + Lemma("date"))) + \
            Question(Pos("."))

    def interpret(self, match):
        formationDate = FormationDateOf(match.team)
        return formationDate, "literal"

class WhoPlayedIn(QuestionTemplate):
    """
        Regex for questions about players of a teamr.
        Ex: "Real Madrid players"
            "What are the players of Manchester United?"
        """

    #^^<http://www.w3.org/2001/XMLSchema#gYear>

    regex1 = Team() + Lemma("player")
    regex2 = Lemma("member") + Pos("IN") + Team()
    regex3 = Pos("WP") + Lemma("be") + Pos("DT") + Lemma("player") + \
             Pos("IN") + Team() + Year()

    regex = (regex1 | regex2 | regex3) + Question(Pos("."))

    def interpret(self, match):
        memberStation = IsCareerStation() + IsTeamOf(match.team) + HasYear(match.year)
        member = IsPerson() + IsCareerStationOf(memberStation)
        member_name = NameOf(member)
        return member_name, "enum"