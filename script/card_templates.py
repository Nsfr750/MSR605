#!/usr/bin/env python3

"""card_templates.py

This module provides template functionality for common card operations,
allowing users to define and apply templates for reading and writing cards.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

from .card_formats import CardFormat


class TemplateType(Enum):
    """Types of card operation templates."""
    READ = auto()
    WRITE = auto()
    BATCH = auto()


@dataclass
class CardTemplate:
    """Represents a template for card operations."""
    name: str
    description: str = ""
    template_type: TemplateType = TemplateType.WRITE
    format: CardFormat = CardFormat.ISO_7813
    tracks: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert template to a dictionary for serialization."""
        return {
            'name': self.name,
            'description': self.description,
            'template_type': self.template_type.name,
            'format': self.format.name,
            'tracks': self.tracks,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CardTemplate':
        """Create a template from a dictionary."""
        return cls(
            name=data.get('name', 'Untitled'),
            description=data.get('description', ''),
            template_type=TemplateType[data.get('template_type', 'WRITE')],
            format=CardFormat[data.get('format', 'ISO_7813')],
            tracks=data.get('tracks', []),
            metadata=data.get('metadata', {})
        )


class TemplateManager:
    """Manages card operation templates."""
    
    def __init__(self, template_dir: Optional[Path] = None):
        """Initialize the template manager.
        
        Args:
            template_dir: Directory to store template files. If None, uses a default directory.
        """
        if template_dir is None:
            template_dir = Path.home() / '.msr605' / 'templates'
        
        self.template_dir = template_dir
        self.template_dir.mkdir(parents=True, exist_ok=True)
        self._templates: Dict[str, CardTemplate] = {}
        self._load_templates()
    
    def _load_templates(self) -> None:
        """Load templates from the template directory."""
        self._templates = {}
        for template_file in self.template_dir.glob('*.json'):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    template = CardTemplate.from_dict(data)
                    self._templates[template.name] = template
            except (json.JSONDecodeError, KeyError, AttributeError) as e:
                print(f"Error loading template {template_file}: {e}")
    
    def save_template(self, template: CardTemplate) -> None:
        """Save a template to disk.
        
        Args:
            template: The template to save.
        """
        self._templates[template.name] = template
        template_file = self.template_dir / f"{template.name}.json"
        with open(template_file, 'w', encoding='utf-8') as f:
            json.dump(template.to_dict(), f, indent=2)
    
    def get_template(self, name: str) -> Optional[CardTemplate]:
        """Get a template by name.
        
        Args:
            name: Name of the template to retrieve.
            
        Returns:
            The template if found, None otherwise.
        """
        return self._templates.get(name)
    
    def list_templates(self, template_type: Optional[TemplateType] = None) -> List[CardTemplate]:
        """List all available templates, optionally filtered by type.
        
        Args:
            template_type: If provided, only return templates of this type.
            
        Returns:
            List of matching templates.
        """
        if template_type is None:
            return list(self._templates.values())
        return [t for t in self._templates.values() if t.template_type == template_type]
    
    def delete_template(self, name: str) -> bool:
        """Delete a template.
        
        Args:
            name: Name of the template to delete.
            
        Returns:
            True if the template was deleted, False if it didn't exist.
        """
        if name in self._templates:
            template_file = self.template_dir / f"{name}.json"
            if template_file.exists():
                template_file.unlink()
            del self._templates[name]
            return True
        return False


class BatchProcessor:
    """Handles batch processing of multiple card operations."""
    
    def __init__(self, card_reader, template_manager: Optional[TemplateManager] = None):
        """Initialize the batch processor.
        
        Args:
            card_reader: Instance of CardReader for card operations.
            template_manager: Optional template manager instance.
        """
        self.card_reader = card_reader
        self.template_manager = template_manager or TemplateManager()
        self.batch_results = []
    
    def process_batch(self, operations: List[Dict]) -> List[Dict]:
        """Process a batch of card operations.
        
        Args:
            operations: List of operation dictionaries with 'type' and other parameters.
            
        Returns:
            List of results for each operation.
        """
        self.batch_results = []
        
        for op in operations:
            op_type = op.get('type', '').lower()
            result = {'operation': op, 'success': False, 'result': None, 'error': None}
            
            try:
                if op_type == 'read':
                    result['result'] = self._process_read(op)
                    result['success'] = True
                elif op_type == 'write':
                    result['result'] = self._process_write(op)
                    result['success'] = True
                elif op_type == 'apply_template':
                    result['result'] = self._process_template(op)
                    result['success'] = True
                else:
                    result['error'] = f"Unknown operation type: {op_type}"
            except Exception as e:
                result['error'] = str(e)
            
            self.batch_results.append(result)
        
        return self.batch_results
    
    def _process_read(self, op: Dict) -> Dict:
        """Process a read operation."""
        detect_format = op.get('detect_format', True)
        return self.card_reader.read_card(detect_format=detect_format)
    
    def _process_write(self, op: Dict) -> Dict:
        """Process a write operation."""
        tracks = op.get('tracks', [])
        format_override = op.get('format')
        if format_override:
            format_override = CardFormat[format_override]
        
        return self.card_reader.write_card(
            tracks=tracks,
            format_override=format_override
        )
    
    def _process_template(self, op: Dict) -> Dict:
        """Process a template application."""
        template_name = op.get('template_name')
        if not template_name:
            raise ValueError("No template name provided")
            
        template = self.template_manager.get_template(template_name)
        if not template:
            raise ValueError(f"Template not found: {template_name}")
        
        if template.template_type == TemplateType.WRITE:
            return self.card_reader.write_card(
                tracks=template.tracks,
                format_override=template.format
            )
        else:
            raise ValueError(f"Unsupported template type: {template.template_type}")
    
    def export_results(self, output_file: str, format: str = 'json') -> bool:
        """Export batch processing results to a file.
        
        Args:
            output_file: Path to the output file.
            format: Output format ('json' or 'csv').
            
        Returns:
            True if export was successful, False otherwise.
        """
        try:
            if format.lower() == 'json':
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(self.batch_results, f, indent=2)
                return True
            elif format.lower() == 'csv':
                # Simple CSV export implementation
                import csv
                with open(output_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    # Write header
                    writer.writerow(['operation', 'success', 'error', 'result'])
                    # Write data
                    for result in self.batch_results:
                        writer.writerow([
                            result['operation'].get('type', ''),
                            result['success'],
                            result.get('error', ''),
                            str(result.get('result', ''))
                        ])
                return True
            else:
                return False
        except Exception as e:
            print(f"Error exporting results: {e}")
            return False
