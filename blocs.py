"""
Module gerant les differentes sortes de blocs pouvant etre affiches a l'ecran
"""
# TODO :
#   - tomber
#   - collisions
#   - pousser pierres
#   - porte
#   - animations
#   - son
#   - menu
#   - score
#   - temps limite
#   - niveaux predefinis
#   - editeur de niveaux
#   - generateur de niveaux automatique
#   - mechants


from constantes import *
from numpy import array


# class Coordonnees(list):
#     def __init__(self, x, y):
#         super(Coordonnees, self).__init__([x, y])
#
#     @property
#     def x(self):
#         return self[0]
#
#     @x.setter
#     def x(self, valeur):
#         self[0] = valeur
#
#     @x.deleter
#     def x(self):
#         raise AttributeError("L'attribut ne peut pas etre supprime.")
#
#     @property
#     def y(self):
#         return self[1]
#
#     @y.setter
#     def y(self, valeur):
#         self[1] = valeur
#
#     @y.deleter
#     def y(self):
#         raise AttributeError("L'attribut ne peut pas etre supprime.")
#
#     def __mul__(self, autre):
#         return Coordonnees(self.x * autre, self.y * autre)
#
#     def __div__(self, autre):
#         return Coordonnees(self.x / autre, self.y / autre)


class Rectangle(pygame.Rect):
    """
    Classe permettant d'avoir des rectangles pouvant etre utilises comme cle de dictionnaire.
    """
    def __init__(self, *args, **kwargs):
        arguments = []
        if len(kwargs) != 0:
            if "left" in kwargs.keys():
                arguments.append(kwargs["left"])
            if "top" in kwargs.keys():
                arguments.append(kwargs["top"])
            if "width" in kwargs.keys():
                arguments.append(kwargs["width"])
            if "height" in kwargs.keys():
                arguments.append(kwargs["height"])
        super(Rectangle, self).__init__(*(args + tuple(arguments)))

    def __eq__(self, autre):
        return (self.x == autre.x and self.y == autre.y and self.width == autre.width and
                self.height == autre.height)

    def __hash__(self):
        """
        Permet de donner une identification unique a chaque rectangle
        :return: hash
        """
        arguments = (self.x, self.y, self.width, self.height)
        return hash(arguments)


class Bloc(pygame.sprite.Sprite):  # Pas besoin d'heriter d'"object", car "pygame.sprite.Sprite" est une classe de nouveau style
    """
    Classe de base pour tous les blocs.
    """
    BOUGEABLE = False

    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)  # On appelle le constructeur de la classe mere
        image = IMAGES[self.__class__.__name__]
        self.image = pygame.transform.scale(image, (rect.width, rect.height))
        self.rect = self.image.get_rect()
        self.rect.x = rect.x
        self.rect.y = rect.y
        self.ancien_rect = self.rect.copy()
        self.z = 0
        self.a_deja_bouge = False
        self.orientation = ORIENTATIONS.DROITE
        self.est_mort = False
        self.doit_bouger = False

    @property
    def rect_hashable(self):
        """
        Permet d'utiliser le rectangle comme cle de dictionnaire.

        :return: Copie de self.rect, mais hashable.
        """
        return Rectangle(self.rect)

    @rect_hashable.setter
    def rect_hashable(self, nouveau):
        raise AttributeError("Le rectangle hashable n'est pas modifiable, utiliser l'attribut \"rect\" a la place.")

    @rect_hashable.deleter
    def rect_hashable(self):
        raise AttributeError("L'attribut ne peut pas etre supprime.")

    def actualiser(self):
        pass
    # TODO : gerer les autres actions (comme tomber)

    def terminer_cycle(self):
        self.a_deja_bouge = False

    def bouger(self, direction):
        """
            Fait bouger le personnage dans la direction "direction".

            :param direction: direction dans laquelle avancer
            :return: "None"
            """
        self.orientation = direction

    # def revenir(self):
    #     """
    #     Annule le dernier mouvement du personnage.
    #
    #     :return: "None"
    #     """
    #     self.rect.x, self.rect.y = self.ancien_rect.x, self.ancien_rect.y

    def tuer(self):
        """
        Methode appelee lorsque le bloc se fait tuer.

        :return: "None"
        """
        self.est_mort = True  # TODO : ajouter une animation pour chaque type de bloc


class Personnage(Bloc):
    """
    Classe permettant de representer un personnage.
    """
    BOUGEABLE = True

    def __init__(self, rect):
        super(Personnage, self).__init__(rect)
        self.est_mort = False
        self.orientation = ORIENTATIONS.DROITE
        self.etait_en_mouvement = False
        self.diamants_ramasses = 0
        self.terre_creusee = 0
        self.caillou_pousse = None

    # def collision(self, groupe):
    #     """
    #     Methode gerant les collisions entre le personnage et les autres blocs.
    #
    #     :param groupe: groupe de blocs potentiellement collisionnes
    #     :return: "None"
    #     """
    #     est_revenu = False
    #     blocs = self.blocs_collisionnes(groupe)  # cherches les blocs qui sont en collision avec le personnage
    #     for bloc in blocs:
    #         type_de_bloc = bloc.__class__
    #         if type_de_bloc == Caillou:
    #             succes = self.pousser_caillou(bloc, groupe)
    #             if not succes:
    #                 self.revenir()
    #                 est_revenu = True
    #         elif type_de_bloc == Terre:
    #             self.creuser_terre(bloc)
    #         elif type_de_bloc == Mur:
    #             self.revenir()
    #             est_revenu = True
    #         elif type_de_bloc == Diamant:
    #             self.ramasser_diamant(bloc)
    #         elif type_de_bloc == Porte:
    #             if not bloc.est_activee:
    #                 self.revenir()
    #                 est_revenu = True
    #     return est_revenu

    def creuser_terre(self, terre):
        terre.tuer()
        self.terre_creusee += 1

    def ramasser_diamant(self, diamant):
        diamant.tuer()
        self.diamants_ramasses += 1

    def pousser(self, caillou, direction):
        caillou.etre_pousse()
        self.bouger(direction)

    def bouger(self, direction):
        super(Personnage, self).bouger(direction)

    def tuer(self):
        super(Personnage, self).tuer()
        print("mort")


class Terre(Bloc):
    """
    Classe permettant de representer de la terre.
    """


class BlocTombant(Bloc):
    """
    Classe permettant de gerer les blocs qui tombent (caillou et diamant)
    """
    BOUGEABLE = True

    def __init__(self, rect):
        super(BlocTombant, self).__init__(rect)
        self.tombe = False

    # def actualiser(self):
    #     Bloc.actualiser(self)
    #     self.tomber()

    # def revenir(self):
    #     Bloc.revenir(self)

    # def collision(self, groupe):
    #     blocs = self.blocs_collisionnes(groupe)  # cherches les blocs qui sont en collision avec le caillou
    #     if len(blocs) != 0:
    #         for bloc in blocs:
    #             type_de_bloc = bloc.__class__
    #             if type_de_bloc in (Caillou, Diamant, Entree, Sortie):
    #                 pass
    #             elif type_de_bloc == Personnage:
    #                 if self.tombe:
    #                     bloc.tuer()
    #         self.revenir()
    #         est_revenu = True
    #     else:
    #         est_revenu = False
    #     return est_revenu

    def tomber(self):
        self.tombe = True


class Caillou(BlocTombant):
    """
    Classe permettant de representer un caillou.
    """
    def __init__(self, rect):
        super(Caillou, self).__init__(rect)
        self.coups_avant_etre_pousse = None
        self.est_pousse = False

    def bouger(self, direction):
        super(Caillou, self).bouger(direction)

    def etre_pousse(self):
        self.est_pousse = True
        if self.coups_avant_etre_pousse is None:
            self.coups_avant_etre_pousse = 1
        elif self.coups_avant_etre_pousse > 0:
            self.coups_avant_etre_pousse -= 1

    def terminer_cycle(self):
        super(Caillou, self).terminer_cycle()
        if not self.est_pousse:
            self.coups_avant_etre_pousse = None
        self.est_pousse = False


class Diamant(BlocTombant):
    """
    Classe permettant de representer un diamant.
    """
    def __init__(self, rect):
        super(Diamant, self).__init__(rect)


class Mur(Bloc):
    """
    Classe permetant de representer un bout de mur.
    """


class Porte(Bloc):
    """
    Classe permettant de representer une porte de maniere generique.
    """
    def __init__(self, rect):
        super(Porte, self).__init__(rect)
        self._est_activee = False

    @property
    def est_activee(self):
        """
        Propriete permettant de savoir si la porte est activee.

        :return: booleen indiquant si la porte est activee
        """
        return self._est_activee

    @est_activee.setter
    def est_activee(self, activee):
        activation = not self._est_activee and activee
        desactivation = self._est_activee and not activee
        self._est_activee = activee
        if activation:
            pass
        elif desactivation:
            pass
        # TODO : ajouter animation de changement d'etat

    def activer(self):
        """
        Methode de convenance permettant d'activer la porte.

        :return: "None"
        """
        self.est_activee = True

    def desactiver(self):
        """
        Methode de convenance permettant de desactiver la porte.

        :return: "None"
        """
        self.est_activee = False


class Entree(Porte):
    """
    Classe permettant de representer une porte d'entree.
    """
    def __init__(self, rect):
        super(Entree, self).__init__(rect)
        self.est_activee = True


class Sortie(Porte):
    """
    Classe permettant de representer une porte de sortie.
    """
    def __init__(self, rect):
        super(Sortie, self).__init__(rect)
        self.est_activee = False
