# CPT_S 453 Graph Theory Final Project Code Implementation  
Final project for CPT_S 453 at WSU-TC Fall 2024  

![Map of Rome](./images/osm.pdf.png)

## Files  
All required files are included in the github repository. These files include:  
- aStar.py  
- bellman-ford.algorithm.py  
- dijkstras.algorithm.py  
- WeightedGraph.py    
- rome_italy.pkl  

### WeightedGraph.py  
This file includes the implementation for creating a graph from a .pkl file containing map data.  

### aStar.py  
This file includes the implementation of the A* algorithm as well as the logic to run the algorithm on the graph created from rome_italy.pkl. The algorithm will run from the Colosseum vertex (8430) to each of the McDonald's vertices(8389, 8390, 8391, 8392, 8393, 8394, 8395, 8396), and return the path, the time to find that path, and the distance of the path.  

### bellman-ford.algorithm.py
This file includes the implementation of the Bellman Ford algorithm as well as the logic to run the algorithm on the graph created from rome_italy.pkl. The algorithm will run from the Colosseum vertex (8430) to each of the McDonald's vertices(8389, 8390, 8391, 8392, 8393, 8394, 8395, 8396), and return the path, the time to find that path, and the distance of the path. The algorithm will run with or without a set destination vertex, finding a shortest path to all of the vertices in the graph. 

### convert_data.py
This file includes the conversion from OpenStreetMap compressed PBF files to the adjacency matrix used by the algorithms. Nodes within 0.2 degrees latitude and longitude of the approximate Colosseum center are kept, while anything outside that range is discarded. Next, any ways that are not roads or don't have known speed limits are discarded. Finally, any nodes not referenced by the filtered set of ways are not included in the final output, aside from nodes representing the Colosseum or McDonalds locations which must be included regardless.

### dijkstras.algorithm.py  
This file includes the implementation of Dijkstra's algorithm as well as the logic to run the algorithm on the graph created from rome_italy.pkl. The algorithm will run from the Colosseum vertex (8430) to each of the McDonald's vertices(8389, 8390, 8391, 8392, 8393, 8394, 8395, 8396), and return the path, the time to find that path, and the distance of the path. The algorithm will run with or without a set destination vertex, finding a shortest path to all of the vertices in the graph.

### rome_italy.pkl  
This file includes all of the map data as an adjacency matrix. Note that this file is derived from data provided by [OpenStreetMap](https://www.openstreetmap.org/copyright) and is therefore licensed under the [Open Data Commons Open Database License](https://opendatacommons.org/licenses/odbl/) (ODbL).  

## Tutorial 
From the command line in the terminal,
1. Navigate to the directory in which all files reside.  
2. A graph is provided in `rome_italy.pkl`, and if you'd like to use that version, continue on. Otherwise, follow the steps in the appendix.
3. Files may be executed by entering the following on the command line:  
```
python3 <file name>  
``` 
4. Results will be displayed in the terminal window.

## Appendix: Acquiring data extracts and converting data

1. Create a free account at [Interline](https://app.interline.io/osm_extracts/interactive_view)
2. Log in and create an API key.
3. Visit the [interactive view](https://app.interline.io/osm_extracts/interactive_view) page and paste your API key in the box at the top of the map.
4. Locate "Rome" in the list of cities and click "download".
5. Copy the file into the directory with `convert_data.py`, ensuring it's named `rome_italy.osm.pbf`.
6. Execute `convert_data.py` as above. The files `rome_italy.pkl`, `osm.png`, and `osm.pdf` should be generated.
