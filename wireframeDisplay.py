import numpy as np
import wireframe
import pygame, math

key_to_function = {
    pygame.K_LEFT:   (lambda x: x.translate(np.array([-10,  0, 0]))),
    pygame.K_RIGHT:  (lambda x: x.translate(np.array([ 10,  0, 0]))),
    pygame.K_UP:     (lambda x: x.translate(np.array([  0,-10, 0]))),
    pygame.K_DOWN:   (lambda x: x.translate(np.array([  0, 10, 0]))),
    pygame.K_EQUALS: (lambda x: x.scale(1.25)),
    pygame.K_MINUS:  (lambda x: x.scale(0.8))}

class WireframeViewer(wireframe.WireframeGroup):
    """ A group of wireframes which can be displayed on a Pygame screen """
    
    def __init__(self, width, height, name="Wireframe Viewer"):
        self.width = width
        self.height = height
        
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(name)
        
        self.wireframes = {}
        self.wireframe_colours = {}
        
        self.displayNodes = False
        self.displayEdges = True
        
        self.background = (10,10,50)
        self.nodeColour = (250,250,250)
        self.nodeRadius = 4
    
    def addWireframe(self, name, wireframe):
        self.wireframes[name] = wireframe  
        self.wireframe_colours[name] = (250,250,250)
    
    def addWireframeGroup(self, wireframe_group):
        # Potential danger of overwriting names
        for name, wireframe in wireframe_group.wireframes.items():
            self.addWireframe(name, wireframe)
    
    def scale(self, scale):
        """ Scale wireframes in all directions from the centre of the group. """
        
        for wireframe in self.wireframes.values():
            wireframe.scale(scale, self.width/2, self.height/2, 0)

    def display(self):
        self.screen.fill(self.background)
        
        for name, wireframe in self.wireframes.items():
            colour = self.wireframe_colours.get(name)
            if colour:
                for edge in wireframe.edges:
                    pygame.draw.aaline(self.screen, colour, (edge.start[0], edge.start[1]), (edge.stop[0], edge.stop[1]), 1)
            
            if self.displayNodes:
                for node in wireframe.nodes:
                    pygame.draw.circle(self.screen, colour, (int(node[0]), int(node[y])), self.nodeRadius, 0)
        
        pygame.display.flip()

    def keyEvent(self, key):
        if key in key_to_function:
            key_to_function[key](self)

    def run(self):
        """ Display wireframe on screen and respond to keydown events """
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.keyEvent(event.key)
            
            self.display()