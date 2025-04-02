import pygame as pg
from vertex import Vertex
# Initialize pg
pg.init()
# Screen settings
WIDTH, HEIGHT = 1920, 1080
screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
pg.display.set_caption("graphmaker -version 1.4")

# Initialize font
font = pg.font.Font(None, 30)  # Default font, size 30
# Constants
EDGE_THICKNESS = 3
CIRCLE_RADIUS = 50
CIRCLE_BORDER_THICKNESS = 3
MANUAL_BUTTON_SIZE = 40

# Colors

BACKGROUND_COLOR = (200,200,200)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BROWN = (150, 75, 0) # color meaning selected for edge
GRAY = (150, 150, 150)


# graph logic
circles = []

edge_set = []


dragging_circle = None

selected_vertex = None

saved_color = WHITE


# drawing the menu

# Button settings
def button_rect(width):
    return pg.Rect(width-(MANUAL_BUTTON_SIZE+10), 10, MANUAL_BUTTON_SIZE, MANUAL_BUTTON_SIZE)  # Manual button

menu_open = False

def draw_menu(width, height):
    menu_width, menu_height = width // 2, height // 2
    menu_x, menu_y = (width - menu_width) // 2, (height - menu_height) // 2
    menu_rect = pg.Rect(menu_x, menu_y, menu_width, menu_height)
    
    # Draw menu background
    pg.draw.rect(screen, GRAY, menu_rect, border_radius=15)
    pg.draw.rect(screen, BLACK, menu_rect, 3, border_radius=15)
    
    # Title
    title_font = pg.font.Font(None, max(40, height // 30))
    body_font = pg.font.Font(None, max(30, height // 40))
    title_surface = title_font.render("Shortcut Manual", True, BLACK)
    title_rect = title_surface.get_rect(center=(menu_x + menu_width // 2, menu_y + 30))
    screen.blit(title_surface, title_rect)
    
    # Shortcuts text
    shortcuts = [
        "",
        "S - Toggle this SHORTCUT menu",
        "",
        "V - Add a VERTEX at the mouse position",
        "",
        "E - Select a vertex to add an EDGE from, then press E on another vertex to add the edge to ",
        "",
        "R - REMOVE the vertex or edge the mouse is on",
        "",
        "Shift + R/G/B - Change vertex color to Red/Green/Blue - use same color again to erase",
        "", 
        "D - Toggle DIRECTED mode: when adding an edge from now on, make it directed",
        "", 
        "W - Toggle WEIGHTED mode: when adding an edge from now on, accepts weight input"
    ]
    
    text_y = menu_y + 70
    text_spacing = max(25, height // 40)  # Adjusts spacing based on screen size
    for text in shortcuts:
        text_surface = body_font.render(text, True, BLACK)
        screen.blit(text_surface, (menu_x + 20, text_y))
        text_y += text_spacing


def draw_edge(v1:Vertex, v2:Vertex):
    if(v1 != None and v2 != None):
        pg.draw.line(screen, BLACK, v1.pos, v2.pos, EDGE_THICKNESS)

def assign_indices():
    for i in range(len(circles)):
        circles[i].index = i

def is_mouse_on_edge(mpos, v1, v2, threshold=5):
    x0, y0 = mpos  # Mouse position
    x1, y1 = v1.pos[0], v1.pos[1]              # Line start
    x2, y2 = v2.pos[0], v2.pos[1]              # Line end
    
    # Line segment length squared
    line_length_squared = (x2 - x1) ** 2 + (y2 - y1) ** 2
    if line_length_squared == 0:
        return False  # Start and end are the same point
    
    # Projection factor t (clamped between 0 and 1 to stay on the segment)
    t = max(0, min(1, ((x0 - x1) * (x2 - x1) + (y0 - y1) * (y2 - y1)) / line_length_squared))
    
    # Closest point on the line segment to the mouse
    closest_x = x1 + t * (x2 - x1)
    closest_y = y1 + t * (y2 - y1)
    
    # Distance from mouse to closest point
    distance_squared = (closest_x - x0) ** 2 + (closest_y - y0) ** 2
    
    return distance_squared <= threshold ** 2  # True if within threshold


# Main loop
running = True

while running:

    screen.fill(BACKGROUND_COLOR) 
    
    for event in pg.event.get():
        # Quit Logic
        if event.type == pg.QUIT:
            running = False

        # Keyboard inputs
        elif event.type == pg.KEYDOWN:

            keys = pg.key.get_pressed()  # Get the state of all keys
            shift_held = keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]  # Check if shift is held
            if shift_held:

            # coloring with keyboard events
                if event.key == pg.K_r:
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    for circle in circles:
                        cx, cy = circle.pos
                        if (cx - mouse_x) ** 2 + (cy - mouse_y) ** 2 <= CIRCLE_RADIUS ** 2:
                            if circle.color == RED:
                                circle.color = WHITE
                            else:
                                circle.color = RED
                elif event.key == pg.K_b:
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    for circle in circles:
                        cx, cy = circle.pos
                        if (cx - mouse_x) ** 2 + (cy - mouse_y) ** 2 <= CIRCLE_RADIUS ** 2:
                            if circle.color == BLUE:
                                circle.color = WHITE
                            else:
                                circle.color = BLUE
                elif event.key == pg.K_g:
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    for circle in circles:
                        cx, cy = circle.pos
                        if (cx - mouse_x) ** 2 + (cy - mouse_y) ** 2 <= CIRCLE_RADIUS ** 2:
                            if circle.color == GREEN:
                                circle.color = WHITE
                            else:
                                 circle.color = GREEN

            # shift not held
            else: 
                # Create Vertex
                if event.key == pg.K_v:
                    circles.append(Vertex(len(circles), 0, [], WHITE, pg.mouse.get_pos()))
                
                # DEBUG CASE
                elif event.key == pg.K_p:
                    print("+-----------+\n| DEBUG LOG | \n+-----------+\n")
                    
                    for vertex in circles:
                        print(f"{vertex.index}: {list(v.index for v in vertex.edges)}")
                
                # creating edges
                elif event.key == pg.K_e:
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    for circle in circles:
                        cx, cy = circle.pos
                        if (cx - mouse_x) ** 2 + (cy - mouse_y) ** 2 <= CIRCLE_RADIUS ** 2:
    
                            # if a vertex has been selected before
                            if selected_vertex != None:
                                # if this vertex is the same as what was selected, undo the selection
                                if selected_vertex.index == circle.index:
                                    selected_vertex = None
                                    circle.color = saved_color
                                else:
                                    # restore color for previously selected vertex
                                    selected_vertex.color = saved_color

                                    # logically add the edges
                                    selected_vertex.add_edge(circle)
                                    circle.add_edge(selected_vertex)

                                    edge_set.append([circle,selected_vertex])

                                    # reset selected vertex
                                    selected_vertex = None
                            
                            # if no vertex was selected before, select one
                            else:
                                saved_color = circle.color
                                circle.color = BROWN
                                selected_vertex = circle

                # Deleting Vertices and Edges
                elif event.key == pg.K_r:
                    mouse_x, mouse_y = pg.mouse.get_pos()

                    # vertices
                    for circle in circles:
                        cx, cy = circle.pos
                        if (cx - mouse_x) ** 2 + (cy - mouse_y) ** 2 <= CIRCLE_RADIUS ** 2:
                            # delete

                            # no vertex has an edge to this vertex anymore
                            for neighbor in circle.edges:
                                neighbor.remove_edge(circle)

                            circles.remove(circle)
                            
                            # delete from edge_set
                            new_edge_set = []
                            for uv in edge_set:
                                if uv[0].index != circle.index and uv[1].index != circle.index:
                                    new_edge_set.append(uv)
                            edge_set = new_edge_set
                            assign_indices()

                    # edges        
                    for edge in edge_set:
                        if is_mouse_on_edge(pg.mouse.get_pos(), edge[0], edge[1]):
                            # delete
                            """
                            edge[0].remove_edge(edge[1])
                            edge[1].remove_edge(edge[0])
                            """
                            edge_set.remove(edge)
                        






        # drag & drop 
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # if clicked on the menu
            if button_rect(screen.get_width()).collidepoint(mouse_x, mouse_y):
                menu_open = not menu_open
            # if clicked on a vertex
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



    

    # Draw all edges
    for edge in edge_set:
        draw_edge(edge[0], edge[1])
        
    # Draw all circles
    for circle in circles:
        pg.draw.circle(screen, circle.color, circle.pos, CIRCLE_RADIUS)
        pg.draw.circle(screen, BLACK, circle.pos, CIRCLE_RADIUS, CIRCLE_BORDER_THICKNESS)  # Black border

         # write indeces:
        text_surface = font.render(str(circle.index), True, BLACK)
        text_rect = text_surface.get_rect(center=circle.pos)
        screen.blit(text_surface, text_rect)
    # Draw Menu
    # Draw manual button
    pg.draw.rect(screen, BLACK, button_rect(screen.get_width()))
    text_surface = font.render("?", True, WHITE)
    screen.blit(text_surface, (button_rect(screen.get_width()).x + 12, button_rect(screen.get_width()).y + 5))
    # Draw menu if open
    if menu_open:
        draw_menu(screen.get_width(), screen.get_height())

    pg.display.flip()

pg.quit()
