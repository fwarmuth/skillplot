from dataclasses import dataclass, field, asdict
from typing import List, Dict
import ruamel.yaml
import numpy as np

@dataclass
class PlotData:
    """Dataclass for holding plot data."""
    level_names: List[str] = \
        field(default_factory=lambda: ['Rare', 'Occasional', 'Regular', 'Frequent', 'Daily'])
    rows: List[str] = \
        field(default_factory=lambda: ['Private\nHobby stuff', 'During study', 'Professional'])
    cols: List[str] = \
        field(default_factory=lambda: ['Python', 'C++', 'SQL', 'Git', 'Docker'])
    levels: List[List[int]] = None

    def __post_init__(self):
        # If the rows or cols are given as a dictionary, convert them to a list
        if type(self.rows) == dict:
            self.data_rows = [row for row_group in self.rows.values() for row in row_group]
        if type(self.cols) == dict:
            self.data_cols = [col for col_group in self.cols.values() for col in col_group]

        # If the levels are not given, create random levels
        if self.levels is None:
            self.levels = np.random.randint(0, 100, size=(len(self.rows), len(self.cols))).tolist()
    
    def get_rows(self):
        if hasattr(self, 'data_rows'):
            return self.data_rows
        return self.rows
    def get_cols(self):
        if hasattr(self, 'data_cols'):
            return self.data_cols
        return self.cols

    @classmethod
    def from_yaml(self, filename):
        """Load plot data from a file.
        
        Args:
            filename (str): The filename to load the plot data from.
        """
        with open(filename, 'r') as f:
            try:
                raw = ruamel.yaml.load(f, Loader=ruamel.yaml.Loader)
                return PlotData(**raw)
            except Exception as e:
                print(e)
        return PlotData()
    
    def to_yaml(self, filename):
        """Save plot data to a file.
        
        Args:
            filename (str): The filename to save the plot data to.
        """
        with open(filename, 'w') as f:
            # If the data is a numpy array, convert it to a list of lists
            if type(self.levels) == np.ndarray:
                self.levels = self.levels.tolist()
            # Create a dictionary from the dataclass
            yaml_obj = asdict(self)
            
            # Create YAML object from the data, by dumping it to a string and loading it again
            yaml_obj : ruamel.yaml.comments.CommentedMap = ruamel.yaml.round_trip_load(ruamel.yaml.dump(yaml_obj))
            # Add comments with names to the data fields
            yaml_obj['levels'].yaml_set_start_comment('The "levels" field is a list of lists representing the levels, '\
                                                    'where each list represents a row in the plot.\n'\
                                                    f'{", ".join(self.get_cols())}\n')

            # Add comments with names to the area field
            for i, area in enumerate(self.get_rows()):
                # Remove line breaks from the area names
                area = area.replace('\n', ' ')
                yaml_obj['levels'].yaml_add_eol_comment(f'{area}', i)

            ruamel.yaml.round_trip_dump(yaml_obj, f)
        pass
