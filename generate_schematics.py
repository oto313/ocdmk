#!/usr/bin/env python3
"""
Generate KiCad schematic files for keyboard matrix from ergogen config.yaml and points.yaml
Creates separate schematics for each PCB defined in the ergogen config using kicad-sch-api

Reference: https://github.com/circuit-synth/kicad-sch-api
"""

from typing import List, Dict
from pathlib import Path
import re

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is not installed. Install it with: pip install pyyaml")
    print("Or install all requirements: pip install -r requirements_schematics.txt")
    exit(1)

try:
    from kicad_sch_api import Schematic, create_schematic
except ImportError:
    print("ERROR: kicad-sch-api is not installed. Install it with: pip install kicad-sch-api")
    print("Or install all requirements: pip install -r requirements_schematics.txt")
    exit(1)


class KeyInfo:
    """Information about a single key in the keyboard matrix"""
    def __init__(self, name: str, column_net: str, row_net: str, x: float, y: float):
        self.name = name
        self.column_net = column_net
        self.row_net = row_net
        self.x = x
        self.y = y


class PCBDefinition:
    """Information about a PCB from ergogen config"""
    def __init__(self, name: str, where_patterns: List[str]):
        self.name = name
        self.where_patterns = where_patterns
        # Compile regex patterns
        self.compiled_patterns = []
        for pattern in where_patterns:
            # Handle both string patterns and regex patterns
            if isinstance(pattern, str):
                if pattern.startswith('/') and pattern.endswith('/'):
                    # It's a regex pattern like /^matrix.*/
                    regex_str = pattern[1:-1]  # Remove leading and trailing /
                    self.compiled_patterns.append(re.compile(regex_str))
                else:
                    # It's a plain string, match exactly
                    self.compiled_patterns.append(re.compile(f'^{re.escape(pattern)}$'))
    
    def matches_key(self, key_name: str) -> bool:
        """Check if a key name matches any of the where patterns"""
        for pattern in self.compiled_patterns:
            if pattern.match(key_name):
                return True
        return False


class KiCadSchematicGenerator:
    """Generates KiCad schematic files for keyboard matrices using kicad-sch-api"""
    
    def __init__(self):
        self.keys: List[KeyInfo] = []
    
    def parse_config_yaml(self, yaml_path: str) -> List[PCBDefinition]:
        """
        Parse config.yaml and extract PCB definitions
        
        Args:
            yaml_path: Path to config.yaml file
        
        Returns:
            List of PCBDefinition objects
        """
        with open(yaml_path, 'r') as f:
            config = yaml.safe_load(f)
        
        pcb_definitions = []
        
        if 'pcbs' in config:
            for pcb_name, pcb_config in config['pcbs'].items():
                # Look for the 'sockets' footprint definition
                if 'footprints' in pcb_config and 'sockets' in pcb_config['footprints']:
                    sockets = pcb_config['footprints']['sockets']
                    if 'where' in sockets:
                        where = sockets['where']
                        # where can be a list or a single string
                        if isinstance(where, list):
                            where_patterns = where
                        else:
                            where_patterns = [where]
                        
                        pcb_def = PCBDefinition(pcb_name, where_patterns)
                        pcb_definitions.append(pcb_def)
                        print(f"Found PCB definition: {pcb_name} with patterns: {where_patterns}")
        
        return pcb_definitions
    
    def parse_points_yaml(self, yaml_path: str, pcb_def: PCBDefinition = None) -> List[KeyInfo]:
        """
        Parse points.yaml and extract key information
        
        Args:
            yaml_path: Path to points.yaml file
            pcb_def: PCBDefinition to filter keys (optional, if None returns all keys)
        
        Returns:
            List of KeyInfo objects
        """
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        
        keys = []
        for key_name, key_data in data.items():
            # Filter by PCB definition if provided
            if pcb_def is not None and not pcb_def.matches_key(key_name):
                continue
            
            if 'meta' in key_data:
                meta = key_data['meta']
                # Skip keys that don't have column_net or row_net (like USB connectors)
                if 'column_net' in meta and 'row_net' in meta:
                    key_info = KeyInfo(
                        name=key_name,
                        column_net=meta['column_net'],
                        row_net=meta['row_net'],
                        x=key_data.get('x', 0),
                        y=key_data.get('y', 0)
                    )
                    keys.append(key_info)
        
        # Don't sort - keep the order from points.yaml for reference numbering
        return keys
    
    def generate_matrix_schematic(self, keys: List[KeyInfo], pcb_name: str, output_path: str):
        """
        Generate complete schematic for a keyboard half using kicad-sch-api
        
        Args:
            keys: List of KeyInfo objects for this keyboard half
            pcb_name: Name of the PCB (e.g., "keyboard_left")
            output_path: Path where to write the schematic file
        """
        # Create a new schematic
        sch = create_schematic()
        
        # Layout parameters
        grid_spacing_x = 16.0  # mm between columns in matrix section
        grid_spacing_y = 16.0  # mm between rows
        led_spacing_x = 16.0   # mm between LEDs
        led_spacing_y = 20.0   # mm between LED rows
        led_start_y = 250.0    # Y position where LEDs start
        
        # Track net positions for labels
        col_net_positions = {}
        row_net_positions = {}
        
        # Build matrix coordinate mapping
        # Extract unique column and row nets and sort them
        col_nets = sorted(set(key.column_net for key in keys))
        row_nets = sorted(set(key.row_net for key in keys))
        
        # Create mapping from net names to matrix coordinates
        col_to_idx = {net: idx for idx, net in enumerate(col_nets)}
        row_to_idx = {net: idx for idx, net in enumerate(row_nets)}
        
        # Generate switch matrix
        for idx, key in enumerate(keys):
            # Use actual matrix position based on column/row nets
            col = col_to_idx[key.column_net]
            row = row_to_idx[key.row_net]
            
            # Column bus position (vertical line on the left)
            col_bus_x = 60.0 + col * grid_spacing_x
            row_bus_y = 60.0 + row * grid_spacing_y
            # Switch position (aligned with grid)
            sw_x = col_bus_x + 6.0
            sw_y = row_bus_y - 8.0
            
            # Add switch - use grid units for alignment
            sw_comp = sch.components.add(
                lib_id="Switch:SW_Push",
                reference=f"S{idx + 1}",
                position=(sw_x, sw_y),
                grid_units=False  # Use mm for precise positioning
            )
            
            # Hide switch value using set_property_effects
            sw_comp.set_property_effects("Reference", {
                "position": (sw_x, sw_y - 5),
            })
            
            # Diode position (below switch, aligned on same vertical line)
            d_x = sw_x + 8.0
            d_y = sw_y + 4.0
            
            # Add diode (vertical, cathode pointing up - REVERSED for col2row scanning)
            d_comp = sch.components.add(
                lib_id="Device:D",
                reference=f"D{idx + 1}",
                position=(d_x, d_y),
                rotation=270,  # Vertical with cathode up (at top), anode down (at bottom)
                grid_units=False  # Use mm for precise positioning
            )
        
            
            # Move diode reference to the left
            d_comp.set_property_effects("Reference", {
                "rotation": 90,
                "position": (d_x - 2.0, d_y),
                "justify_h": "right"
            })
            
            # Get pin positions for wiring
            sw_pins = sch.components.get_pins_info(f"S{idx + 1}")
            d_pins = sch.components.get_pins_info(f"D{idx + 1}")
            
            # Wire: Switch pin 1 (top) connects directly to column bus above
            sw_pin1_pos = sw_pins[0].position
            # Wire from switch to column bus above (vertical line up)
            sch.wires.add(start=(sw_pin1_pos.x, sw_pin1_pos.y), end=(col_bus_x, sw_pin1_pos.y))
            
            # Wire: Switch pin 2 (bottom) to Diode CATHODE (top pin when rotated 270°)
            # Signal flow: Column → Switch → CATHODE → ANODE → Row (reversed diode)
            sw_pin2_pos = sw_pins[1].position
            d_cathode_pos = d_pins[1].position  # Pin 1 is cathode, at TOP when rotated 270°
            sch.wires.add(start=(sw_pin2_pos.x, sw_pin2_pos.y), 
                         end=(d_cathode_pos.x, d_cathode_pos.y))
            
            # Wire: Diode ANODE (bottom pin when rotated 270°) to row bus
            d_anode_pos = d_pins[0].position  # Pin 2 is anode, at BOTTOM when rotated 270°
            sch.wires.add(start=(d_anode_pos.x, d_anode_pos.y), 
                         end=(d_anode_pos.x, row_bus_y))
            
            # Store positions for bus drawing and labels
            if key.column_net not in col_net_positions:
                col_net_positions[key.column_net] = (col_bus_x, 35.0)
            
            # Store row position using the actual row's y coordinate
            row_label_x = 60.0 + len(col_nets) * grid_spacing_x + 30.0
            if key.row_net not in row_net_positions:
                row_net_positions[key.row_net] = (row_label_x, row_bus_y)
            
            # LED position (separate section below matrix)
            led_col = idx % 15  # 15 LEDs per row
            led_row = idx // 15
            led_x = 50.0 + led_col * led_spacing_x
            led_y = led_start_y + led_row * led_spacing_y
            
            # Add LED without any connections
            sch.components.add(
                lib_id="Device:LED",
                reference=f"LEDT{idx + 1}",
                position=(led_x, led_y)
            )
            sch.components.add(
                lib_id="Device:LED",
                reference=f"LEDB{idx + 1}",
                position=(led_x, led_y-5.0)
            )
        
        # Collect positions from already-placed components for bus drawing
        # col_idx -> list of (x, y) tuples for switch connections
        col_switch_positions = {}
        # row_idx -> list of (x, y) tuples for diode connections
        row_diode_positions = {}
        
        # Initialize dictionaries
        for key in keys:
            col_idx = col_to_idx[key.column_net]
            row_idx = row_to_idx[key.row_net]
            if col_idx not in col_switch_positions:
                col_switch_positions[col_idx] = []
            if row_idx not in row_diode_positions:
                row_diode_positions[row_idx] = []
        
        # Collect actual pin positions from placed components
        for idx, key in enumerate(keys):
            col_idx = col_to_idx[key.column_net]
            row_idx = row_to_idx[key.row_net]
            
            col_bus_x = 60.0 + col_idx * grid_spacing_x
            row_bus_y = 60.0 + row_idx * grid_spacing_y
            
            # Get switch pin position for column bus
            sw_ref = f"S{idx + 1}"
            sw_pins = sch.components.get_pins_info(sw_ref)
            sw_pin1_y = sw_pins[0].position.y
            col_switch_positions[col_idx].append((col_bus_x, sw_pin1_y))
            
            # Get diode anode pin position for row bus
            d_ref = f"D{idx + 1}"
            d_pins = sch.components.get_pins_info(d_ref)
            d_anode_x = d_pins[0].position.x  # Anode is pin 1 when rotated 270°
            row_diode_positions[row_idx].append((d_anode_x, row_bus_y))
        
        # Draw column buses
        for col_idx, col_net in enumerate(col_nets):
            col_bus_x = 60.0 + col_idx * grid_spacing_x
            
            if col_idx in col_switch_positions and col_switch_positions[col_idx]:
                positions = col_switch_positions[col_idx]
                min_y = min(pos[1] for pos in positions)
                max_y = max(pos[1] for pos in positions)
                
                # Draw vertical column bus
                bus_top_y = 35.0
                sch.wires.add(start=(col_bus_x, bus_top_y), end=(col_bus_x, max_y))
                
                # Add junctions at each connection point
                for pos in positions:
                    sch.junctions.add(position=pos)
        
        # Draw row buses (horizontal lines) - each row is independent
        for row_idx, row_net in enumerate(row_nets):
            row_bus_y = 60.0 + row_idx * grid_spacing_y
            
            if row_idx in row_diode_positions and row_diode_positions[row_idx]:
                positions = row_diode_positions[row_idx]
                min_x = min(pos[0] for pos in positions)
                max_x = max(pos[0] for pos in positions)
                
                # Draw horizontal row bus
                bus_right_x = 60.0 + len(col_nets) * grid_spacing_x + 30.0
                sch.wires.add(start=(min_x, row_bus_y), end=(bus_right_x, row_bus_y))
                
                # Add junctions at each connection point
                for pos in positions:
                    sch.junctions.add(position=pos)
        
        # Add column net labels
        for col_net, (x, y) in col_net_positions.items():
            sch.labels.add(text=col_net, position=(x, y))
        
        # Add row net labels
        for row_net, (x, y) in row_net_positions.items():
            sch.labels.add(text=row_net, position=(x, y))
        
        # Save the schematic
        sch.save(file_path=output_path)
        print(f"Generated schematic: {output_path}")
    
    def generate_schematics(self, config_yaml_path: str, points_yaml_path: str, output_dir: str):
        """Generate schematic files for all PCBs defined in config.yaml"""
        
        # Parse config.yaml to get PCB definitions
        pcb_definitions = self.parse_config_yaml(config_yaml_path)
        
        if not pcb_definitions:
            print("ERROR: No PCB definitions found in config.yaml")
            print("Make sure your config.yaml has a 'pcbs' section with 'sockets' footprints")
            return
        
        # Generate schematic for each PCB
        for pcb_def in pcb_definitions:
            print(f"\n--- Processing {pcb_def.name} ---")
            
            # Parse keys for this PCB
            keys = self.parse_points_yaml(points_yaml_path, pcb_def)
            print(f"Found {len(keys)} keys for {pcb_def.name}")
            
            if not keys:
                print(f"WARNING: No keys found for {pcb_def.name}, skipping schematic generation")
                continue
            
            # Generate schematic
            output_file = Path(output_dir) / f"{pcb_def.name}.kicad_sch"
            self.generate_matrix_schematic(keys, pcb_def.name, str(output_file))
        
        print("\n=== Schematic generation complete! ===")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate KiCad schematics for keyboard matrices from ergogen config.yaml using kicad-sch-api'
    )
    parser.add_argument(
        '--config',
        default='ergogen/config.yaml',
        help='Path to ergogen config.yaml file (default: ergogen/config.yaml)'
    )
    parser.add_argument(
        '--points',
        default='output/points/points.yaml',
        help='Path to points.yaml file (default: output/points/points.yaml)'
    )
    parser.add_argument(
        '--output',
        default='pcb',
        help='Output directory for schematic files (default: pcb)'
    )
    
    args = parser.parse_args()
    
    # Validate input files exist
    config_path = Path(args.config)
    points_path = Path(args.points)
    
    if not config_path.exists():
        print(f"ERROR: Config file not found: {config_path}")
        print("Please specify the correct path with --config")
        exit(1)
    
    if not points_path.exists():
        print(f"ERROR: Points file not found: {points_path}")
        print("Please run ergogen first to generate points.yaml")
        exit(1)
    
    # Create output directory if it doesn't exist
    Path(args.output).mkdir(parents=True, exist_ok=True)
    
    # Generate schematics
    generator = KiCadSchematicGenerator()
    generator.generate_schematics(str(config_path), str(points_path), args.output)
    
    print("\nNote: Generated KiCad 8 compatible schematic files.")
    print("      You can open them directly in KiCad and assign footprints.")


if __name__ == '__main__':
    main()
