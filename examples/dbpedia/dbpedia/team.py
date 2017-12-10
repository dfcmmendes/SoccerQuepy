#Web Semantics 2017/2018

#Soccer team related class
#University of Coimbra
#Authors:   Daniel  Mendes  <dfmendes@student.dei.uc.pt>
#           Pedro   Silva   <@student.dei.uc.pt>

from refo import Plus, Question
from quepy.dsl import HasKeyword
from quepy.parsing import Lemma, Lemmas, Pos, QuestionTemplate, Particle
from dsl import IsTeam, IsManager, ManagerOf, IsPerson, NameOf, IsLeague, HasName, MostSuccessfulOf, ChairmanOf, IsPlace, GroundOf

nouns = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))

class Team(Particle):
    regex = Question(Pos("DT")) + nouns
    def interpret(self, match):
        name = match.words.tokens
        return IsTeam() + HasName(name)

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

class ChairmanOfQuestion(QuestionTemplate):
    regex = ((Lemmas("who")+ Lemma("be") + Pos("DT") + Lemma("chairman") +
              Pos("of") + Team()) |
             (Lemma("who") + Lemma("be")  + Team())) + Lemma("chairman") + \
            Question(Pos("."))

    def interpret(self, match):
        chairman = IsPerson() + ChairmanOf(match.team)
        chairman_name = NameOf(chairman)
        return chairman_name, "literal"

class GroundOfQuestion(QuestionTemplate):
    regex = ((Lemmas("which")+ Lemma("be") + Pos("DT") + Lemma("ground") +
              Lemma("of") + Team()) |
             (Lemma("which") + Lemma("be")  + Team())) + Lemma("ground") + \
            Question(Pos("."))

    def interpret(self, match):
        ground = IsPlace() + GroundOf(match.team)
        ground_name = NameOf(ground)
        return ground_name, "literal"

class ManagerOfQuestion(QuestionTemplate):
    """
    Ex: "Who is the manager of Real Madrid?"
        "who manages Manchester United?"
    """

    regex = ((Lemmas("who be") + Pos("DT") + Lemma("manager") +
             Pos("of") + Team()) |
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

    regex = ((Lemmas("who win") + Lemma("more") +
             Pos("of") + League()) |
             (Lemma("who") + Lemma("win") + Lemma("more") + League() + Lemma("title"))) + \
            Question(Pos("."))

    def interpret(self, match):
        team = IsTeam() + MostSuccessfulOf(match.league)
        team_name = NameOf(team)
        return team_name, "literal"

