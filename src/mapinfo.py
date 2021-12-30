from src.ruby_loader import DataLoader
from kivy.uix.treeview import TreeView
from kivy.uix.treeview import TreeViewLabel

class MapList(TreeView):
    def __init__(self, **kwargs):
        super(MapList, self).__init__(**kwargs)

        self.mapinfos = DataLoader().load_data('Data/MapInfos.rxdata')
        self.mapinfos_sorted = {}
        self.nodes = {}
        self.order_mapinfos()
        self.load_mapinfos()
        self.root_options = {'text': 'Maps'}

        self.size_hint_y = None
        self.bind(on_node_expand = self.set_height, on_node_collapse = self.set_height)
        

    def order_mapinfos(self):
        self.mapinfos_sorted = dict(sorted(self.mapinfos.items(), key=lambda item: item[1].order))
    
    def load_mapinfos(self):
        self.nodes = {}
        for key, value in self.mapinfos_sorted.items():
            if type(value.name) == bytes:
                self.nodes[int(key)] = TreeViewLabel(text=value.name.decode())
            else:
                self.nodes[int(key)] = TreeViewLabel(text=value.name.text)

        for key, value in self.mapinfos_sorted.items():
            if value.parent_id == 0:
                self.add_node(self.nodes[key])
            else:
                self.add_node(self.nodes[key], self.nodes[value.parent_id])
            
            if value.expanded:
                self.toggle_node(self.nodes[key])
        
        self.select_node(self.nodes[list(self.mapinfos_sorted.keys())[0]])
        self.set_height()
    
    def set_height(self, *args):
        min_width = min_height = 0
        for count, node in enumerate(self.iterate_open_nodes(self.root)):
            node.odd = False if count % 2 else True
            min_width = max(min_width, node.right - self.x)
            min_height += node.height
        self.width = min_width
        self.height = min_height
        
    def get_selected_map(self):
        selected_node = self.selected_node
        for key, value in self.nodes.items():
            if value == selected_node:
                return key
        return 1
