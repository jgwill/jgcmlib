# CLAUDE.md - jgcmlib

## Project Overview

**jgcmlib** (>= 1.0.59) is a Python library for ABC music notation processing and MIDI conversion. It provides CLI tools and Python modules for working with ABC music files and converting them to various formats.

## Core Functionality

### CLI Tools
- **`jgabcli`**: Main CLI for ABC file processing
  - Convert ABC files to MIDI format
  - Process JSON inference responses containing ABC notation
  - Handle batch processing of music files

### Python Modules
- **`jgcmlib.jgabcli`**: Core ABC processing functionality
- **`jgcmlib.jgcmhelper`**: Helper utilities for ABC file manipulation

## Usage Patterns

### Command Line Interface
```bash
# Convert ABC file to MIDI
jgabcli myabcfile.abc

# Process JSON inference response containing ABC notation
jgabcli myinferenceresponse.json
```

### Python API
```python
from jgcmlib.module import Module

# Create module instance
module = Module()

# Process ABC notation
result = module.some_method()
```

## Integration Context

This library is used as a git submodule in the **orpheuspypractice** project, providing the core ABC notation processing capabilities for the music generation pipeline. It works in conjunction with:

- **jghfmanager**: HuggingFace model management for AI music generation
- **orpheuspypractice**: Main package orchestrating the complete workflow

## Development Notes

- **Version**: >= 1.0.59 (as required by orpheuspypractice)
- **License**: MIT License
- **Testing**: Uses `tests/an_ok_abc_file_for_test.abc` for validation
- **Build System**: Standard Python setuptools with Makefile

## Key Dependencies

- Standard Python libraries for file processing
- ABC notation parsing capabilities
- MIDI generation functionality

## Important Context

This is a focused library for ABC music notation processing. When working with this codebase:

1. **ABC Format Focus**: All functionality revolves around ABC music notation standard
2. **CLI-First Design**: Primary interface is command-line tools
3. **Integration Ready**: Designed to work as part of larger music processing pipelines
4. **Minimal Dependencies**: Keeps external dependencies minimal for reliability

The library serves as the foundation for music notation processing in AI-driven music generation workflows.