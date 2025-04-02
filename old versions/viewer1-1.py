import pygame as pg
from vertex import Vertex
# Initialize pg
pg.init()
# Screen settings
WIDTH, HEIGHT = 1920, 1080
screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
pg.display.set_caption("graphmaker -version")


# Constants
EDGE_THICKNESS = 3
CIRCLE_RADIUS = 50
CIRCLE_BORDER_THICKNESS = 3

# Colors

BACKGROUND_COLOR = (200,200,200)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BROWN = (150, 75, 0) # color meaning selected for edge


# graph logic
circles = []

# using 0-indexing
n = 0
dragging_circle = None
edges = []
edge_set = []

selected_vertex = None

saved_color = WHITE


def draw_edge(v1:Vertex, v2:Vertex):
    if(v1 != None and v2 != None):
        pg.draw.line(screen, BLACK, v1.pos, v2.pos, EDGE_THICKNESS)



# Main loop
running = True

while running:

    screen.fill(BACKGROUND_COLOR) 
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_v:
                circles.append( Vertex(n, 0, [], WHITE, (WIDTH // 2, HEIGHT // 2)))
                n += 1
                edges.append([])
            # DEBUG CASE
            elif event.key == pg.K_p:
                for couple in edge_set:
                    print(couple[0].index, couple[1].index)
            
            # creating edges
            elif event.key == pg.K_e:
                mouse_x, mouse_y = pg.mouse.get_pos()
                for circle in circles:
                    cx, cy = circle.pos
                    if (cx - mouse_x) ** 2 + (cy - mouse_y) ** 2 <= CIRCLE_RADIUS ** 2:
   

                        if selected_vertex != None:
                            if selected_vertex.index == circle.index:
                                selected_vertex = None
                                circle.color = saved_color
                            else:
                                selected_vertex.color = saved_color
                                selected_vertex.add_edge(circle)
                                circle.add_edge(selected_vertex)
                                edges[selected_vertex.index].append(circle.index)
                                edges[circle.index].append(selected_vertex.index)
                                edge_set.append([circle, selected_vertex])
                                selected_vertex = None
                            
                        else:
                            saved_color = circle.color
                            circle.color = BROWN
                            selected_vertex = circle

            
            # Deleting Vertices and Edges
            elif event.key == pg.K_d:
                mouse_x, mouse_y = pg.mouse.get_pos()
                for circle in circles:
                    cx, cy = circle.pos
                    if (cx - mouse_x) ** 2 + (cy - mouse_y) ** 2 <= CIRCLE_RADIUS ** 2:
                        # delete
                        pass


            # COLORING
            elif event.key == pg.K_w:
                mouse_x, mouse_y = pg.mouse.get_pos()
                for circle in circles:
                    cx, cy = circle.pos
                    if (cx - mouse_x) ** 2 + (cy - mouse_y) ** 2 <= CIRCLE_RADIUS ** 2:
                        circle.color = WHITE
            elif event.key == pg.K_r:
                mouse_x, mouse_y = pg.mouse.get_pos()
                for circle in circles:
                    cx, cy = circle.pos
                    if (cx - mouse_x) ** 2 + (cy - mouse_y) ** 2 <= CIRCLE_RADIUS ** 2:
                        circle.color = RED
            elif event.key == pg.K_b:
                mouse_x, mouse_y = pg.mouse.get_pos()
                for circle in circles:
                    cx, cy = circle.pos
                    if (cx - mouse_x) ** 2 + (cy - mouse_y) ** 2 <= CIRCLE_RADIUS ** 2:
                        circle.color = BLUE
            elif event.key == pg.K_g:
                mouse_x, mouse_y = pg.mouse.get_pos()
                for circle in circles:
                    cx, cy = circle.pos
                    if (cx - mouse_x) ** 2 + (cy - mouse_y) ** 2 <= CIRCLE_RADIUS ** 2:
                        circle.color = GREEN
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for circle in circles:
                cx, cy = circle.pos
                if (cx - mouse_x) ** 2 + (cy - mouse_y) ** 2 <= CIRCLE_RADIUS ** 2:
                    circle.dragging = True
                    dragging_circle = circle
        elif event.type == pg.MOUSEBUTTONUP:
            if dragging_circle:
                dragging_circle.dragging = False
                dragging_circle = None
        elif event.type == pg.MOUSEMOTION:
            if dragging_circle:
                dragging_circle.pos = event.pos


    #Draw all edges
    for edge in edge_set:
        draw_edge(edge[0], edge[1])
        
    # Draw all circles
    for circle in circles:
        pg.draw.circle(screen, circle.color, circle.pos, CIRCLE_RADIUS)
        pg.draw.circle(screen, BLACK, circle.pos, CIRCLE_RADIUS, CIRCLE_BORDER_THICKNESS)  # Black border

    
    pg.display.flip()

pg.quit()
