# graphviewer

This is a small desktop-app using **Pygame** that lets you create & visualize graphs easily.

## Features
- Create automatically indexed vertices
- Create edges between your vertices
- Do graph coloring

## How to Run
1. Install **Pygame** if you haven't:
    ```bash
        pip install pygame
    ```
2. Run the script
    ```bash
        python main.py
    ```
## File Structure:
```bash
main_folder/
│── main.py              # run this
│── vertex.py            # vertex class
│── edge.py              # edge class
│── assets/  
│   ├── fonts/  
│   │   ├── UbuntuMono-Regular.ttf  
│── README.md            
```

## TODO
- Make weighted graphs by taking user input
- Two set - mapping view for bipartite graphs
- BFS & DFS & Dijkstra tools
- Flow-Algorithm tools
- MST tool
- Improve UI
- Optimize performance
