import pygame


class Ballot(object):
    def __init__(self, position, ballot_img):
        self.ballot_image = pygame.image.load(ballot_img).convert_alpha()
        self.envelope_image = pygame.image.load("assets/img/envelope.png")
        self.votes = 0
        self.position = position
        self.pendingVotes = []

    def add_votes(self, nbvotes):
        for i in range(nbvotes):
            self.pendingVotes.append(
                Vote(
                    self.envelope_image,
                    [
                        self.position[0] + ((self.ballot_image.get_size()[0] - self.envelope_image.get_size()[0]) // 2),
                        self.position[1] - 50 - (2 * i)
                    ],
                    self.position[1] + (self.ballot_image.get_size()[1] // 2)
                )
            )

    def update(self, screen):
        for vote in self.pendingVotes[:]:
            if vote.update(screen.timeElapsed):
                self.votes += 1
                del self.pendingVotes[self.pendingVotes.index(vote)]

    def draw(self, screen):
        votes_img = screen.fonts["25"].render(str(self.votes), 1, (0, 0, 0))
        screen.blit(self.ballot_image, self.position)
        vote_pos = (
            self.position[0] + ((self.ballot_image.get_size()[0] - votes_img.get_size()[0]) // 2),
            self.position[1] + ((self.ballot_image.get_size()[1] - votes_img.get_size()[1]) // 2)
        )
        screen.blit(votes_img, vote_pos)
        for vote in self.pendingVotes:
            vote.draw(screen)
