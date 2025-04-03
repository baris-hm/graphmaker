import pygame as pg
from vertex import Vertex
import math

# Initialize pg
pg.init()
# Screen settings
WIDTH, HEIGHT = 1920, 1080
screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
pg.display.set_caption("graphmaker -version 1.4")

# Initialize font
font_path = "assets/fonts/UbuntuMono-Regular.ttf"  # Adjust path if needed

font = pg.font.Font(font_path, 30)  # Default font, size 30
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
vertices = []

edge_set = []


dragging_vertex = None

selected_vertex = None

saved_color = WHITE


# drawing the menu

# Button settings
def button_rect(width):
    return pg.Rect(width-(MANUAL_BUTTON_SIZE+10), 10, MANUAL_BUTTON_SIZE, MANUAL_BUTTON_SIZE)  # Manual button

# toggles
menu_open = False
directed_mode = False
weighted_mode = False


def draw_settings(width, height):
    menu_width, menu_height = width // 6, height // 10
    menu_x, menu_y = 20, 20
    menu_rect = pg.Rect(menu_x, menu_y, menu_width, menu_height)
    
    # Draw menu background
    pg.draw.rect(screen, GRAY, menu_rect, border_radius=15)
    pg.draw.rect(screen, BLACK, menu_rect, 3, border_radius=15)
    
    body_font = pg.font.Font(font_path, max(30, height // 40))

    
    # texts
    texts = [
        "",
        f"Weighted Mode: {'On' if weighted_mode else 'Off'}", 
        f"Directed Mode: {'On' if directed_mode else 'Off'}"
    ]
    
    text_y = menu_y
    text_spacing = max(25, height // 40)  # Adjusts spacing based on screen size
    for text in texts:
        text_surface = body_font.render(text, True, BLACK)
        screen.blit(text_surface, (menu_x + menu_width/2 - (len(text) / 2 * max(30, height // 40) * 0.5), text_y))
        text_y += text_spacing    

def draw_menu(width, height):
    menu_width, menu_height = width // 2, height // 2
    menu_x, menu_y = (width - menu_width) // 2, (height - menu_height) // 2
    menu_rect = pg.Rect(menu_x, menu_y, menu_width, menu_height)
    
    # Draw menu background
    pg.draw.rect(screen, GRAY, menu_rect, border_radius=15)
    pg.draw.rect(screen, BLACK, menu_rect, 3, border_radius=15)
    
    # Title
    title_font = pg.font.Font(font_path, max(40, height // 30))
    body_font = pg.font.Font(font_path, max(20, height // 54))
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
        screen.blit(text_surface, (menu_x + 15, text_y))
        text_y += text_spacing


def draw_undirected_edge(v1:Vertex, v2:Vertex):
    if(v1 != None and v2 != None):
        pg.draw.line(screen, BLACK, v1.pos, v2.pos, EDGE_THICKNESS)

 

def draw_directed_edge(v1, v2):
    if v1 is not None and v2 is not None:
        # Compute the direction vector
        dx, dy = v2.pos[0] - v1.pos[0], v2.pos[1] - v1.pos[1]
        length = math.sqrt(dx**2 + dy**2)
        if length == 0:
            return  # Avoid division by zero

        # Normalize the direction vector
        ux, uy = dx / length, dy / length

        # Adjust the endpoint to be CIRCLE_RADIUS away from v2
        v2_adjusted = (
            v2.pos[0] - ux * CIRCLE_RADIUS,
            v2.pos[1] - uy * CIRCLE_RADIUS
        )

        # Draw the main line up to the adjusted point
        pg.draw.line(screen, BLACK, v1.pos, v2_adjusted, EDGE_THICKNESS)

        # Arrowhead parameters
        arrow_length = 10  # Length of the arrow
        arrow_angle = math.radians(30)  # Angle of arrow wings

        # Compute two points for the arrowhead
        left_x = v2_adjusted[0] - arrow_length * (ux * math.cos(arrow_angle) - uy * math.sin(arrow_angle))
        left_y = v2_adjusted[1] - arrow_length * (uy * math.cos(arrow_angle) + ux * math.sin(arrow_angle))

        right_x = v2_adjusted[0] - arrow_length * (ux * math.cos(-arrow_angle) - uy * math.sin(-arrow_angle))
        right_y = v2_adjusted[1] - arrow_length * (uy * math.cos(-arrow_angle) + ux * math.sin(-arrow_angle))

        # Draw the arrowhead as two small lines
        pg.draw.line(screen, BLACK, v2_adjusted, (left_x, left_y), EDGE_THICKNESS)
        pg.draw.line(screen, BLACK, v2_adjusted, (right_x, right_y), EDGE_THICKNESS)


def assign_indices():
    for i in range(len(vertices)):
        vertices[i].index = i

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
                    for vertex in vertices:
                        cx, cy = vertex.pos
                        if (cx - mouse_x) ** 2 + (cy - mouse_y) ** 2 <= CIRCLE_RADIUS ** 2:
                            if vertex.color == RED:
                                vertex.color = WHITE
                            else:
                                vertex.color = RED
                elif event.key == pg.K_b:
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    for vertex in vertices:
                        cx, cy = vertex.pos
                        if (cx - mouse_x) ** 2 + (cy - mouse_y) ** 2 <= CIRCLE_RADIUS ** 2:
                            if vertex.color == BLUE:
                                vertex.color = WHITE
                            else:
                                vertex.color = BLUE
                elif event.key == pg.K_g:
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    for vertex in vertices:
                        cx, cy = vertex.pos
                        if (cx - mouse_x) ** 2 + (cy - mouse_y) ** 2 <= CIRCLE_RADIUS ** 2:
                            if vertex.color == GREEN:
                                vertex.color = WHITE
                            else:
                                 vertex.color = GREEN

            # shift not held
            else: 
                # create vertex
                if event.key == pg.K_v:
                    vertices.append(Vertex(len(vertices), 0, [], WHITE, pg.mouse.get_pos()))
                
                # debug case -comment out later
                elif event.key == pg.K_p:
                    print("+-----------+\n| DEBUG LOG | \n+-----------+\n")
                    
                    for vertex in vertices:
                        print(f"{vertex.index}: {list(v.index for v in vertex.edges)}")
                
                # creating edges
                elif event.key == pg.K_e:
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    for vertex in vertices:
                        cx, cy = vertex.pos
                        if (cx - mouse_x) ** 2 + (cy - mouse_y) ** 2 <= CIRCLE_RADIUS ** 2:
    
                            # if a vertex has been selected before
                            if selected_vertex != None:
                                # if this vertex is the same as what was selected, undo the selection
                                if selected_vertex.index == vertex.index:
                                    selected_vertex = None
                                    vertex.color = saved_color
                                else:
                                    # restore color for previously selected vertex
                                    selected_vertex.color = saved_color


                                    # directed graph, only add if the exact isn't already in there
                                    if directed_mode:
                                        if (selected_vertex, vertex) not in edge_set:
                                            edge_set.append((selected_vertex,vertex))
                                            selected_vertex.add_edge(vertex)

                                        else:
                                            print(f"edge {selected_vertex.index, vertex.index} already exists!")
                                    
                                    # undirected graph, don't add if already exists
                                    else:
                                        if (selected_vertex, vertex) not in edge_set and (vertex, selected_vertex) not in edge_set :
                                            edge_set.append((selected_vertex, vertex))
                                            selected_vertex.add_edge(vertex)
                                            vertex.add_edge(selected_vertex)
                                        else:
                                            print(f"edge {selected_vertex.index, vertex.index} already exists!")


                                    # reset selected vertex
                                    selected_vertex = None
                            
                            # if no vertex was selected before, select one
                            else:
                                saved_color = vertex.color
                                vertex.color = BROWN
                                selected_vertex = vertex

                # deleting vertices & edges
                elif event.key == pg.K_r:
                    mouse_x, mouse_y = pg.mouse.get_pos()

                    # vertices
                    for vertex in vertices:
                        cx, cy = vertex.pos
                        if (cx - mouse_x) ** 2 + (cy - mouse_y) ** 2 <= CIRCLE_RADIUS ** 2:
                            # delete

                            # no vertex has an edge to this vertex anymore
                            for neighbor in vertex.edges:
                                neighbor.remove_edge(vertex)

                            vertices.remove(vertex)
                            
                            # delete from edge_set
                            new_edge_set = []
                            for uv in edge_set:
                                if uv[0].index != vertex.index and uv[1].index != vertex.index:
                                    new_edge_set.append(uv)
                            edge_set = new_edge_set
                            assign_indices()

                    # edges        
                    for edge in edge_set:
                        if is_mouse_on_edge(pg.mouse.get_pos(), edge[0], edge[1]):
                            # delete
                            edge[0].remove_edge(edge[1])
                            edge[1].remove_edge(edge[0])
                            edge_set.remove(edge)
                        
                # shortcut menu
                elif event.key == pg.K_s:
                    menu_open = not menu_open
                
                # weighted mode
                elif event.key == pg.K_w:
                    weighted_mode = not weighted_mode
               
                # directed mode
                elif event.key == pg.K_d:
                    directed_mode = not directed_mode



        # drag & drop 
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # if clicked on the menu
            if button_rect(screen.get_width()).collidepoint(mouse_x, mouse_y):
                menu_open = not menu_open
            # if clicked on a vertex
            for vertex in vertices:
                cx, cy = vertex.pos
                if (cx - mouse_x) ** 2 + (cy - mouse_y) ** 2 <= CIRCLE_RADIUS ** 2:
                    vertex.dragging = True
                    dragging_vertex = vertex
        elif event.type == pg.MOUSEBUTTONUP:
            if dragging_vertex:
                dragging_vertex.dragging = False
                dragging_vertex = None
        elif event.type == pg.MOUSEMOTION:
            if dragging_vertex:
                dragging_vertex.pos = event.pos



    

    # Draw all edges
    for edge in edge_set:
        if directed_mode:
            draw_directed_edge(edge[0], edge[1])
        else:
            draw_undirected_edge(edge[0], edge[1])


    # Draw all vertices
    for vertex in vertices:
        pg.draw.circle(screen, vertex.color, vertex.pos, CIRCLE_RADIUS)
        pg.draw.circle(screen, BLACK, vertex.pos, CIRCLE_RADIUS, CIRCLE_BORDER_THICKNESS)  # Black border

         # write indeces:
        text_surface = font.render(str(vertex.index), True, BLACK)
        text_rect = text_surface.get_rect(center=vertex.pos)
        screen.blit(text_surface, text_rect)
    # Draw Menu
    # Draw manual button
    pg.draw.rect(screen, BLACK, button_rect(screen.get_width()))
    text_surface = font.render("?", True, WHITE)
    screen.blit(text_surface, (button_rect(screen.get_width()).x + 12, button_rect(screen.get_width()).y + 5))
    # Draw menu if open
    if menu_open:
        draw_menu(screen.get_width(), screen.get_height())
    draw_settings(screen.get_width(), screen.get_height())
    pg.display.flip()

pg.quit()