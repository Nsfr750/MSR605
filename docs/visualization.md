# Card Data Visualization

This document describes the advanced card data visualization features available in the MSR605 Card Reader/Writer application.

## Overview

The visualization module provides interactive and static visualizations of magnetic stripe card data, helping users analyze and understand the structure and content of card tracks. The visualizations are integrated into the application's UI and update automatically when new card data is read.

## Features

### 1. Character Distribution

Visualizes the frequency of each character in a track's data using a bar chart. This helps identify:

- Most common characters
- Data patterns
- Potential anomalies or corruption

### 2. Bit Pattern

Displays the binary representation of the track data as a waveform, showing:

- Individual bit values (0/1)
- Bit transitions
- Data density

### 3. Data Density Metrics

Presents key metrics about the track data:

- Total length (in characters)
- Number of unique characters
- Character density (unique characters / total length)

### 4. Field Analysis

Analyzes and visualizes the structure of track data by:

- Detecting field separators (^, =)
- Displaying field lengths
- Highlighting field boundaries

## Usage

### Accessing Visualizations

1. Read a card using the main interface
2. Click on the "Visualization" tab in the Advanced Functions window
3. View the generated visualizations for each track

### Customization

- **Theme**: Choose from different color themes (dark, light, seaborn, ggplot, etc.)
- **Refresh**: Click the "Refresh Visualizations" button to update with the latest data
- **Interactive**: Hover over charts to see detailed information

## Technical Details

### Dependencies

- `matplotlib`: For creating static visualizations
- `seaborn`: For enhanced statistical visualizations
- `plotly`: For interactive visualizations (future use)

### Implementation

The visualization system is implemented in `script/visualization.py` and integrated with the main UI through the `AdvancedFunctionsWidget` class.

## Examples

### Character Distribution

```
Track 1: %B1234567890123456^DOE/JOHN^24051234567890123456789?
```

- Shows frequency of each character (digits, letters, symbols)
- Helps identify patterns in the data

### Bit Pattern

```
Track 2: ;1234567890123456=240512345678901?
```

- Displays the binary representation of the track
- Shows bit transitions and density

## Troubleshooting

### No Visualizations Appear

1. Ensure a card has been read successfully
2. Check that the track data is not empty
3. Verify that all dependencies are installed (run `pip install -r requirements.txt`)

### Visualizations Look Incorrect

1. Try refreshing the visualizations
2. Select a different theme
3. Check the application logs for any error messages

## Future Enhancements

- Add more visualization types (heatmaps, histograms)
- Support for saving visualizations as images
- Interactive data exploration
- Export visualization data (CSV, JSON)
