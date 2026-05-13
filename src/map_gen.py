from asyncio.windows_events import NULL

import pygame

class MapGen(pygame.sprite.Sprite):
    def __init__(self, pos, map_graph, is_on, width=50, height=50, r=0, g=0, b=0):
        super().__init__()
        
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((r, g, b))
        self.rect = self.image.get_rect(center=pos)
        
        self.is_on = is_on
        self.map_graph = map_graph
    
    def toggle(self):
        if self.is_on == 0:
            self.is_on = 1
        else:
            self.is_on = 0 
        
        return self.is_on

    def graph_append(self, node1, node2):
        self.map_graph[node1] = node2

    def graph_remove(self, node1):
        self.map_graph[node1] = NULL

    def node_split(self):
        # Calculate half height
        half_height = self.rect.height // 2

        # Create two new rects
        image_top = pygame.Surface((self.rect.width, half_height), pygame.SRCALPHA)
        image_top.fill((0, 0, 0))
        rect_top = image_top.get_rect((0,0))

        image_buttom = pygame.Surface((self.rect.width, half_height), pygame.SRCALPHA)
        image_buttom.fill((255, 255, 255))
        rect_buttom = image_top.get_rect((half_height,0))

        # Remove the splitted rect
        self.graph_remove(self, self.rect)

        # Add the resulting 2 nodes to the graph instead
        self.graph_append(self, rect_top, rect_buttom)

# To-Do:
#     1- Every rect is a node in an undirected graph
#     2- Every "Split" produce 2 (or more) rects
#     3- Product rects are therfore new nodes in the graph
#     5- Every node in the graph is a province (tile)
#     6- Sub graphs are contients and/or strategic zones
#     7- Deadline: 6 pm

    